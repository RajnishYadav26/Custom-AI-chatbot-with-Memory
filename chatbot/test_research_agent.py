from chatbot.research_agent import ResearchAgent

agent = ResearchAgent()

question = "Explain Retrieval Augmented Generation"

prompt = agent.research(question)

print("\n========== FINAL PROMPT ==========\n")

print(prompt)