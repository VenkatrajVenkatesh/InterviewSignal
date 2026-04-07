from sqlalchemy import Column, Integer, String, Text
from app.database.db import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False, index=True)
    difficulty = Column(String, nullable=False, index=True)
    topic = Column(String, nullable=False)
    question_text = Column(Text, nullable=False)