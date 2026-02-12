from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str


@dataclass
class Source:
    title: str
    url: str
    content: str
    relevance_score: float = 0.0


@dataclass
class ResearchSection:
    heading: str
    content: str
    sources: list[Source] = field(default_factory=list)


@dataclass
class ResearchReport:
    topic: str
    summary: str
    sections: list[ResearchSection] = field(default_factory=list)
    sources: list[Source] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
