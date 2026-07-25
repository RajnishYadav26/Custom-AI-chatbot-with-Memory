from chatbot.web_search import WebSearch


class BaseSearch(WebSearch):

    def search(
        self,
        query,
        max_results=5
    ):
        raise NotImplementedError