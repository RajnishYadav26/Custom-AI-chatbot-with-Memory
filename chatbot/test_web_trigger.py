from chatbot.web_trigger import WebTrigger

trigger = WebTrigger()

questions = [

    "Explain Retrieval Augmented Generation",

    "Latest AI News",

    "Search the web for OpenAI",

    "Current weather in Nepal",

    "What is Python?"

]

contexts = [

    "RAG combines retrieval and generation." * 20,

    "",

    "",

    "",

    "Python is a programming language." * 20

]

for question, context in zip(questions, contexts):

    print("=" * 60)

    print(question)

    print(

        trigger.should_search(

            question,

            context

        )

    )