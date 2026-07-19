from chatbot.retrieval_metrics import RetrievalMetrics
from chatbot.test_queries import test_queries

from chatbot.embeddings import EmbeddingModel
from chatbot.vector_store import VectorStore
from chatbot.retriever import Retriever
from chatbot.keyword_search import KeywordSearch
from chatbot.hybrid_search import HybridSearch


# ----------------------------
# Load Vector Database
# ----------------------------

embedder = EmbeddingModel()

vector_store = VectorStore()
vector_store.load()


# ----------------------------
# Semantic Search
# ----------------------------

retriever = Retriever(
    embedder=embedder,
    vector_store=vector_store
)


# ----------------------------
# BM25 Search
# ----------------------------

keyword_search = KeywordSearch()
keyword_search.build(vector_store.metadata)


# ----------------------------
# Hybrid Search
# ----------------------------

hybrid_search = HybridSearch(
    semantic_search=retriever,
    keyword_search=keyword_search
)


# ----------------------------
# Metrics
# ----------------------------

metrics = RetrievalMetrics()

precision_scores = []
recall_scores = []
mrr_scores = []
hit_scores = []


# ----------------------------
# Evaluate
# ----------------------------

for item in test_queries:

    print("=" * 60)
    print("Question:", item["question"])

    retrieved = hybrid_search.search(
        item["question"],
        top_k=5
    )

    print("Retrieved Chunk IDs:")

    for chunk in retrieved:
        print(chunk["chunk_id"])

    precision_scores.append(
        metrics.precision_at_k(
            retrieved,
            item["relevant_chunks"]
        )
    )

    recall_scores.append(
        metrics.recall_at_k(
            retrieved,
            item["relevant_chunks"]
        )
    )

    mrr_scores.append(
        metrics.mrr(
            retrieved,
            item["relevant_chunks"]
        )
    )

    hit_scores.append(
        metrics.hit_rate(
            retrieved,
            item["relevant_chunks"]
        )
    )


print("\n" + "=" * 60)
print("FINAL RESULTS")
print("=" * 60)

print(f"Precision@5 : {sum(precision_scores)/len(precision_scores):.4f}")
print(f"Recall@5    : {sum(recall_scores)/len(recall_scores):.4f}")
print(f"MRR         : {sum(mrr_scores)/len(mrr_scores):.4f}")
print(f"Hit Rate    : {sum(hit_scores)/len(hit_scores):.4f}")