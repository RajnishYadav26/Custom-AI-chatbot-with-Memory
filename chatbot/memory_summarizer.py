from google import genai
from dotenv import load_dotenv
import os

load_dotenv()


class MemorySummarizer:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def summarize(self, memories):

        if not memories:
            return ""

        memory_text = ""

        for memory in memories:

            memory_text += f"- {memory['text']}\n"

        prompt = f"""
You are an AI memory manager.

Summarize the following memories.

Rules:
- Keep only long-term facts.
- Remove duplicates.
- Keep user preferences.
- Keep important information.
- Maximum 10 bullet points.

Memories:

{memory_text}
"""

        response = self.client.models.generate_content(

            model="gemini-2.5-flash",

            contents=prompt

        )

        return response.text