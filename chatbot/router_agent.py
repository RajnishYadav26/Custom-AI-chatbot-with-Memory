import re


class RouterAgent:

    def __init__(self):

        pass

    def needs_memory(self, query):

        patterns = [

            r"\bmy\b",

            r"\bremember\b",

            r"\bi am\b",

            r"\bwho am i\b",

            r"\bmy name\b",

            r"\bfavorite\b"

    ]

        query = query.lower()

        return any(
            re.search(p, query)
            for p in patterns
    )

    def needs_research(self, query):

        patterns = [

            r"what is",

            r"explain",

            r"define",

            r"difference",

           r"compare",

           r"advantages",

           r"disadvantages",

           r"how does"

    ]

        query = query.lower()

        return any(
            p in query
            for p in patterns
    )


    def needs_pdf(self, query):

        patterns = [

            "pdf",

            "document",

            "page",

            "uploaded",

            "chapter",

            "paper",

            "summarize this file"

    ]

        query = query.lower()

        return any(
            p in query
            for p in patterns
    )

    def needs_code(self, query):

        patterns = [

            "python",

            "java",

            "javascript",

            "react",

            "fastapi",

            "sql",

           "docker",

           "api",

           "bug",

           "debug",

           "code",

           "algorithm"

    ]

        query = query.lower()

        return any(
            p in query
            for p in patterns
    )


    def route(self, query):

        agents = []

        if self.needs_memory(query):

            agents.append("memory")

        if self.needs_research(query):

            agents.append("research")

        if self.needs_pdf(query):

            agents.append("pdf")

        if self.needs_code(query):

            agents.append("code")

        if not agents:

            agents.append("research")

        return agents

        if trigger.should_search(query, rag_context):

            agents.append("web")