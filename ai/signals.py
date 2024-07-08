from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from .models import Room, Assistant
from django.db.models import Q

User = get_user_model()


@receiver(signal=pre_save, sender=Room)
def make_default_room_of_user_expired_if_new_room_is_created(sender, instance, **kwargs):
    created = True
    if instance.id:
        created = False
    
    if not created:
        return False
    
    room = Room.objects.get_user_room(instance.user)
    if room is None:
        return False
    
    if room.expired == True:
        return False
    
    room.expired = True
    room.save()
    print(f"Signals: Made Room {room} Expired...")
    return room


@receiver(signal=post_save, sender=Assistant)
def make_other_assistants_undefault_when_create_new_default_assistant(sender, instance, created, **kwargs):
    if not created:
        return False
    
    if instance.default == True:
        queryset = Assistant.objects.filter(~Q(id=instance.id, default=True))
        if queryset.exists():
            queryset.update(default=False)
            return True
        return False
    return False
