from abc import ABC, abstractmethod


class WebSearch(ABC):

    @abstractmethod
    def search(
        self,
        query,
        max_results=5
    ):
        """
        Return list of search results.
        """
        pass