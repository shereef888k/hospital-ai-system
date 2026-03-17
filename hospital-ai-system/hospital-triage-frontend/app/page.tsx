export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-red-50 flex items-center justify-center p-6">
      <div className="bg-white shadow-2xl rounded-2xl p-10 w-full max-w-2xl border border-gray-100">
        <div className="text-center mb-8">
          <div className="inline-block bg-blue-100 text-blue-700 px-4 py-1 rounded-full text-sm font-semibold mb-4">
            AI-Powered Hospital Support
          </div>

          <h1 className="text-4xl font-bold text-gray-900 mb-3">
            Hospital Triage AI
          </h1>

          <p className="text-gray-600 text-lg">
            Smart system to assess patient urgency, suggest the right department,
            and support faster decision-making.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <a
            href="/patient"
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-4 rounded-xl text-center font-semibold shadow-md transition"
          >
            Patient Form
          </a>

          <a
            href="/text-triage"
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-4 rounded-xl text-center font-semibold shadow-md transition"
          >
            AI Text Triage
          </a>

          <a
            href="/history"
            className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-4 rounded-xl text-center font-semibold shadow-md transition"
          >
            Patient History
          </a>

          <a
            href="/admin"
            className="bg-red-600 hover:bg-red-700 text-white px-6 py-4 rounded-xl text-center font-semibold shadow-md transition"
          >
            Admin Dashboard
          </a>
        </div>

        <div className="mt-10 grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
          <div className="bg-gray-50 rounded-xl p-4 border">
            <h2 className="font-semibold text-gray-900 mb-1">Fast Triage</h2>
            <p className="text-sm text-gray-600">
              Quickly assess urgency using rule-based and ML-supported logic.
            </p>
          </div>

          <div className="bg-gray-50 rounded-xl p-4 border">
            <h2 className="font-semibold text-gray-900 mb-1">Patient Records</h2>
            <p className="text-sm text-gray-600">
              Store and review patient triage history in one place.
            </p>
          </div>

          <div className="bg-gray-50 rounded-xl p-4 border">
            <h2 className="font-semibold text-gray-900 mb-1">Admin Insights</h2>
            <p className="text-sm text-gray-600">
              View dashboard analytics and hospital triage trends.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}