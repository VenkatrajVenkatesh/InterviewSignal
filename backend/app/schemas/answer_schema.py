from pydantic import BaseModel, Field


class AnswerCreate(BaseModel):
    session_id: int
    question_id: int
    answer_text: str = Field(..., min_length=10)

class AnswerResponse(BaseModel):
    id: int
    session_id: int
    question_id: int
    answer_text: str

    class Config:
        orm_mode = True