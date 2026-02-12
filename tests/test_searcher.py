from research_agent.models import SearchResult
from research_agent.searcher import Searcher


def _make_result(title: str, url: str, snippet: str = "snippet") -> SearchResult:
    return SearchResult(title=title, url=url, snippet=snippet)


class TestSearch:
    def test_search_returns_results_from_fn(self):
        results = [
            _make_result("A", "https://a.com"),
            _make_result("B", "https://b.com"),
            _make_result("C", "https://c.com"),
        ]
        searcher = Searcher(search_fn=lambda q: results)
        got = searcher.search("test query")
        assert len(got) == 3
        assert got[0].title == "A"
        assert got[2].url == "https://c.com"

    def test_search_limits_max_results(self):
        results = [_make_result(f"R{i}", f"https://{i}.com") for i in range(10)]
        searcher = Searcher(search_fn=lambda q: results)
        got = searcher.search("query", max_results=3)
        assert len(got) == 3

    def test_search_default_fn_returns_empty(self):
        searcher = Searcher()
        got = searcher.search("anything")
        assert got == []


class TestMultiSearch:
    def test_multi_search_combines_queries(self):
        def fake_search(query: str) -> list[SearchResult]:
            if query == "q1":
                return [_make_result("A", "https://a.com")]
            if query == "q2":
                return [_make_result("B", "https://b.com")]
            return []

        searcher = Searcher(search_fn=fake_search)
        got = searcher.multi_search(["q1", "q2"])
        assert len(got) == 2
        titles = {r.title for r in got}
        assert titles == {"A", "B"}

    def test_multi_search_deduplicates_by_url(self):
        def fake_search(query: str) -> list[SearchResult]:
            return [_make_result(f"Title-{query}", "https://same.com")]

        searcher = Searcher(search_fn=fake_search)
        got = searcher.multi_search(["q1", "q2", "q3"])
        assert len(got) == 1
        assert got[0].url == "https://same.com"

    def test_multi_search_respects_max_per_query(self):
        results = [_make_result(f"R{i}", f"https://{i}.com") for i in range(10)]
        searcher = Searcher(search_fn=lambda q: results)
        got = searcher.multi_search(["q1", "q2", "q3"], max_results_per=2)
        # 3 queries x 2 max each, but all unique URLs from same pool
        # q1 returns R0,R1; q2 returns R0,R1 (duped); q3 returns R0,R1 (duped)
        # Only R0 and R1 survive dedup
        assert len(got) == 2
