from __future__ import annotations

from research_agent.models import SearchResult


class Searcher:
    def __init__(self, search_fn=None):
        self._search_fn = search_fn or self._default_search

    def search(self, query: str, max_results: int = 5) -> list[SearchResult]:
        results = self._search_fn(query)
        return results[:max_results]

    def multi_search(self, queries: list[str], max_results_per: int = 3) -> list[SearchResult]:
        all_results: list[SearchResult] = []
        seen_urls: set[str] = set()
        for query in queries:
            results = self.search(query, max_results_per)
            for r in results:
                if r.url not in seen_urls:
                    all_results.append(r)
                    seen_urls.add(r.url)
        return all_results

    @staticmethod
    def _default_search(query: str) -> list[SearchResult]:
        return []
