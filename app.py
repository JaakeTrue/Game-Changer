
FastAPI Deprecation and Port Conflict Fixes
app.py
PY 3.41KB
README.md
MD 761B
requirements.txt
TXT 27B
Application (1).docx
DOCX 239.42KB
PQ_Calculation_Rules.docx
DOCX 36.86KB
deepseek_json_20250505_a2fc37.json
JSON 138B
0000000Document (2).docx
DOCX 16.97KB
0000001.docx
DOCX 8.09KB
Provisional Patent Application Draft ANSM.docx
DOCX 19KB
deepseek_json_20250505_a2fc37 (1).json
JSON 138B
deepseek_bash_20250505_3816a1.sh
SH 81B
why following sign occur in my app.py?  @app.on_event("startup")

INFO: Started server process [1325]

INFO: Waiting for application startup.

INFO: Application startup complete.

ERROR: [Errno 98] error while attempting to bind on address ('0.0.0.0', 8000): [errno 98] address already in use

INFO: Waiting for application shutdown.

INFO: Application shutdown complete.

2025-05-05 22:39:59.716 Session with id c514ff6b-b75d-447b-b1cc-efc9957be257 is already connected! Connecting to a new session.

/mount/src/game-changer/app.py:145: DeprecationWarning: 

on_event is deprecated, use lifespan event handlers instead.

Read more about it in the

[FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).

@app.on_event("startup")

INFO: Started server process [1325]

INFO: Waiting for application startup.

INFO: Application startup complete.

ERROR: [Errno 98] error while attempting to bind on address ('0.0.0.0', 8000): [errno 98] address already in use

INFO: Waiting for application shutdown.

INFO: Application shutdown complete.

[22:42:11] 🐙 Pulling code changes from Github...

2025-05-05 22:42:12.809 Received event for non-watched file: /mount/src/game-changer/app.py

[22:42:12] 📦 Processing dependencies...

[22:42:12] 📦 Processed dependencies!

/mount/src/game-changer/app.py:145: DeprecationWarning: 

on_event is deprecated, use lifespan event handlers instead.

Read more about it in the

[FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).

The issues you're seeing in your app.py are related to several different problems. Let me break them down and explain how to fix them:

1. @app.on_event("startup") Deprecation Warning
The warning message indicates that on_event is deprecated in FastAPI and you should use lifespan event handlers instead. This is exactly why you're seeing:

DeprecationWarning: on_event is deprecated, use lifespan event handlers instead.
Solution:
You already have the correct lifespan handler in your code (the @asynccontextmanager at the top), so you should:

Remove the @app.on_event("startup") decorator

Move its initialization code into your existing lifespan handler

2. "Address already in use" Error
The error [Errno 98] error while attempting to bind on address ('0.0.0.0', 8000) means that:

Your FastAPI server is already running (likely from a previous execution)

When you try to start it again, it can't bind to port 8000 because it's already taken

Solutions:

Make sure to stop any previous instances before restarting

Or change the port number if you need multiple instances

Or add code to automatically kill the previous process (not recommended for production)

3. Session Connection Message
The message about session ID being already connected suggests your application is trying to maintain session state but encountering duplicates.

Recommended Fixes
First, update your app.py to remove the deprecated code:

python
# Remove this entire block:
@app.on_event("startup")
async def load_sample():
    """Load sample questions on startup"""
    QUESTION_BANK[3] = [
        # ... your question definitions ...
    ]

# And move the initialization into your lifespan handler
Make sure you're not running multiple instances. Before restarting:

Manually kill any existing Python processes

Or use fuser -k 8000/tcp (Linux/Mac) to free the port

For the session issue, ensure you're generating unique session IDs properly.

Why This Happened
The deprecation warning occurs because FastAPI has moved to a newer lifespan events system that's more flexible and async-compatible.

The port conflict happens because:

Your script starts the server in a background thread

When you make changes and Streamlit reloads, it runs the script again

The new instance tries to bind to the same port

The session messages suggest your session management needs proper cleanup.

Best Practice Solution
For the FastAPI server:

python
# Replace the background thread approach with something more robust
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
For Streamlit, consider separating the UI and API into different services that you start separately.

For sessions, implement proper session cleanup in your lifespan handler.

Would you like me to provide a complete revised version of your app.py that addresses all these issues?

Dckapp.py
PY 5.38KB
compare the appy with yours attached. what is the differences
Here's a detailed comparison between your Dckapp.py and the original app.py I provided earlier:

Key Differences:
Structure & Organization:

