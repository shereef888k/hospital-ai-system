"use client";

import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

type DepartmentStat = {
  department: string;
  count: number;
};

type AdminStats = {
  total_patients: number;
  emergency: number;
  high: number;
  medium: number;
  low: number;
  departments: DepartmentStat[];
};

export default function AdminPage() {
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/stats`);
        const data = await res.json();
        setStats(data);
      } catch (error) {
        console.error("Failed to fetch admin stats:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const urgencyData = stats
    ? [
        { name: "Emergency", value: stats.emergency },
        { name: "High", value: stats.high },
        { name: "Medium", value: stats.medium },
        { name: "Low", value: stats.low },
      ]
    : [];

  return (
    <main className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          Hospital Admin Dashboard
        </h1>

        {loading ? (
          <p className="text-gray-600">Loading dashboard...</p>
        ) : !stats ? (
          <p className="text-red-600">Failed to load dashboard data.</p>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
              <div className="bg-white rounded-xl shadow p-5">
                <p className="text-gray-500">Total Patients</p>
                <h2 className="text-3xl font-bold">{stats.total_patients}</h2>
              </div>

              <div className="bg-red-600 text-white rounded-xl shadow p-5">
                <p>Emergency</p>
                <h2 className="text-3xl font-bold">{stats.emergency}</h2>
              </div>

              <div className="bg-orange-500 text-white rounded-xl shadow p-5">
                <p>High</p>
                <h2 className="text-3xl font-bold">{stats.high}</h2>
              </div>

              <div className="bg-yellow-400 text-black rounded-xl shadow p-5">
                <p>Medium</p>
                <h2 className="text-3xl font-bold">{stats.medium}</h2>
              </div>

              <div className="bg-green-600 text-white rounded-xl shadow p-5">
                <p>Low</p>
                <h2 className="text-3xl font-bold">{stats.low}</h2>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow p-6 mb-8">
              <h2 className="text-2xl font-semibold mb-4 text-gray-900">
                Department Distribution
              </h2>

              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={stats.departments}>
                  <XAxis dataKey="department" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-white rounded-xl shadow p-6">
              <h2 className="text-2xl font-semibold mb-4 text-gray-900">
                Urgency Distribution
              </h2>

              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={urgencyData}>
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#2563eb" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </>
        )}
      </div>
    </main>
  );
}