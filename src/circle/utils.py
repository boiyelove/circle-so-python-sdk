"""Shared utilities."""
from __future__ import annotations
from typing import Any, Dict, List


def text_to_tiptap(text: str) -> Dict[str, Any]:
    """Convert plain text to Circle's tiptap rich_text_body format.

    Splits on double newlines for paragraphs, single newlines for hard breaks.
    The returned dict can be passed as ``tiptap_body`` to ``create_post`` or
    as ``rich_text_body`` to ``create_chat_message``.

    Example::

        >>> text_to_tiptap("Hello\\n\\nWorld")
        {'body': {'type': 'doc', 'content': [
            {'type': 'paragraph', 'content': [{'type': 'text', 'text': 'Hello'}]},
            {'type': 'paragraph', 'content': [{'type': 'text', 'text': 'World'}]},
        ]}}
    """
    content: List[Dict[str, Any]] = []
    for p in text.split("\n\n"):
        if not p.strip():
            continue
        lines = p.split("\n")
        para_content: List[Dict[str, Any]] = []
        for i, line in enumerate(lines):
            if i > 0:
                para_content.append({"type": "hardBreak"})
            para_content.append({"type": "text", "text": line})
        content.append({"type": "paragraph", "content": para_content})
    return {"body": {"type": "doc", "content": content}}
