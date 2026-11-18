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
model = MODELS[0]
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

    # Send conversation
    contents = []

    for message in st.session_state.messages:
        contents.append(
            f"{message['role']}: {message['content']}"
        )

    # Gemini request with retry
    response = None

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=model,
                contents="\n\n".join(contents),
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(
                        thinking_level="low"
                    ),
                    max_output_tokens=1000
                )
            )
            break

        except Exception as e:
            error_text = str(e)

            if "503" in error_text or "UNAVAILABLE" in error_text:
                if attempt < 2:
                    time.sleep(2 ** attempt)
                else:
                    st.error(
                        "Gemini is temporarily busy. "
                        "Please try again in a few seconds."
                    )
                    st.stop()

            elif "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                if attempt < 2:
                    time.sleep(10)
                else:
                    st.error(
                        "Free tier ka quota khatam ho gaya hai. "
                        "1 minute baad try karein."
                    )
                    st.stop()

            else:
                st.error(f"Gemini error: {e}")
                st.stop()

    answer = response.text

    # Display response
    with st.chat_message("assistant"):
        st.markdown(answer)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
