from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.models.question_model import Question
from app.schemas.question_schema import QuestionCreate, QuestionResponse
from app.services.auth_service import get_current_user
from app.models.user_models import User

router = APIRouter()


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


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


@router.get("/", response_model=list[QuestionResponse])
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