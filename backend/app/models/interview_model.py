from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.db import Base


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    status = Column(String, default="pending")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)