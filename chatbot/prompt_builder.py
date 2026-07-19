class PromptBuilder:

    def build_prompt(
        self,
        context,
        question
    ):

        prompt = f"""
You are an expert AI assistant specialized in answering questions from uploaded PDF documents.

==============================
Instructions
==============================

1. Use ONLY the information provided in the Context.
2. Do NOT use your own knowledge.
3. Do NOT hallucinate or invent facts.
4. If the answer is not available in the Context, reply exactly:

"I couldn't find this information in the uploaded document."

5. If multiple documents contain relevant information,
combine the information into one clear answer.

6. After answering, include the sources in this format:

Sources:
- Document Name (Page Number)

==============================
Context
==============================

{context}

==============================
Question
==============================

{question}

==============================
Answer
==============================
"""

        return prompt