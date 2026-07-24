from chatbot.query_expansion import QueryExpansion
from chatbot.dynamic_topk import DynamicTopK
from chatbot.hybrid_search import HybridSearch
from chatbot.prompt_builder import PromptBuilder
from chatbot.retriever import Retriever
from chatbot.embeddings import EmbeddingModel
from chatbot.chroma_store import ChromaStore
from chatbot.keyword_search import KeywordSearch
from chatbot.duplicate_remover import DuplicateRemover


class ResearchAgent:

    def __init__(self):

        self.embedder = EmbeddingModel()

        self.vector_store = ChromaStore()

        self.retriever = Retriever(
            embedder=self.embedder,
            vector_store=self.vector_store
        )

        self.keyword = KeywordSearch()

        self.keyword.build(
            self.vector_store.get_all_chunks()
        )

        self.hybrid = HybridSearch(
            semantic_search=self.retriever,
            keyword_search=self.keyword
        )

        self.query_expansion = QueryExpansion()

        self.dynamic_topk = DynamicTopK()

        self.duplicate = DuplicateRemover()

        self.prompt_builder = PromptBuilder()

    def search(self, question):

        expanded = self.query_expansion.expand(
            question
        )

        top_k = self.dynamic_topk.get_top_k(
            expanded
        )

        chunks = self.hybrid.search(
            expanded,
            top_k
        )

        chunks = self.duplicate.remove_duplicates(
            chunks
        )

        return chunks

    def build_context(self, question):

        chunks = self.search(question)

        if not chunks:
            return ""

        return self.retriever.build_context(
            chunks
        )

    def research(self, question):

        context = self.build_context(
            question
        )

        if not context:

            return question

        return self.prompt_builder.build_prompt(
            context,
            question
        )

    def retrieve_only(self, question):

        return self.search(question)


    def context_only(self, question):

        return self.build_context(question)