"""Synthesize search results into report sections."""

from __future__ import annotations

from collections.abc import Callable
from typing import Optional

from research_agent.models import ResearchSection, Source

SNIPPET_MAX_LENGTH: int = 200

SummarizeFn = Callable[[str, list[Source]], str]


class Synthesizer:
    """Combines sources into structured report sections."""

    def __init__(self, summarize_fn: Optional[SummarizeFn] = None) -> None:
        self._summarize_fn: SummarizeFn = summarize_fn or self._default_summarize

    def synthesize(self, topic: str, sources: list[Source]) -> list[ResearchSection]:
        """Create report sections from the provided sources.

        Args:
            topic: The research topic.
            sources: Fetched sources to synthesize.

        Returns:
            A list of ``ResearchSection`` instances.
        """
        if not sources:
            return []
        section = ResearchSection(
            heading=f"Research on {topic}",
            content=self._summarize_fn(topic, sources),
            sources=sources,
        )
        return [section]

    @staticmethod
    def _default_summarize(topic: str, sources: list[Source]) -> str:
        snippets = [s.content[:SNIPPET_MAX_LENGTH] for s in sources]
        return f"Summary of {len(sources)} sources about {topic}: " + " | ".join(snippets)
