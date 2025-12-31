from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .resources import COMMON_WORDLIST_PATH


@dataclass(frozen=True)
class Wordlist:
    """
    Holds a set of words for fast membership checks.
    We keep it simple and factual: just loading + lookups.
    """
    words: frozenset[str]

    @classmethod
    def from_file(cls, path: Path) -> "Wordlist":
        cleaned: set[str] = set()
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                w = line.strip().lower()
                if not w or w.startswith("#"):
                    continue
                cleaned.add(w)
        return cls(words=frozenset(cleaned))

    def contains(self, word: str) -> bool:
        return word.lower() in self.words


# Load once (cached in module memory)
_COMMON_WORDLIST: Wordlist | None = None


def get_common_wordlist() -> Wordlist:
    global _COMMON_WORDLIST
    if _COMMON_WORDLIST is None:
        _COMMON_WORDLIST = Wordlist.from_file(COMMON_WORDLIST_PATH)
    return _COMMON_WORDLIST


def find_dictionary_words(password: str, *, min_len: int = 4) -> list[dict]:
    """
    Finds dictionary words that appear as substrings inside the password.
    Returns factual hits (word + start/end indices).

    Example return item:
      {"word": "pass", "start": 0, "end": 4}
    """
    wl = get_common_wordlist()
    s = password.lower()

    hits: list[dict] = []
    n = len(s)

    # brute force substring search (fine for typical password lengths)
    for i in range(n):
        for j in range(i + min_len, n + 1):
            sub = s[i:j]
            if wl.contains(sub):
                hits.append({"word": sub, "start": i, "end": j})

    return hits

def filter_overlapping_hits(hits: list[dict]) -> list[dict]:
    """
    Keep a clean subset of dictionary hits by removing overlaps.
    Strategy: prefer longer hits; keep non-overlapping.
    """
    if not hits:
        return []

    # Sort: longer words first, then earlier start
    hits_sorted = sorted(
        hits,
        key=lambda h: (-(h["end"] - h["start"]), h["start"], h["end"])
    )

    kept: list[dict] = []
    occupied = [False] * (max(h["end"] for h in hits_sorted))

    for h in hits_sorted:
        start, end = h["start"], h["end"]
        # check overlap with already-kept spans
        if any(occupied[i] for i in range(start, end)):
            continue
        kept.append(h)
        for i in range(start, end):
            occupied[i] = True

    # Optional: return in reading order
    kept.sort(key=lambda h: (h["start"], h["end"]))
    return kept