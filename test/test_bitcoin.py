"""比特幣價格 API 單元測試。"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """建立測試用 FastAPI client。"""
    return TestClient(app)


# ============================================================
# GET /api/specialinfo/bitcoin
# ============================================================

class TestGetBitcoinPrices:
    """測試 /api/specialinfo/bitcoin 端點。"""

    @patch("src.services.bitcoin_service.engine")
    def test_response_format(self, mock_engine, client):
        """回應應包含 bitcoin 清單。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-03-01",
                "Product": "Bitcoin",
                "Open": 85000.50,
                "High": 87200.00,
                "Low": 84500.00,
                "Close": 86800.25,
                "Volume": 25000000000,
            },
        ]

        res = client.get("/api/specialinfo/bitcoin?days=30")
        assert res.status_code == 200

        data = res.json()
        assert "bitcoin" in data
        assert len(data["bitcoin"]) == 1
        assert data["bitcoin"][0]["close"] == 86800.25
        assert data["bitcoin"][0]["product"] == "Bitcoin"

    @patch("src.services.bitcoin_service.engine")
    def test_empty_result(self, mock_engine, client):
        """無資料時應回傳空清單。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = []

        res = client.get("/api/specialinfo/bitcoin?days=7")
        assert res.status_code == 200

        data = res.json()
        assert data["bitcoin"] == []

    @patch("src.services.bitcoin_service.engine")
    def test_multiple_days(self, mock_engine, client):
        """多天資料應按日期排序。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-02-28",
                "Product": "Bitcoin",
                "Open": 83000.00,
                "High": 85000.00,
                "Low": 82500.00,
                "Close": 84500.00,
                "Volume": 24000000000,
            },
            {
                "Date": "2026-03-01",
                "Product": "Bitcoin",
                "Open": 85000.50,
                "High": 87200.00,
                "Low": 84500.00,
                "Close": 86800.25,
                "Volume": 25000000000,
            },
        ]

        res = client.get("/api/specialinfo/bitcoin?days=7")
        assert res.status_code == 200

        data = res.json()
        assert len(data["bitcoin"]) == 2
        assert data["bitcoin"][0]["date"] == "2026-02-28"
        assert data["bitcoin"][1]["date"] == "2026-03-01"

    def test_days_validation(self, client):
        """days 參數應在 1-365 範圍內。"""
        res = client.get("/api/specialinfo/bitcoin?days=0")
        assert res.status_code == 422

        res = client.get("/api/specialinfo/bitcoin?days=366")
        assert res.status_code == 422

    @patch("src.services.bitcoin_service.engine")
    def test_default_days(self, mock_engine, client):
        """未指定 days 時預設為 30。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = []

        res = client.get("/api/specialinfo/bitcoin")
        assert res.status_code == 200


# ============================================================
# GET /api/specialinfo/bitcoin/latest
# ============================================================

class TestGetBitcoinLatest:
    """測試 /api/specialinfo/bitcoin/latest 端點。"""

    @patch("src.services.bitcoin_service.engine")
    def test_response_format(self, mock_engine, client):
        """回應應包含 bitcoin 最新一筆資料。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-03-01",
                "Product": "Bitcoin",
                "Open": 85000.50,
                "High": 87200.00,
                "Low": 84500.00,
                "Close": 86800.25,
                "Volume": 25000000000,
            },
        ]

        res = client.get("/api/specialinfo/bitcoin/latest")
        assert res.status_code == 200

        data = res.json()
        assert data["bitcoin"] is not None
        assert data["bitcoin"]["close"] == 86800.25
        assert data["bitcoin"]["date"] == "2026-03-01"
        assert data["bitcoin"]["open"] == 85000.50
        assert data["bitcoin"]["high"] == 87200.00
        assert data["bitcoin"]["low"] == 84500.00
        assert data["bitcoin"]["volume"] == 25000000000

    @patch("src.services.bitcoin_service.engine")
    def test_empty_result(self, mock_engine, client):
        """無資料時 bitcoin 應為 null。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = []

        res = client.get("/api/specialinfo/bitcoin/latest")
        assert res.status_code == 200

        data = res.json()
        assert data["bitcoin"] is None
