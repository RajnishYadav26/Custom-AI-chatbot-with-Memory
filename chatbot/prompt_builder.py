class PromptBuilder:

    def build_prompt(self, context, question):

        return f"""
You are an expert AI assistant.

The context below may come from:

• Uploaded PDFs
• Long-Term Memory
• Web Search

Always answer using the provided context.

Priority:

1. PDF information
2. Long-Term Memory
3. Web Search

If multiple sources provide information,
combine them naturally.

If the context is empty,
reply:

"I couldn't find enough information."

Context
--------------------

{context}

Question
--------------------

{question}

Answer
"""