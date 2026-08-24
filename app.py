import json
import string
import streamlit as st

with open("faqs.json", "r") as f:
    faqs = json.load(f)

def get_answer(user_question):
    user_question = user_question.lower().translate(str.maketrans('','',string.punctuation))
    for faq in faqs:
        faq_question = faq["question"].lower().translate(str.maketrans('','',string.punctuation))
        if faq_question in user_question:
            return faq["answer"]
    return "Sorry, I don't have an answer for that yet."

st.title("chatbot3")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask me something:")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    answer = get_answer(question)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)