import re
from typing import Any

from markdown_it import MarkdownIt

from docguard.contracts.docs import DocSpan

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9`\"'])")


def extract_inline_metadata(tokens: list[Any]) -> tuple[str, list[str], list[str]]:
    text_parts: list[str] = []
    inline_code: list[str] = []
    links: list[str] = []

    for t in tokens:
        if t.type == "text":
            text_parts.append(t.content)
        elif t.type == "code_inline":
            text_parts.append(t.content)
            inline_code.append(t.content)
        elif t.type == "link_open":
            href = t.attrs.get("href") if hasattr(t, "attrs") and t.attrs else None
            if href:
                links.append(str(href))
        elif hasattr(t, "children") and t.children:
            sub_text, sub_code, sub_links = extract_inline_metadata(t.children)
            text_parts.append(sub_text)
            inline_code.extend(sub_code)
            links.extend(sub_links)

    return "".join(text_parts), inline_code, links


class MarkdownExtractor:
    """Transforms Markdown documentation into line-accurate, structured DocSpan objects."""

    def __init__(self) -> None:
        self.md = MarkdownIt("gfm-like", {"html": False})

    def extract(self, path: str, content: str) -> list[DocSpan]:
        if not content.strip():
            return []

        raw_lines = content.splitlines(keepends=True)
        tokens = self.md.parse(content)

        spans: list[DocSpan] = []
        heading_stack: list[str] = []

        current_row_cells: list[str] = []
        current_row_inlines: list[str] = []
        current_row_start = 1
        current_row_end = 1
        in_table_row = False

        idx = 0
        while idx < len(tokens):
            token = tokens[idx]

            # Headings
            if token.type == "heading_open":
                tag_level = (
                    int(token.tag[1:]) if len(token.tag) > 1 and token.tag[1:].isdigit() else 1
                )
                inline_token = tokens[idx + 1] if idx + 1 < len(tokens) else None
                heading_text = inline_token.content if inline_token else ""

                while len(heading_stack) >= tag_level:
                    heading_stack.pop()
                heading_stack.append(heading_text.strip())

                t_map = token.map
                line_start = t_map[0] + 1 if t_map else 1
                line_end = t_map[1] if t_map else line_start

                spans.append(
                    DocSpan(
                        span_id=f"doc-{len(spans) + 1}",
                        path=path,
                        block_type="heading",
                        heading_path=list(heading_stack),
                        text=heading_text.strip(),
                        raw_text=heading_text,
                        line_start=line_start,
                        line_end=line_end,
                    )
                )

            # Paragraphs
            elif token.type == "paragraph_open":
                inline_token = tokens[idx + 1] if idx + 1 < len(tokens) else None
                t_map = token.map
                line_start = t_map[0] + 1 if t_map else 1
                line_end = t_map[1] if t_map else line_start

                text = ""
                inline_code: list[str] = []
                links: list[str] = []

                if inline_token and inline_token.children:
                    text, inline_code, links = extract_inline_metadata(inline_token.children)
                elif inline_token:
                    text = inline_token.content

                raw_slice = "".join(raw_lines[line_start - 1 : line_end]).strip()

                sentences = [s.strip() for s in SENTENCE_SPLIT_RE.split(text) if s.strip()]
                if len(sentences) > 1:
                    current_line = line_start
                    for s in sentences:
                        s_start_line = current_line
                        for line_idx in range(current_line - 1, line_end):
                            if s[:20] in raw_lines[line_idx]:
                                s_start_line = line_idx + 1
                                break
                        s_end_line = s_start_line
                        for line_idx in range(s_start_line - 1, line_end):
                            if s[-20:] in raw_lines[line_idx]:
                                s_end_line = line_idx + 1
                                break

                        s_inline = [c for c in inline_code if c in s]
                        s_links = [link for link in links if link in s]
                        spans.append(
                            DocSpan(
                                span_id=f"doc-{len(spans) + 1}",
                                path=path,
                                block_type="paragraph",
                                heading_path=list(heading_stack),
                                text=s,
                                raw_text=s,
                                line_start=s_start_line,
                                line_end=max(s_start_line, s_end_line),
                                inline_code=s_inline,
                                links=s_links,
                            )
                        )
                else:
                    spans.append(
                        DocSpan(
                            span_id=f"doc-{len(spans) + 1}",
                            path=path,
                            block_type="paragraph",
                            heading_path=list(heading_stack),
                            text=text.strip(),
                            raw_text=raw_slice or text.strip(),
                            line_start=line_start,
                            line_end=line_end,
                            inline_code=inline_code,
                            links=links,
                        )
                    )

            # Fenced code blocks
            elif token.type == "fence":
                t_map = token.map
                line_start = t_map[0] + 1 if t_map else 1
                line_end = t_map[1] if t_map else line_start
                lang = token.info.strip() if token.info else None

                spans.append(
                    DocSpan(
                        span_id=f"doc-{len(spans) + 1}",
                        path=path,
                        block_type="fence",
                        heading_path=list(heading_stack),
                        text=token.content.strip(),
                        raw_text=token.content,
                        line_start=line_start,
                        line_end=line_end,
                        language=lang,
                    )
                )

            # Table rows
            elif token.type == "tr_open":
                in_table_row = True
                current_row_cells = []
                current_row_inlines = []
                t_map = token.map
                current_row_start = t_map[0] + 1 if t_map else 1
                current_row_end = t_map[1] if t_map else current_row_start

            elif token.type in ("th_open", "td_open") and in_table_row:
                inline_token = tokens[idx + 1] if idx + 1 < len(tokens) else None
                cell_text = ""
                cell_inlines: list[str] = []
                if inline_token and inline_token.children:
                    cell_text, cell_inlines, _ = extract_inline_metadata(inline_token.children)
                elif inline_token:
                    cell_text = inline_token.content

                if cell_text.strip():
                    current_row_cells.append(cell_text.strip())
                    current_row_inlines.extend(cell_inlines)

            elif token.type == "tr_close" and in_table_row:
                in_table_row = False
                if current_row_cells:
                    row_text = " | ".join(current_row_cells)
                    # If token had no map, estimate line from raw lines
                    if current_row_start == 1:
                        for l_idx, r_line in enumerate(raw_lines, start=1):
                            if current_row_cells[0] in r_line:
                                current_row_start = l_idx
                                current_row_end = l_idx
                                break

                    spans.append(
                        DocSpan(
                            span_id=f"doc-{len(spans) + 1}",
                            path=path,
                            block_type="table_cell",
                            heading_path=list(heading_stack),
                            text=row_text,
                            raw_text=f"| {row_text} |",
                            line_start=current_row_start,
                            line_end=current_row_end,
                            inline_code=current_row_inlines,
                        )
                    )

            idx += 1

        return spans
