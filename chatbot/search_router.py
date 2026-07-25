import os

from dotenv import load_dotenv

from chatbot.search_providers.tavily_search import TavilySearch
from chatbot.search_providers.duckduckgo_search import DuckDuckGoSearch

load_dotenv()

class SearchRouter:

    def __init__(self):

        self.tavily = TavilySearch()

        self.duckduckgo = DuckDuckGoSearch()

    def has_tavily(self):

        key = os.getenv("TAVILY_API_KEY")

        if key:

            return True

        return False


    def search(

        self,

        query,

        max_results=5

    ):

        try:

            if self.has_tavily():

                print("Using Tavily")

                return self.tavily.search(

                    query,

                    max_results

                )

        except Exception as e:

            print("Tavily Failed")

            print(e)

        print("Fallback DuckDuckGo")

        return self.duckduckgo.search(

            query,

            max_results

        )

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