from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import engine, Base
from app.models import *;
from app.routes import user_routes, interview_routes, question_routes,answer_routes

app = FastAPI(title="InterviewSignal API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Create DB tables
Base.metadata.create_all(bind=engine)
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(interview_routes.router, prefix="/interviews", tags=["Interviews"])
app.include_router(question_routes.router, prefix="/questions", tags=["Questions"])
app.include_router(answer_routes.router, prefix="/answers", tags=["Answers"])

@app.get("/")
def root():
    return {"message": "InterviewSignal API is running"}