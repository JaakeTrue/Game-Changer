from __future__ import annotations
from datetime import timedelta
from typing import Dict, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
import streamlit as st
import requests

# If you have other module imports, include them here
# from .models import DailyScore, Question, ConstructivistTask, QUESTION_BANK, TASK_BANK

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic moved from @app.on_event("startup")
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
    yield

app = FastAPI(
    title="Game Changer – Enhanced Math API",
    description="Adaptive math practice with ANSM, diagnostic logic, and constructivist tasks.",
    lifespan=lifespan,
)

# Map of session → list of daily scores
PQ_HISTORY: Dict[str, List['DailyScore']] = {}

# Ensure timedelta calls are correctly closed
# Example usage in your code:
# return timedelta(hours=max(1, min(720, interval * 24)))

# ... rest of your existing app code goes here ...
