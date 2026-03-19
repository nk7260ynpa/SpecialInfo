"""匯率 API 路由。

提供各幣別對台幣匯率的歷史走勢與最新報價查詢。
"""

import logging

from fastapi import APIRouter, Query

from src.services.currency_service import (
    get_currency_prices,
    get_latest_currency_price,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/specialinfo/currency", tags=["currency"])


@router.get("")
def currency_prices(
    days: int = Query(30, ge=1, le=365, description="查詢天數，預設 30 天"),
) -> dict:
    """取得最近 N 天的匯率走勢。

    同時回傳 USDTWD 與 JPYTWD 的匯率資料。
    """
    logger.info("API 查詢匯率: days=%d", days)
    return get_currency_prices(days)


@router.get("/latest")
def currency_latest() -> dict:
    """取得最新一筆匯率。

    回傳 USDTWD 與 JPYTWD 各自最新的匯率。
    """
    logger.info("API 查詢最新匯率")
    return get_latest_currency_price()
