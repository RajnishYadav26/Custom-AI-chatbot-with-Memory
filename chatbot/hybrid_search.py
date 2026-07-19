from chatbot.reciprocal_rank_fusion import ReciprocalRankFusion
from chatbot.reranker import ReRanker


class HybridSearch:

    def __init__(
        self,
        semantic_search,
        keyword_search
    ):

        self.semantic = semantic_search
        self.keyword = keyword_search
        self.rrf = ReciprocalRankFusion()
        self.reranker = ReRanker()

    def search(
        self,
        question,
        top_k=3
    ):

        # ----------------------------
        # Semantic Search
        # ----------------------------
        semantic_results = self.semantic.retrieve(
            question,
            top_k
        )
        print("\n===== SEMANTIC RESULTS =====")
        print(semantic_results)
        print("============================")

        # ----------------------------
        # BM25 Search
        # ----------------------------
        keyword_results = self.keyword.search(
            question,
            top_k
        )
        print("\n===== BM25 RESULTS =====")
        print(keyword_results)
        print("========================")

        # ----------------------------
        # Reciprocal Rank Fusion
        # ----------------------------
        fused_results = self.rrf.fuse(
            semantic_results,
            keyword_results
        )
        print("\n===== RRF RESULTS =====")
        print(fused_results)
        print("=======================")

        # ----------------------------
        # Cross-Encoder Re-ranking
        # ----------------------------
        reranked_results = self.reranker.rerank(
            query=question,
            chunks=fused_results,
            top_k=top_k,
            threshold=-999
)
        print("\n===== RERANK RESULTS =====")
        print(reranked_results)
        print("==========================")
        # ----------------------------
        # Similarity Threshold
        # ----------------------------
        if not reranked_results:
            return []

        return reranked_results