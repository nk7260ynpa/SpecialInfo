"""黃金價格 API 單元測試。"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """建立測試用 FastAPI client。"""
    return TestClient(app)


# ============================================================
# GET /api/specialinfo/gold
# ============================================================

class TestGetGoldPrices:
    """測試 /api/specialinfo/gold 端點。"""

    @patch("src.services.gold_service.engine")
    def test_response_format(self, mock_engine, client):
        """回應應包含 gold 清單。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-03-01",
                "Product": "Gold",
                "Open": 2050.30,
                "High": 2065.50,
                "Low": 2048.00,
                "Close": 2060.10,
                "Volume": 180000,
            },
        ]

        res = client.get("/api/specialinfo/gold?days=30")
        assert res.status_code == 200

        data = res.json()
        assert "gold" in data
        assert len(data["gold"]) == 1
        assert data["gold"][0]["close"] == 2060.10
        assert data["gold"][0]["product"] == "Gold"

    @patch("src.services.gold_service.engine")
    def test_empty_result(self, mock_engine, client):
        """無資料時應回傳空清單。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = []

        res = client.get("/api/specialinfo/gold?days=7")
        assert res.status_code == 200

        data = res.json()
        assert data["gold"] == []

    @patch("src.services.gold_service.engine")
    def test_multiple_days(self, mock_engine, client):
        """多天資料應按日期排序。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-02-28",
                "Product": "Gold",
                "Open": 2040.00,
                "High": 2055.00,
                "Low": 2038.00,
                "Close": 2050.00,
                "Volume": 170000,
            },
            {
                "Date": "2026-03-01",
                "Product": "Gold",
                "Open": 2050.30,
                "High": 2065.50,
                "Low": 2048.00,
                "Close": 2060.10,
                "Volume": 180000,
            },
        ]

        res = client.get("/api/specialinfo/gold?days=7")
        assert res.status_code == 200

        data = res.json()
        assert len(data["gold"]) == 2
        assert data["gold"][0]["date"] == "2026-02-28"
        assert data["gold"][1]["date"] == "2026-03-01"

    def test_days_validation(self, client):
        """days 參數應在 1-365 範圍內。"""
        res = client.get("/api/specialinfo/gold?days=0")
        assert res.status_code == 422

        res = client.get("/api/specialinfo/gold?days=366")
        assert res.status_code == 422

    @patch("src.services.gold_service.engine")
    def test_default_days(self, mock_engine, client):
        """未指定 days 時預設為 30。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = []

        res = client.get("/api/specialinfo/gold")
        assert res.status_code == 200


# ============================================================
# GET /api/specialinfo/gold/latest
# ============================================================

class TestGetGoldLatest:
    """測試 /api/specialinfo/gold/latest 端點。"""

    @patch("src.services.gold_service.engine")
    def test_response_format(self, mock_engine, client):
        """回應應包含 gold 最新一筆資料。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-03-01",
                "Product": "Gold",
                "Open": 2050.30,
                "High": 2065.50,
                "Low": 2048.00,
                "Close": 2060.10,
                "Volume": 180000,
            },
        ]

        res = client.get("/api/specialinfo/gold/latest")
        assert res.status_code == 200

        data = res.json()
        assert data["gold"] is not None
        assert data["gold"]["close"] == 2060.10
        assert data["gold"]["date"] == "2026-03-01"
        assert data["gold"]["open"] == 2050.30
        assert data["gold"]["high"] == 2065.50
        assert data["gold"]["low"] == 2048.00
        assert data["gold"]["volume"] == 180000

    @patch("src.services.gold_service.engine")
    def test_empty_result(self, mock_engine, client):
        """無資料時 gold 應為 null。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = []

        res = client.get("/api/specialinfo/gold/latest")
        assert res.status_code == 200

        data = res.json()
        assert data["gold"] is None
