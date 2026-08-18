from chatbot_base.conversation_manager import ConversationManager

def main():
    conv_manager = ConversationManager(system_prompt="You are a mad scientist")
    response = conv_manager.chat_completion("what's your latest invention?") 

    print(response["message"])
    print(f"\n\n {'='*50} \n\n")
    print(f"Total tokens = {response["total_tokens"]}")
    print(f"Finish reason = {response["finish_reason"]}")

if __name__ == "__main__":
    main()
