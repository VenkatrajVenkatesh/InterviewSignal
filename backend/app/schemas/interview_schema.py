from pydantic import BaseModel


class InterviewCreate(BaseModel):
    role: str
    difficulty: str

class InterviewResponse(BaseModel):
    id: int
    role: str
    difficulty: str
    status: str
    user_id: int
    
    class Config:
        orm_mode = True