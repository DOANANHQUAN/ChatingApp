from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("friends/", views.FriendListView.as_view(), name="friend_list"),
    path("friends/request/", views.ManageFriendRequestView.as_view(), name="friend_request"),
]
