from chatbot.web_result_ranker import WebResultRanker


ranker = WebResultRanker()


query = "Python machine learning"


results = [

    {
        "title": "Python Machine Learning Tutorial",

        "url": "https://example.com/python",

        "content": (
            "Python is widely used for "
            "machine learning and data science."
        ),

        "score": 0.90
    },

    {
        "title": "Best Travel Destinations",

        "url": "https://example.com/travel",

        "content": (
            "Nepal has many beautiful "
            "tourism destinations."
        ),

        "score": 0.80
    },

    {
        "title": "Machine Learning with Python",

        "url": "https://example.com/ml",

        "content": (
            "Machine learning can be implemented "
            "using Python libraries."
        ),

        "score": 0.85
    }

]


ranked = ranker.rank(

    query,

    results,

    top_k=3

)


print("=" * 60)

print("RANKED RESULTS")

print("=" * 60)


for i, result in enumerate(

    ranked,

    start=1

):

    print()

    print("Rank:", i)

    print("Title:", result["title"])

    print(
        "Score:",
        result["relevance_score"]
    )

    print("URL:", result["url"])

    print("-" * 60)