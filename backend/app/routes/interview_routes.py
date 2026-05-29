from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.models.interview_model import InterviewSession
from app.models.question_model import Question
from app.models.session_question_model import SessionQuestion
from app.models.user_models import User
from app.schemas.interview_schema import InterviewCreate,InterviewResponse
from app.services.auth_service import get_current_user

router = APIRouter()


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post("/create")
def create_interview(
    interview: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    questions = db.query(Question).filter(
        Question.role == interview.role,
        Question.difficulty == interview.difficulty
    ).limit(5).all()

    if not questions:
        raise HTTPException(
            status_code=404,
            detail="No questions found for selected role and difficulty"
        )

    new_session = InterviewSession(
        role=interview.role,
        difficulty=interview.difficulty,
        status="pending",
        user_id=current_user.id
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    for question in questions:
        session_question = SessionQuestion(
            session_id=new_session.id,
            question_id=question.id
        )
        db.add(session_question)

    db.commit()

    return {
        "message": "Interview session created successfully",
        "session_id": new_session.id,
        "questions_assigned": len(questions)
    }


@router.get("/my-sessions", response_model=list[InterviewResponse])
def get_my_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sessions = db.query(InterviewSession).filter(
        InterviewSession.user_id == current_user.id
    ).all()

    return sessions


@router.get("/{session_id}/questions")
def get_session_questions(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id,
        InterviewSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session_questions = db.query(SessionQuestion).filter(
        SessionQuestion.session_id == session_id
    ).all()

    question_ids = [sq.question_id for sq in session_questions]

    questions = db.query(Question).filter(Question.id.in_(question_ids)).all()

    return questions