from chatbot.search_providers.tavily_search import TavilySearch

search = TavilySearch()

results = search.search(

    "What is Retrieval Augmented Generation?",

    max_results=3

)

print()

print("=" * 60)

print("RESULTS")

print("=" * 60)

for i, result in enumerate(results, start=1):

    print()

    print(f"Result {i}")

    print("Title :", result["title"])

    print("URL   :", result["url"])

    print("Score :", result["score"])

    print("Content")

    print(result["content"])

    print("-" * 60)


context = search.build_context(results)

print()

print("=" * 60)

print(context)