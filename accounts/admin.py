from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Contact, FriendRequest

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ["username", "email", "first_name", "last_name", "is_online", "last_seen", "is_staff"]
    fieldsets = UserAdmin.fieldsets + (
        ("Messenger Info", {"fields": ("avatar", "is_online", "last_seen")}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Contact)
admin.site.register(FriendRequest)
