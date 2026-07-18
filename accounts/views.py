from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, View
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.db.models import Q
from .models import User, Contact, FriendRequest
from .forms import CustomUserCreationForm

class RegisterView(CreateView):
    """
    Class-Based View to handle user registration using MTV pattern.
    """
    model = User
    form_class = CustomUserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("chat:conversation_list")

    def form_valid(self, form):
        # Save user and log them in immediately
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class LoginView(DjangoLoginView):
    """
    Standard Django login view configured for Messenger layout.
    """
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class LogoutView(DjangoLogoutView):
    """
    Standard Django logout view.
    """
    next_page = reverse_lazy("accounts:login")


class FriendListView(LoginRequiredMixin, ListView):
    """
    Display the list of contacts (friends) and handle user search to add friends.
    """
    model = Contact
    template_name = "accounts/friend_list.html"
    context_object_name = "contacts"

    def get_queryset(self):
        # Fetch all contacts for current user
        return Contact.objects.filter(
            Q(user1=self.request.user) | Q(user2=self.request.user)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add sent/received friend requests to context
        context["sent_requests"] = FriendRequest.objects.filter(
            sender=self.request.user, status="pending"
        )
        context["received_requests"] = FriendRequest.objects.filter(
            receiver=self.request.user, status="pending"
        )
        
        # User search feature
        query = self.request.GET.get("q")
        if query:
            # Exclude current user and existing friends
            friend_ids = []
            for contact in self.get_queryset():
                friend_ids.append(contact.user1_id if contact.user2_id == self.request.user.id else contact.user2_id)
            
            context["search_results"] = User.objects.filter(
                Q(username__icontains=query) | Q(email__icontains=query)
            ).exclude(id__in=friend_ids + [self.request.user.id])
            
        return context


class ManageFriendRequestView(LoginRequiredMixin, View):
    """
    Functionality handled via POST request (FBV-like behavior wrapped in a View)
    to send/accept/reject friend requests.
    """
    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        target_user_id = request.POST.get("user_id")
        
        if not target_user_id:
            return redirect("accounts:friend_list")
            
        target_user = User.objects.get(id=target_user_id)

        if action == "send":
            FriendRequest.objects.get_or_create(sender=request.user, receiver=target_user)
        elif action == "accept":
            req = FriendRequest.objects.filter(sender=target_user, receiver=request.user, status="pending").first()
            if req:
                req.status = "accepted"
                req.save()
                # Create Contact entry (always user1_id < user2_id to keep uniform unique records)
                u1, u2 = (request.user, target_user) if request.user.id < target_user.id else (target_user, request.user)
                Contact.objects.get_or_create(user1=u1, user2=u2)
        elif action == "reject":
            req = FriendRequest.objects.filter(sender=target_user, receiver=request.user, status="pending").first()
            if req:
                req.status = "rejected"
                req.save()

        return redirect("accounts:friend_list")
