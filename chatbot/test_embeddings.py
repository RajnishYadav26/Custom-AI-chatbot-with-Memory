from pdf_loader import PDFLoader
from chunker import TextChunker
from embeddings import EmbeddingModel

loader = PDFLoader()

text = loader.load_pdf(
    "chatbot/documents/resume.pdf"
)

chunker = TextChunker()

chunks = chunker.split_text(text)

embedder = EmbeddingModel()

vectors = embedder.create_embeddings(chunks)

print("=" * 60)
print("Total Embeddings:", len(vectors))
print("=" * 60)

print("\nFirst Chunk")

print(vectors[0]["text"][:300])

print("\nEmbedding Dimension")

print(len(vectors[0]["embedding"]))

print("\nFirst 10 Values")

print(vectors[0]["embedding"][:10])