Your version (Dckapp.py) is more systematically organized with clear section comments (# Enhanced Data Models, # Enhanced In-Memory Stores, etc.)

The original had a simpler structure without these demarcations

Data Models:

Your version adds several new models:

Misconception (for tracking error patterns)

ConstructivistTask (for hands-on learning tasks)

The original only had basic Question and session-related models

Error Analysis:

Your version includes analyze_error_pattern() function that:

Detects specific error types (sign errors, order of operations)

Builds a misconception graph

The original had no such error pattern analysis

Interval Calculation:

Your calculate_interval() is more sophisticated, incorporating:

PQ (Penta Quotient) scores

Misconception penalties

Memory stability factors

The original just used random intervals between 2-36 hours

Constructivist Tasks:

Your version has dedicated endpoints for:

/task/next - Gets constructivist tasks

/task/submit - Handles task submissions

The original only handled traditional questions

Startup Initialization:

Both use startup initialization but:

Your version calls it load_enhanced_data()

The original called it load_sample()

Your initialization includes constructivist tasks

Memory Stores:

Your version adds:

MISCONCEPTION_GRAPH

TASK_BANK

The original only had basic question and session storage

Running the Server:

Your version uses standard if __name__ == "__main__": pattern

The original launched the server in a background thread

Key Improvements in Your Version:
Enhanced Pedagogical Features:

Proper error pattern analysis

Constructivist (hands-on) tasks

Misconception tracking

More Sophisticated Scheduling:

Interval calculation based on multiple factors

Adaptive timing based on student performance

Better Organization:

Clear section headers

More logical grouping of related functionality

Production-Ready Structure:

Proper main-block execution

More complete data models

Missing from Original:
The original was more basic - it didn't have:

The misconception analysis system

Constructivist tasks

Sophisticated interval calculation

As many data stores

As many endpoints

Recommendations:
You might want to:

Add lifespan handlers (replace @app.on_event("startup"))

Include more error handling

Add documentation strings

Consider adding the PQ calculation logic

For deployment:

Your version is better structured for production

The original was more of a quick demo

Would you like me to suggest any specific improvements to your enhanced version? For example, we could:

Add proper lifespan handlers

Enhance the error analysis

Add more constructivist task types

Implement the full PQ calculation system

than please update app.py and let me down
Here's an enhanced version of app.py that incorporates the best elements from both versions while fixing the issues and adding improvements:

python
from __future__ import annotations
from datetime import timedelta
from typing import Dict, List, Optional, Tuple
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from datetime import datetime
import random
import uvicorn

# ======================
# Data Models
# ======================
class Choice(BaseModel):
    label: str
    text: str

class Misconception(BaseModel):
    root_topic: str
    related_topics: List[str]
    error_patterns: List[str]

class ConstructivistTask(BaseModel):
    type: str
    components: List[str]
    correct_configuration: Dict[str, float]

class Question(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    grade: int
    topic: str
    difficulty: int = 1  # 1=easy, 2=medium, 3=hard
    text: str
    choices: Optional[List[Choice]] = None
    answer: str
    hint: Optional[str] = None
    prerequisites: List[str] = []

class DailyScore(BaseModel):
    date: datetime
    score: float

class SessionStart(BaseModel):
    student_id: str
    grade: int
    subject: str = "Math"

class AnswerSubmission(BaseModel):
    session_id: UUID
    question_id: str
    answer: str

# ======================
# Application State
# ======================
QUESTION_BANK: Dict[int, List[Question]] = {}
TASK_BANK: Dict[str, List[ConstructivistTask]] = {}
SESSIONS: Dict[UUID, Dict] = {}
MEMORY: Dict[Tuple[str, str], Dict] = {}  # (student_id, question_id) -> {stability, due}
ATTEMPTS: Dict[Tuple[str, str], int] = {}  # (student_id, question_id) -> wrong count
PQ_HISTORY: Dict[str, List[DailyScore]] = {}
MISCONCEPTION_GRAPH: Dict[Tuple[str, str], Misconception] = {}

# ======================
# Helper Functions
# ======================
def analyze_error_pattern(student_id: str, question: Question, incorrect_answer: str) -> None:
    """Detects and records error patterns in student responses."""
    patterns = {
        "sign_errors": ["+-", "-+"],
        "order_of_ops": ["÷ before ×", "^ before ×"],
        "decomposition": ["partial_area"]
    }
    
    detected = [
        pattern for pattern, indicators in patterns.items()
        if any(ind in incorrect_answer for ind in indicators)
    ]
    
    key = (student_id, question.topic)
    current = MISCONCEPTION_GRAPH.get(key, Misconception(
        root_topic=question.topic,
        related_topics=[],
        error_patterns=[]
    ))
    
    current.error_patterns = list(set(current.error_patterns + detected))
    current.related_topics = list(set(current.related_topics + question.prerequisites))
    MISCONCEPTION_GRAPH[key] = current

def calculate_pq_score(student_id: str) -> float:
    """Calculates Penta Quotient score based on historical data."""
    scores = PQ_HISTORY.get(student_id, [])
    if not scores:
        return 50.0  # Default starting score
    
    # Simple average for demonstration
    return sum(score.score for score in scores) / len(scores)

def calculate_interval(student_id: str, question: Question) -> timedelta:
    """Calculates optimal review interval using ANSM principles."""
    mem_data = MEMORY.get((student_id, question.id), {"stability": 2.5, "difficulty": 0.3})
    pq_score = calculate_pq_score(student_id)
    pq_factor = 1 + (pq_score / 100)
    misconception_penalty = 1 + len(MISCONCEPTION_GRAPH.get((student_id, question.topic), []))
    
    # ANSM interval formula
    interval_hours = mem_data["stability"] * pq_factor / misconception_penalty
    return timedelta(hours=max(1, min(720, interval_hours * 24)))

# ======================
# FastAPI Application
# ======================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application state with sample data."""
    # Initialize question bank
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
        )
    ]
    
    # Initialize constructivist tasks
    TASK_BANK["decomposition"] = [
        ConstructivistTask(
            type="area_decompose",
            components=["rectangle", "triangle"],
            correct_configuration={"rectangle": 12.0, "triangle": 6.0}
        )
    ]
    
    yield  # Application runs here
    
    # Cleanup on shutdown
    QUESTION_BANK.clear()
    TASK_BANK.clear()

