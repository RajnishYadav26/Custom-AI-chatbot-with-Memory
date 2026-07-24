from chatbot.response_agent import ResponseAgent

agent = ResponseAgent()

response = agent.answer(

    question="What is Retrieval Augmented Generation?",

    memory="User prefers Python.",

    research="RAG retrieves relevant context before generation.",

    pdf="The uploaded paper explains vector databases.",

    code=""

)

for token in response:

    print(token, end="")