from pdf_loader import PDFLoader
from chunker import TextChunker

loader = PDFLoader()

text = loader.load_pdf(
    "chatbot/documents/resume.pdf"
)

chunker = TextChunker()

chunks = chunker.split_text(text)

print("=" * 50)
print("Total Chunks:", len(chunks))
print("=" * 50)

for chunk in chunks:

    print("=" * 60)

    print("Chunk ID :", chunk["id"])

    print("Length :", chunk["length"])

    print("-" * 60)

    print(chunk["text"])