import pandas as pd
from pathlib import Path


# функція для завантаження і первинної обробки даних
def load_data(file_path):
    # читаємо екседб файл, беремо саме лист "Данi.ua"
    df = pd.read_excel(file_path, sheet_name="Данi.ua")

    # прибираємо рядок, де замість коду написано коди це службовий рядок з поясненнями, він нам не потрібен для аналізу
    df = df[df["code"] != "коди"]

    # нормалізація типів даних та переводимо period у формат дати (щоб можна було працювати як з часовим рядом)
    df["period"] = pd.to_datetime(df["period"], format="%Y %m", errors="coerce")

    # переводимо числові колонки у числовий тип якщо є помилки або пропуски — вони стануть nan
    df["data1"] = pd.to_numeric(df["data1"], errors="coerce")
    df["data2"] = pd.to_numeric(df["data2"], errors="coerce")
    df["data3"] = pd.to_numeric(df["data3"], errors="coerce")

    # перейменовуємо колонки для зручності роботи
    df = df.rename(columns={
        "attributes": "region",
        "data1": "total_change",
        "data2": "natural_change",
        "data3": "migration_change"
    })

    return df


if __name__ == "__main__":
    # шлях до сирого файлу
    input_path = Path("data/raw/population_change_regions.xlsx")

    # шлях куди зберігати оброблені дані
    output_path = Path("data/processed/population_change_regions.csv")

    # завантажуємо дані
    df = load_data(input_path)

    # якщо папки processed ще немає — створюємо її
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # зберігаємо у CSV, щоб надалі працювати вже з очищеними даними
    df.to_csv(output_path, index=False)

    print("Дані завантажені та збережені")