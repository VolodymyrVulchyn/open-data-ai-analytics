import os
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DB_PATH = os.getenv("DB_PATH", "/app/storage/open_data.db")
TABLE_NAME = os.getenv("TABLE_NAME", "open_data_table")
FIGURES_DIR = Path("/app/reports/figures")


def load_data_from_db(db_path: str, table_name: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    finally:
        conn.close()

    df["period"] = pd.to_datetime(df["period"], errors="coerce")
    return df


def plot_regions_total_change(df: pd.DataFrame, output_path: Path) -> None:
    data = (
        df.groupby("region")["total_change"]
        .sum()
        .sort_values()
        .head(10)
    )

    plt.figure(figsize=(10, 6))
    data.plot(kind="barh")
    plt.title("10 регіонів з найбільшим скороченням населення")
    plt.xlabel("Сумарний total_change")
    plt.ylabel("Регіон")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_natural_vs_migration(df: pd.DataFrame, output_path: Path) -> None:
    natural_sum = df["natural_change"].sum()
    migration_sum = df["migration_change"].sum()

    plt.figure(figsize=(8, 5))
    plt.bar(["natural_change", "migration_change"], [natural_sum, migration_sum])
    plt.title("Порівняння природного та міграційного факторів")
    plt.ylabel("Сума змін")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


if __name__ == "__main__":
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data_from_db(DB_PATH, TABLE_NAME)

    fig1 = FIGURES_DIR / "regions_total_change.png"
    fig2 = FIGURES_DIR / "natural_vs_migration.png"

    plot_regions_total_change(df, fig1)
    print(f"Збережено графік: {fig1}")

    plot_natural_vs_migration(df, fig2)
    print(f"Збережено графік: {fig2}")