from chatbot.web_agent import WebAgent

agent = WebAgent()

data = agent.retrieve_with_sources(

    "Latest AI News",

    max_results=3

)

print("=" * 60)

print("CONTEXT")

print("=" * 60)

print(data["context"])

print()

print("=" * 60)

print("SOURCES")

print("=" * 60)

for source in data["sources"]:

    print(source["title"])

    print(source["url"])

    print("-" * 50)