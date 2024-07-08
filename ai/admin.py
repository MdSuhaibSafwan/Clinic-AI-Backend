from django.contrib import admin
from .models import Assistant, Room, Message


class AssistantAdmin(admin.ModelAdmin):
    list_display = ["id", "assistant_id", "default", "date_created"]


class RoomAdmin(admin.ModelAdmin):
    list_display = ["gpt_thread_id", "date_created"]


class MessageAdmin(admin.ModelAdmin):
    list_display = ["room", "date_created"]


admin.site.register(Assistant, AssistantAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
