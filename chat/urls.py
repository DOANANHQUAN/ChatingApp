from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.ConversationListView.as_view(), name="conversation_list"),
    path("<int:pk>/", views.ConversationDetailView.as_view(), name="conversation_detail"),
    path("<int:pk>/send/", views.SendMessageView.as_view(), name="send_message"),
    path("start/<int:user_id>/", views.StartPrivateChatView.as_view(), name="start_chat"),
]