app = FastAPI(
    title="Game Changer – Enhanced Math API",
    description="Adaptive math practice with ANSM, diagnostic logic, and constructivist tasks.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# API Endpoints
# ======================
@app.post("/session/start")
async def start_session(payload: SessionStart):
    """Initialize a new learning session."""
    session_id = uuid4()
    SESSIONS[session_id] = {
        "student_id": payload.student_id,
        "grade": payload.grade,
        "history": [],  # List of (question_id, correct, timestamp)
        "correct_streak": 0,
    }
    return {"session_id": session_id}

@app.get("/question/next")
async def next_question(session_id: UUID):
    """Get the next question based on learning state."""
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    
    # Priority 1: Due reviews
    now = datetime.now()
    due = [
        q for q in QUESTION_BANK.get(session["grade"], [])
        if (session["student_id"], q.id) in MEMORY
        and MEMORY[(session["student_id"], q.id)]["due"] <= now
    ]
    
    if due:
        return random.choice(due)
    
    # Priority 2: Unseen questions
    seen = {qid for qid, *_ in session["history"]}
    unseen = [
        q for q in QUESTION_BANK.get(session["grade"], [])
        if q.id not in seen
    ]
    
    return random.choice(unseen) if unseen else QUESTION_BANK[session["grade"]][0]

@app.post("/question/submit")
async def submit_answer(payload: AnswerSubmission):
    """Process answer submission with adaptive learning logic."""
    session = SESSIONS.get(payload.session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    
    # Find question and check answer
    question = next(
        (q for q in QUESTION_BANK.get(session["grade"], [])
         if q.id == payload.question_id),
        None
    )
    if not question:
        raise HTTPException(404, "Question not found")
    
    correct = payload.answer.strip().lower() == question.answer.strip().lower()
    timestamp = datetime.now()
    
    # Update session history
    session["history"].append((question.id, correct, timestamp))
    
    # Update memory stability
    key = (session["student_id"], question.id)
    mem_data = MEMORY.get(key, {"stability": 2.5, "difficulty": 0.3})
    mem_data["stability"] += 1 if correct else -1
    mem_data["due"] = timestamp + calculate_interval(session["student_id"], question)
    MEMORY[key] = mem_data
    
    # Track misconceptions if wrong
    if not correct:
        analyze_error_pattern(session["student_id"], question, payload.answer)
    
    return {
        "correct": correct,
        "hint": question.hint if not correct else None,
        "next_review": mem_data["due"].isoformat(),
        "stability": mem_data["stability"]
    }

@app.post("/task/next")
async def get_constructivist_task(session_id: UUID, topic: str):
    """Get a constructivist task targeting misconceptions."""
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    
    misconceptions = MISCONCEPTION_GRAPH.get((session["student_id"], topic))
    if not misconceptions:
        return {"task": None}
    
    # Find tasks matching error patterns
    tasks = []
    for pattern in misconceptions.error_patterns:
        tasks.extend(TASK_BANK.get(pattern, []))
    
    return {"task": random.choice(tasks) if tasks else None}

# ======================
# Main Execution
# ======================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
