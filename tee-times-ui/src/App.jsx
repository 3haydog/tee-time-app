import { useState } from 'react'

const API_BASE = 'https://tee-times-production.up.railway.app' // your live backend

export default function App() {
  const [date, setDate] = useState('')
  const [teeTimes, setTeeTimes] = useState([])
  const [loading, setLoading] = useState(false)

  const fetchTeeTimes = async () => {
    if (!date) return
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/tee-times?date=${date}`)
      const data = await res.json()
      setTeeTimes(data.tee_times || [])
    } catch (err) {
      console.error('Error fetching tee times:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6 font-sans">
      <h1 className="text-2xl font-bold mb-4">Golf Tee Times</h1>

      <div className="flex gap-4 mb-6">
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          className="border px-3 py-2 rounded"
        />
        <button
          onClick={fetchTeeTimes}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Get Tee Times
        </button>
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : teeTimes.length > 0 ? (
        <table className="w-full border">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2 text-left">Course</th>
              <th className="p-2 text-left">Time</th>
              <th className="p-2 text-left">Holes</th>
              <th className="p-2 text-left">Players</th>
              <th className="p-2 text-left">Price</th>
              <th className="p-2 text-left">Side</th>
            </tr>
          </thead>
          <tbody>
            {teeTimes.map((t, i) => (
              <tr key={i} className="border-t">
                <td className="p-2">{t.course}</td>
                <td className="p-2">{t.time}</td>
                <td className="p-2">{t.holes}</td>
                <td className="p-2">{t.players}</td>
                <td className="p-2">{t.price}</td>
                <td className="p-2">{t.side || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No tee times available for this date.</p>
      )}
    </div>
  )
}