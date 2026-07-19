from chatbot.embeddings import EmbeddingModel
from chatbot.chroma_store import ChromaStore


class Retriever:

    def __init__(

        self,

        embedder: EmbeddingModel,

        vector_store: ChromaStore

    ):

        self.embedder = embedder

        self.vector_store = vector_store

    def retrieve(

        self,

        question,

        top_k=3,

        where=None

    ):

        query_embedding = self.embedder.create_embedding(
            question
        )

        return self.vector_store.search(

            query_embedding=query_embedding,

            top_k=top_k,

            where=where

        )

    def build_context(

        self,

        chunks

    ):

        return "\n\n".join(

            chunk["text"]

            for chunk in chunks

        )