import re


class RouterAgent:

    def __init__(self):
        pass

    def needs_memory(self, query):

        query = query.lower()

        patterns = [

            r"\bmy\b",

            r"\bremember\b",

            r"\bi am\b",

            r"\bwho am i\b",

            r"\bmy name\b",

            r"\bfavorite\b"

        ]

        return any(
            re.search(pattern, query)
            for pattern in patterns
        )

    def needs_pdf(self, query):

        query = query.lower()

        keywords = [

            "pdf",

            "document",

            "uploaded",

            "page",

            "chapter",

            "paper",

            "resume",

            "summarize this file"

        ]

        return any(
            keyword in query
            for keyword in keywords
        )

    def needs_code(self, query):

        query = query.lower()

        keywords = [

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

        return any(
            keyword in query
            for keyword in keywords
        )

    def needs_research(self, query):

        query = query.lower()

        keywords = [

            "what is",

            "explain",

            "define",

            "difference",

            "compare",

            "advantages",

            "disadvantages",

            "how does"

        ]

        return any(
            keyword in query
            for keyword in keywords
        )

    def route(self, query):

        if self.needs_pdf(query):
            return "pdf"

        if self.needs_memory(query):
            return "memory"

        if self.needs_code(query):
            return "code"

        if self.needs_research(query):
           return "research"

        return "general"