"""原油價格 API 路由。

提供 WTI 與 Brent 原油價格的歷史走勢與最新報價查詢。
"""

import logging

from fastapi import APIRouter, Query

from src.services.oil_service import get_latest_oil_price, get_oil_prices

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/specialinfo/oil", tags=["oil"])


@router.get("")
def oil_prices(
    days: int = Query(30, ge=1, le=365, description="查詢天數，預設 30 天"),
) -> dict:
    """取得最近 N 天的原油價格走勢。

    同時回傳 WTI 與 Brent 兩種原油的歷史資料。
    """
    logger.info("API 查詢原油價格: days=%d", days)
    return get_oil_prices(days)


@router.get("/latest")
def oil_latest() -> dict:
    """取得最新一筆原油價格。

    回傳 WTI 與 Brent 各自最新的收盤價格。
    """
    logger.info("API 查詢最新原油價格")
    return get_latest_oil_price()
