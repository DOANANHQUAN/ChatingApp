from django.shortcuts import redirect
from django.views import View

class IndexView(View):
    """
    Landing page redirecting user depending on authentication status.
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("chat:conversation_list")
        return redirect("accounts:login")
