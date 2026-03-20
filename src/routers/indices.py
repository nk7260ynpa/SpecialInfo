"""股市指數 API 路由。

提供道瓊工業指數與納斯達克指數的歷史走勢與最新報價查詢。
"""

import logging

from fastapi import APIRouter, Query

from src.services.indices_service import get_indices_prices, get_latest_indices_price

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/specialinfo/indices", tags=["indices"])


@router.get("")
def indices_prices(
    days: int = Query(30, ge=1, le=365, description="查詢天數，預設 30 天"),
) -> dict:
    """取得最近 N 天的股市指數走勢。

    同時回傳道瓊工業指數與納斯達克指數的歷史資料。
    """
    logger.info("API 查詢股市指數: days=%d", days)
    return get_indices_prices(days)


@router.get("/latest")
def indices_latest() -> dict:
    """取得最新一筆股市指數。

    回傳道瓊工業指數與納斯達克指數各自最新的收盤價格。
    """
    logger.info("API 查詢最新股市指數")
    return get_latest_indices_price()
