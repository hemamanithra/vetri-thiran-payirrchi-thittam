from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    version="1.0.0",
    description=(
        "AI-powered educational assistant for questions, "
        "explanations, quizzes, summaries and learning paths."
    ),
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


# HTML templates
templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# ============================================================
# REQUEST MODELS
# ============================================================

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class QuizRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )


# ============================================================
# FRONTEND
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health():

    from ai_client import is_gemini_configured

    return {
        "status": "ok",
        "gemini_configured": is_gemini_configured()
    }


# ============================================================
# QUESTION ANSWERING
# ============================================================

@app.post("/qa")
async def qa(payload: QuestionRequest):

    result = answer_question(
        payload.question
    )

    return {
        "result": result
    }


# ============================================================
# EXPLANATION
# ============================================================

@app.post("/explain")
async def explain(payload: TextRequest):

    result = explain_topic(
        payload.text
    )

    return {
        "result": result
    }


# ============================================================
# QUIZ
# ============================================================

@app.post("/quiz")
async def quiz(payload: QuizRequest):

    result = generate_quiz(
        payload.text
    )

    return {
        "result": result
    }


# ============================================================
# SUMMARY
# ============================================================

@app.post("/summarize")
async def summarize(payload: TextRequest):

    result = summarize_text(
        payload.text
    )

    return {
        "result": result
    }


# ============================================================
# LEARNING PATH
# ============================================================

@app.post("/learn/recommendations")
async def recommendations(payload: TextRequest):

    result = get_learning_recommendations(
        payload.text
    )

    return {
        "result": result
    }


# ============================================================
# API INFORMATION
# ============================================================

@app.get("/api")
async def api_info():

    return {
        "name": "EduGenie API",
        "version": "1.0.0",
        "endpoints": [
            "/qa",
            "/explain",
            "/quiz",
            "/summarize",
            "/learn/recommendations"
        ]
    }