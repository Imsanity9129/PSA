# Password-Strength-Analyzer-V1
Local-only password strength analyzer with explainable security feedback

# Password Strength Analyzer (PSA)

A modular password strength analyzer that performs factual password analysis and explainable scoring.  
The core logic is designed to be reused later in a GUI, web app, or API without rewriting anything.

---

## Overview

This project analyzes passwords using multiple structural detectors (dictionary words, keyboard patterns, sequential runs, repeated characters) and produces:

- a detailed factual analysis of the password
- an explainable strength score (0–100)
- human-readable reasons for bonuses and penalties

The goal is to avoid “black box” password scoring and instead provide transparent, understandable results.

---

## Design Philosophy

- Clear separation of concerns  
- Analysis is factual, scoring is policy-based  
- Easy to extend with new detectors or a GUI later  

---

## What the Analyzer Detects

### Character Composition
- total length  
- lowercase, uppercase, digits, symbols  
- whitespace and non-ASCII characters  
- number of character classes used  

---

### Dictionary Words

Detects dictionary words embedded inside passwords (not just exact matches).

Overlapping matches are filtered so the most informative word is kept.

Example:
```json
{"word": "password", "start": 2, "end": 10}
```

---

### Pattern Detection

#### Consecutive Repeats
Detects repeated characters such as:
```
aaaa, !!!!, 1111
```

Returns the maximum repeat length.

---

#### Sequential Runs (Case-Insensitive)
Detects alphabetic and numeric sequences:
```
abcd, CBA, 1234, 987
```

Returns the run type, direction, indices, and sequence.

---

#### Keyboard Adjacency (QWERTY)
Detects adjacent key patterns on QWERTY rows:
```
qwerty, asdf, zxcv, lkj
```

This catches common “keyboard walk” passwords that entropy-based checks often miss.

---

## Scoring Model

Scoring is implemented separately from analysis and is designed to be explainable.

### Key Principles
- Length dominates the score (up to 90 points)
- Symbols are explicitly rewarded
- Common weak patterns apply softer penalties instead of hard failures

---

## Example Usage

```python
from psa.api import evaluate_password

result = evaluate_password("MyPassword123!!qWeRtY987")
print(result["score"])
```

Example output:
```json
{
  "score": 64,
  "rating": "Moderate",
  "reasons": [
    "Includes symbol(s) (+4).",
    "Uses 4 character classes (+4).",
    "Contains dictionary word(s) (max length 8) (-14).",
    "Contains keyboard run (max length 6) (-14).",
    "Contains sequential run (max length 3) (-6)."
  ]
}
```

---

## Usage

### Analysis only
```python
from psa.analyzer import analyze_password

analysis = analyze_password("ExamplePassword123")
```

### Scoring only
```python
from psa.scoring import score_password

score = score_password(analysis)
```

### Recommended (single call)
```python
from psa.api import evaluate_password

result = evaluate_password("ExamplePassword123")
```

---

## Why This Project

This project was built to practice:
- clean Python package design
- algorithmic pattern detection
- explainable security tooling
- writing code that can be extended into a GUI or API

---

## Future Work

- GUI or web interface
- REST API (FastAPI)
- configurable scoring weights
- additional wordlists or languages
- password improvement suggestions

---

## Status

Core analysis and scoring are complete.  
Project is structured for easy extension and UI integration.
