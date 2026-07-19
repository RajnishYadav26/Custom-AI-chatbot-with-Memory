from rag import RAGPipeline

rag = RAGPipeline()

# Index PDF
rag.index_document(
    "chatbot/documents/resume.pdf"
)

print("=" * 60)

while True:

    question = input("\nYou : ")

    if question.lower() == "exit":
        break

    answer = rag.ask(question)

    print("\nAI :", answer)