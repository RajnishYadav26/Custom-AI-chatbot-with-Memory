from chatbot.search_router import SearchRouter
from chatbot.web_result_ranker import WebResultRanker

class WebAgent:

    def __init__(self):

        self.search_router = SearchRouter()
        self.ranker = WebResultRanker()

    def search(

        self,

        query,

        max_results=5

    ):

        return self.search_router.search(

            query,

            max_results

        )

    def build_context(

        self,

        query,

        max_results=5

    ):

        results = self.search(

            query,

            max_results

        )

        return self.search_router.build_context(

            results

        )

    def retrieve(

        self,

        query,

        max_results=5

):

        results = self.search(

            query,

            max_results=max_results

    )

    # Rank web results

        results = self.ranker.rank(

            query,

            results,

            top_k=max_results

    )

        context = self.search_router.build_context(

            results

    )

        return {

            "results": results,

            "context": context

    }

    def get_sources(

        self,

        results

    ):

        sources = []

        for result in results:

            sources.append(

                {

                    "title": result["title"],

                    "url": result["url"]

                }

            )

        return sources


    def retrieve_with_sources(

        self,

        query,

        max_results=5

):

        data = self.retrieve(

            query,

            max_results

    )

        sources = []

        for result in data["results"]:

            sources.append({

                "title":
                    result["title"],

                "url":
                    result["url"],

                "score":
                    result.get(
                        "relevance_score",
                        0
                )

        })

        data["sources"] = sources

        return data