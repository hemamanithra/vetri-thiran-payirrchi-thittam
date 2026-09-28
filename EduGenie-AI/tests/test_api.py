from fastapi.testclient import TestClient

import main
import qna
import explanation_module
import summary_module
import learning_path
import quiz_module


client = TestClient(
    main.app
)


# ============================================================
# HOME
# ============================================================

def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text


# ============================================================
# HEALTH
# ============================================================

def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        ==
        "ok"
    )


# ============================================================
# API INFORMATION
# ============================================================

def test_api_info():

    response = client.get(
        "/api"
    )

    assert response.status_code == 200

    assert (
        "/qa"
        in
        response.json()["endpoints"]
    )


# ============================================================
# Q&A
# ============================================================

def test_qa(monkeypatch):

    monkeypatch.setattr(
        qna,
        "generate_text",
        lambda prompt:
            "Artificial Intelligence is..."
    )


    response = client.post(

        "/qa",

        json={
            "question":
                "What is AI?"
        }

    )


    assert response.status_code == 200

    assert (
        response.json()["result"]
        ==
        "Artificial Intelligence is..."
    )


# ============================================================
# EXPLANATION
# ============================================================

def test_explanation(monkeypatch):

    monkeypatch.setattr(

        explanation_module,

        "generate_text",

        lambda prompt, **kwargs:
            "This is a simple explanation."

    )


    response = client.post(

        "/explain",

        json={
            "text":
                "Photosynthesis"
        }

    )


    assert response.status_code == 200


# ============================================================
# SUMMARY
# ============================================================

def test_summary(monkeypatch):

    monkeypatch.setattr(

        summary_module,

        "generate_text",

        lambda prompt, **kwargs:
            "Short summary."

    )


    response = client.post(

        "/summarize",

        json={
            "text":
                "This is a long passage."
        }

    )


    assert response.status_code == 200


# ============================================================
# LEARNING PATH
# ============================================================

def test_learning_path(monkeypatch):

    monkeypatch.setattr(

        learning_path,

        "generate_text",

        lambda prompt, **kwargs:
            "Beginner to advanced learning path."

    )


    response = client.post(

        "/learn/recommendations",

        json={
            "text":
                "Python programming"
        }

    )


    assert response.status_code == 200


# ============================================================
# QUIZ
# ============================================================

def test_quiz(monkeypatch):

    quiz_data = {

        "questions": [

            {

                "question":
                    "Question 1?",

                "options": [
                    "A",
                    "B",
                    "C",
                    "D"
                ],

                "answer":
                    "A",

                "explanation":
                    "A is correct."

            },

            {

                "question":
                    "Question 2?",

                "options": [
                    "A",
                    "B",
                    "C",
                    "D"
                ],

                "answer":
                    "B",

                "explanation":
                    "B is correct."

            },

            {

                "question":
                    "Question 3?",

                "options": [
                    "A",
                    "B",
                    "C",
                    "D"
                ],

                "answer":
                    "C",

                "explanation":
                    "C is correct."

            }

        ]

    }


    monkeypatch.setattr(

        main,

        "generate_quiz",

        lambda text:
            quiz_data

    )


    response = client.post(

        "/quiz",

        json={
            "text":
                "Study passage"
        }

    )


    assert response.status_code == 200


    questions = (
        response
        .json()["result"]["questions"]
    )


    assert len(
        questions
    ) == 3