"use client";

import { useState } from "react";

export default function PatientPage() {
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("male");
  const [symptoms, setSymptoms] = useState("");
  const [durationDays, setDurationDays] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
    const response = await fetch(
  `${process.env.NEXT_PUBLIC_API_URL}/triage`,
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      age: Number(age),
      gender,
      symptoms: symptoms.split(","),
      duration_days: Number(durationDays),
    }),
  }
);

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({ error: "Failed to connect to backend" });
    } finally {
      setLoading(false);
    }
  };

  const getUrgencyBadge = (urgency: string) => {
    if (urgency === "Emergency") {
      return "bg-red-600 text-white px-3 py-1 rounded-full text-sm font-semibold";
    }
    if (urgency === "High") {
      return "bg-orange-500 text-white px-3 py-1 rounded-full text-sm font-semibold";
    }
    if (urgency === "Medium") {
      return "bg-yellow-400 text-black px-3 py-1 rounded-full text-sm font-semibold";
    }
    return "bg-green-500 text-white px-3 py-1 rounded-full text-sm font-semibold";
  };

  return (
    <main className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
      <div className="bg-white shadow-xl rounded-xl p-8 w-full max-w-xl">
        <h1 className="text-3xl font-bold text-gray-900 mb-6 text-center">
          Patient Triage Form
        </h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="number"
            placeholder="Age"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            className="w-full border rounded-lg px-4 py-3"
            required
          />

          <select
            value={gender}
            onChange={(e) => setGender(e.target.value)}
            className="w-full border rounded-lg px-4 py-3"
          >
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>

          <input
            type="text"
            placeholder="Symptoms (comma separated)"
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            className="w-full border rounded-lg px-4 py-3"
            required
          />

          <input
            type="number"
            placeholder="Duration in days"
            value={durationDays}
            onChange={(e) => setDurationDays(e.target.value)}
            className="w-full border rounded-lg px-4 py-3"
            required
          />

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium"
          >
            {loading ? "Checking..." : "Check Triage"}
          </button>
        </form>

        {result && (
          <div className="mt-8 p-6 border rounded-xl bg-gray-50">
            {result.error ? (
              <p className="text-red-600 font-medium">{result.error}</p>
            ) : (
              <>
                <h2 className="text-2xl font-semibold mb-4 text-gray-900">
                  Triage Result
                </h2>

                <div className="space-y-3 text-gray-800">
                  <div className="flex items-center gap-2">
                    <strong>Urgency:</strong>
                    <span className={getUrgencyBadge(result.urgency)}>
                      {result.urgency}
                    </span>
                  </div>

                  <p>
                    <strong>Department:</strong> {result.department}
                  </p>

                  <p>
                    <strong>Advice:</strong> {result.advice}
                  </p>

                  {result.score !== undefined && (
                    <p>
                      <strong>Score:</strong> {result.score}
                    </p>
                  )}

                  {result.confidence !== undefined && result.confidence !== null && (
                    <p>
                      <strong>Confidence:</strong> {(result.confidence * 100).toFixed(1)}%
                    </p>
                  )}

                  {result.ml_department && (
                    <p>
                      <strong>ML Suggested Department:</strong> {result.ml_department}
                    </p>
                  )}
                </div>

                {result.factors && result.factors.length > 0 && (
                  <div className="mt-5">
                    <h3 className="font-semibold text-gray-900 mb-2">Risk Factors</h3>
                    <ul className="list-disc ml-6 space-y-1 text-gray-700">
                      {result.factors.map((factor: string, index: number) => (
                        <li key={index}>{factor}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </main>
  );
}