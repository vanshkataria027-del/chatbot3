import json

faqs = []
with open("faqs.json", "r") as f:
    faqs = json.load(f)

def get_answer(user_question):
    user_question = user_question.lower()
    for faq in faqs:
        if faq["question"].lower() in user_question:
            return faq["answer"]
    return "Sorry, I don't have an answer for that yet."

print("Program started")

while True:
    q = input("Ask me something (or 'quit'): ")
    if q.lower() == "quit":
        break
    print(get_answer(q))

print("Program ended")