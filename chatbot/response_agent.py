import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class ResponseAgent:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def build_prompt(

        self,

        user_question,

        memory_context="",

        research_context="",

        pdf_context="",

        code_context=""

    ):

        prompt = f"""
You are an enterprise AI assistant.

Use every available context.

----------------------------------

MEMORY

{memory_context}

----------------------------------

RESEARCH

{research_context}

----------------------------------

PDF

{pdf_context}

----------------------------------

CODE

{code_context}

----------------------------------

QUESTION

{user_question}

----------------------------------

Answer professionally.
"""

        return prompt


    def generate(

        self,

        prompt

    ):

        response = self.client.models.generate_content(

            model="gemini-2.5-flash",

            contents=prompt

        )

        return response.text


    def stream(

        self,

        prompt

    ):

        response = self.client.models.generate_content_stream(

            model="gemini-2.5-flash",

            contents=prompt

        )

        for chunk in response:

            if chunk.text:

                yield chunk.text

    def answer(

        self,

        question,

        memory="",

        research="",

        pdf="",

        code=""

    ):

        prompt = self.build_prompt(

            question,

            memory,

            research,

            pdf,

            code

        )

        return self.stream(prompt)