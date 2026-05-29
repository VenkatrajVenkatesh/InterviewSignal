"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/services/api";

export default function SessionPage() {
  const params = useParams();
  const sessionId = Number(params.id);

  const [questions, setQuestions] = useState<any[]>([]);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [feedback, setFeedback] = useState<Record<number, any>>({});

  useEffect(() => {
    const fetchQuestions = async () => {
      const token = localStorage.getItem("access_token");

      if (!token) {
        alert("Please login first");
        return;
      }

      if (!sessionId || Number.isNaN(sessionId)) {
        alert("Invalid session id");
        return;
      }

      const data = await api.getSessionQuestions(sessionId, token);
      setQuestions(data);
    };

    fetchQuestions();
  }, [sessionId]);

  const handleSubmitAnswer = async (questionId: number) => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      alert("Please login first");
      return;
    }

    const answerText = answers[questionId];

    if (!answerText || answerText.trim().length < 10) {
      alert("Please write an answer with at least 10 characters");
      return;
    }

    const result = await api.submitAnswer(
      {
        session_id: sessionId,
        question_id: questionId,
        answer_text: answerText,
      },
      token
    );

    if (result.feedback) {
      setFeedback((prev) => ({
        ...prev,
        [questionId]: result.feedback,
      }));
    } else {
      alert(JSON.stringify(result));
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-10">
      <h1 className="mb-6 text-3xl font-bold">Interview Questions</h1>

      {questions.map((question) => (
        <div key={question.id} className="mb-6 rounded bg-white p-6 shadow">
          <h2 className="mb-2 font-semibold">{question.topic}</h2>

          <p className="mb-4">{question.question_text}</p>

          <textarea
            className="mb-4 w-full rounded border p-3"
            rows={4}
            placeholder="Write your answer here..."
            value={answers[question.id] || ""}
            onChange={(e) =>
              setAnswers((prev) => ({
                ...prev,
                [question.id]: e.target.value,
              }))
            }
          />

          <button
            onClick={() => handleSubmitAnswer(question.id)}
            className="rounded bg-black px-4 py-2 text-white"
          >
            Submit Answer
          </button>

          {feedback[question.id] && (
            <div className="mt-4 rounded bg-green-100 p-4">
              <p className="font-bold">
                Score: {feedback[question.id].score}/10
              </p>
              <p>{feedback[question.id].feedback_text}</p>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}