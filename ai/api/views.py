from rest_framework.views import APIView
from ..utils import send_message_and_get_response_from_ai
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from .serializers import AssistantSerializer, RoomListSerializer, RoomCreateSerializer, MessageCreateSerializer, \
    MessageListSerializer, RoomDeleteSerializer
from ..models import Room, Message, Assistant
from django.contrib.sessions.backends.db import SessionStore
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets


class AssistantViewSet(viewsets.ModelViewSet):
    serializer_class = AssistantSerializer
    queryset = Assistant.objects.all()
    permission_classes = [IsAdminUser, ]


class UserChatSessionCreateAPIView(CreateAPIView):
    permission_classes = []
    method_serializer_classes = {
        ("GET", ): RoomListSerializer,
        ("POST", ): RoomCreateSerializer,
    }
    
    def get_serializer_class(self):
        for methods, serializer_cls in self.method_serializer_classes.items():
            if self.request.method in methods:
                return serializer_cls
        
        raise MethodNotAllowed(f"{self.request.method} not allowed")


class UserChatCreateAPIView(CreateAPIView):
    permission_classes = []
    method_serializer_classes = {
        ("GET", ): MessageListSerializer,
        ("POST", ): MessageCreateSerializer
    }

    def get_serializer_class(self):
        for methods, serializer_cls in self.method_serializer_classes.items():
            if self.request.method in methods:
                return serializer_cls
            
        raise MethodNotAllowed(f"{self.request.method} not allowed")

    def create(self, *args, **kwargs):
        serializer = self.get_serializer_class()(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        data = {
            "gpt_response": obj.gpt_response,
        }

        return Response(data, status=status.HTTP_201_CREATED)


@api_view(http_method_names=["POST", ])
@permission_classes([])
def end_user_chat_session(request):
    serializer = RoomDeleteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    thread_id = serializer.perform_deletion()

    response_data = {
        "message": f"session of {thread_id} ended successfully",
    }

    return Response(response_data, status=status.HTTP_200_OK)
