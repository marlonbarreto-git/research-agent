from unittest.mock import MagicMock

from research_agent.models import Source
from research_agent.synthesizer import Synthesizer


def _make_source(title="Source 1", url="https://example.com", content="Some content"):
    return Source(title=title, url=url, content=content)


def test_synthesize_empty_sources_returns_empty_list():
    synth = Synthesizer()
    result = synth.synthesize("AI", [])
    assert result == []


def test_synthesize_creates_section_with_topic():
    synth = Synthesizer()
    sections = synth.synthesize("AI", [_make_source()])
    assert len(sections) == 1
    assert "AI" in sections[0].heading


def test_synthesize_uses_summarize_fn():
    mock_fn = MagicMock(return_value="custom summary")
    synth = Synthesizer(summarize_fn=mock_fn)
    sources = [_make_source()]
    sections = synth.synthesize("AI", sources)
    mock_fn.assert_called_once_with("AI", sources)
    assert sections[0].content == "custom summary"


def test_synthesize_section_includes_sources():
    synth = Synthesizer()
    sources = [_make_source(), _make_source(title="Source 2")]
    sections = synth.synthesize("AI", sources)
    assert sections[0].sources == sources


def test_default_summarize_includes_source_count():
    result = Synthesizer._default_summarize("AI", [_make_source(), _make_source()])
    assert "2" in result
