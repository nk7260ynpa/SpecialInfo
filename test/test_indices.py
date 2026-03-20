"""股市指數 API 單元測試。"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """建立測試用 FastAPI client。"""
    return TestClient(app)


# ============================================================
# GET /api/specialinfo/indices
# ============================================================

class TestGetIndicesPrices:
    """測試 /api/specialinfo/indices 端點。"""

    @patch("src.services.indices_service.engine")
    def test_response_format(self, mock_engine, client):
        """回應應包含 dowjones 和 nasdaq 清單。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-03-01",
                "Product": "DowJones",
                "Open": 41500.00,
                "High": 42000.00,
                "Low": 41400.00,
                "Close": 41985.35,
                "Volume": 0,
            },
            {
                "Date": "2026-03-01",
                "Product": "Nasdaq",
                "Open": 17800.00,
                "High": 18100.00,
                "Low": 17750.00,
                "Close": 18012.50,
                "Volume": 0,
            },
        ]

        res = client.get("/api/specialinfo/indices?days=30")
        assert res.status_code == 200

        data = res.json()
        assert "dowjones" in data
        assert "nasdaq" in data
        assert len(data["dowjones"]) == 1
        assert len(data["nasdaq"]) == 1
        assert data["dowjones"][0]["close"] == 41985.35
        assert data["dowjones"][0]["product"] == "DowJones"
        assert data["nasdaq"][0]["close"] == 18012.50
        assert data["nasdaq"][0]["product"] == "Nasdaq"

    @patch("src.services.indices_service.engine")
    def test_empty_result(self, mock_engine, client):
        """無資料時應回傳空清單。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = []

        res = client.get("/api/specialinfo/indices?days=7")
        assert res.status_code == 200

        data = res.json()
        assert data["dowjones"] == []
        assert data["nasdaq"] == []

    @patch("src.services.indices_service.engine")
    def test_multiple_days(self, mock_engine, client):
        """多天資料應按日期排序並正確分類。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-02-28",
                "Product": "DowJones",
                "Open": 41000.00,
                "High": 41500.00,
                "Low": 40800.00,
                "Close": 41200.00,
                "Volume": 0,
            },
            {
                "Date": "2026-02-28",
                "Product": "Nasdaq",
                "Open": 17500.00,
                "High": 17800.00,
                "Low": 17400.00,
                "Close": 17700.00,
                "Volume": 0,
            },
            {
                "Date": "2026-03-01",
                "Product": "DowJones",
                "Open": 41500.00,
                "High": 42000.00,
                "Low": 41400.00,
                "Close": 41985.35,
                "Volume": 0,
            },
            {
                "Date": "2026-03-01",
                "Product": "Nasdaq",
                "Open": 17800.00,
                "High": 18100.00,
                "Low": 17750.00,
                "Close": 18012.50,
                "Volume": 0,
            },
        ]

        res = client.get("/api/specialinfo/indices?days=7")
        assert res.status_code == 200

        data = res.json()
        assert len(data["dowjones"]) == 2
        assert len(data["nasdaq"]) == 2
        # 確認按日期排序（ASC）
        assert data["dowjones"][0]["date"] == "2026-02-28"
        assert data["dowjones"][1]["date"] == "2026-03-01"

    def test_days_validation(self, client):
        """days 參數應在 1-365 範圍內。"""
        res = client.get("/api/specialinfo/indices?days=0")
        assert res.status_code == 422

        res = client.get("/api/specialinfo/indices?days=366")
        assert res.status_code == 422

    @patch("src.services.indices_service.engine")
    def test_default_days(self, mock_engine, client):
        """未指定 days 時預設為 30。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = []

        res = client.get("/api/specialinfo/indices")
        assert res.status_code == 200


# ============================================================
# GET /api/specialinfo/indices/latest
# ============================================================

class TestGetIndicesLatest:
    """測試 /api/specialinfo/indices/latest 端點。"""

    @patch("src.services.indices_service.engine")
    def test_response_format(self, mock_engine, client):
        """回應應包含 dowjones 和 nasdaq 各一筆最新資料。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-03-01",
                "Product": "DowJones",
                "Open": 41500.00,
                "High": 42000.00,
                "Low": 41400.00,
                "Close": 41985.35,
                "Volume": 0,
            },
            {
                "Date": "2026-03-01",
                "Product": "Nasdaq",
                "Open": 17800.00,
                "High": 18100.00,
                "Low": 17750.00,
                "Close": 18012.50,
                "Volume": 0,
            },
        ]

        res = client.get("/api/specialinfo/indices/latest")
        assert res.status_code == 200

        data = res.json()
        assert data["dowjones"] is not None
        assert data["nasdaq"] is not None
        assert data["dowjones"]["close"] == 41985.35
        assert data["dowjones"]["date"] == "2026-03-01"
        assert data["nasdaq"]["close"] == 18012.50
        assert data["nasdaq"]["open"] == 17800.00
        assert data["nasdaq"]["high"] == 18100.00
        assert data["nasdaq"]["low"] == 17750.00
        assert data["nasdaq"]["volume"] == 0

    @patch("src.services.indices_service.engine")
    def test_empty_result(self, mock_engine, client):
        """無資料時 dowjones 和 nasdaq 應為 null。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = []

        res = client.get("/api/specialinfo/indices/latest")
        assert res.status_code == 200

        data = res.json()
        assert data["dowjones"] is None
        assert data["nasdaq"] is None

    @patch("src.services.indices_service.engine")
    def test_partial_data(self, mock_engine, client):
        """只有一種指數資料時，另一種應為 null。"""
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__ = lambda _: mock_conn
        mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.mappings.return_value.all.return_value = [
            {
                "Date": "2026-03-01",
                "Product": "DowJones",
                "Open": 41500.00,
                "High": 42000.00,
                "Low": 41400.00,
                "Close": 41985.35,
                "Volume": 0,
            },
        ]

        res = client.get("/api/specialinfo/indices/latest")
        assert res.status_code == 200

        data = res.json()
        assert data["dowjones"] is not None
        assert data["nasdaq"] is None
