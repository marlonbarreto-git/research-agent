"""Synthesize search results into report sections."""

from __future__ import annotations

from research_agent.models import ResearchSection, Source


class Synthesizer:
    def __init__(self, summarize_fn=None):
        self._summarize_fn = summarize_fn or self._default_summarize

    def synthesize(self, topic: str, sources: list[Source]) -> list[ResearchSection]:
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
        snippets = [s.content[:200] for s in sources]
        return f"Summary of {len(sources)} sources about {topic}: " + " | ".join(snippets)
