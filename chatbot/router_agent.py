import re


class RouterAgent:

    def __init__(self):
        pass

    # -----------------------------------------
    # MEMORY QUESTIONS
    # -----------------------------------------

    def needs_memory(self, query):

        query = query.lower()

        patterns = [

            r"\bremember\b",
            r"\bwho am i\b",
            r"\bmy name\b",
            r"\bmy favorite\b",
            r"\bmy goal\b",
            r"\bmy preference\b"

        ]

        return any(
            re.search(pattern, query)
            for pattern in patterns
        )

    # -----------------------------------------
    # PDF / RESUME QUESTIONS
    # -----------------------------------------

    def needs_pdf(self, query):

        query = query.lower()

        keywords = [

            "resume",
            "cv",

            "my resume",
            "my cv",

            "about my resume",
            "about my cv",

            "tell me about my resume",
            "tell me about my cv",

            "summarize my resume",
            "summarize my cv",

            "resume summary",
            "cv summary",

            "candidate",
            "candidate name",
            "candidate skills",
            "candidate education",
            "candidate experience",
            "candidate projects",

            "my skills",
            "my education",
            "my experience",
            "my projects",

            "uploaded document",
            "uploaded file",
            "uploaded pdf",

            "pdf",
            "document",
            "page",
            "chapter"

        ]

        return any(
            keyword in query
            for keyword in keywords
        )

    # -----------------------------------------
    # CODE QUESTIONS
    # -----------------------------------------

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

    # -----------------------------------------
    # RESEARCH / GENERAL KNOWLEDGE
    # -----------------------------------------

    def needs_research(self, query):

        query = query.lower()

        keywords = [

            "what is",
            "what are",
            "explain",
            "define",
            "difference",
            "compare",
            "advantages",
            "disadvantages",
            "how does",
            "why does",
            "why is"

        ]

        return any(
            keyword in query
            for keyword in keywords
        )

    # -----------------------------------------
    # ROUTER
    # -----------------------------------------

    def route(self, query):

        # IMPORTANT:
        # PDF must be checked BEFORE memory.
        #
        # Otherwise:
        # "tell me about my resume"
        #
        # contains "my"
        # and incorrectly becomes "memory".

        if self.needs_pdf(query):
            return "pdf"

        if self.needs_code(query):
            return "code"

        if self.needs_research(query):
            return "research"

        if self.needs_memory(query):
            return "memory"

        return "general"