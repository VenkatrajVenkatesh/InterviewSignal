# InterviewSignal

InterviewSignal is an AI-ready mock interview platform that helps software engineers practise technical interviews, submit answers, and receive structured feedback.

## Features

- User signup and login
- JWT-based authentication
- Protected API routes
- Interview session creation
- Role and difficulty-based question bank
- Automatic question assignment to sessions
- Answer submission workflow
- Mock feedback and scoring pipeline
- Swagger API documentation

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Passlib
- Swagger/OpenAPI
- Git & GitHub

## Backend Workflow

1. User signs up and logs in
2. User receives JWT token
3. User creates interview session
4. System assigns questions
5. User submits answers
6. System generates feedback score

## API Documentation

Run the backend and visit:

```text
http://127.0.0.1:8000/docs