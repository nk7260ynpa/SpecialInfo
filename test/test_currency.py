"""匯率 API 單元測試。"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """建立測試用 FastAPI client。"""
    return TestClient(app)


# ============================================================
# GET /api/specialinfo/currency
# ============================================================

class TestGetCurrencyPrices:
    """測試 /api/specialinfo/currency 端點。"""

    @patch("src.services.currency_service.engine")
    def test_response_format(self, mock_engine, client):
        """回應應包含 usdtwd 和 jpytwd 清單。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-03-01",
                "Product": "JPYTWD",
                "Open": 0.2135,
                "High": 0.2142,
                "Low": 0.2130,
                "Close": 0.2140,
                "Volume": 0,
            },
            {
                "Date": "2026-03-01",
                "Product": "USDTWD",
                "Open": 32.5100,
                "High": 32.6200,
                "Low": 32.4800,
                "Close": 32.5500,
                "Volume": 0,
            },
        ]

        res = client.get("/api/specialinfo/currency?days=30")
        assert res.status_code == 200

        data = res.json()
        assert "usdtwd" in data
        assert "jpytwd" in data
        assert len(data["usdtwd"]) == 1
        assert len(data["jpytwd"]) == 1
        assert data["usdtwd"][0]["close"] == 32.55
        assert data["usdtwd"][0]["product"] == "USDTWD"
        assert data["jpytwd"][0]["close"] == 0.214
        assert data["jpytwd"][0]["product"] == "JPYTWD"

    @patch("src.services.currency_service.engine")
    def test_empty_result(self, mock_engine, client):
        """無資料時應回傳空清單。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = []

        res = client.get("/api/specialinfo/currency?days=7")
        assert res.status_code == 200

        data = res.json()
        assert data["usdtwd"] == []
        assert data["jpytwd"] == []

    @patch("src.services.currency_service.engine")
    def test_multiple_days(self, mock_engine, client):
        """多天資料應按日期排序並正確分類。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-02-28",
                "Product": "USDTWD",
                "Open": 32.4000,
                "High": 32.5000,
                "Low": 32.3500,
                "Close": 32.4500,
                "Volume": 0,
            },
            {
                "Date": "2026-02-28",
                "Product": "JPYTWD",
                "Open": 0.2120,
                "High": 0.2130,
                "Low": 0.2115,
                "Close": 0.2125,
                "Volume": 0,
            },
            {
                "Date": "2026-03-01",
                "Product": "USDTWD",
                "Open": 32.5100,
                "High": 32.6200,
                "Low": 32.4800,
                "Close": 32.5500,
                "Volume": 0,
            },
            {
                "Date": "2026-03-01",
                "Product": "JPYTWD",
                "Open": 0.2135,
                "High": 0.2142,
                "Low": 0.2130,
                "Close": 0.2140,
                "Volume": 0,
            },
        ]

        res = client.get("/api/specialinfo/currency?days=7")
        assert res.status_code == 200

        data = res.json()
        assert len(data["usdtwd"]) == 2
        assert len(data["jpytwd"]) == 2
        assert data["usdtwd"][0]["date"] == "2026-02-28"
        assert data["usdtwd"][1]["date"] == "2026-03-01"

    def test_days_validation(self, client):
        """days 參數應在 1-365 範圍內。"""
        res = client.get("/api/specialinfo/currency?days=0")
        assert res.status_code == 422

        res = client.get("/api/specialinfo/currency?days=366")
        assert res.status_code == 422

    @patch("src.services.currency_service.engine")
    def test_default_days(self, mock_engine, client):
        """未指定 days 時預設為 30。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = []

        res = client.get("/api/specialinfo/currency")
        assert res.status_code == 200

    @patch("src.services.currency_service.engine")
    def test_unknown_product_ignored(self, mock_engine, client):
        """未知的 Product 應被忽略。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-03-01",
                "Product": "EURTWD",
                "Open": 35.0000,
                "High": 35.1000,
                "Low": 34.9000,
                "Close": 35.0500,
                "Volume": 0,
            },
        ]

        res = client.get("/api/specialinfo/currency?days=7")
        assert res.status_code == 200

        data = res.json()
        assert data["usdtwd"] == []
        assert data["jpytwd"] == []


# ============================================================
# GET /api/specialinfo/currency/latest
# ============================================================

class TestGetCurrencyLatest:
    """測試 /api/specialinfo/currency/latest 端點。"""

    @patch("src.services.currency_service.engine")
    def test_response_format(self, mock_engine, client):
        """回應應包含 usdtwd 和 jpytwd 各一筆最新資料。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-03-01",
                "Product": "JPYTWD",
                "Open": 0.2135,
                "High": 0.2142,
                "Low": 0.2130,
                "Close": 0.2140,
                "Volume": 0,
            },
            {
                "Date": "2026-03-01",
                "Product": "USDTWD",
                "Open": 32.5100,
                "High": 32.6200,
                "Low": 32.4800,
                "Close": 32.5500,
                "Volume": 0,
            },
        ]

        res = client.get("/api/specialinfo/currency/latest")
        assert res.status_code == 200

        data = res.json()
        assert data["usdtwd"] is not None
        assert data["jpytwd"] is not None
        assert data["usdtwd"]["close"] == 32.55
        assert data["usdtwd"]["date"] == "2026-03-01"
        assert data["jpytwd"]["close"] == 0.214
        assert data["jpytwd"]["date"] == "2026-03-01"

    @patch("src.services.currency_service.engine")
    def test_empty_result(self, mock_engine, client):
        """無資料時 usdtwd 和 jpytwd 應為 null。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = []

        res = client.get("/api/specialinfo/currency/latest")
        assert res.status_code == 200

        data = res.json()
        assert data["usdtwd"] is None
        assert data["jpytwd"] is None

    @patch("src.services.currency_service.engine")
    def test_partial_data(self, mock_engine, client):
        """只有一種匯率資料時，另一種應為 null。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-03-01",
                "Product": "USDTWD",
                "Open": 32.5100,
                "High": 32.6200,
                "Low": 32.4800,
                "Close": 32.5500,
                "Volume": 0,
            },
        ]

        res = client.get("/api/specialinfo/currency/latest")
        assert res.status_code == 200

        data = res.json()
        assert data["usdtwd"] is not None
        assert data["jpytwd"] is None
