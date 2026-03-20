"""股市指數資料查詢服務。

提供道瓊工業指數與納斯達克指數的歷史與最新資料查詢功能。
資料來源為 MySQL SPECIAL_INFO.IndicesPrice 資料表。
"""

import logging
import os
from datetime import date
from decimal import Decimal

from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)

DB_HOST = os.environ.get("DB_HOST", "tw_stock_database")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASS = os.environ.get("DB_PASSWORD", "stock")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/SPECIAL_INFO"

engine = create_engine(DB_URL, pool_pre_ping=True)


def _to_float(val) -> float:
    """將 Decimal 或其他數值安全轉為 float。"""
    if val is None:
        return 0.0
    if isinstance(val, Decimal):
        return float(val)
    return float(val)


def _serialize_row(row: dict) -> dict:
    """序列化單筆股市指數資料。"""
    return {
        "date": str(row["Date"]),
        "product": row["Product"],
        "open": _to_float(row["Open"]),
        "high": _to_float(row["High"]),
        "low": _to_float(row["Low"]),
        "close": _to_float(row["Close"]),
        "volume": _to_float(row["Volume"]),
    }


def get_indices_prices(days: int = 30) -> dict:
    """查詢最近 N 天的股市指數。

    同時回傳道瓊工業指數和納斯達克指數的歷史價格資料。

    Args:
        days: 查詢天數，預設 30 天。

    Returns:
        包含 dowjones 和 nasdaq 兩個清單的字典。
    """
    logger.info("查詢最近 %d 天股市指數", days)

    sql = text("""
        SELECT Date, Product, Open, High, Low, Close, Volume
        FROM IndicesPrice
        WHERE Date >= (
            SELECT DATE_SUB(MAX(Date), INTERVAL :days DAY)
            FROM IndicesPrice
        )
        ORDER BY Date ASC, Product ASC
    """)

    with engine.connect() as conn:
        rows = conn.execute(sql, {"days": days}).mappings().all()

    dowjones = []
    nasdaq = []
    for row in rows:
        item = _serialize_row(dict(row))
        if row["Product"] == "DowJones":
            dowjones.append(item)
        elif row["Product"] == "Nasdaq":
            nasdaq.append(item)

    return {"dowjones": dowjones, "nasdaq": nasdaq}


def get_latest_indices_price() -> dict:
    """查詢最新一筆股市指數。

    回傳道瓊工業指數和納斯達克指數各自最新一筆的收盤資料。

    Returns:
        包含 dowjones 和 nasdaq 各一筆最新資料的字典。
    """
    logger.info("查詢最新股市指數")

    sql = text("""
        SELECT Date, Product, Open, High, Low, Close, Volume
        FROM IndicesPrice
        WHERE Date = (SELECT MAX(Date) FROM IndicesPrice)
        ORDER BY Product ASC
    """)

    with engine.connect() as conn:
        rows = conn.execute(sql).mappings().all()

    result = {"dowjones": None, "nasdaq": None}
    for row in rows:
        item = _serialize_row(dict(row))
        if row["Product"] == "DowJones":
            result["dowjones"] = item
        elif row["Product"] == "Nasdaq":
            result["nasdaq"] = item

    return result
