from fastapi import FastAPI

app = FastAPI(title="InterviewSignal API")


@app.get("/")
def root():
    return {"message": "InterviewSignal API is running"}