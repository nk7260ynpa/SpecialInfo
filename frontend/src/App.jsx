import { useState, useEffect } from 'react'
import OilPriceCard from './components/OilPriceCard'
import './App.css'

function App() {
  const [oilData, setOilData] = useState({ wti: [], brent: [] })
  const [latestOil, setLatestOil] = useState({ wti: null, brent: null })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)

        const [pricesRes, latestRes] = await Promise.all([
          fetch('/api/specialinfo/oil?days=30'),
          fetch('/api/specialinfo/oil/latest'),
        ])

        if (!pricesRes.ok || !latestRes.ok) {
          throw new Error('無法取得原油價格資料')
        }

        const pricesData = await pricesRes.json()
        const latestData = await latestRes.json()

        setOilData(pricesData)
        setLatestOil(latestData)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  return (
    <div className="app">
      <div className="dashboard-header">
        <h1>特殊資訊 Dashboard</h1>
        <p>國際金融商品走勢一覽</p>
      </div>

      {error && (
        <div style={{
          background: '#fef2f2',
          color: '#dc2626',
          padding: '1rem',
          borderRadius: '8px',
          marginBottom: '1.5rem',
          textAlign: 'center',
        }}>
          {error}
        </div>
      )}

      <div className="card-grid">
        <OilPriceCard
          title="WTI 原油"
          data={oilData.wti}
          latest={latestOil.wti}
          loading={loading}
          color="#ef4444"
        />
        <OilPriceCard
          title="Brent 原油"
          data={oilData.brent}
          latest={latestOil.brent}
          loading={loading}
          color="#3b82f6"
        />
      </div>
    </div>
  )
}

export default App
