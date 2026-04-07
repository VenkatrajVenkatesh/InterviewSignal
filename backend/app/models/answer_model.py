from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from datetime import datetime
from app.database.db import Base


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer_text = Column(Text, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)