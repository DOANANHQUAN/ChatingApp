from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Notification

class NotificationListView(LoginRequiredMixin, ListView):
    """
    List user notifications.
    """
    model = Notification
    template_name = "notifications/notification_list.html"
    context_object_name = "notifications"

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)


class MarkNotificationReadView(LoginRequiredMixin, View):
    """
    Mark a single or all notifications as read.
    """
    def post(self, request, pk=None):
        if pk:
            notification = get_object_or_404(Notification, id=pk, recipient=request.user)
            notification.is_read = True
            notification.save()
            return JsonResponse({"status": "success"})
        else:
            Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
            if request.headers.get("HX-Request"):
                return render(request, "notifications/partials/notification_bell.html", {"unread_notifications_count": 0})
            return redirect("notifications:list")
        
        return JsonResponse({"status": "error"}, status=400)
