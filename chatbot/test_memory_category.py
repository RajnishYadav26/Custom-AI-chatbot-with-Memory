from chatbot.memory_agent import MemoryAgent

agent = MemoryAgent()

agent.add_user_message("I like Python")

agent.add_ai_message("Great!")

results = agent.get_memories_by_category("Programming")

print(results)