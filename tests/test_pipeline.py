from unittest.mock import MagicMock, call

from research_agent.models import SearchResult, Source, ResearchSection
from research_agent.pipeline import ResearchPipeline


def _make_search_result(title="Result", url="https://example.com", snippet="snip"):
    return SearchResult(title=title, url=url, snippet=snippet)


def _make_pipeline(search_results=None, sections=None, fetch_fn=None):
    searcher = MagicMock()
    searcher.multi_search.return_value = search_results or []
    synthesizer = MagicMock()
    synthesizer.synthesize.return_value = sections or []
    return ResearchPipeline(
        searcher=searcher,
        synthesizer=synthesizer,
        fetch_fn=fetch_fn,
    ), searcher, synthesizer


def test_research_uses_default_query():
    pipeline, searcher, _ = _make_pipeline()
    pipeline.research("AI")
    searcher.multi_search.assert_called_once_with(["AI"])


def test_research_uses_custom_queries():
    pipeline, searcher, _ = _make_pipeline()
    queries = ["AI history", "AI future"]
    pipeline.research("AI", queries=queries)
    searcher.multi_search.assert_called_once_with(queries)


def test_research_fetches_all_search_results():
    results = [_make_search_result(url="https://a.com"), _make_search_result(url="https://b.com")]
    fetch_fn = MagicMock(return_value="content")
    pipeline, _, _ = _make_pipeline(search_results=results, fetch_fn=fetch_fn)
    pipeline.research("AI")
    assert fetch_fn.call_count == 2
    fetch_fn.assert_any_call("https://a.com")
    fetch_fn.assert_any_call("https://b.com")


def test_research_creates_sources_from_results():
    results = [_make_search_result(title="T1", url="https://a.com")]
    fetch_fn = MagicMock(return_value="fetched content")
    pipeline, _, synthesizer = _make_pipeline(search_results=results, fetch_fn=fetch_fn)
    pipeline.research("AI")
    sources_arg = synthesizer.synthesize.call_args[0][1]
    assert len(sources_arg) == 1
    assert sources_arg[0].title == "T1"
    assert sources_arg[0].url == "https://a.com"
    assert sources_arg[0].content == "fetched content"


def test_research_calls_synthesizer():
    results = [_make_search_result()]
    fetch_fn = MagicMock(return_value="content")
    pipeline, _, synthesizer = _make_pipeline(search_results=results, fetch_fn=fetch_fn)
    pipeline.research("AI")
    synthesizer.synthesize.assert_called_once()
    args = synthesizer.synthesize.call_args[0]
    assert args[0] == "AI"


def test_research_returns_complete_report():
    results = [_make_search_result()]
    section = ResearchSection(heading="h", content="c", sources=[])
    fetch_fn = MagicMock(return_value="content")
    pipeline, _, _ = _make_pipeline(search_results=results, sections=[section], fetch_fn=fetch_fn)
    report = pipeline.research("AI")
    assert report.topic == "AI"
    assert "AI" in report.summary
    assert len(report.sections) == 1
    assert len(report.sources) == 1
