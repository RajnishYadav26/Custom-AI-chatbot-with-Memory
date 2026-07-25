from duckduckgo_search import DDGS

from chatbot.search_providers.base_search import BaseSearch


class DuckDuckGoSearch(BaseSearch):

    def __init__(self):

        self.ddgs = DDGS()

    def search(

        self,

        query,

        max_results=5

    ):

        response = self.ddgs.text(

            query,

            max_results=max_results

        )

        results = []

        for item in response:

            results.append(

                {

                    "title": item.get("title", ""),

                    "url": item.get("href", ""),

                    "content": item.get("body", ""),

                    "score": 0.0

                }

            )

        return results

    def build_context(

        self,

        results

    ):

        context = ""

        for result in results:

            context += (

                f"Title: {result['title']}\n"

                f"Source: {result['url']}\n"

                f"Content: {result['content']}\n\n"

            )

        return context