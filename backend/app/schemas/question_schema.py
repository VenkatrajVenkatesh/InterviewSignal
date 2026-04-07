from pydantic import BaseModel


class QuestionCreate(BaseModel):
    role: str
    difficulty: str
    topic: str
    question_text: str