from __future__ import annotations
from datetime import timedelta
from typing import Dict, List
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import threading
import uvicorn

# Streamlit imports
import streamlit as st
import requests

# FastAPI setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: populate question and task banks
    # Example data structures, replace with actual imports or definitions
    try:
        QUESTION_BANK[3] = [
            Question(
                grade=3,
                topic="Fractions",
                prerequisites=["grade2_fractions"],
                text="What is 1/2 + 1/4?",
                answer="3/4",
                hint="Find common denominator"
            ),
            Question(
                grade=3,
                topic="Multiplication",
                prerequisites=["grade2_addition"],
                text="3 × 5 = ?",
                answer="15",
                hint="Repeated addition"
            ),
        ]
        TASK_BANK["decomposition"] = [
            ConstructivistTask(
                type="area_decompose",
                components=["rectangle", "triangle"],
                correct_configuration={"rectangle": 12.0, "triangle": 6.0}
            )
        ]
    except NameError:
        # Banks not defined; ensure they are imported above
        pass
    yield
    # Shutdown logic (if needed) here

app = FastAPI(
    title="Game Changer – Enhanced Math API",
    description="Adaptive math practice with ANSM, diagnostic logic, and constructivist tasks.",
    lifespan=lifespan,
)

# Allow cross-origin for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory history
PQ_HISTORY: Dict[str, List['DailyScore']] = {}

# Example API endpoint
@app.post("/task/next")
async def get_next_task(session_id: str):
    # Simplified example logic; replace with real implementation
    history = PQ_HISTORY.setdefault(session_id, [])
    # Return a dummy question if no real logic
    if not history:
        return {"text": "What is 2+2?", "topic": "Addition"}
    return {"text": "This is a follow-up question", "topic": "General"}

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Start API in background thread
api_thread = threading.Thread(target=run_api, daemon=True)
api_thread.start()

# Streamlit UI for students
st.set_page_config(page_title="Game Changer: Student", layout="centered")
st.title("🎯 Game Changer: Student Practice")

session_id = st.text_input("Enter Session ID", value="student_session")
if st.button("Get Next Question"):
    try:
        resp = requests.post(
            "http://localhost:8000/task/next",
            json={"session_id": session_id}
        )
        resp.raise_for_status()
        st.session_state.current_question = resp.json()
    except Exception as e:
        st.error(f"Error fetching question: {e}")

if "current_question" in st.session_state:
    q = st.session_state.current_question
    st.markdown(f"**Question:** {q.get('text', 'No text')}")
    answer = st.text_input("Your Answer", key="answer_input")
    if st.button("Submit Answer"):
        st.success(f"You answered: {answer}")
        # Clear for next question
        del st.session_state["current_question"]
        del st.session_state["answer_input"]
