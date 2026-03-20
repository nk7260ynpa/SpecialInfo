import { useState, useEffect } from 'react'
import OilPriceCard from './components/OilPriceCard'
import PriceCard from './components/PriceCard'
import './App.css'

function App() {
  // 原油
  const [oilData, setOilData] = useState({ wti: [], brent: [] })
  const [latestOil, setLatestOil] = useState({ wti: null, brent: null })
  const [oilLoading, setOilLoading] = useState(true)
  const [oilError, setOilError] = useState(null)

  // 黃金
  const [goldData, setGoldData] = useState([])
  const [goldLoading, setGoldLoading] = useState(true)
  const [goldError, setGoldError] = useState(null)

  // 比特幣
  const [bitcoinData, setBitcoinData] = useState([])
  const [bitcoinLoading, setBitcoinLoading] = useState(true)
  const [bitcoinError, setBitcoinError] = useState(null)

  // 股市指數
  const [indicesData, setIndicesData] = useState({ dowjones: [], nasdaq: [] })
  const [indicesLoading, setIndicesLoading] = useState(true)
  const [indicesError, setIndicesError] = useState(null)

  // 匯率
  const [currencyData, setCurrencyData] = useState({ usdtwd: [], jpytwd: [] })
  const [currencyLoading, setCurrencyLoading] = useState(true)
  const [currencyError, setCurrencyError] = useState(null)

  // 取得原油資料
  useEffect(() => {
    const fetchOil = async () => {
      try {
        setOilLoading(true)
        setOilError(null)

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
        setOilError(err.message)
      } finally {
        setOilLoading(false)
      }
    }

    fetchOil()
  }, [])

  // 取得黃金資料
  useEffect(() => {
    const fetchGold = async () => {
      try {
        setGoldLoading(true)
        setGoldError(null)

        const res = await fetch('/api/specialinfo/gold?days=30')
        if (!res.ok) throw new Error('無法取得黃金價格資料')

        const data = await res.json()
        setGoldData(data.gold || [])
      } catch (err) {
        setGoldError(err.message)
      } finally {
        setGoldLoading(false)
      }
    }

    fetchGold()
  }, [])

  // 取得比特幣資料
  useEffect(() => {
    const fetchBitcoin = async () => {
      try {
        setBitcoinLoading(true)
        setBitcoinError(null)

        const res = await fetch('/api/specialinfo/bitcoin?days=30')
        if (!res.ok) throw new Error('無法取得比特幣價格資料')

        const data = await res.json()
        setBitcoinData(data.bitcoin || [])
      } catch (err) {
        setBitcoinError(err.message)
      } finally {
        setBitcoinLoading(false)
      }
    }

    fetchBitcoin()
  }, [])

  // 取得股市指數資料
  useEffect(() => {
    const fetchIndices = async () => {
      try {
        setIndicesLoading(true)
        setIndicesError(null)

        const res = await fetch('/api/specialinfo/indices?days=30')
        if (!res.ok) throw new Error('無法取得股市指數資料')

        const data = await res.json()
        setIndicesData({
          dowjones: data.dowjones || [],
          nasdaq: data.nasdaq || [],
        })
      } catch (err) {
        setIndicesError(err.message)
      } finally {
        setIndicesLoading(false)
      }
    }

    fetchIndices()
  }, [])

  // 取得匯率資料
  useEffect(() => {
    const fetchCurrency = async () => {
      try {
        setCurrencyLoading(true)
        setCurrencyError(null)

        const res = await fetch('/api/specialinfo/currency?days=30')
        if (!res.ok) throw new Error('無法取得匯率資料')

        const data = await res.json()
        setCurrencyData({
          usdtwd: data.usdtwd || [],
          jpytwd: data.jpytwd || [],
        })
      } catch (err) {
        setCurrencyError(err.message)
      } finally {
        setCurrencyLoading(false)
      }
    }

    fetchCurrency()
  }, [])

  const hasGlobalError = oilError && goldError && bitcoinError && indicesError && currencyError

  return (
    <div className="app">
      <div className="dashboard-header">
        <h1>特殊資訊 Dashboard</h1>
        <p>國際金融商品走勢一覽</p>
      </div>

      {hasGlobalError && (
        <div style={{
          background: '#fef2f2',
          color: '#dc2626',
          padding: '1rem',
          borderRadius: '8px',
          marginBottom: '1.5rem',
          textAlign: 'center',
        }}>
          無法連線至後端服務，請確認服務是否啟動。
        </div>
      )}

      {/* 大宗商品區 */}
      <div className="section-title">大宗商品</div>
      <div className="card-grid">
        <OilPriceCard
          title="WTI 原油"
          data={oilData.wti}
          latest={latestOil.wti}
          loading={oilLoading}
          color="#ef4444"
        />
        <OilPriceCard
          title="Brent 原油"
          data={oilData.brent}
          latest={latestOil.brent}
          loading={oilLoading}
          color="#3b82f6"
        />
        <PriceCard
          title="黃金"
          data={goldData}
          color="#FFD700"
          pricePrefix="$"
          decimalPlaces={2}
          showVolume={true}
          loading={goldLoading}
          error={goldError}
        />
        <PriceCard
          title="比特幣"
          data={bitcoinData}
          color="#F7931A"
          pricePrefix="$"
          decimalPlaces={2}
          showVolume={true}
          loading={bitcoinLoading}
          error={bitcoinError}
        />
      </div>

      {/* 股市指數區 */}
      <div className="section-title">股市指數</div>
      <div className="card-grid">
        <PriceCard
          title="道瓊工業指數"
          data={indicesData.dowjones}
          color="#1E88E5"
          pricePrefix=""
          decimalPlaces={2}
          showVolume={false}
          loading={indicesLoading}
          error={indicesError}
        />
        <PriceCard
          title="納斯達克指數"
          data={indicesData.nasdaq}
          color="#43A047"
          pricePrefix=""
          decimalPlaces={2}
          showVolume={false}
          loading={indicesLoading}
          error={indicesError}
        />
      </div>

      {/* 匯率區 */}
      <div className="section-title">匯率</div>
      <div className="card-grid">
        <PriceCard
          title="美元 / 台幣"
          data={currencyData.usdtwd}
          color="#2E7D32"
          pricePrefix="NT$"
          decimalPlaces={4}
          showVolume={false}
          loading={currencyLoading}
          error={currencyError}
        />
        <PriceCard
          title="日圓 / 台幣"
          data={currencyData.jpytwd}
          color="#7B1FA2"
          pricePrefix="NT$"
          decimalPlaces={4}
          showVolume={false}
          loading={currencyLoading}
          error={currencyError}
        />
      </div>
    </div>
  )
}

export default App
