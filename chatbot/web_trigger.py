import re


class WebTrigger:

    def __init__(self):

        pass

    def is_live_query(self, query):

        keywords = [

            "latest",

            "today",

            "current",

            "news",

            "recent",

            "yesterday",

            "this week",

            "this month",

            "2026",

            "2027"

        ]

        query = query.lower()

        return any(

            keyword in query

            for keyword in keywords

        )

    def user_requested_web(self, query):

        keywords = [

            "search the web",

            "search online",

            "google",

            "internet",

            "look online",

            "browse"

        ]

        query = query.lower()

        return any(

            keyword in query

            for keyword in keywords

        )

    def rag_failed(

        self,

        context

    ):

        if context is None:

            return True

        if len(context.strip()) == 0:

            return True

        if len(context) < 150:

            return True

        return False

    def should_search(

        self,

        query,

        rag_context

    ):

        if self.user_requested_web(query):

            return True

        if self.is_live_query(query):

            return True

        if self.rag_failed(rag_context):

            return True

        return False

