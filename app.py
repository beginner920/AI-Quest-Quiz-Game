import random
import time
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from questions import QUESTIONS

st.set_page_config(page_title="AI Quest | Units I & II", page_icon="🧠", layout="centered")

st.markdown("""
<style>
.main {max-width: 920px; padding-top: 1.5rem;}
.hero {padding: 1.25rem 1.4rem; border-radius: 18px; background: linear-gradient(120deg,#172554,#4338ca); color:white; margin-bottom:1rem;}
.hero h1 {color:white; margin:0;}
div.stButton > button {border-radius: 10px; min-height: 2.6rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🧠 AI Quest: Units I & II</h1><p>Think like an intelligent agent. Explore, reason, and solve!</p></div>', unsafe_allow_html=True)
st.caption("Artificial Intelligence • Interactive quiz game • Exactly 50 unique questions in the question bank")

def check_answer(q, response):
    if response is None:
        return False
    if q["type"] == "fill":
        norm = str(response).strip().lower().replace("-", " ").replace("_", " ")
        accepted = [a.strip().lower().replace("-", " ").replace("_", " ") for a in q.get("accepted_answers", [q["answer"]])]
        return norm in accepted
    return response == q["answer"]

def reset_game():
    st.session_state.started = False
    st.session_state.finished = False
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.responses = []
    st.session_state.await_next = False
    st.session_state.question_set = []
    st.session_state.question_start = time.time()
    st.session_state.used_hint = False
    st.session_state.timeout_recorded = False

if "started" not in st.session_state:
    reset_game()

with st.sidebar:
    st.header("Game settings")
    player = st.text_input("Player name (optional)", value=st.session_state.get("player", ""))
    total = st.select_slider("Questions per game", options=[10, 15, 20, 25, 30, 40, 50], value=20)
    difficulty = st.selectbox("Difficulty", ["All levels", "Easy", "Medium", "Hard"])
    topics = sorted({q["topic"] for q in QUESTIONS})
    selected_topics = st.multiselect("Topics (leave blank for all)", topics, default=[])
    timed = st.checkbox("Enable per-question timer", value=True)
    seconds = st.select_slider("Seconds per question", options=[15, 20, 30, 45, 60], value=30, disabled=not timed)
    st.markdown("---")
    st.caption("Scoring: +1 for a correct answer. If you reveal a hint, a correct answer earns 0.5 points. Timeout or incorrect answer earns 0 points.")

def start_game():
    pool = QUESTIONS[:]
    if selected_topics:
        pool = [q for q in pool if q["topic"] in selected_topics]
    if difficulty != "All levels":
        pool = [q for q in pool if q["difficulty"] == difficulty]
    if not pool:
        st.error("No questions match those filters. Choose more topics or another difficulty.")
        return
    random.shuffle(pool)
    st.session_state.question_set = pool[:min(total, len(pool))]
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.responses = []
    st.session_state.started = True
    st.session_state.finished = False
    st.session_state.player = player
    st.session_state.timed = timed
    st.session_state.seconds = seconds
    st.session_state.question_start = time.time()
    st.session_state.used_hint = False
    st.session_state.await_next = False
    st.session_state.timeout_recorded = False
    st.rerun()

if not st.session_state.started and not st.session_state.finished:
    st.subheader("Ready to begin?")
    st.write("Choose your settings in the sidebar, then start a round. Questions are drawn randomly from the 50-question bank.")
    st.info("Formats include MCQs, True/False, fill-in-the-blank, assertion–reason, matching, real-world scenarios, and search problems.")
    if st.button("🚀 Start Quiz", type="primary", use_container_width=True):
        start_game()
    with st.expander("Explore the topics covered"):
        for topic in topics:
            st.write("• " + topic)

elif st.session_state.started and not st.session_state.finished:
    idx = st.session_state.index
    qs = st.session_state.question_set
    q = qs[idx]
    n = len(qs)

    # Auto-refresh the active question once per second so the countdown visibly changes.
    # On expiry, the current question is recorded automatically as unanswered.
    if st.session_state.timed and not st.session_state.await_next:
        st_autorefresh(interval=1000, key=f"timer_refresh_{q['id']}_{idx}")

    elapsed = time.time() - st.session_state.question_start
    remaining = max(0, int(st.session_state.seconds - elapsed)) if st.session_state.timed else None

    st.progress(idx / n, text=f"Question {idx + 1} of {n}")
    st.markdown(f"**Topic:** {q['topic']}  ·  **Difficulty:** {q['difficulty']}  ·  **Format:** {q['type'].replace('_',' ').title()}")
    st.subheader(q["question"])

    if st.session_state.timed:
        st.caption(f"⏱️ Time remaining: **{remaining} seconds**")
        if remaining <= 0 and not st.session_state.await_next and not st.session_state.timeout_recorded:
            st.session_state.responses.append({
                "id": q["id"], "topic": q["topic"], "question": q["question"],
                "your_answer": "(Time expired)", "correct_answer": q["answer"],
                "correct": False, "earned": 0.0, "explanation": q["explanation"],
                "timed_out": True
            })
            st.session_state.last_result = {
                "correct": False, "timed_out": True, "answer": q["answer"],
                "explanation": q["explanation"]
            }
            st.session_state.await_next = True
            st.session_state.timeout_recorded = True
            st.rerun()

    if not st.session_state.await_next:
        if q.get("hint") and st.button("💡 Show hint"):
            st.session_state.used_hint = True
            st.info(q["hint"])

        form_key = f"answer_form_{q['id']}_{idx}"
        with st.form(form_key):
            if q["type"] == "fill":
                response = st.text_input("Your answer", key=f"fill_{q['id']}_{idx}")
            else:
                response = st.radio("Choose one answer", q["options"], key=f"radio_{q['id']}_{idx}", index=None)
            submitted = st.form_submit_button("Submit answer", type="primary", use_container_width=True)

        if submitted:
            timed_out = st.session_state.timed and (time.time() - st.session_state.question_start >= st.session_state.seconds)
            correct = False if timed_out else check_answer(q, response)
            earned = (0.5 if st.session_state.get("used_hint", False) else 1.0) if correct else 0.0
            st.session_state.score += earned
            st.session_state.responses.append({
                "id": q["id"], "topic": q["topic"], "question": q["question"],
                "your_answer": response if response else "(No answer)",
                "correct_answer": q["answer"], "correct": correct, "earned": earned,
                "explanation": q["explanation"], "timed_out": timed_out
            })
            st.session_state.last_result = {
                "correct": correct, "timed_out": timed_out,
                "answer": q["answer"], "explanation": q["explanation"]
            }
            st.session_state.await_next = True
            st.rerun()

    if st.session_state.get("await_next", False):
        result = st.session_state.last_result
        if result["timed_out"]:
            st.error("Time expired. No point awarded.")
            st.write("Correct answer:", result["answer"])
            st.write(result["explanation"])
        elif result["correct"]:
            st.success("Correct! " + result["explanation"])
        else:
            st.error("Not quite. Correct answer: " + result["answer"])
            st.write(result["explanation"])
        if st.button("Next question ➜", type="primary", use_container_width=True):
            st.session_state.index += 1
            st.session_state.await_next = False
            st.session_state.used_hint = False
            st.session_state.timeout_recorded = False
            st.session_state.question_start = time.time()
            if st.session_state.index >= len(st.session_state.question_set):
                st.session_state.started = False
                st.session_state.finished = True
            st.rerun()

    st.markdown("---")
    st.caption(f"Current score: {st.session_state.score:g} / {len(st.session_state.responses)}")
    if not st.session_state.await_next and st.button("End quiz and see results"):
        st.session_state.started = False
        st.session_state.finished = True
        st.rerun()

elif st.session_state.finished:
    responses = st.session_state.responses
    possible = len(responses)
    score = st.session_state.score
    pct = (score / possible * 100) if possible else 0
    st.balloons()
    st.subheader("🏁 Quiz complete!")
    name = st.session_state.get("player", "").strip() or "Player"
    st.write(f"Well done, **{name}**.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Score", f"{score:g} / {possible}")
    c2.metric("Correct answers", f"{sum(r['correct'] for r in responses)}/{possible}" if possible else "0/0")
    c3.metric("Percentage", f"{pct:.1f}%")
    if pct >= 80:
        st.success("Excellent understanding. Try a harder round or review the topics you missed.")
    elif pct >= 60:
        st.info("Good effort. Review the explanations for missed questions and try another round.")
    else:
        st.warning("Use the answer review below to revise the concepts, then play again.")
    st.subheader("Answer review")
    for i, r in enumerate(responses, 1):
        with st.expander(f"{i}. {'✅' if r['correct'] else '❌'} {r['question']}"):
            st.write("**Your answer:**", r["your_answer"])
            st.write("**Correct answer:**", r["correct_answer"])
            st.write("**Topic:**", r["topic"])
            st.write(r["explanation"])
    report = pd.DataFrame(responses)
    st.download_button("⬇️ Download answer review (CSV)", report.to_csv(index=False).encode("utf-8"), "ai_quest_results.csv", "text/csv")
    if st.button("🔁 Play another round", type="primary", use_container_width=True):
        reset_game()
        st.rerun()
