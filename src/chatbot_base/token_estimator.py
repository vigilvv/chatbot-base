from openai import OpenAI
import tiktoken

# Function to count the number of tokens in a text
def count_tokens(model_name, text):
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        encoding = tiktoken.get_encoding("o200k_harmony") # Fallback value

    tokens = encoding.encode(text)
    return len(tokens)

# Function to calculate the total number of tokens used in the conversation history
def total_tokens_used(model_name, conversation_history):
    return sum(count_tokens(model_name, message['content']) for message in conversation_history)
