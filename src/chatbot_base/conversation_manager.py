import os
from dotenv import load_dotenv
from openai import OpenAI
from chatbot_base.token_estimator import total_tokens_used
load_dotenv()

DEFAULT_API_KEY = os.environ.get("DEFAULT_API_KEY")
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL")
BASE_URL = os.environ.get("BASE_URL") or None # Set this if you are using any 3rd party provider that is compatible with the OpenAI ChatCompletion API
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 512
DEFAULT_TOKEN_BUDGET = 4096
DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."


class ConversationManager:
    def __init__(self, api_key=None, model=None, system_prompt=None, temperature=None, max_tokens=None, token_budget=None):
        self.client = OpenAI(base_url=BASE_URL, api_key=api_key or DEFAULT_API_KEY)
        self.model = model or DEFAULT_MODEL
        self.temperature = temperature if temperature is not None else DEFAULT_TEMPERATURE
        self.max_tokens =  max_tokens if max_tokens is not None else DEFAULT_MAX_TOKENS
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]
        self.token_budget = token_budget if token_budget else DEFAULT_TOKEN_BUDGET

    def enforce_token_budget(self):
        while total_tokens_used(self.model, self.conversation_history) > self.token_budget:
            if len(self.conversation_history) <= 1:
                break   # Break only if system message is left
            self.conversation_history.pop(1) # Remove first messaage after system message

    def chat_completion(self, user_prompt, temperature=None, max_tokens=None):
        self.enforce_token_budget()
        self.conversation_history.append({"role": "user", "content": user_prompt})

        response = self.client.chat.completions.create(
            model = self.model,
            messages = self.conversation_history,
            temperature = temperature if temperature is not None else self.temperature,
            max_tokens = max_tokens if max_tokens is not None else self.max_tokens
        )

        message = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": message})
        
        # print(f"Total tokens used: {total_tokens_used(self.model, self.conversation_history)}")

        return {"message": message, "total_tokens": response.usage.total_tokens, "finish_reason": response.choices[0].finish_reason}

