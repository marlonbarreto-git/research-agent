"""Main research pipeline — orchestrates search, fetch, and synthesis."""

from __future__ import annotations

from collections.abc import Callable
from typing import Optional

from research_agent.models import ResearchReport, Source
from research_agent.searcher import Searcher
from research_agent.synthesizer import Synthesizer

FetchFn = Callable[[str], str]


class ResearchPipeline:
    """Orchestrates searching, fetching, and synthesizing into a report."""

    def __init__(
        self,
        searcher: Searcher,
        synthesizer: Synthesizer,
        fetch_fn: Optional[FetchFn] = None,
    ) -> None:
        self.searcher = searcher
        self.synthesizer = synthesizer
        self._fetch_fn: FetchFn = fetch_fn or self._default_fetch

    def research(self, topic: str, queries: list[str] | None = None) -> ResearchReport:
        """Run the full research pipeline for a given topic.

        Args:
            topic: The subject to research.
            queries: Optional list of search queries; defaults to ``[topic]``.

        Returns:
            A complete ``ResearchReport``.
        """
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
