"""原油價格 API 單元測試。"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """建立測試用 FastAPI client。"""
    return TestClient(app)


# ============================================================
# GET /api/specialinfo/oil
# ============================================================

class TestGetOilPrices:
    """測試 /api/specialinfo/oil 端點。"""

    @patch("src.services.oil_service.engine")
    def test_response_format(self, mock_engine, client):
        """回應應包含 wti 和 brent 清單。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-03-01",
                "Product": "WTI",
                "Open": 68.50,
                "High": 69.20,
                "Low": 68.10,
                "Close": 69.00,
                "Volume": 350000,
            },
            {
                "Date": "2026-03-01",
                "Product": "Brent",
                "Open": 72.30,
                "High": 73.00,
                "Low": 72.00,
                "Close": 72.80,
                "Volume": 280000,
            },
        ]

        res = client.get("/api/specialinfo/oil?days=30")
        assert res.status_code == 200

        data = res.json()
        assert "wti" in data
        assert "brent" in data
        assert len(data["wti"]) == 1
        assert len(data["brent"]) == 1
        assert data["wti"][0]["close"] == 69.00
        assert data["wti"][0]["product"] == "WTI"
        assert data["brent"][0]["close"] == 72.80
        assert data["brent"][0]["product"] == "Brent"

    @patch("src.services.oil_service.engine")
    def test_empty_result(self, mock_engine, client):
        """無資料時應回傳空清單。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = []

        res = client.get("/api/specialinfo/oil?days=7")
        assert res.status_code == 200

        data = res.json()
        assert data["wti"] == []
        assert data["brent"] == []

    @patch("src.services.oil_service.engine")
    def test_multiple_days(self, mock_engine, client):
        """多天資料應按日期排序並正確分類。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-02-28",
                "Product": "WTI",
                "Open": 67.00,
                "High": 68.00,
                "Low": 66.50,
                "Close": 67.80,
                "Volume": 320000,
            },
            {
                "Date": "2026-02-28",
                "Product": "Brent",
                "Open": 71.00,
                "High": 72.00,
                "Low": 70.80,
                "Close": 71.50,
                "Volume": 260000,
            },
            {
                "Date": "2026-03-01",
                "Product": "WTI",
                "Open": 68.50,
                "High": 69.20,
                "Low": 68.10,
                "Close": 69.00,
                "Volume": 350000,
            },
            {
                "Date": "2026-03-01",
                "Product": "Brent",
                "Open": 72.30,
                "High": 73.00,
                "Low": 72.00,
                "Close": 72.80,
                "Volume": 280000,
            },
        ]

        res = client.get("/api/specialinfo/oil?days=7")
        assert res.status_code == 200

        data = res.json()
        assert len(data["wti"]) == 2
        assert len(data["brent"]) == 2
        # 確認按日期排序（ASC）
        assert data["wti"][0]["date"] == "2026-02-28"
        assert data["wti"][1]["date"] == "2026-03-01"

    def test_days_validation(self, client):
        """days 參數應在 1-365 範圍內。"""
        res = client.get("/api/specialinfo/oil?days=0")
        assert res.status_code == 422

        res = client.get("/api/specialinfo/oil?days=366")
        assert res.status_code == 422

    @patch("src.services.oil_service.engine")
    def test_default_days(self, mock_engine, client):
        """未指定 days 時預設為 30。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = []

        res = client.get("/api/specialinfo/oil")
        assert res.status_code == 200


# ============================================================
# GET /api/specialinfo/oil/latest
# ============================================================

class TestGetOilLatest:
    """測試 /api/specialinfo/oil/latest 端點。"""

    @patch("src.services.oil_service.engine")
    def test_response_format(self, mock_engine, client):
        """回應應包含 wti 和 brent 各一筆最新資料。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-03-01",
                "Product": "Brent",
                "Open": 72.30,
                "High": 73.00,
                "Low": 72.00,
                "Close": 72.80,
                "Volume": 280000,
            },
            {
                "Date": "2026-03-01",
                "Product": "WTI",
                "Open": 68.50,
                "High": 69.20,
                "Low": 68.10,
                "Close": 69.00,
                "Volume": 350000,
            },
        ]

        res = client.get("/api/specialinfo/oil/latest")
        assert res.status_code == 200

        data = res.json()
        assert data["wti"] is not None
        assert data["brent"] is not None
        assert data["wti"]["close"] == 69.00
        assert data["wti"]["date"] == "2026-03-01"
        assert data["brent"]["close"] == 72.80
        assert data["brent"]["open"] == 72.30
        assert data["brent"]["high"] == 73.00
        assert data["brent"]["low"] == 72.00
        assert data["brent"]["volume"] == 280000

    @patch("src.services.oil_service.engine")
    def test_empty_result(self, mock_engine, client):
        """無資料時 wti 和 brent 應為 null。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = []

        res = client.get("/api/specialinfo/oil/latest")
        assert res.status_code == 200

        data = res.json()
        assert data["wti"] is None
        assert data["brent"] is None

    @patch("src.services.oil_service.engine")
    def test_partial_data(self, mock_engine, client):
        """只有一種原油資料時，另一種應為 null。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-03-01",
                "Product": "WTI",
                "Open": 68.50,
                "High": 69.20,
                "Low": 68.10,
                "Close": 69.00,
                "Volume": 350000,
            },
        ]

        res = client.get("/api/specialinfo/oil/latest")
        assert res.status_code == 200

        data = res.json()
        assert data["wti"] is not None
        assert data["brent"] is None
