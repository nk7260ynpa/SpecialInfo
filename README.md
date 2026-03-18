# SpecialInfo

特殊資訊 Dashboard — 展示國際金融商品走勢（原油價格等）。

## 功能

- WTI 原油價格走勢與最新報價
- Brent 原油價格走勢與最新報價
- 收盤價折線圖（近 30 天）
- 卡片式佈局，可擴展更多金融商品

## 專案架構

```
SpecialInfo/
├── docker/
│   ├── build.sh              # 建立 Docker image
│   └── Dockerfile            # Multi-stage build (Node + Python)
├── run.sh                    # 啟動 Docker 容器
├── pyproject.toml            # Python 套件定義
├── requirements.txt          # 釘版依賴
├── src/
│   ├── __init__.py
│   ├── main.py               # FastAPI 主程式
│   ├── routers/
│   │   ├── __init__.py
│   │   └── oil.py            # 原油價格 API 路由
│   └── services/
│       ├── __init__.py
│       └── oil_service.py    # 原油價格資料查詢服務
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── App.jsx           # 主 Dashboard 頁面
│       ├── App.css
│       ├── main.jsx
│       ├── index.css
│       └── components/
│           └── OilPriceCard.jsx  # 原油價格卡片元件
├── test/
│   ├── __init__.py
│   ├── test_main.py          # 主程式測試
│   └── test_oil.py           # 原油 API 測試
├── logs/
│   └── .gitkeep
├── .gitignore
├── CLAUDE.md
└── README.md
```

## 安裝與使用

### Docker 部署

```bash
# 建置 Docker image
bash docker/build.sh

# 啟動服務
bash run.sh
```

服務啟動後可透過 `http://localhost:5055` 存取。

### 本機開發

```bash
# 安裝 Python 依賴
pip install -r requirements.txt

# 啟動後端
python src/main.py

# 安裝前端依賴並啟動開發伺服器
cd frontend
npm install
npm run dev
```

### 執行測試

```bash
# Docker 內執行
docker run --rm nk7260ynpa/tw_stock_specialinfo:latest pytest test/ -v

# 本機執行
pytest test/ -v
```

## API 說明

| Method | Path | 說明 |
|--------|------|------|
| GET | `/api/health` | 健康檢查 |
| GET | `/api/specialinfo/oil?days=30` | 查詢最近 N 天原油價格（WTI + Brent），days 範圍 1-365 |
| GET | `/api/specialinfo/oil/latest` | 查詢最新一筆原油價格（WTI + Brent） |

### 回應範例

#### GET /api/specialinfo/oil?days=7

```json
{
  "wti": [
    {
      "date": "2026-03-01",
      "product": "WTI",
      "open": 68.50,
      "high": 69.20,
      "low": 68.10,
      "close": 69.00,
      "volume": 350000
    }
  ],
  "brent": [
    {
      "date": "2026-03-01",
      "product": "Brent",
      "open": 72.30,
      "high": 73.00,
      "low": 72.00,
      "close": 72.80,
      "volume": 280000
    }
  ]
}
```

#### GET /api/specialinfo/oil/latest

```json
{
  "wti": {
    "date": "2026-03-01",
    "product": "WTI",
    "open": 68.50,
    "high": 69.20,
    "low": 68.10,
    "close": 69.00,
    "volume": 350000
  },
  "brent": {
    "date": "2026-03-01",
    "product": "Brent",
    "open": 72.30,
    "high": 73.00,
    "low": 72.00,
    "close": 72.80,
    "volume": 280000
  }
}
```

## 資料庫

- **Database**: `SPECIAL_INFO`
- **Table**: `OilPrice`
  - `Date` — 日期
  - `Product` — 產品名稱（WTI / Brent）
  - `Open` — 開盤價
  - `High` — 最高價
  - `Low` — 最低價
  - `Close` — 收盤價
  - `Volume` — 成交量

## 環境變數

| 變數 | 預設值 | 說明 |
|------|--------|------|
| `DB_HOST` | `tw_stock_database` | MySQL 主機 |
| `DB_USER` | `root` | MySQL 使用者 |
| `DB_PASSWORD` | `stock` | MySQL 密碼 |
| `DB_PORT` | `3306` | MySQL 端口 |

## 技術堆疊

- **後端**: FastAPI + Uvicorn + SQLAlchemy + PyMySQL
- **前端**: React 18 + Vite + Recharts
- **部署**: Docker (multi-stage build)
- **網路**: Docker `db_network`
- **Port**: 5055
