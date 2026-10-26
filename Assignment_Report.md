# Assignment Report: AI Quest — Interactive AI Quiz Game (Units I & II)

## 1. Objective
The objective is to design and develop an interactive quiz game assessing understanding of Artificial Intelligence Units I and II through varied, application-oriented questions.

## 2. Tools and Technology
- **Language:** Python
- **Framework:** Streamlit
- **Libraries:** `streamlit-autorefresh` for a live countdown and pandas for CSV export
- **Data storage:** Python dictionaries in `questions.py`
- **Deployment:** Runs locally and can be deployed on Streamlit Community Cloud

The app is a quiz about AI concepts and does not require an external AI API key.

## 3. Game Design
The application displays one question at a time. Players can choose a quiz length up to 50 questions, filter by topic and difficulty, and enable or disable a timer. Questions are randomized. Answers receive immediate feedback with explanations. A progress indicator and final score summary support learning and self-assessment.

## 4. Question Bank and Coverage
The question bank contains **exactly 50 unique questions**. Formats include MCQs, True/False, fill-in-the-blank, assertion–reason, matching, scenario/application questions, and search problems. Topics covered include:
- Foundations and applications of AI; Turing Test
- Rational and intelligent agents; agents and environments
- Good behaviour and performance measures; nature of environments
- Problem formulation, problem spaces, and state-space search
- Production systems, problem characteristics, and search program design
- BFS, DFS, iterative deepening, hill climbing and variations
- Heuristic and best-first search
- Constraint satisfaction problems (CSP)
- Means-end analysis

The bank includes more than 10 application-oriented scenarios, such as medical decision support, product recommendations, driver assistance, route planning, fraud detection, spam filtering, customer-service chatbots, crop monitoring, and scheduling. Multiple questions require search reasoning about BFS, DFS, branching, or depth-first backtracking.

## 5. Interaction and Scoring
- One point for a correct answer.
- A correct answer after revealing a hint earns 0.5 points.
- Incorrect answers and timed-out questions earn zero points.
- Optional countdown timer can be set to 15, 20, 30, 45, or 60 seconds.
- The countdown visibly refreshes every second.
- If time expires, the question is automatically recorded as unanswered and the correct answer with explanation is shown.
- Final screen displays score, number correct, percentage, explanations, and a downloadable CSV answer review.

## 6. Implementation
Each question record contains a unique ID, topic, type, difficulty, prompt, options where applicable, correct answer, explanation, and hint. The application filters and randomizes questions, tracks responses in Streamlit session state, evaluates answers, and calculates the score. The timer uses periodic refreshes to update the visible countdown and process expiry.

## 7. Testing Checklist
Before submission, verify:
1. The question bank contains exactly 50 questions.
2. The timer visibly counts down once per second.
3. A timed-out question is automatically marked unanswered.
4. Correct and incorrect answers show appropriate feedback.
5. Using a hint reduces the maximum score for a correct answer to 0.5.
6. The final screen calculates score and percentage correctly.
7. The answer review CSV downloads successfully.
8. Topic and difficulty filters return relevant questions.

## 8. How to Run and Demonstrate
Install Python 3.10 or later. In the project folder, run `pip install -r requirements.txt` and then `streamlit run app.py`. Demonstrate the setup screen, a live countdown, a hint, feedback, a timeout, and the final results screen.

## 9. Conclusion
AI Quest turns the AI syllabus into a structured interactive learning activity. Its 50-question bank, practical scenarios, search exercises, explanations, timer, and score review encourage students to apply concepts and identify topics needing revision.
