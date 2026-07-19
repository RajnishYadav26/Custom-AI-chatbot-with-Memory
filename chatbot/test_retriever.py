from retriever import Retriever

retriever = Retriever()

question = input("Ask Question: ")

results = retriever.retrieve(
    question,
    top_k=3
)

context = retriever.build_context(results)

print("=" * 70)

print("Retrieved Context")

print("=" * 70)

print(context)