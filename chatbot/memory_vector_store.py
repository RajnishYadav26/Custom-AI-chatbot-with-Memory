import chromadb


class MemoryVectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="memory_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="memories"
        )

    # ----------------------------
    # Add Memory
    # ----------------------------

    def add_memory(
        self,
        memory_id,
        text,
        embedding,
        metadata
    ):

        self.collection.add(

            ids=[memory_id],

            documents=[text],

            embeddings=[embedding],

            metadatas=[metadata]

        )

    # ----------------------------
    # Search
    # ----------------------------

    def search(

        self,

        query_embedding,

        top_k=5,

        where=None

    ):

        results = self.collection.query(

            query_embeddings=[query_embedding],

            n_results=top_k,

            where=where

        )

        memories = []

        docs = results["documents"][0]

        metas = results["metadatas"][0]

        distances = results["distances"][0]

        ids = results["ids"][0]

        for i in range(len(ids)):

            memories.append({

                "id": ids[i],

                "text": docs[i],

                "metadata": metas[i],

                "distance": distances[i]

            })

        return memories

    # ----------------------------
    # Delete
    # ----------------------------

    def delete(self, memory_id):

        self.collection.delete(ids=[memory_id])