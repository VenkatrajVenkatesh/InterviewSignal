from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.models.interview_model import InterviewSession
from app.models.user_models import User
from app.schemas.interview_schema import InterviewCreate
from app.services.auth_service import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
def create_interview(
    interview: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_session = InterviewSession(
        role=interview.role,
        difficulty=interview.difficulty,
        status="pending",
        user_id=current_user.id
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return {
        "message": "Interview session created successfully",
        "session_id": new_session.id
    }


@router.get("/my-sessions")
def get_my_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sessions = db.query(InterviewSession).filter(
        InterviewSession.user_id == current_user.id
    ).all()

    return sessions