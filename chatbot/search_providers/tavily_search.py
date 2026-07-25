import os

from dotenv import load_dotenv
from tavily import TavilyClient

from chatbot.search_providers.base_search import BaseSearch

load_dotenv()


class TavilySearch(BaseSearch):

    def __init__(self):

        self.client = TavilyClient(

            api_key=os.getenv("TAVILY_API_KEY")

        )

    def search(

        self,

        query,

        max_results=5

    ):

        response = self.client.search(

            query=query,

            max_results=max_results

        )

        results = []

        for item in response["results"]:

            results.append(

                {

                    "title": item["title"],

                    "url": item["url"],

                    "content": item["content"],

                    "score": item.get("score", 0)

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

       