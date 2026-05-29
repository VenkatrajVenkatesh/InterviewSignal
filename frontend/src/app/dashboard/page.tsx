"use client";

export default function DashboardPage() {
  const token =
    typeof window !== "undefined"
      ? localStorage.getItem("access_token")
      : null;

  return (
    <div className="p-10">
      <h1 className="text-3xl font-bold">
        InterviewSignal Dashboard
      </h1>

      <p className="mt-4">
        Logged in successfully.
      </p>

      <p className="mt-4 break-all text-sm">
        Token:
      </p>

      <div className="mt-2 rounded bg-gray-100 p-4">
        {token}
      </div>
    </div>
  );
}