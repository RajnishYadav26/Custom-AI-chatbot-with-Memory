from chatbot.memory_store import MemoryStore

store = MemoryStore()

memories = [

    {
        "type": "favorite_language",
        "value": "Python",
        "importance": 1.0
    },

    {
        "type": "profession",
        "value": "Computer Engineering Student",
        "importance": 0.9
    },

    {
        "type": "goal",
        "value": "Become an AI Engineer",
        "importance": 0.95
    },

    {
        "type": "university",
        "value": "NCIT",
        "importance": 0.8
    }

]

documents = store.prepare(memories)

print("\n===== MEMORY STORE TEST =====\n")

for doc in documents:
    print(doc)

print("\n===== TEST COMPLETED =====")