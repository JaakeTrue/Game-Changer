# appy_enhanced.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Tuple
from uuid import uuid4, UUID
from datetime import datetime, timedelta
import random

app = FastAPI(
    title="Game Changer – Enhanced Math API",
    description="Adaptive math practice with ANSM, diagnostic logic, and constructivist tasks."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Enhanced Data Models
# -----------------------------
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
    difficulty: int = 1
    text: str
    choices: Optional[List[Choice]] = None
    answer: str
    hint: Optional[str] = None
    prerequisites: List[str] = []

class SessionStart(BaseModel):
    student_id: str
    grade: int
    subject: str = "Math"

class AnswerSubmission(BaseModel):
    session_id: UUID
    question_id: str
    answer: str

# ... (Keep other existing models) ...

# -----------------------------
# Enhanced In-Memory Stores
# -----------------------------
QUESTION_BANK: Dict[int, List[Question]] = {}
SESSIONS: Dict[UUID, Dict] = {}
MEMORY: Dict[Tuple[str, str], Dict] = {}
ATTEMPTS: Dict[Tuple[str, str], int] = {}
PQ_HISTORY: Dict[str, List[DailyScore]] = {}
MISCONCEPTION_GRAPH: Dict[Tuple[str, str], Misconception] = {}
TASK_BANK: Dict[str, List[ConstructivistTask]] = {}

# -----------------------------
# Enhanced Helper Functions
# -----------------------------
def analyze_error_pattern(student_id: str, question: Question, incorrect_answer: str):
    patterns = {
        "sign_errors": ["+-", "-+"],
        "order_of_ops": ["÷ before ×", "^ before ×"],
        "decomposition": ["partial_area"]
    }
    
    detected = []
    for pattern, indicators in patterns.items():
        if any(ind in incorrect_answer for ind in indicators):
            detected.append(pattern)
    
    key = (student_id, question.topic)
    current = MISCONCEPTION_GRAPH.get(key, Misconception(
        root_topic=question.topic,
        related_topics=[],
        error_patterns=[]
    ))
    
    current.error_patterns = list(set(current.error_patterns + detected))
    current.related_topics = list(set(current.related_topics + question.prerequisites))
    MISCONCEPTION_GRAPH[key] = current

def calculate_interval(student_id: str, question: Question) -> timedelta:
    mem_data = MEMORY.get((student_id, question.id), {"stability": 2.5, "difficulty": 0.3})
    pq = PQ_HISTORY.get(student_id, [])
    pq_factor = 1 + (pq[-1].score/100 if pq else 0)
    misconception_penalty = 1 + len(MISCONCEPTION_GRAPH.get((student_id, question.topic), []))
    interval = mem_data["stability"] * pq_factor / misconception_penalty
    return timedelta(hours=max(1, min(720, interval * 24)))

# -----------------------------
# Enhanced Endpoints
# -----------------------------
@app.post("/task/next")
async def get_constructivist_task(session_id: UUID, topic: str):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    
    misconceptions = MISCONCEPTION_GRAPH.get((session["student_id"], topic))
    if not misconceptions:
        return {"task": None}
    
    tasks = []
    for pattern in misconceptions.error_patterns:
        tasks.extend(TASK_BANK.get(pattern, []))
    
    return {"task": random.choice(tasks) if tasks else None}

@app.post("/task/submit")
async def submit_task(session_id: UUID, task: ConstructivistTask, submission: Dict):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    
    correct = submission == task.correct_configuration
    if correct:
        key = (session["student_id"], task.type)
        if key in MISCONCEPTION_GRAPH:
            del MISCONCEPTION_GRAPH[key]
    
    return {"correct": correct, "feedback": "Great job!" if correct else "Try again"}

# -----------------------------
# Enhanced Startup Data
# -----------------------------
@app.on_event("startup")
async def load_enhanced_data():
    # Grade 3 Questions with Prerequisites
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
    
    # Constructivist Tasks
    TASK_BANK["decomposition"] = [
        ConstructivistTask(
            type="area_decompose",
            components=["rectangle", "triangle"],
            correct_configuration={"rectangle": 12.0, "triangle": 6.0}
        )
    ]

# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)