"""主程式與健康檢查端點測試。"""

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """建立測試用 FastAPI client。"""
    return TestClient(app)


class TestHealthCheck:
    """測試健康檢查端點。"""

    def test_health_check_returns_ok(self, client):
        """健康檢查應回傳 status ok。"""
        res = client.get("/api/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "ok"
        assert data["service"] == "specialinfo"


class TestRouteRegistered:
    """測試 API 路由是否正確註冊。"""

    def test_oil_route_exists(self, client):
        """原油價格路由應存在。"""
        routes = [r.path for r in app.routes]
        assert "/api/specialinfo/oil" in routes

    def test_oil_latest_route_exists(self, client):
        """原油最新價格路由應存在。"""
        routes = [r.path for r in app.routes]
        assert "/api/specialinfo/oil/latest" in routes

    def test_health_route_exists(self, client):
        """健康檢查路由應存在。"""
        routes = [r.path for r in app.routes]
        assert "/api/health" in routes
