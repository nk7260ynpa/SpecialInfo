"""匯率資料查詢服務。

提供各幣別對台幣匯率的歷史與最新資料查詢功能。
資料來源為 MySQL SPECIAL_INFO.CurrencyPrice 資料表。
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

# 支援的匯率產品與對應 key
CURRENCY_PRODUCTS = {
    "USDTWD": "usdtwd",
    "JPYTWD": "jpytwd",
}


def _to_float(val) -> float:
    """將 Decimal 或其他數值安全轉為 float。"""
    if val is None:
        return 0.0
    if isinstance(val, Decimal):
        return float(val)
    return float(val)


def _serialize_row(row: dict) -> dict:
    """序列化單筆匯率資料。"""
    return {
        "date": str(row["Date"]),
        "product": row["Product"],
        "open": _to_float(row["Open"]),
        "high": _to_float(row["High"]),
        "low": _to_float(row["Low"]),
        "close": _to_float(row["Close"]),
        "volume": _to_float(row["Volume"]),
    }


def get_currency_prices(days: int = 30) -> dict:
    """查詢最近 N 天的匯率資料。

    同時回傳所有支援幣別對台幣的匯率歷史資料，按 Product 分組。

    Args:
        days: 查詢天數，預設 30 天。

    Returns:
        包含各幣別清單的字典，如 {"usdtwd": [...], "jpytwd": [...]}.
    """
    logger.info("查詢最近 %d 天匯率", days)

    sql = text("""
        SELECT Date, Product, Open, High, Low, Close, Volume
        FROM CurrencyPrice
        WHERE Date >= (
            SELECT DATE_SUB(MAX(Date), INTERVAL :days DAY)
            FROM CurrencyPrice
        )
        ORDER BY Date ASC, Product ASC
    """)

    with engine.connect() as conn:
        rows = conn.execute(sql, {"days": days}).mappings().all()

    result = {key: [] for key in CURRENCY_PRODUCTS.values()}
    for row in rows:
        item = _serialize_row(dict(row))
        product = row["Product"]
        key = CURRENCY_PRODUCTS.get(product)
        if key:
            result[key].append(item)

    return result


def get_latest_currency_price() -> dict:
    """查詢最新一筆匯率資料。

    回傳各幣別各自最新一筆的匯率資料。

    Returns:
        包含各幣別最新資料的字典，如 {"usdtwd": {...}, "jpytwd": {...}}.
    """
    logger.info("查詢最新匯率")

    sql = text("""
        SELECT Date, Product, Open, High, Low, Close, Volume
        FROM CurrencyPrice
        WHERE Date = (SELECT MAX(Date) FROM CurrencyPrice)
        ORDER BY Product ASC
    """)

    with engine.connect() as conn:
        rows = conn.execute(sql).mappings().all()

    result = {key: None for key in CURRENCY_PRODUCTS.values()}
    for row in rows:
        item = _serialize_row(dict(row))
        product = row["Product"]
        key = CURRENCY_PRODUCTS.get(product)
        if key:
            result[key] = item

    return result
