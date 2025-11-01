"use client";
import { useState } from "react";

export default function ProfilePage() {
  const [major, setMajor] = useState("");
  const [year, setYear] = useState("");
  const [status, setStatus] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("Sending...");
    try {
      const res = await fetch("https://httpbin.org/post", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ major, year }),
      });
      if (res.ok) setStatus("✅ Submitted successfully!");
      else setStatus("❌ Failed to send.");
    } catch (err) {
      setStatus("❌ Network error");
    }
  }

  return (
    <main className="p-8">
      <h1 className="text-2xl font-semibold mb-4">Profile Setup</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-64">
        <input
          type="text"
          placeholder="Major"
          value={major}
          onChange={(e) => setMajor(e.target.value)}
          className="border p-2 rounded"
        />
        <input
          type="text"
          placeholder="Year"
          value={year}
          onChange={(e) => setYear(e.target.value)}
          className="border p-2 rounded"
        />
        <button
          type="submit"
          className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Submit
        </button>
      </form>
      <p className="mt-3">{status}</p>
    </main>
  );
}
