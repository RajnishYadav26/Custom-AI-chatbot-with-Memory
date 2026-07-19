import pickle

with open("vector_db/metadata.pkl", "rb") as f:
    data = pickle.load(f)

print("Total chunks:", len(data))
print()

chunk = data[0]

print("Keys:", chunk.keys())
print()

for k, v in chunk.items():
    print(f"{k}:")
    print(v)
    print("-" * 50)