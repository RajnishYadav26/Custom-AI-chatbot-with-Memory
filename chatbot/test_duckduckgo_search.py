from chatbot.search_providers.duckduckgo_search import DuckDuckGoSearch

search = DuckDuckGoSearch()

results = search.search(

    "What is Retrieval Augmented Generation?",

    max_results=3

)

print()

print("=" * 60)

print("SEARCH RESULTS")

print("=" * 60)

for i, result in enumerate(results, start=1):

    print(f"\nResult {i}")

    print("Title :", result["title"])

    print("URL   :", result["url"])

    print("Content")

    print(result["content"])

    print("-" * 60)


context = search.build_context(results)

print()

print("=" * 60)

print("FINAL CONTEXT")

print("=" * 60)

print(context)