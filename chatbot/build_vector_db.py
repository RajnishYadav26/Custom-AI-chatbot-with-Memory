from rag import RAGPipeline

rag = RAGPipeline()

rag.index_document("chatbot/documents/resume.pdf")   # Change to your PDF filename

print("Vector database created successfully!")