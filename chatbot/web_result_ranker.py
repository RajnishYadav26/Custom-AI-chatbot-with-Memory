import re


class WebResultRanker:

    def __init__(self):

        pass

    # -----------------------------------------
    # Keyword Relevance
    # -----------------------------------------

    def keyword_score(self, query, result):

        query_words = set(
            re.findall(
                r"\b\w+\b",
                query.lower()
            )
        )

        text = (
            result.get("title", "") + " " +
            result.get("content", "")
        ).lower()

        text_words = set(
            re.findall(
                r"\b\w+\b",
                text
            )
        )

        if not query_words:

            return 0.0

        matches = query_words.intersection(
            text_words
        )

        return len(matches) / len(query_words)

    # -----------------------------------------
    # Final Score
    # -----------------------------------------

    def calculate_score(self, query, result):

        keyword_score = self.keyword_score(
            query,
            result
        )

        provider_score = result.get(
            "score",
            0.0
        )

        final_score = (

            0.6 * keyword_score +

            0.4 * provider_score

        )

        return final_score

    # -----------------------------------------
    # Rank Results
    # -----------------------------------------

    def rank(

        self,

        query,

        results,

        top_k=5

    ):

        # Remove duplicate URLs

        results = self.remove_duplicates(
            results
        )

        ranked = []

        for result in results:

            score = self.calculate_score(
                query,
                result
            )

            result = result.copy()

            result["relevance_score"] = score

            ranked.append(result)

        # Remove weak results

        ranked = self.filter_results(
            ranked
        )

        # Highest score first

        ranked.sort(

            key=lambda x:
            x["relevance_score"],

            reverse=True

        )

        return ranked[:top_k]

    def remove_duplicates(self, results):

        seen = set()

        unique_results = []

        for result in results:

            url = result.get(
                "url",
                ""
            ).strip()

            if not url:

                continue

            if url in seen:

                continue

            seen.add(url)

            unique_results.append(result)

        return unique_results
    
    def filter_results(

        self,

        results,

        min_score=0.15

    ):

        return [

            result

            for result in results

            if result.get(
                "relevance_score",
                0
            ) >= min_score

        ]