import os
import sqlite3
import pandas as pd
from pathlib import Path


# функція для завантаження і первинної обробки даних з Excel
def load_data(file_path):
    # читаємо Excel-файл, беремо саме лист "Данi.ua"
    df = pd.read_excel(file_path, sheet_name="Данi.ua")

    # прибираємо службовий рядок
    df = df[df["code"] != "коди"]

    # нормалізація типів даних
    df["period"] = pd.to_datetime(df["period"], format="%Y %m", errors="coerce")
    df["data1"] = pd.to_numeric(df["data1"], errors="coerce")
    df["data2"] = pd.to_numeric(df["data2"], errors="coerce")
    df["data3"] = pd.to_numeric(df["data3"], errors="coerce")

    # перейменовуємо колонки для зручності
    df = df.rename(columns={
        "attributes": "region",
        "data1": "total_change",
        "data2": "natural_change",
        "data3": "migration_change"
    })

    return df


# функція для імпорту CSV у SQLite
def import_csv_to_db(csv_path, db_path, table_name):
    # читаємо вже підготовлений CSV
    df = pd.read_csv(csv_path)

    # створюємо папку для БД, якщо її ще немає
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    # підключення до SQLite
    conn = sqlite3.connect(db_path)

    try:
        # створення таблиці та імпорт даних
        df.to_sql(table_name, conn, if_exists="replace", index=False)

        # перевірка кількості записів
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]

        print(f"Таблицю '{table_name}' створено в БД")
        print(f"Імпортовано записів: {row_count}")

    finally:
        conn.close()


if __name__ == "__main__":
    # шляхи
    input_path = Path("data/raw/population_change_regions.xlsx")
    output_path = Path("data/processed/population_change_regions.csv")

    # параметри БД з .env
    db_path = os.getenv("DB_PATH", "storage/open_data.db")
    table_name = os.getenv("TABLE_NAME", "open_data_table")

    # завантажуємо та очищаємо дані з Excel
    df = load_data(input_path)

    # якщо папки processed ще немає — створюємо її
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # зберігаємо очищені дані у CSV
    df.to_csv(output_path, index=False)
    print("CSV-файл успішно створено")

    # імпортуємо CSV у SQLite
    import_csv_to_db(output_path, db_path, table_name)

    print("Дані завантажені, збережені у CSV та імпортовані в базу даних")