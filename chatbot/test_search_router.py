from chatbot.search_router import SearchRouter

router = SearchRouter()

results = router.search(

    "Latest AI News",

    max_results=3

)

print()

print("="*60)

print("RESULTS")

print("="*60)

for result in results:

    print()

    print(result["title"])

    print(result["url"])

    print(result["content"])

context = router.build_context(results)

print()

print("="*60)

print("CONTEXT")

print("="*60)

print(context)