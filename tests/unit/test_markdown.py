from docguard.extractors.markdown import MarkdownExtractor


def test_markdown_extractor_headings_and_paragraphs() -> None:
    doc = """# Client Guide
This document explains how to configure client connections.

## Networking
The default timeout is 30 seconds. Connect takes a host parameter.
"""
    extractor = MarkdownExtractor()
    spans = extractor.extract("docs/guide.md", doc)
    assert len(spans) >= 3

    # Check headings
    heading_spans = [s for s in spans if s.block_type == "heading"]
    assert len(heading_spans) == 2
    assert heading_spans[0].text == "Client Guide"
    assert heading_spans[1].text == "Networking"

    # Check paragraph / sentence spans
    para_spans = [s for s in spans if s.block_type == "paragraph"]
    assert any("The default timeout is 30 seconds." in s.text for s in para_spans)

    target_span = next(s for s in para_spans if "The default timeout is 30 seconds." in s.text)
    assert target_span.heading_path == ["Client Guide", "Networking"]
    assert target_span.line_start >= 4


def test_markdown_extractor_fenced_code() -> None:
    doc = """# Examples
```python
client = Client(timeout=30)
```
"""
    extractor = MarkdownExtractor()
    spans = extractor.extract("docs/examples.md", doc)
    fence_spans = [s for s in spans if s.block_type == "fence"]
    assert len(fence_spans) == 1
    assert "timeout=30" in fence_spans[0].text
    assert fence_spans[0].language == "python"
