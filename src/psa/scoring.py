from __future__ import annotations

def score_password(analysis: dict) -> dict:
    """
    Score report:
      {
        "score": int 0..100,
        "rating": "Weak"|"Moderate"|"Strong",
        "reasons": [ ... ]
      }

    Design goals:
    - Length dominates (up to 90 points)
    - Symbols are explicitly rewarded
    - Still penalize common weak patterns (dictionary, sequences, keyboard, repeats)
    """
    reasons: list[str] = []

    length = analysis["length"]
    symbols = analysis.get("symbols", 0)

    # ---------- Base score: LENGTH (0..90) ----------
    # Full 90 at 20+ chars (you can change 20 if you want)
    max_len_for_full = 20
    length_points = round(min(1.0, length / max_len_for_full) * 90)
    score = int(length_points)

    # ---------- Rewards ----------
    # Reward having symbols (explicit)
    # Cap so you can't farm score with 50 symbols
    if symbols > 0:
        symbol_bonus = min(8, symbols * 2)   # 1 sym=2, 2 sym=4, 3 sym=6, 4 sym=8+
        score += symbol_bonus
        reasons.append(f"Includes symbol(s) (+{symbol_bonus}).")

    # Small bonus for class diversity (kept small since length dominates)
    classes = analysis.get("char_classes_used", 0)
    diversity_bonus = min(4, classes)        # 0..4
    if diversity_bonus:
        score += diversity_bonus
        reasons.append(f"Uses {classes} character classes (+{diversity_bonus}).")

    # ---------- Penalties (SOFTER) ----------

    # Dictionary words (softer)
    dict_hits = analysis.get("dictionary_hits", [])
    if dict_hits:
        max_word_len = max(h["end"] - h["start"] for h in dict_hits)
        penalty = min(18, 6 + max_word_len)   # was much harsher
        score -= penalty
        reasons.append(f"Contains dictionary word(s) (max length {max_word_len}) (-{penalty}).")

    # Keyboard patterns (softer)
    keyboard_runs = analysis.get("keyboard_runs", [])
    if keyboard_runs:
        max_k_len = max(len(r["sequence"]) for r in keyboard_runs)
        penalty = min(20, 6 + 2 * (max_k_len - 2))  # 3->8, 6->14
        score -= penalty
        reasons.append(f"Contains keyboard run (max length {max_k_len}) (-{penalty}).")

    # Sequential runs (softer)
    seq_runs = analysis.get("sequential_runs", [])
    if seq_runs:
        max_s_len = max(len(r["sequence"]) for r in seq_runs)
        penalty = min(14, 4 + 2 * (max_s_len - 2))  # 3->6, 6->12
        score -= penalty
        reasons.append(f"Contains sequential run (max length {max_s_len}) (-{penalty}).")

    # Repeats (softer)
    max_rep = analysis.get("max_consecutive_repeats", 1)
    if max_rep >= 3:
        penalty = min(12, 3 * (max_rep - 2))  # 3->3, 4->6, 5->9
        score -= penalty
        reasons.append(f"Repeated character run (max repeat {max_rep}) (-{penalty}).")

    # Clamp score
    score = max(0, min(100, int(score)))

    # Rating buckets (adjustable)
    if score < 40:
        rating = "Weak"
    elif score < 70:
        rating = "Moderate"
    else:
        rating = "Strong"

    return {"score": score, "rating": rating, "reasons": reasons}