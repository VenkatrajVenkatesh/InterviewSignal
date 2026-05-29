from pydantic import BaseModel


class QuestionCreate(BaseModel):
     role: str = Field(..., min_length=3)
     difficulty: str = Field(..., min_length=3)
     topic: str = Field(..., min_length=3)
     question_text: str = Field(..., min_length=10)

class QuestionResponse(BaseModel):
    id: int
    role: str
    difficulty: str
    topic: str
    question_text: str

    class Config:
        orm_mode = True