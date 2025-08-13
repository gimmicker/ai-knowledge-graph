"""Text processing utilities for the knowledge graph generator.

This module adds Korean-aware sentence splitting and flexible chunking
mechanisms. The default behaviour still works for English but when
``language="ko"`` is supplied additional logic is triggered.
"""

from __future__ import annotations

import re
from typing import List

try:  # pragma: no cover - optional dependency
    import kss  # type: ignore
except Exception:  # pragma: no cover
    kss = None


KOREAN_SENT_SPLIT_REGEX = re.compile(r"(?<=[.!?])\s+")


def split_sentences_ko(text: str) -> List[str]:
    """Split Korean text into sentences using kss if available.

    Falls back to a simple regular expression split when ``kss`` is not
    installed or raises an error.
    """

    if kss is not None:  # pragma: no branch
        try:
            return [s.strip() for s in kss.split_sentences(text)]
        except Exception:
            pass

    # Fallback – very naive but guarantees progress
    return [s.strip() for s in KOREAN_SENT_SPLIT_REGEX.split(text) if s.strip()]


def estimate_token_len_ko(text: str) -> int:
    """Rudimentary token length estimator for Korean text."""

    return len(text)


def _chunk_by_chars(text: str, chunk_size: int, overlap: int) -> List[str]:
    chunks: List[str] = []
    start = 0
    length = len(text)

    while start < length:
        end = min(start + chunk_size, length)
        chunks.append(text[start:end])
        if end == length:
            break
        start = max(0, end - overlap)
    return chunks


def _chunk_by_sentences(sentences: List[str], chunk_size: int, overlap: int) -> List[str]:
    chunks: List[str] = []
    start = 0

    while start < len(sentences):
        end = min(start + chunk_size, len(sentences))
        chunk = " ".join(sentences[start:end])
        chunks.append(chunk)
        if end == len(sentences):
            break
        start = max(0, end - overlap)
    return chunks


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
    token_unit: str = "words",
    sentence_splitter: str = "none",
    language: str = "en",
) -> List[str]:
    """Split text into chunks.

    Parameters mirror configuration options. ``token_unit`` controls how
    ``chunk_size`` and ``overlap`` are interpreted:

    - ``words``: existing behaviour (default for English)
    - ``chars``: character based (recommended for Korean)
    - ``sentences``: number of sentences per chunk
    """

    if token_unit == "chars":
        return _chunk_by_chars(text, chunk_size, overlap)

    if token_unit == "sentences":
        if language == "ko" and sentence_splitter == "kss":
            sentences = split_sentences_ko(text)
        else:
            sentences = [s for s in re.split(r"(?<=[.!?])\s+", text) if s]
        return _chunk_by_sentences(sentences, chunk_size, overlap)

    # Word based (original behaviour)
    words = text.split()
    if len(words) <= chunk_size:
        return [text]

    chunks: List[str] = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = max(0, end - overlap)

    return chunks


def strip_korean_particles(text: str) -> str:
    """Remove common Korean particles from the end of ``text``."""

    particle_re = re.compile(
        r"(을|를|이|가|은|는|과|와|에게|으로|에서|부터|까지|도|만|랑|의)$"
    )
    return particle_re.sub("", text)


__all__ = [
    "chunk_text",
    "split_sentences_ko",
    "estimate_token_len_ko",
    "strip_korean_particles",
]

