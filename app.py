import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 My AI Chatbot")
st.caption("Powered by Gemini")

# Gemini API key
genai.configure(api_key=st.secrets["AQ.Ab8RN6Kd4PvDeAiaDNxs-4FXQy93mXbKKINck6M17Xs-EBU4-Qs"])


model = genai.GenerativeModel("gemini-1.5-flash")

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
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = model.generate_content(user_input)
            answer = response.text

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
