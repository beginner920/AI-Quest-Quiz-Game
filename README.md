# AI Quest: Interactive AI Quiz Game — Units I & II

## Overview
AI Quest is a Streamlit-based quiz game for Artificial Intelligence Units I and II. The question bank contains **exactly 50 unique questions**, with answers, hints, and explanations. It includes MCQs, True/False, fill-in-the-blank, assertion–reason, match-the-following style items, application scenarios, and search problems.

## Features
- Exactly 50 unique questions in the bank; each round can use a selected subset
- Randomized questions, topic filters, and difficulty filters
- Optional per-question countdown timer that visibly updates every second
- Automatic timeout handling: expired questions are recorded as unanswered
- Immediate answer feedback and explanations
- Hint button (a correct answer after using a hint earns 0.5 points)
- Progress indicator, score, percentage, answer review
- Downloadable answer review CSV
- No external AI API key required

## Run locally
1. Install Python 3.10 or later.
2. Open a terminal in this folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the game:
   ```bash
   streamlit run app.py
   ```
5. Your browser should open the local app. If not, visit the URL printed in the terminal (usually `http://localhost:8501`).

## Files
- `app.py` — Streamlit interface, timer, and scoring logic
- `questions.py` — exactly 50 question records
- `question_bank.csv` — flat copy of the question bank for review
- `Assignment_Report.md` — brief report for submission
- `requirements.txt` — dependencies

## Suggested demonstration
Start with 10 questions, show the countdown changing, use a hint, submit both a correct and incorrect answer, and let one question time out. Complete the round to demonstrate scoring, answer review, and CSV export.
