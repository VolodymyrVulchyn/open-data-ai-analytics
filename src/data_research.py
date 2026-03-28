import os
import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = os.getenv("DB_PATH", "/app/storage/open_data.db")
TABLE_NAME = os.getenv("TABLE_NAME", "open_data_table")
REPORT_PATH = Path("/app/reports/data_research_report.txt")


def load_data_from_db(db_path: str, table_name: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    finally:
        conn.close()

    df["period"] = pd.to_datetime(df["period"], errors="coerce")
    return df


def build_report(df: pd.DataFrame) -> str:
    top_regions = (
        df.groupby("region")["total_change"]
        .sum()
        .sort_values()
        .head(5)
    )

    natural_sum = df["natural_change"].sum()
    migration_sum = df["migration_change"].sum()

    before_2022 = df[df["period"] < "2022-01-01"]["total_change"].mean()
    after_2022 = df[df["period"] >= "2022-01-01"]["total_change"].mean()

    if pd.notna(before_2022) and pd.notna(after_2022):
        if after_2022 < before_2022:
            conclusion = "Після 2022 року середній показник став нижчий (скорочення посилилось)."
        else:
            conclusion = "Після 2022 року середній показник не знизився."
    else:
        conclusion = "Недостатньо даних для порівняння періодів."

    report = []
    report.append("Дослідження даних")
    report.append("")
    report.append("5 регіонів з найбільшим скороченням (total_change):")
    report.append(top_regions.to_string())
    report.append("")
    report.append(f"Сума natural_change (природний фактор): {natural_sum}")
    report.append(f"Сума migration_change (міграційний фактор): {migration_sum}")
    report.append("")
    report.append(f"Середнє total_change до 2022: {before_2022}")
    report.append(f"Середнє total_change після 2022: {after_2022}")
    report.append("")
    report.append(conclusion)

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