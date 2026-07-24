from chatbot.pdf_loader import PDFLoader
from chatbot.chunker import TextChunker
from chatbot.embeddings import EmbeddingModel
from chatbot.chroma_store import ChromaStore
from chatbot.retriever import Retriever
from chatbot.prompt_builder import PromptBuilder
import os


class PDFAgent:

    def __init__(self):

        self.loader = PDFLoader()

        self.chunker = TextChunker()

        self.embedder = EmbeddingModel()

        self.vector_store = ChromaStore()

        self.retriever = Retriever(
            embedder=self.embedder,
            vector_store=self.vector_store
        )

        self.prompt_builder = PromptBuilder()



    def upload_pdf(self, pdf_path):

        


        pages = self.loader.load_pdf(pdf_path)

        document_name = os.path.basename(pdf_path)

        chunks = self.chunker.split_pages(
            pages,
            document_name
)

        embedded_chunks = self.embedder.create_embeddings(
            chunks
)

        self.vector_store.add_documents(
            embedded_chunks
)

        return len(embedded_chunks)


    def ask_pdf(self, question):

        chunks = self.retriever.retrieve(
            question,
            top_k=5
    )

        context = self.retriever.build_context(
            chunks
    )

        return self.prompt_builder.build_prompt(
            context,
            question
    )

     

    def summarize_pdf(self):

        chunks = self.vector_store.get_all_chunks()

        context = self.retriever.build_context(
            chunks[:15]
    )

        prompt = f"""
    Summarize this document.

    {context}
"""

        return prompt

    def search_pdf(self, query):

        return self.retriever.retrieve(
            query,
            top_k=10
    )

    def find_pages(self, query):

        results = self.search_pdf(query)

        pages = []

        for chunk in results:

            if chunk["page"] not in pages:

                pages.append(chunk["page"])

        return sorted(pages)

    def compare_pdfs(
        self,
        question
):

        chunks = self.retriever.retrieve(
            question,
            top_k=10
    )

        context = self.retriever.build_context(
            chunks
    )

        return f"""
    Compare the documents.

    Question:

    {question}
pages = self.loader.load_pdf(pdf_path)

        chunks = self.chunker.chunk(pages)

        embedded_chunks = self.embedder.create_embeddings(
            chunks
    )

        self.vector_store.add_documents(
            embedded_chunks
   Context:

   {context}
"""