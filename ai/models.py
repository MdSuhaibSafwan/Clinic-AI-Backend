import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models.query import QuerySet


User = get_user_model()

def create_hex():
    u = uuid.uuid4()
    return u.hex


class AssistantManager(models.Manager):

    def get_default_assistant(self):
        obj = self.get_queryset().filter(default=True).first()
        if obj is None:
            raise ValueError("No Default Assistant Found")
        
        return obj


class Assistant(models.Model):
    assistant_id = models.CharField(
        verbose_name="Assistant ID",
        max_length=100,
        unique=True,
        help_text="Id of OpenAI Assistant",
    )

    instructions = models.TextField(
        help_text="Instructions Given while creating assistant",
        null=True,
        blank=True
    )

    default = models.BooleanField(
        default=False,
        help_text="Suggests that current assistant being used",
    )

    date_created = models.DateTimeField(
        auto_now_add=True
    )

    objects = AssistantManager()

    def __str__(self):
        return str(self.assistant_id)

    class Meta:
        db_table = "db_assistant"


class RoomManager(models.Manager):

    def get_user_room(self, user):
        obj = self.get_queryset().filter(expired=False, user=user).first()
        return obj
        

class Room(models.Model):
    gpt_thread_id = models.CharField(
        max_length=100,
        verbose_name="GPT Thread",
        help_text="Thread Id of the assistant"
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
    )

    last_updated = models.DateTimeField(
        auto_now=True
    )

    objects = RoomManager()

    def __str__(self):
        return str(self.room_id)

    class Meta:
        db_table = "db_room"
        ordering = ["-date_created", ]


class MessageQuerySet(models.QuerySet):
    
    def filter_via_params(self, params=None):
        if params is None:
            return self
        final_params = {}
        for i, j in params.items():
            if getattr(Message, i, None) is not None:
                final_params[i] = "".join(j)

        queryset = self.filter(**final_params)
        return queryset

    def get_user_message_of_current_room(self, user):
        qs = self.all().filter(Q(room__user=user, room__expired=False))
        return qs


class Message(models.Model):
    room = models.ForeignKey(
        to=Room,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Room ID",
        help_text="Room Id of the message sent to GPT"
    )

    user_message = models.TextField(
        verbose_name="User Message to GPT"
    )

    gpt_response = models.TextField(
        verbose_name="Response from OpenAI"
    )

    additional_text = models.TextField(
        verbose_name="Additional Information from response",
        null=True,
        blank=True,
    )
    additional_data = models.JSONField(
        verbose_name="Additional Data from GPT",
        default=dict,
        null=True,
        blank=True
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
    )

    objects = MessageQuerySet.as_manager()

    class Meta:
        db_table = "db_message"
        ordering = ["-date_created", ]

    def __str__(self):
        return str(self.id)

