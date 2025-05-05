from __future__ import annotations
from datetime import timedelta
from typing import Dict, List
from contextlib import asynccontextmanager
import threading

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import streamlit as st
import requests

# Placeholder imports; replace with your actual models and data structures
try:
    from models import DailyScore, Question, ConstructivistTask, QUESTION_BANK, TASK_BANK
except ImportError:
    class DailyScore:
        pass

    class Question:
        def __init__(self, grade, topic, prerequisites, text, answer, hint):
            self.grade = grade
            self.topic = topic
            self.prerequisites = prerequisites
            self.text = text
            self.answer = answer
            self.hint = hint

    class ConstructivistTask:
        def __init__(self, type, components, correct_configuration):
            self.type = type
            self.components = components
            self.correct_configuration = correct_configuration

    QUESTION_BANK: Dict[int, List[Question]] = {}
    TASK_BANK: Dict[str, List[ConstructivistTask]] = {}

# FastAPI lifespan for startup logic
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Populate question and task banks
    QUESTION_BANK[3] = [
        Question(3, "Fractions", ["grade2_fractions"], "What is 1/2 + 1/4?", "3/4", "Find common denominator"),
        Question(3, "Multiplication", ["grade2_addition"], "3 × 5 = ?", "15", "Repeated addition"),
    ]
    TASK_BANK["decomposition"] = [
        ConstructivistTask("area_decompose", ["rectangle", "triangle"], {"rectangle": 12.0, "triangle": 6.0})
    ]
    yield  # Optional shutdown logic

app = FastAPI(
    title="Game Changer – Enhanced Math API",
    description="Adaptive math practice with ANSM, diagnostic logic, and constructivist tasks.",
    lifespan=lifespan,
)

# Allow CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session history
PQ_HISTORY: Dict[str, List['DailyScore']] = {}

@app.post("/task/next")
async def get_next_task(payload: dict):
    session_id = payload.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id is required")
    history = PQ_HISTORY.setdefault(session_id, [])
    if not history:
        return {"text": "What is 2 + 2?", "topic": "Addition"}
    return {"text": "Tell me more about your reasoning.", "topic": "Reflection"}

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

# Start FastAPI in background thread
threading.Thread(target=run_api, daemon=True).start()

# Streamlit UI for students
st.set_page_config(page_title="Game Changer: Student", layout="centered")
st.title("🎯 Game Changer: Student Practice")

session_id = st.text_input("Enter Session ID", value="student_session")
if st.button("Get Next Question"):
    try:
        resp = requests.post("http://localhost:8000/task/next", json={"session_id": session_id})
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
        del st.session_state["current_question"]
        del st.session_state["answer_input"]
