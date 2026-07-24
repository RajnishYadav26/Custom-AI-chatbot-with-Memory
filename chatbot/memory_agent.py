from chatbot.memory import MemoryManager
from chatbot.user_profile import UserProfile
from chatbot.session import SessionManager
from chatbot.chroma_store import ChromaStore
from chatbot.embeddings import EmbeddingModel
from chatbot.retriever import Retriever
from chatbot.memory_ranker import MemoryRanker
from chatbot.memory_extractor import MemoryExtractor
from chatbot.memory_store import MemoryStore
from chatbot.memory_vector_store import MemoryVectorStore
import uuid
from chatbot.memory_compressor import MemoryCompressor
from chatbot.memory_summarizer import MemorySummarizer


class MemoryAgent:

    def __init__(self):

        self.memory = MemoryManager()

        self.profile = UserProfile()

        self.session = SessionManager()

        self.ranker = MemoryRanker()

        self.extractor = MemoryExtractor()

        self.memory_store = MemoryStore()

        self.memory_vector_store = MemoryVectorStore()

        self.compressor = MemoryCompressor()

        self.summarizer = MemorySummarizer()

       

    # Long-Term Memory Components
        self.embedder = EmbeddingModel()

        self.vector_store = ChromaStore()

        self.retriever = Retriever(
            embedder=self.embedder,
            vector_store=self.vector_store
    )
    # ----------------------------
    # User Profile
    # ----------------------------

    def get_profile(self):

        return self.profile.load_profile()

    def update_profile(self, profile_data):

        self.profile.save_profile(profile_data)

    # ----------------------------
    # Conversation Memory
    # ----------------------------

    def get_history(self):

        return self.memory.get_history()

    def add_user_message(self, message):

        self.memory.add_user_message(message)

    def add_ai_message(self, message):

        self.memory.add_ai_message(message)

    def clear_history(self):

        self.memory.load_history([])

    

    # ----------------------------
    # Session
    # ----------------------------

    def save_session(self):

        self.session.save_session(
            self.memory.save_history()
        )

    def load_session(self):

        history = self.session.load_session()

        self.memory.load_history(history)

        return history

    # ----------------------------------
# Long-Term Memory Retrieval
# ----------------------------------

    def search_memory(
        self,
        query,
        top_k=5
):

        memories = self.retriever.retrieve(
            query,
            top_k
    )

        ranked = self.ranker.rank(memories)

        ranked = self.memory_store.remove_expired(
    ranked
)

        compressed = self.compressor.compress(
        ranked
)

        return compressed

    def get_memory_context(
        self,
        query,
        top_k=5
):

        memories = self.search_memory(
            query,
            top_k
    )

        if not memories:
            return ""

        return self.retriever.build_context(
            memories
    )

    def extract_memories(self, text):

        memories = self.extractor.extract(text)

        if not memories:
            return []

        documents = self.memory_store.prepare(memories)

        for doc in documents:

            embedding = self.embedder.create_embedding(
    doc["text"]
)

            self.memory_vector_store.add_memory(

                memory_id=str(uuid.uuid4()),

                text=doc["text"],

                embedding=embedding,

                metadata=doc["metadata"]

        )

        return documents

    def summarize_memories(self):

        memories = self.search_memory("")

        return self.summarizer.summarize(
            memories
    )

    def save_summary(self):

        summary = self.summarize_memories()

        if not summary:
            return

        self.extract_memories(summary)

        print("Summary saved.")