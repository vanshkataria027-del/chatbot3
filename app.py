import json 
import streamlit as st 

st.write("App started")

with open("faqs.json", "r") as f:
    faqs = json.load(f)
st.write("JSON load successfully")

def get_answer(user_question):
    user_question = user_question.lower()
    for faq in faqs:
        if faq["question"].lower() in user_question:
            return faq["answer"]
        return "Sorry, I don't have an answer for that yet."
    st.title("chatbot3")

    question = st.text_input("Ask me something:")

    if question:
        answer = get_answer(question)
        st.write(answer)