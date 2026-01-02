import math
from pathlib import Path
from .wordlist import find_dictionary_words, filter_overlapping_hits
from .patterns import max_consecutive_repeats, sequential_runs, keyboard_runs_qwerty


def analyze_password(password: str) -> dict:
    length = len(password)

    lower = 0
    upper = 0
    digits = 0
    symbols = 0
    whitespace = 0
    non_ascii = 0

    char_frequency = {}

    # Dictionary words
    raw_dictionary_hits = find_dictionary_words(password, min_len=4)
    dictionary_hits = filter_overlapping_hits(raw_dictionary_hits)

    # Patterns
    max_repeat_run = max_consecutive_repeats(password)
    sequences = sequential_runs(password, min_len=3)
    keyboard_runs = keyboard_runs_qwerty(password, min_len=3)


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
        "max_consecutive_repeats": max_repeat_run,
        "sequential_runs": sequences,
        "keyboard_runs": keyboard_runs,
        "dictionary_hits": dictionary_hits
    }

    

""" if __name__ == "__main__":
    pw = input("Enter password: ")

    analysis = analyze_password(pw)
    score = score_password(analysis)
    rating = rating_from_score(score)

    print("Analysis:", analysis)
    print("Score:", score)
    print("Rating:", rating)
     """
    