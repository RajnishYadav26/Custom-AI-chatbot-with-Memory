from chatbot.router_agent import RouterAgent

router = RouterAgent()

questions = [

    "My name is Rajnish",

    "Explain Retrieval Augmented Generation",

    "Summarize uploaded PDF",

    "Write FastAPI CRUD",

    "What is my favorite language?",

    "Compare RAG and Fine Tuning",

    "Debug this Python code"

]

for q in questions:

    print("=" * 60)

    print(q)

    print(router.route(q))