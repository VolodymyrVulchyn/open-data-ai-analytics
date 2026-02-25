import pandas as pd

# завантажуємо вже очищені дані
df = pd.read_csv("data/processed/population_change_regions.csv")

print("Перевірка якості даних")

print("Розмір датасету:", df.shape)

print("\nКількість пропущених значень:")
print(df.isnull().sum())

duplicates = df.duplicated().sum()
print("\nКількість дублікатів:", duplicates)

print("\nТипи даних:")
print(df.dtypes)

print("\nОписова статистика:")
print(df.describe())