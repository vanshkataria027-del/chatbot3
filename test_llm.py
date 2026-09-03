import ollama

print("🤖 Local AI Chatbot started!")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("AI:", response["message"]["content"])