"""比特幣價格資料查詢服務。

提供比特幣價格的歷史與最新資料查詢功能。
資料來源為 MySQL SPECIAL_INFO.BitcoinPrice 資料表。
"""

import logging
import os
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
    """序列化單筆比特幣價格資料。"""
    return {
        "date": str(row["Date"]),
        "product": row["Product"],
        "open": _to_float(row["Open"]),
        "high": _to_float(row["High"]),
        "low": _to_float(row["Low"]),
        "close": _to_float(row["Close"]),
        "volume": _to_float(row["Volume"]),
    }


def get_bitcoin_prices(days: int = 30) -> dict:
    """查詢最近 N 天的比特幣價格。

    Args:
        days: 查詢天數，預設 30 天。

    Returns:
        包含 bitcoin 清單的字典。
    """
    logger.info("查詢最近 %d 天比特幣價格", days)

    sql = text("""
        SELECT Date, Product, Open, High, Low, Close, Volume
        FROM BitcoinPrice
        WHERE Date >= (
            SELECT DATE_SUB(MAX(Date), INTERVAL :days DAY)
            FROM BitcoinPrice
        )
        ORDER BY Date ASC
    """)

    with engine.connect() as conn:
        rows = conn.execute(sql, {"days": days}).mappings().all()

    bitcoin = [_serialize_row(dict(row)) for row in rows]
    return {"bitcoin": bitcoin}


def get_latest_bitcoin_price() -> dict:
    """查詢最新一筆比特幣價格。

    Returns:
        包含 bitcoin 最新一筆資料的字典。
    """
    logger.info("查詢最新比特幣價格")

    sql = text("""
        SELECT Date, Product, Open, High, Low, Close, Volume
        FROM BitcoinPrice
        WHERE Date = (SELECT MAX(Date) FROM BitcoinPrice)
    """)

    with engine.connect() as conn:
        rows = conn.execute(sql).mappings().all()

    result = {"bitcoin": None}
    for row in rows:
        result["bitcoin"] = _serialize_row(dict(row))

    return result
