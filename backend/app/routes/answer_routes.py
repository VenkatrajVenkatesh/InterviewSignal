from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.models.answer_model import Answer
from app.models.feedback_model import Feedback
from app.models.interview_model import InterviewSession
from app.models.question_model import Question
from app.models.session_question_model import SessionQuestion
from app.models.user_models import User
from app.schemas.answer_schema import AnswerCreate, AnswerResponse
from app.services.auth_service import get_current_user
from app.services.feedback_services import generate_mock_feedback

router = APIRouter()


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post("/submit")
def submit_answer(
    payload: AnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(InterviewSession).filter(
        InterviewSession.id == payload.session_id,
        InterviewSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")

    question = db.query(Question).filter(
        Question.id == payload.question_id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    session_question = db.query(SessionQuestion).filter(
        SessionQuestion.session_id == payload.session_id,
        SessionQuestion.question_id == payload.question_id
    ).first()

    if not session_question:
        raise HTTPException(
            status_code=400,
            detail="This question is not assigned to the session"
        )

    existing_answer = db.query(Answer).filter(
        Answer.session_id == payload.session_id,
        Answer.question_id == payload.question_id
    ).first()

    if existing_answer:
        raise HTTPException(
            status_code=400,
            detail="Answer already submitted for this question"
        )

    new_answer = Answer(
        session_id=payload.session_id,
        question_id=payload.question_id,
        answer_text=payload.answer_text
    )

    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    feedback_result = generate_mock_feedback(payload.answer_text)

    new_feedback = Feedback(
        answer_id=new_answer.id,
        score=feedback_result["score"],
        feedback_text=feedback_result["feedback_text"]
    )

    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    return {
        "message": "Answer submitted successfully",
        "answer_id": new_answer.id,
        "feedback": {
            "score": new_feedback.score,
            "feedback_text": new_feedback.feedback_text
        }
    }


@router.get("/session/{session_id}", response_model=list[AnswerResponse])
def get_session_answers(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id,
        InterviewSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")

    answers = db.query(Answer).filter(Answer.session_id == session_id).all()

    return answers


@router.get("/{answer_id}/feedback")
def get_feedback_for_answer(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    answer = db.query(Answer).filter(Answer.id == answer_id).first()

    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    session = db.query(InterviewSession).filter(
        InterviewSession.id == answer.session_id,
        InterviewSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=403, detail="Not authorized to view this feedback")

    feedback = db.query(Feedback).filter(Feedback.answer_id == answer_id).first()

    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    return feedback