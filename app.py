import streamlit as st
import ollama

st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 My AI Chatbot")
st.caption("Powered by Ollama • Llama 3.2")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ollama.chat(
                model="llama3.2",
                messages=st.session_state.messages
            )

            answer = response["message"]["content"]
            st.markdown(answer)

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
