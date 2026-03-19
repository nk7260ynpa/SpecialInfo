import { useMemo } from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

const styles = {
  card: {
    background: '#ffffff',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06)',
    padding: '1.5rem',
    transition: 'box-shadow 0.2s',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '1rem',
  },
  title: {
    fontSize: '1.1rem',
    fontWeight: 600,
    color: '#1e293b',
  },
  priceContainer: {
    textAlign: 'right',
  },
  price: {
    fontSize: '1.5rem',
    fontWeight: 700,
  },
  change: {
    fontSize: '0.85rem',
    fontWeight: 500,
    marginTop: '2px',
  },
  info: {
    display: 'flex',
    gap: '1rem',
    marginBottom: '1rem',
    fontSize: '0.8rem',
    color: '#64748b',
  },
  infoItem: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  infoLabel: {
    fontSize: '0.7rem',
    color: '#94a3b8',
  },
  infoValue: {
    fontWeight: 600,
    color: '#1e293b',
  },
  loading: {
    textAlign: 'center',
    color: '#94a3b8',
    padding: '3rem 0',
  },
  noData: {
    textAlign: 'center',
    color: '#94a3b8',
    padding: '2rem 0',
    fontSize: '0.9rem',
  },
  chartContainer: {
    marginTop: '0.5rem',
  },
  error: {
    textAlign: 'center',
    color: '#dc2626',
    padding: '2rem 0',
    fontSize: '0.9rem',
  },
}

function PriceCard({
  title,
  data,
  color,
  pricePrefix = '$',
  priceSuffix = '',
  decimalPlaces = 2,
  showVolume = true,
  loading = false,
  error = null,
}) {
  // 計算最新價與漲跌幅
  const latest = useMemo(() => {
    if (!data || data.length === 0) return null
    return data[data.length - 1]
  }, [data])

  const changeInfo = useMemo(() => {
    if (!data || data.length < 2) return null

    const current = data[data.length - 1]
    const previous = data[data.length - 2]

    if (!current || !previous || previous.close === 0) return null

    const change = current.close - previous.close
    const changePct = (change / previous.close) * 100

    return {
      change: change.toFixed(decimalPlaces),
      changePct: changePct.toFixed(2),
      isUp: change >= 0,
    }
  }, [data, decimalPlaces])

  // 格式化圖表資料
  const chartData = useMemo(() => {
    if (!data) return []
    return data.map((item) => ({
      date: item.date.slice(5), // MM-DD
      close: item.close,
      fullDate: item.date,
    }))
  }, [data])

  if (loading) {
    return (
      <div style={styles.card}>
        <div style={styles.title}>{title}</div>
        <div style={styles.loading}>載入中...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div style={styles.card}>
        <div style={styles.title}>{title}</div>
        <div style={styles.error}>{error}</div>
      </div>
    )
  }

  const displayPrice = latest ? latest.close : null
  const displayDate = latest ? latest.date : null

  const formatPrice = (val) =>
    `${pricePrefix}${val.toFixed(decimalPlaces)}${priceSuffix}`

  return (
    <div style={styles.card}>
      <div style={styles.header}>
        <div>
          <div style={styles.title}>{title}</div>
          {displayDate && (
            <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '2px' }}>
              {displayDate}
            </div>
          )}
        </div>
        <div style={styles.priceContainer}>
          {displayPrice != null ? (
            <>
              <div style={{ ...styles.price, color }}>
                {formatPrice(displayPrice)}
              </div>
              {changeInfo && (
                <div
                  style={{
                    ...styles.change,
                    color: changeInfo.isUp ? '#16a34a' : '#dc2626',
                  }}
                >
                  {changeInfo.isUp ? '+' : ''}{changeInfo.change}
                  {' '}({changeInfo.isUp ? '+' : ''}{changeInfo.changePct}%)
                </div>
              )}
            </>
          ) : (
            <div style={{ ...styles.price, color: '#94a3b8' }}>--</div>
          )}
        </div>
      </div>

      {latest && (
        <div style={styles.info}>
          <div style={styles.infoItem}>
            <span style={styles.infoLabel}>開盤</span>
            <span style={styles.infoValue}>
              {formatPrice(latest.open)}
            </span>
          </div>
          <div style={styles.infoItem}>
            <span style={styles.infoLabel}>最高</span>
            <span style={styles.infoValue}>
              {formatPrice(latest.high)}
            </span>
          </div>
          <div style={styles.infoItem}>
            <span style={styles.infoLabel}>最低</span>
            <span style={styles.infoValue}>
              {formatPrice(latest.low)}
            </span>
          </div>
          {showVolume && (
            <div style={styles.infoItem}>
              <span style={styles.infoLabel}>成交量</span>
              <span style={styles.infoValue}>{latest.volume.toLocaleString()}</span>
            </div>
          )}
        </div>
      )}

      <div style={styles.chartContainer}>
        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis
                dataKey="date"
                tick={{ fontSize: 11, fill: '#94a3b8' }}
                tickLine={false}
                axisLine={{ stroke: '#e2e8f0' }}
              />
              <YAxis
                domain={['auto', 'auto']}
                tick={{ fontSize: 11, fill: '#94a3b8' }}
                tickLine={false}
                axisLine={{ stroke: '#e2e8f0' }}
                width={65}
                tickFormatter={(val) => `${pricePrefix}${val}`}
              />
              <Tooltip
                contentStyle={{
                  borderRadius: '8px',
                  border: 'none',
                  boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                  fontSize: '0.85rem',
                }}
                formatter={(value) => [formatPrice(value), '收盤價']}
                labelFormatter={(label, payload) => {
                  if (payload && payload[0]) {
                    return payload[0].payload.fullDate
                  }
                  return label
                }}
              />
              <Line
                type="monotone"
                dataKey="close"
                stroke={color}
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4, fill: color }}
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div style={styles.noData}>暫無走勢資料</div>
        )}
      </div>
    </div>
  )
}

export default PriceCard
