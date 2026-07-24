from chatbot.memory_agent import MemoryAgent

agent = MemoryAgent()

agent.extract_memories(
    "My favorite language is Python"
)

print("Stored")

agent.extract_memories(
    "I am a Computer Engineering student"
)

print("Stored")

agent.extract_memories(
    "My name is Rajnish"
)

print("Stored")