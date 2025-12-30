from __future__ import annotations

from pathlib import Path

def repo_root() -> Path:
    """
    Returns the project root directory, assuming this file lives at:
    <root>/src/psa/resources.py
    So we go up 3 levels: resources.py -> psa -> src -> root
    """
    return Path(__file__).resolve().parents[2]

def wordlists_dir() -> Path:
    """Absolute path to the repo's wordlists directory."""
    return repo_root() / "wordlists"

COMMON_WORDLIST_PATH: Path = wordlists_dir() / "common.txt"