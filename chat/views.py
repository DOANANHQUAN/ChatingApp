import os
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Max, Q, Count, OuterRef, Subquery
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Conversation, ConversationParticipant, Message, MessageAttachment, MessageStatus
from accounts.models import User, Contact

def get_hydrated_conversations(user):
    """
    Helper function to retrieve and format all conversations for the sidebar.
    """
    queryset = Conversation.objects.filter(participants__user=user).annotate(
        latest_message_time=Max("messages__created_at")
    ).order_by("-latest_message_time")
    
    hydrated_conversations = []
    for conv in queryset:
        other_participant = None
        if not conv.is_group:
            part = conv.participants.exclude(user=user).first()
            if part:
                other_participant = part.user
        
        unread_count = MessageStatus.objects.filter(
            message__conversation=conv,
            user=user,
            is_read=False
        ).count()
        
        latest_msg = conv.messages.all().order_by("-created_at").first()

        hydrated_conversations.append({
            "instance": conv,
            "other_participant": other_participant,
            "unread_count": unread_count,
            "latest_message": latest_msg
        })
    return hydrated_conversations


class ConversationListView(LoginRequiredMixin, ListView):
    """
    CBV to display the active chat conversations list.
    Displays conversations sorted by latest message activity, including unread message counts.
    """
    model = Conversation
    template_name = "chat/conversation_list.html"
    context_object_name = "conversations"

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants__user=user).annotate(
            latest_message_time=Max("messages__created_at")
        ).order_by("-latest_message_time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context["hydrated_conversations"] = get_hydrated_conversations(user)
        context["contacts"] = Contact.objects.filter(
            Q(user1=user) | Q(user2=user)
        )
        return context


class ConversationDetailView(LoginRequiredMixin, DetailView):
    """
    CBV to display a specific chat room's messages.
    """
    model = Conversation
    template_name = "chat/conversation_detail.html"
    context_object_name = "conversation"

    def get_queryset(self):
        # Prevent users who aren't participants from viewing the chat
        return Conversation.objects.filter(participants__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conv = self.get_object()
        user = self.request.user
        
        # Mark all messages in this conversation as read for this user
        unread_statuses = MessageStatus.objects.filter(
            message__conversation=conv,
            user=user,
            is_read=False
        )
        for status in unread_statuses:
            status.is_read = True
            status.read_at = timezone.now()
            status.save()

        # Get messages in chronological order
        context["messages_list"] = conv.messages.all().prefetch_related("attachments", "statuses")
        
        # Determine the recipient user if 1-1
        context["other_participant"] = None
        if not conv.is_group:
            part = conv.participants.exclude(user=user).first()
            if part:
                context["other_participant"] = part.user

        # Provide sidebar data for inherited layout
        context["hydrated_conversations"] = get_hydrated_conversations(user)
        context["active_conversation_id"] = conv.id
        context["contacts"] = Contact.objects.filter(
            Q(user1=user) | Q(user2=user)
        )
                
        return context


class StartPrivateChatView(LoginRequiredMixin, View):
    """
    Finds or creates a 1-1 conversation with another user.
    """
    def get(self, request, user_id):
        other_user = get_object_or_404(User, id=user_id)
        
        # Search for a 1-1 conversation between request.user and other_user
        conversations = Conversation.objects.filter(is_group=False).filter(
            participants__user=request.user
        ).filter(
            participants__user=other_user
        )
        
        if conversations.exists():
            conversation = conversations.first()
        else:
            # Create new conversation
            conversation = Conversation.objects.create(is_group=False)
            ConversationParticipant.objects.create(conversation=conversation, user=request.user)
            ConversationParticipant.objects.create(conversation=conversation, user=other_user)
            
        return redirect("chat:conversation_detail", pk=conversation.id)


class SendMessageView(LoginRequiredMixin, View):
    """
    Handles message sending via standard HTTP POST.
    Required for uploading file attachments, but also acts as a fallback for text messages.
    Triggers Django Channels layer to broadcast to WebSockets.
    """
    def post(self, request, pk):
        conversation = get_object_or_404(Conversation, id=pk, participants__user=request.user)
        content = request.POST.get("content")
        files = request.FILES.getlist("files")
        
        if not content and not files:
            return JsonResponse({"error": "Không thể gửi tin nhắn rỗng"}, status=400)
            
        # 1. Create message
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        
        # 2. Save attachments
        attachments_data = []
        for file in files:
            attachment = MessageAttachment.objects.create(message=message, file=file)
            attachments_data.append({
                "url": attachment.file.url,
                "name": os.path.basename(attachment.file.name),
                "type": attachment.file_type
            })

        # 3. Create message status tracking for other participants
        participants = conversation.participants.exclude(user=request.user)
        for participant in participants:
            MessageStatus.objects.create(
                message=message,
                user=participant.user,
                is_read=False
            )
            
        # Update conversation time
        conversation.save() # Triggers auto_now update for updated_at

        # 4. Broadcast to WebSocket group via Django Channels
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{conversation.id}",
            {
                "type": "chat_message",
                "message_id": message.id,
                "sender_id": request.user.id,
                "sender_username": request.user.username,
                "sender_avatar": request.user.avatar.url if request.user.avatar else "/static/images/default_avatar.png",
                "content": message.content,
                "attachments": attachments_data,
                "created_at": message.created_at.strftime("%H:%M - %d/%m/%Y")
            }
        )
        
        # Render a single message bubble partial if request is HTMX/AJAX
        if request.headers.get("HX-Request"):
            return render(request, "chat/partials/message_bubble.html", {"msg": message})
            
        return JsonResponse({
            "status": "success",
            "message_id": message.id
        })


class CreateGroupChatView(LoginRequiredMixin, View):
    """
    Creates a group chat room and adds the selected participants.
    """
    def post(self, request):
        title = request.POST.get("title")
        member_ids = request.POST.getlist("members")
        
        if not title:
            title = f"Nhóm của {request.user.first_name or request.user.username}"
            
        # Create group conversation
        conversation = Conversation.objects.create(title=title, is_group=True)
        
        # Add creator as admin
        ConversationParticipant.objects.create(
            conversation=conversation, 
            user=request.user, 
            is_admin=True
        )
        
        # Add selected friends
        for m_id in member_ids:
            try:
                member_user = User.objects.get(id=m_id)
                ConversationParticipant.objects.create(
                    conversation=conversation, 
                    user=member_user, 
                    is_admin=False
                )
            except User.DoesNotExist:
                continue
                
        return redirect("chat:conversation_detail", pk=conversation.id)
