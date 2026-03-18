"""特殊資訊 Dashboard 主程式。

提供國際金融商品走勢展示的 FastAPI 後端服務，
同時掛載 React 前端靜態檔案。
"""

import logging
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.routers.oil import router as oil_router

# 設定 logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/specialinfo.log", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)

app = FastAPI(title="特殊資訊 Dashboard", version="1.0.0")

# 註冊 API 路由
app.include_router(oil_router)


@app.get("/api/health")
def health_check() -> dict:
    """健康檢查端點。"""
    return {"status": "ok", "service": "specialinfo"}


# 前端靜態檔案（React 建置產出）
_static_candidates = [
    os.environ.get("STATIC_DIR", ""),
    "/app/static",
    str(Path(__file__).resolve().parent.parent / "static"),
    str(Path(__file__).resolve().parent.parent / "frontend" / "dist"),
]
STATIC_DIR: Path | None = None
for _candidate in _static_candidates:
    if _candidate and Path(_candidate).is_dir():
        STATIC_DIR = Path(_candidate)
        break

if STATIC_DIR is not None:
    logger.info("靜態檔案目錄: %s", STATIC_DIR)
    assets_dir = STATIC_DIR / "assets"
    if assets_dir.is_dir():
        app.mount(
            "/assets", StaticFiles(directory=str(assets_dir)), name="assets"
        )

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str) -> FileResponse:
        """處理所有非 API 路徑，回傳 index.html（SPA 路由）。"""
        file_path = STATIC_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(
            STATIC_DIR / "index.html",
            headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
        )
else:
    logger.warning("找不到前端靜態檔案目錄，嘗試路徑: %s", _static_candidates)

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=5055,
        reload=False,
    )
