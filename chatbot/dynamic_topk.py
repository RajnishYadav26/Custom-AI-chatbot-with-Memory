class DynamicTopK:

    def __init__(self):
        pass

    def get_top_k(self, question):

        words = len(question.split())

        # Very short queries
        if words <= 3:
            return 2

        # Normal queries
        elif words <= 8:
            return 3

        # Long queries
        elif words <= 15:
            return 5

        # Very detailed queries
        else:
            return 8