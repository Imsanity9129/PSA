import math
from pathlib import Path

def load_wordlist(path: str | Path, min_len: int = 3) -> set[str]:
    """
    Load a newline-delimited wordlist file into a set.
    """
    path = Path(path)
    words: set[str] = set()

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            w = line.strip().lower()
            # keep it simple + clean
            if len(w) >= min_len and w.isalpha():
                words.add(w)

    return words

def analyze_password(password: str) -> dict:
    length = len(password)

    lower = 0
    upper = 0
    digits = 0
    symbols = 0
    whitespace = 0
    non_ascii = 0

    char_frequency = {}

    for c in password:
        # frequency
        char_frequency[c] = char_frequency.get(c, 0) + 1

        # character classes
        if c.islower():
            lower += 1
        elif c.isupper():
            upper += 1
        elif c.isdigit():
            digits += 1
        elif c.isspace():
            whitespace += 1
        else:
            symbols += 1

        if ord(c) > 127:
            non_ascii += 1

    char_classes_used = sum([
        lower > 0,
        upper > 0,
        digits > 0,
        symbols > 0,
    ])

    unique_chars = len(char_frequency)

    # entropy (Shannon)
    entropy = 0.0
    if length > 0:
        for count in char_frequency.values():
            p = count / length
            entropy -= p * math.log2(p)

    entropy_bits = round(entropy * length, 2)

    return {
        "length": length,
        "lowercase": lower,
        "uppercase": upper,
        "digits": digits,
        "symbols": symbols,
        "whitespace": whitespace,
        "non_ascii": non_ascii,
        "char_classes_used": char_classes_used,
        "unique_chars": unique_chars,
        "char_frequency": char_frequency,
        "entropy_bits": entropy_bits,
    }

def score_password(analysis: dict) -> int:
    """
    Score a password on a 0–100 scale based on analysis.
    """
    score = 0
    length = analysis["length"]

    # Length is king
    score += min(length * 4, 60)

    # Diversity helps, but doesn't dominate
    score += analysis["char_classes_used"] * 7.5

    # Short password penalty
    if length < 8:
        score -= 20

    return max(0, min(100, int(score)))

def rating_from_score(score: int) -> str:
    if score < 40:
        return "Weak"
    elif score < 70:
        return "Moderate"
    else:
        return "Strong"
    

if __name__ == "__main__":
    pw = input("Enter password: ")

    analysis = analyze_password(pw)
    score = score_password(analysis)
    rating = rating_from_score(score)

    print("Analysis:", analysis)
    print("Score:", score)
    print("Rating:", rating)
    
    