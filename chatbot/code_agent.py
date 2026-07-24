import re


class CodeAgent:

    def __init__(self):

        pass

    def detect_language(self, code):

        patterns = {

            "python": r"(def |import |from |print\()",

            "javascript": r"(function|const |let |=>)",

            "java": r"(public class|System\.out)",

            "cpp": r"(#include|std::)",

            "sql": r"(SELECT|INSERT|UPDATE|DELETE)",

            "html": r"(<html|<div|<body)",

            "css": r"(\.container|display:|color:)",

            "docker": r"(FROM |RUN |CMD )"

    }

        for language, pattern in patterns.items():

            if re.search(pattern, code, re.IGNORECASE):

                return language

        return "unknown"

    def generate_code(self, request):

        return f"""
    You are an expert software engineer.

    Generate clean,

    production-ready,

    well-documented code.

   Task:

    {request}
    """  

    def explain_code(self, code):

        language = self.detect_language(code)

        return f"""
    Explain the following {language} code.

    Include:

    • Overview

    • Logic

    • Functions

    • Complexity

    Code:

    {code}
    """

    def debug_code(self, code):

        language = self.detect_language(code)

        return f"""
    Find bugs in this {language} code.

    Explain

    • Bug

    • Cause

    • Fix

    • Improved code

    Code:

    {code}
    """

    def refactor_code(self, code):

        language = self.detect_language(code)

        return f"""
    Refactor this {language} code.

    Improve

    • Readability

    • Performance

    • Naming

    • Documentation

    • Best Practices

    Code:

    {code}
    """

    def generate_sql(self, request):

        return f"""
    Generate optimized SQL.

    Task

    {request}
    """

    def generate_fastapi(self, request):

        return f"""
    Generate FastAPI project.

    Task

    {request}
    """

    def generate_react(self, request):

        return f"""
    Generate React component.

    Task

    {request}
    """

    def generate_docker(self, request):

        return f"""
    Generate Dockerfile.

    Task

    {request}
    """
    
    