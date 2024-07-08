from rest_framework import serializers
from ..models import Assistant, Room, Message
from ..adapters import GPTAdapter
from ..utils import send_message_and_get_response_from_ai, send_message_and_get_response_from_ai_using_thread_id
from django.forms.models import model_to_dict


class AssistantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assistant
        fields = "__all__"


class RoomListSerializer(serializers.ModelSerializer):
    assistant = AssistantSerializer()
    expired_at = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_expired_at(self, obj):
        if not obj.expired:
            return None
        
        return obj.last_updated


class RoomCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = "__all__"
        read_only_fields = ["session_key", "gpt_thread_id"]

    def create(self, validated_data):
        request = self.context.get("request")
        adapter = GPTAdapter()
        thread = adapter.create_thread()
        session_key = request.session.session_key
        room = self.Meta.model(**validated_data, gpt_thread_id=thread.id)
        # room.save()
        return room


class RoomDeleteSerializer(serializers.Serializer):
    thread_id = serializers.CharField()

    def perform_deletion(self):
        thread_id = self.validated_data.get("thread_id")
        adapter = GPTAdapter()
        adapter.delete_thread(thread_id)
        return thread_id


class MessageListSerializer(serializers.ModelSerializer):
    room = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = "__all__"

    def get_room(self, obj):
        room = obj.room
        dict_obj = model_to_dict(room)
        return dict_obj


class MessageCreateSerializer(serializers.Serializer):
    thread_id = serializers.CharField()
    user_message = serializers.CharField()

    def create(self, validated_data):
        user_message = validated_data.get("user_message")
        thread_id = validated_data.get("thread_id")
        try:
            gpt_response = send_message_and_get_response_from_ai_using_thread_id(thread_id, user_message)
            obj = Message(user_message=user_message, gpt_response=gpt_response)
        except ValueError as e:
            raise serializers.ValidationError(e)

        return obj
