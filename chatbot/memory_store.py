from datetime import datetime
from chatbot.memory_categories import MemoryCategories
from chatbot.memory_expiration import MemoryExpiration


class MemoryStore:

    def __init__(self):

        self.category_classifier = MemoryCategories()
        
  
        self.expiration = MemoryExpiration()


    # -----------------------------------------
    # Prepare memories for ChromaDB
    # -----------------------------------------
    def prepare(self, memories):

        documents = []

        for memory in memories:

            category = self.category_classifier.classify(
                memory["type"],
                memory["value"]
        )

        metadata = self.expiration.add_expiration({

            "type": memory["type"],

            "importance": memory["importance"],

            "timestamp": datetime.now().isoformat(),

            "usage_count": 0,

            "category": memory.get("category", "General")

})



        return documents
    # -----------------------------------------
    # Filter memories by category
    # -----------------------------------------
    def get_by_category(self, documents, category):

        filtered = []

        for doc in documents:

            if doc["metadata"]["category"] == category:

                filtered.append(doc)

        return filtered

    def remove_expired(self, memories):

        filtered = []

        for memory in memories:

            if not self.expiration.is_expired(
                memory["metadata"]
        ):

                filtered.append(memory)

        return filtered