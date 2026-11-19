import time
import streamlit as st
from google import genai
from google.genai import types

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

MODELS = ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-2.5-flash"]

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

    # Send conversation (sirf last 6 messages)
    contents = []
    for message in st.session_state.messages[-6:]:
        contents.append(f"{message['role']}: {message['content']}")

    # Gemini request: har model try karo
    response = None
    last_error = ""

    for m in MODELS:
        try:
            if m.startswith("gemini-3"):
                config = types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(
                        thinking_level="low"
                    ),
                    max_output_tokens=1000,
                )
            else:
                config = types.GenerateContentConfig(
                    max_output_tokens=1000
                )

            response = client.models.generate_content(
                model=m,
                contents="\n\n".join(contents),
                config=config,
            )
            break
        except Exception as e:
            last_error = str(e)
            time.sleep(1)

    if response is None:
        if "429" in last_error or "RESOURCE_EXHAUSTED" in last_error:
            st.error("Free tier ka quota khatam ho gaya hai. 1 minute baad try karein.")
        else:
            st.error("Gemini is temporarily busy. Please try again in a few seconds.")
        st.stop()

    answer = response.text

    # Display response
    with st.chat_message("assistant"):
        st.markdown(answer)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
