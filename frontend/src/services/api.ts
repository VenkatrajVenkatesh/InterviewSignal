const API_BASE_URL = "http://127.0.0.1:8000";

export const api = {
  signup: async (data: { email: string; password: string }) => {
    const res = await fetch(`${API_BASE_URL}/users/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    return res.json();
  },
  login: async (data: { email: string; password: string }) => {
  const res = await fetch(`${API_BASE_URL}/users/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  return res.json();
},
createInterview: async (
  data: { role: string; difficulty: string },
  token: string
) => {
  const res = await fetch(`${API_BASE_URL}/interviews/create`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });

  return res.json();
},
getSessionQuestions: async (
  sessionId: number,
  token: string
) => {
  const res = await fetch(
    `${API_BASE_URL}/interviews/${sessionId}/questions`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return res.json();
},
submitAnswer: async (
  data: {
    session_id: number;
    question_id: number;
    answer_text: string;
  },
  token: string
) => {
  const res = await fetch(`${API_BASE_URL}/answers/submit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });

  return res.json();
},
};