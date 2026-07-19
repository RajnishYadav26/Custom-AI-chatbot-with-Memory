from pdf_loader import PDFLoader

loader = PDFLoader()

text = loader.load_pdf("chatbot/documents/resume.pdf")

print(text)