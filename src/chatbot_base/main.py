from chatbot_base.conversation_manager import ConversationManager

def main():
    conv_manager = ConversationManager()
    print(conv_manager.chat_completion("You are a mad scientist",  "what's your latest invention?"))

if __name__ == "__main__":
    main()
