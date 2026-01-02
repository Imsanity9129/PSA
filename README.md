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


