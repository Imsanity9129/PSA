from __future__ import annotations

from .analyzer import analyze_password
from .scoring import score_password

def evaluate_password(password: str) -> dict:
    analysis = analyze_password(password)
    score = score_password(analysis)
    return {
        "analysis": analysis,
        "score": score,
    }