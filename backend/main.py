from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper import scrape_wikipedia
from llm import generate_quiz
from database import SessionLocal
from models import Quiz
import json

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Wiki Quiz Generator running"}

# ---------------- GENERATE ----------------
@app.post("/generate")
def generate(url: str):
    db = SessionLocal()
    try:
        data = scrape_wikipedia(url)
        quiz = generate_quiz(data["content"])


        new_quiz = Quiz(
            url=url,
            content=data["content"][:3000],
            quiz_json=json.dumps({
              "title": data["title"],
            "summary": data["summary"],
            "sections": data["sections"],
            "quiz": quiz["quiz"],
            "related_topics": quiz["related_topics"]
            })
        )


        db.add(new_quiz)
        db.commit()
        db.refresh(new_quiz)

        return {
    "id": new_quiz.id,
    "url": url,
    "title": data["title"],
    "summary": data["summary"],
    "sections": data["sections"],
    "quiz": quiz["quiz"],
    "related_topics": quiz["related_topics"]
}


    except Exception as e:
        print("SERVER ERROR:", e)
        return {"error": "Internal server error"}
        
    finally:
        db.close()

# ---------------- HISTORY ----------------
@app.get("/history")
def history():
    db = SessionLocal()
    quizzes = db.query(Quiz).order_by(Quiz.id.desc()).all()
    db.close()

    return [
        {
            "id": q.id,
            "url": q.url,
            "created_at": q.created_at
        }
        for q in quizzes
    ]

# ---------------- HISTORY DETAILS ----------------
@app.get("/history/{quiz_id}")
def quiz_details(quiz_id: int):
    db = SessionLocal()
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    db.close()

    if not quiz:
        return {"error": "Quiz not found"}

    return {
        "id": quiz.id,
        "url": quiz.url,
        "quiz": json.loads(quiz.quiz_json),
        "created_at": quiz.created_at
    }
