import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DEFAULT_API_KEY = os.environ.get("DEFAULT_API_KEY")
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL")
BASE_URL = os.environ.get("BASE_URL") or None # Set this if you are using any 3rd party provider that is compatible with the OpenAI ChatCompletion API

class ConversationManager:
    def __init__(self, api_key=None, model=None):
        self.client = OpenAI(base_url=BASE_URL, api_key=api_key or DEFAULT_API_KEY)
        self.model = model or DEFAULT_MODEL

    def chat_completion(self, system_prompt, user_prompt):
        messages = [{"role": "system", "content": system_prompt}, {"role": "system", "content": user_prompt}]

        response = self.client.chat.completions.create(
            model = self.model,
            messages = messages,
        )

        return response.choices[0].message.content

