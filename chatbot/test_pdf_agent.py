from chatbot.pdf_agent import PDFAgent

agent = PDFAgent()

agent.upload_pdf(
    "chatbot/documents/resume.pdf"
)

prompt = agent.ask_pdf(
    "summarize the resume?"
)

print(prompt)