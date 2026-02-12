from __future__ import annotations

from collections.abc import Callable
from typing import Optional

from research_agent.models import SearchResult

DEFAULT_MAX_RESULTS: int = 5
DEFAULT_MAX_RESULTS_PER_QUERY: int = 3

SearchFn = Callable[[str], list[SearchResult]]


class Searcher:
    """Executes search queries and deduplicates results."""

    def __init__(self, search_fn: Optional[SearchFn] = None) -> None:
        self._search_fn: SearchFn = search_fn or self._default_search

    def search(self, query: str, max_results: int = DEFAULT_MAX_RESULTS) -> list[SearchResult]:
        """Run a single search query and return up to *max_results* results."""
        results = self._search_fn(query)
        return results[:max_results]

    def multi_search(
        self, queries: list[str], max_results_per: int = DEFAULT_MAX_RESULTS_PER_QUERY,
    ) -> list[SearchResult]:
        """Run multiple queries and return deduplicated results."""
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
