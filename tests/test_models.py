from research_agent.models import SearchResult, Source, ResearchSection, ResearchReport


class TestSearchResult:
    def test_search_result_creation(self):
        result = SearchResult(title="Test", url="https://example.com", snippet="A snippet")
        assert result.title == "Test"
        assert result.url == "https://example.com"
        assert result.snippet == "A snippet"


class TestSource:
    def test_source_default_relevance(self):
        source = Source(title="Src", url="https://src.com", content="Some content")
        assert source.relevance_score == 0.0

    def test_source_custom_relevance(self):
        source = Source(title="Src", url="https://src.com", content="Content", relevance_score=0.95)
        assert source.relevance_score == 0.95


class TestResearchSection:
    def test_research_section_empty_sources(self):
        section = ResearchSection(heading="Intro", content="Introduction text")
        assert section.sources == []
        assert section.heading == "Intro"
        assert section.content == "Introduction text"


class TestResearchReport:
    def test_research_report_has_timestamp(self):
        report = ResearchReport(topic="AI", summary="About AI")
        assert report.generated_at is not None
        assert len(report.generated_at) > 0

    def test_research_report_with_sections(self):
        source = Source(title="S1", url="https://s1.com", content="c1", relevance_score=0.8)
        section = ResearchSection(heading="H1", content="Body", sources=[source])
        report = ResearchReport(
            topic="Topic",
            summary="Summary",
            sections=[section],
            sources=[source],
        )
        assert report.topic == "Topic"
        assert report.summary == "Summary"
        assert len(report.sections) == 1
        assert report.sections[0].heading == "H1"
        assert len(report.sources) == 1
        assert report.sources[0].relevance_score == 0.8
