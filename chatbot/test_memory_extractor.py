from chatbot.memory_extractor import MemoryExtractor
from chatbot.memory_store import MemoryStore

extractor = MemoryExtractor()

store = MemoryStore()

text = """

My name is Rajnish.

My favorite language is Python.

"""

memories = extractor.extract(text)

documents = store.prepare(memories)

print(documents)