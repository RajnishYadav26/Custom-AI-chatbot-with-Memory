import tiktoken


class TokenCounter:

    def __init__(self):

        self.encoding = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text):

        return len(
            self.encoding.encode(text)
        )

    def count_history(self, history):

        total = 0

        for msg in history:
            total += self.count_tokens(msg["text"])

        return total