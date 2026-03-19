"""黃金價格 API 路由。

提供黃金價格的歷史走勢與最新報價查詢。
"""

import logging

from fastapi import APIRouter, Query

from src.services.gold_service import get_gold_prices, get_latest_gold_price

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/specialinfo/gold", tags=["gold"])


@router.get("")
def gold_prices(
    days: int = Query(30, ge=1, le=365, description="查詢天數，預設 30 天"),
) -> dict:
    """取得最近 N 天的黃金價格走勢。"""
    logger.info("API 查詢黃金價格: days=%d", days)
    return get_gold_prices(days)


@router.get("/latest")
def gold_latest() -> dict:
    """取得最新一筆黃金價格。"""
    logger.info("API 查詢最新黃金價格")
    return get_latest_gold_price()
