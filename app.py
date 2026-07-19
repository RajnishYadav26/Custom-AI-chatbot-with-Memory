from chatbot.llm import (
    get_ai_response,
    get_token_usage,
    clear_chat,
    memory,
    session
)


def show_banner():

    print("=" * 60)
    print("🤖 Custom AI Chatbot with Memory")
    print("=" * 60)
    print("Commands")
    print("-" * 60)
    print("help      - Show commands")
    print("history   - Show conversation")
    print("clear     - Clear memory")
    print("tokens    - Show token usage")
    print("sessions  - Show saved sessions")
    print("exit      - Exit chatbot")
    print("=" * 60)


show_banner()

while True:

    user_input = input("\nYou : ").strip()

    if not user_input:
        continue

    command = user_input.lower()

    # -----------------------------
    # Exit
    # -----------------------------
    if command == "exit":
        print("\n👋 Goodbye!")
        break

    # -----------------------------
    # Help
    # -----------------------------
    elif command == "help":
        show_banner()
        continue

    # -----------------------------
    # Clear Memory
    # -----------------------------
    elif command == "clear":

        clear_chat()

        print("\n✅ Memory cleared.")

        continue

    # -----------------------------
    # History
    # -----------------------------
    elif command == "history":

        print("\nConversation History\n")

        for msg in memory.get_history():

            print(
                f"{msg['role']} : {msg['text']}"
            )

        continue

    # -----------------------------
    # Token Usage
    # -----------------------------
    elif command == "tokens":

        print(
            f"\nCurrent Tokens : {get_token_usage()}"
        )

        continue

    # -----------------------------
    # Sessions
    # -----------------------------
    elif command == "sessions":

        session.list_sessions()

        continue

    # -----------------------------
    # AI Response
    # -----------------------------
    try:

        response = get_ai_response(user_input)

        print("\nAI :", response)

    except Exception as e:

        print("\n❌ Error")

        print(e)