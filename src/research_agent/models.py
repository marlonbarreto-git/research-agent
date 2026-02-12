from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SearchResult:
    """A single result returned from a search query."""

    title: str
    url: str
    snippet: str


@dataclass
class Source:
    """A fetched source with its content and relevance score."""

    title: str
    url: str
    content: str
    relevance_score: float = 0.0


@dataclass
class ResearchSection:
    """A section within a research report."""

    heading: str
    content: str
    sources: list[Source] = field(default_factory=list)


@dataclass
class ResearchReport:
    """A complete research report containing sections and sources."""

    topic: str
    summary: str
    sections: list[ResearchSection] = field(default_factory=list)
    sources: list[Source] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
