"use client";

import { useState } from "react";
import { api } from "@/services/api";

export default function CreateInterviewPage() {
  const [role, setRole] = useState("backend engineer");
  const [difficulty, setDifficulty] = useState("medium");

  const handleCreate = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      alert("Please login first");
      return;
    }

    const result = await api.createInterview(
      { role, difficulty },
      token
    );

    if(result.session_id) {
      window.location.href = `/session/${result.session_id}`;
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <div className="w-full max-w-md rounded bg-white p-8 shadow">
        <h1 className="mb-6 text-2xl font-bold">Create Interview</h1>

        <input
          className="mb-4 w-full rounded border p-3"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        />

        <select
          className="mb-4 w-full rounded border p-3"
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
        >
          <option value="easy">easy</option>
          <option value="medium">medium</option>
          <option value="hard">hard</option>
        </select>

        <button
          onClick={handleCreate}
          className="w-full rounded bg-black p-3 text-white"
        >
          Start Interview
        </button>
      </div>
    </div>
  );
}