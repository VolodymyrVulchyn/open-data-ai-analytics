import os
import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = os.getenv("DB_PATH", "/app/storage/open_data.db")
TABLE_NAME = os.getenv("TABLE_NAME", "open_data_table")
REPORT_PATH = Path("/app/reports/data_quality_report.txt")


def load_data_from_db(db_path: str, table_name: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    finally:
        conn.close()

    df["period"] = pd.to_datetime(df["period"], errors="coerce")
    return df


def build_report(df: pd.DataFrame) -> str:
    missing = df.isnull().sum()
    duplicates = int(df.duplicated().sum())
    dtypes = df.dtypes.astype(str)
    numeric_desc = df.select_dtypes(include="number").describe()

    report = []
    report.append("Перевірка якості даних")
    report.append("")
    report.append(f"Розмір датасету: {df.shape}")
    report.append("")
    report.append("Кількість пропущених значень:")
    report.append(missing.to_string())
    report.append("")
    report.append(f"Кількість дублікатів: {duplicates}")
    report.append("")
    report.append("Типи даних:")
    report.append(dtypes.to_string())
    report.append("")
    report.append("Описова статистика:")
    report.append(numeric_desc.to_string())

    return "\n".join(report)


def save_report(report_text: str, report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text, encoding="utf-8")


if __name__ == "__main__":
    df = load_data_from_db(DB_PATH, TABLE_NAME)
    report_text = build_report(df)
    save_report(report_text, REPORT_PATH)
    print(report_text)
    print(f"\nЗвіт збережено: {REPORT_PATH}")