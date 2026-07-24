from chatbot.memory_agent import MemoryAgent

agent = MemoryAgent()

agent.extract_memories(
    "My favorite language is Python"
)

agent.extract_memories(
    "I like Python"
)

agent.extract_memories(
    "Python is my preferred programming language"
)

results = agent.search_memory("Python")

print("Compressed Memories:\n")

for memory in results:

    print(memory)