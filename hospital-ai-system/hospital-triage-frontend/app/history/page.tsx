"use client";

import { useEffect, useState } from "react";

type PatientRecord = {
  id: number;
  age: number;
  gender: string;
  symptoms: string;
  duration_days: number;
  urgency: string;
  department: string;
  score: number;
};

export default function HistoryPage() {
  const [patients, setPatients] = useState<PatientRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/patients/");
        const data = await res.json();fetch(`${process.env.NEXT_PUBLIC_API_URL}/history`)
        setPatients(data);
      } catch (error) {
        console.error("Failed to fetch patients:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPatients();
  }, []);

  const getUrgencyBadge = (urgency: string) => {
    if (urgency === "Emergency") {
      return "bg-red-600 text-white";
    }
    if (urgency === "High") {
      return "bg-orange-500 text-white";
    }
    if (urgency === "Medium") {
      return "bg-yellow-400 text-black";
    }
    return "bg-green-500 text-white";
  };

  return (
    <main className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-6xl mx-auto bg-white rounded-xl shadow-xl p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          Patient History
        </h1>

        {loading ? (
          <p className="text-gray-600">Loading patient records...</p>
        ) : patients.length === 0 ? (
          <p className="text-gray-600">No patient records found.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-200 text-left">
                  <th className="p-3">ID</th>
                  <th className="p-3">Age</th>
                  <th className="p-3">Gender</th>
                  <th className="p-3">Symptoms</th>
                  <th className="p-3">Duration</th>
                  <th className="p-3">Urgency</th>
                  <th className="p-3">Department</th>
                  <th className="p-3">Score</th>
                </tr>
              </thead>
              <tbody>
                {patients.map((patient) => (
                  <tr key={patient.id} className="border-b">
                    <td className="p-3">{patient.id}</td>
                    <td className="p-3">{patient.age}</td>
                    <td className="p-3 capitalize">{patient.gender}</td>
                    <td className="p-3">{patient.symptoms}</td>
                    <td className="p-3">{patient.duration_days} days</td>
                    <td className="p-3">
                      <span
                        className={`px-3 py-1 rounded-full text-sm font-semibold ${getUrgencyBadge(
                          patient.urgency
                        )}`}
                      >
                        {patient.urgency}
                      </span>
                    </td>
                    <td className="p-3">{patient.department}</td>
                    <td className="p-3">{patient.score}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </main>
  );
}