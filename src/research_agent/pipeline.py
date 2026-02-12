"""Main research pipeline — orchestrates search, fetch, and synthesis."""

from __future__ import annotations

from research_agent.models import ResearchReport, Source


class ResearchPipeline:
    def __init__(self, searcher, synthesizer, fetch_fn=None):
        self.searcher = searcher
        self.synthesizer = synthesizer
        self._fetch_fn = fetch_fn or self._default_fetch

    def research(self, topic: str, queries: list[str] | None = None) -> ResearchReport:
        if queries is None:
            queries = [topic]

        search_results = self.searcher.multi_search(queries)

        sources = []
        for sr in search_results:
            content = self._fetch_fn(sr.url)
            sources.append(Source(
                title=sr.title, url=sr.url, content=content,
            ))

        sections = self.synthesizer.synthesize(topic, sources)

        summary = f"Research report on '{topic}' with {len(sources)} sources."

        return ResearchReport(
            topic=topic, summary=summary, sections=sections, sources=sources,
        )

    @staticmethod
    def _default_fetch(url: str) -> str:
        return f"Content from {url}"
