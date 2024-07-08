from .adapters import GPTAdapter
from .models import Room, Assistant
from .gpt_cache import get_response_from_cache, set_question_and_response_in_cache
from datetime import datetime


def send_message_and_get_response_from_ai(user, message, gpt_thread_id=None):
    adapter = GPTAdapter(user)
    if not gpt_thread_id:
        thread = adapter.create_thread()
        gpt_thread_id = thread.id
        add_thread_id_against_user(user, gpt_thread_id)
    
    cache_msg = get_response_from_cache(message)
    if cache_msg is not None:
        return cache_msg

    adapter.create_message(gpt_thread_id, message=message)
    run = adapter.run_thread(thread_id=gpt_thread_id)
    adapter.check_run(run_id=run.id, thread_id=gpt_thread_id)
    response = adapter.get_response(thread_id=gpt_thread_id)
    
    set_question_and_response_in_cache(message, response)

    return response


def send_message_and_get_response_from_ai_using_thread_id(thread_id, message):
    adapter = GPTAdapter()
    cache_msg = get_response_from_cache(message)
    if cache_msg is not None:
        return cache_msg

    t1 = datetime.now()
    adapter.create_message(thread_id, message=message)
    run = adapter.run_thread(thread_id=thread_id)
    adapter.check_run(run_id=run.id, thread_id=thread_id)
    response = adapter.get_response(thread_id=thread_id)
    t2 = datetime.now()
    print("Time to get Response from AI ", (t2-t1).seconds)

    t1 = datetime.now()
    set_question_and_response_in_cache(message, response)
    t2 = datetime.now()
    print("Time to set cache response ", (t2-t1))
    return response


def add_thread_id_against_user(user, gpt_thread_id):
    assistant = Assistant.objects.get_default_assistant()
    room = Room(assistant=assistant, user=user, gpt_thread_id=gpt_thread_id)
    room.save()
    return room
