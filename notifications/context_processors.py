from .models import Notification

def unread_notifications(request):
    """
    Context processor to inject unread notification count globally.
    """
    if request.user.is_authenticated:
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return {"unread_notifications_count": count}
    return {"unread_notifications_count": 0}
