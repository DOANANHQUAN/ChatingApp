from django.contrib import admin
from .models import Conversation, ConversationParticipant, Message, MessageAttachment, MessageStatus

class ParticipantInline(admin.TabularInline):
    model = ConversationParticipant
    extra = 1

class AttachmentInline(admin.TabularInline):
    model = MessageAttachment
    extra = 0

class ConversationAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "is_group", "created_at", "updated_at"]
    inlines = [ParticipantInline]

class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "conversation", "sender", "content_snippet", "created_at"]
    inlines = [AttachmentInline]

    def content_snippet(self, obj):
        return obj.content[:50] if obj.content else "[Tệp đính kèm]"
    content_snippet.short_description = "Nội dung"

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(MessageAttachment)
admin.site.register(MessageStatus)
