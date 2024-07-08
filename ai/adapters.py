import os
import time
import openai
from openai import OpenAI
from .models import Assistant, Room

api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


class GPTAdapter(object):

    def __init__(self):
        self.set_default_assistant()

    def set_default_assistant(self):
        assistant_id = os.environ.get("ASSISTANT_ID", None)
        self.assistant_id = assistant_id

    def create_thread(self):
        try:
            thread = client.beta.threads.create()
        
        except openai.APIConnectionError as e:
            raise ValueError(e)
        
        except openai.RateLimitError as e:
            raise ValueError(e)
        
        except openai.BadRequestError as e:
            raise ValueError(e)

        except openai.InternalServerError as e:
            raise ValueError(e)

        self.thread = thread
        return thread

    def delete_thread(self, thread_id):
        response = client.beta.threads.delete(thread_id)
        return response
    
    def create_message(self, thread_id, message):
        try:
            message = client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message
            )
        
        except openai.BadRequestError as e:
            raise ValueError(e)

        except openai.NotFoundError as e:
            raise ValueError(e)

        except openai.RateLimitError as e:
            raise ValueError(e)
        
        except openai.APIConnectionError as e:
            raise ValueError(e)
        
        except openai.InternalServerError as e:
            raise ValueError(e)

        return message

    def run_thread(self, thread_id):
        try:
            run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=self.assistant_id,
            )
        
        except openai.BadRequestError as e:
            raise ValueError(e)
        
        except openai.InternalServerError as e:
            raise ValueError(e)
        
        except openai.RateLimitError as e:
            raise ValueError(e)
        
        except openai.APIConnectionError as e:
            raise ValueError(e)

        return run

    def check_run(self, run_id, thread_id):
        while True:
            run = self.check_run_status(run_id, thread_id)
            if run.status == "completed":
                print("Run is Completed")
                break

            elif run.status == "expired":
                print("Run is expired")
                break

            elif run.status == "requires_action":
                print("Run Requires Action")
                break

            else:
                print(f"Run is not Completed Yet, Waiting {run.status}")
                time.sleep(3)

        return run

    def check_run_status(self, run_id, thread_id):
        try:
            run = client.beta.threads.runs.retrieve(
                run_id=run_id,
                thread_id=thread_id,
            )
        
        except openai.APIConnectionError as e:
            raise ValueError(e)
        
        return run

    def get_response(self, thread_id):
        try:
            messages = client.beta.threads.messages.list(
                thread_id=thread_id
            )
        
        except openai.APIConnectionError as e:
            raise ValueError(e)
        
        gpt_response = messages.data[0].content[0].text.value
        print(f"OpenAI: {gpt_response}")
        return gpt_response
