from chatbot.memory_expiration import MemoryExpiration

expiration = MemoryExpiration()

metadata = {

    "type": "temporary"

}

metadata = expiration.add_expiration(metadata)

print(metadata)

print(expiration.is_expired(metadata))