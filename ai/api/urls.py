from django.urls import path
from .views import UserChatSessionCreateAPIView, UserChatCreateAPIView, end_user_chat_session

urlpatterns = [
    path("chat/sessions/", UserChatSessionCreateAPIView.as_view(), ),
    path("chat/message/", UserChatCreateAPIView.as_view(), ),
    path("chat/sessions/end/", end_user_chat_session),
]
