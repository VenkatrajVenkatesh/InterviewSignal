from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.models.question_model import Question
from app.schemas.question_schema import QuestionCreate
from app.services.auth_service import get_current_user
from app.models.user_models import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_question = Question(
        role=question.role,
        difficulty=question.difficulty,
        topic=question.topic,
        question_text=question.question_text
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return {
        "message": "Question created successfully",
        "question_id": new_question.id
    }


@router.get("/")
def get_questions(
    role: str,
    difficulty: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    questions = db.query(Question).filter(
        Question.role == role,
        Question.difficulty == difficulty
    ).all()

    return questions