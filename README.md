# Password-Strength-Analyzer-V1
Local-only password strength analyzer with explainable security feedback

Password Strength Analyzer (PSA)

A modular, library-first password strength analyzer that performs factual password analysis and explainable scoring.
The project is designed so the core logic can be reused later in a GUI, web app, or API without rewriting anything.

⸻

Overview

This project analyzes passwords using multiple structural detectors (dictionary words, keyboard patterns, sequential runs, repeated characters) and produces:
	•	a detailed factual analysis of the password
	•	an explainable strength score (0–100)
	•	human-readable reasons for bonuses and penalties

The goal was to avoid “black box” password scoring and instead build something that is transparent, modular, and extensible.

⸻

Design Philosophy
	•	Library-first (no CLI dependency)
	•	Clear separation of concerns
	•	Analysis is factual, scoring is policy-based
	•	Easy to extend with new detectors or a GUI later
