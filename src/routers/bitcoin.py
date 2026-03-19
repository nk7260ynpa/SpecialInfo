"""比特幣價格 API 路由。

提供比特幣價格的歷史走勢與最新報價查詢。
"""

import logging

from fastapi import APIRouter, Query

from src.services.bitcoin_service import (
    get_bitcoin_prices,
    get_latest_bitcoin_price,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/specialinfo/bitcoin", tags=["bitcoin"])


@router.get("")
def bitcoin_prices(
    days: int = Query(30, ge=1, le=365, description="查詢天數，預設 30 天"),
) -> dict:
    """取得最近 N 天的比特幣價格走勢。"""
    logger.info("API 查詢比特幣價格: days=%d", days)
    return get_bitcoin_prices(days)


@router.get("/latest")
def bitcoin_latest() -> dict:
    """取得最新一筆比特幣價格。"""
    logger.info("API 查詢最新比特幣價格")
    return get_latest_bitcoin_price()
