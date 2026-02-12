# Research Agent

Agent that researches topics via web search, synthesizes information, and generates structured reports.

## Overview

Research Agent automates the process of investigating a topic by searching for information, fetching content from sources, and synthesizing findings into structured reports. It supports multi-query search with deduplication, pluggable search and summarization backends, and produces reports organized into sections with source attribution.

## Architecture

```
Topic + Queries
       |
       v
+---------------+
|   Searcher    |
| (multi-query, |
|  dedup URLs)  |
+---------------+
       |
  SearchResult[]
       |
       v
+------------------+
| ResearchPipeline |
| (fetch content,  |
|  orchestrate)    |
+------------------+
       |
   Source[]
       |
       v
+---------------+
|  Synthesizer  |
| (summarize,   |
|  sectionize)  |
+---------------+
       |
       v
  ResearchReport
  (summary, sections, sources)
```

## Features

- Multi-query search with URL deduplication
- Pluggable search backend (inject any search function)
- Content fetching with pluggable fetch function
- Source synthesis into structured report sections
- Structured report output with topic, summary, sections, and sources
- Relevance scoring for sources
- Timestamp tracking on generated reports

## Tech Stack

- Python 3.11+
- Pydantic (data validation)

## Quick Start

```bash
git clone https://github.com/marlonbarreto-git/research-agent.git
cd research-agent
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Project Structure

```
src/research_agent/
  __init__.py
  models.py        # SearchResult, Source, ResearchSection, ResearchReport
  searcher.py      # Searcher with multi-query and dedup
  synthesizer.py   # Synthesizer for report sections
  pipeline.py      # ResearchPipeline orchestrator
tests/
  test_models.py
  test_searcher.py
  test_synthesizer.py
  test_pipeline.py
```

## Testing

```bash
pytest -v --cov=src/research_agent
```

23 tests covering data models, search operations, synthesis, and end-to-end pipeline behavior.

## License

MIT
