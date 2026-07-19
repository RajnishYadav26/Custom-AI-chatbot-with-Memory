import os

from dotenv import load_dotenv
from google import genai

from pdf_loader import PDFLoader
from chunker import TextChunker
from embeddings import EmbeddingModel
from vector_store import VectorStore
from retriever import Retriever
from prompt_builder import PromptBuilder

# ----------------------------------------
# Load Environment Variables
# ----------------------------------------

load_dotenv()


class RAGPipeline:

    def __init__(self):

        # -----------------------------
        # Gemini Client
        # -----------------------------

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        # -----------------------------
        # Components
        # -----------------------------

        self.loader = PDFLoader()

        self.chunker = TextChunker()

        self.embedder = EmbeddingModel()

        self.vector_store = VectorStore()

        self.prompt_builder = PromptBuilder()

        # Load existing vector database if available
        try:
            self.vector_store.load()
        except Exception:
            pass

        self.retriever = Retriever(
            embedder=self.embedder,
            vector_store=self.vector_store
        )

    # ==================================================
    # Index Single PDF
    # ==================================================

    def index_document(self, pdf_path):

        print("\nLoading PDF...")

        pages = self.loader.load_pdf(pdf_path)

        document_name = os.path.basename(pdf_path)

        print("PDF Loaded Successfully.")

        print("\nCreating Chunks...")

        chunks = self.chunker.split_pages(
            pages,
            document_name
        )

        print(f"{len(chunks)} Chunks Created.")

        print("\nGenerating Embeddings...")

        vectors = self.embedder.create_embeddings(
            chunks
        )

        print("Embeddings Generated.")

        print("\nCreating Vector Database...")

        self.vector_store.create_index(
            vectors
        )

        self.vector_store.save()

        print("Vector Database Saved.")

    # ==================================================
    # Index Multiple PDFs
    # ==================================================

    def index_documents(
        self,
        pdf_paths
    ):

        all_chunks = []

        for pdf in pdf_paths:

            print(f"\nProcessing {pdf}")

            pages = self.loader.load_pdf(pdf)

            document_name = os.path.basename(pdf)

            chunks = self.chunker.split_pages(
                pages,
                document_name
            )

            all_chunks.extend(chunks)

        print(f"\nTotal Chunks : {len(all_chunks)}")

        vectors = self.embedder.create_embeddings(
            all_chunks
        )

        self.vector_store.create_index(
            vectors
        )

        self.vector_store.save()

        print("\nKnowledge Base Created.")

    # ==================================================
    # Ask Question
    # ==================================================

    def ask(
        self,
        question,
        top_k=3
    ):

        try:

            retrieved_chunks = self.retriever.retrieve(
                question,
                top_k
            )

            context = self.retriever.build_context(
                retrieved_chunks
            )

            if context == "":

                return (
                    "I couldn't find relevant information "
                    "inside the uploaded documents."
                )

            prompt = self.prompt_builder.build_prompt(
                context,
                question
            )

            response = self.client.models.generate_content(

                model="gemini-2.5-flash",

                contents=prompt

            )

            return response.text

        except Exception as e:

            return f"Error : {e}"