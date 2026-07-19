import chromadb


class ChromaStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

    # ------------------------------------
    # Add Documents
    # ------------------------------------

    def add_documents(self, chunks):

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in chunks:

            ids.append(
                f'{chunk["document"]}_{chunk["chunk_id"]}'
            )

            documents.append(chunk["text"])

            embeddings.append(chunk["embedding"])

            metadatas.append(
                {
                    "chunk_id": chunk["chunk_id"],
                    "document": chunk["document"],
                    "page": chunk["page"],
                    "length": chunk["length"]
                }
            )

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    # ------------------------------------
    # Semantic Search
    # ------------------------------------

    def search(
        self,
        query_embedding,
        top_k=3,
        where=None
    ):

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where
        )

        retrieved = []

        ids = results["ids"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for i in range(len(ids)):

            retrieved.append(
                {
                    "chunk_id": metadatas[i]["chunk_id"],
                    "document": metadatas[i]["document"],
                    "page": metadatas[i]["page"],
                    "text": documents[i],
                    "length": metadatas[i]["length"],
                    "distance": distances[i]
                }
            )

        return retrieved

    # ------------------------------------
    # Get All Chunks
    # ------------------------------------

    def get_all_chunks(self):

        results = self.collection.get()

        chunks = []

        documents = results["documents"]
        metadatas = results["metadatas"]

        for doc, meta in zip(documents, metadatas):

            chunks.append(
                {
                    "chunk_id": meta["chunk_id"],
                    "document": meta["document"],
                    "page": meta["page"],
                    "text": doc,
                    "length": meta["length"]
                }
            )

        return chunks

    # ------------------------------------
    # Delete Document
    # ------------------------------------

    def delete_document(self, document_name):

        self.collection.delete(
            where={
                "document": document_name
            }
        )

        print(f"{document_name} deleted successfully.")

    # ------------------------------------
    # Update Document
    # ------------------------------------

    def update_document(self, chunks):

        if not chunks:
            return

        document_name = chunks[0]["document"]

        self.delete_document(document_name)

        self.add_documents(chunks)

        print(f"{document_name} updated successfully.")