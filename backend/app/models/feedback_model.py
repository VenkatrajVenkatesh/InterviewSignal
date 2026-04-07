from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from datetime import datetime
from app.database.db import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    answer_id = Column(Integer, ForeignKey("answers.id"), nullable=False)
    score = Column(Integer, nullable=False)
    feedback_text = Column(Text, nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)