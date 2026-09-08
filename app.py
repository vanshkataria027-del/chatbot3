import streamlit as st
from google import genai

st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 My AI Chatbot")
st.caption("Powered by Gemini")

# Gemini
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = "gemini-3.8-flash"

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your message..."):

    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Send complete conversation to Gemini
    contents = []

    for message in st.session_state.messages:
        contents.append(
            f"{message['role']}: {message['content']}"
        )

    response = client.models.generate_content(
        model=model,
        contents="\n\n".join(contents)
    )

    answer = response.text

    # Display response
    with st.chat_message("assistant"):
        st.markdown(answer)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
        )
