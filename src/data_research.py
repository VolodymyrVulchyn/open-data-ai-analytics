import pandas as pd


# завантажуємо оброблені дані (вони вже підготовлені модулем data_load)
df = pd.read_csv("data/processed/population_change_regions.csv")

print("Дослідження даних")

# шукаємо регіони з найбільшим скороченням населення та робимо суму total_change по кожному регіону
region_total = df.groupby("region")["total_change"].sum().sort_values()

print("\n5 регіонів з найбільшим скороченням (total_change):")
print(region_total.head(5))

# порівнюємо вплив природного та міграційного факторів
natural_sum = df["natural_change"].sum()
migration_sum = df["migration_change"].sum()

print("\nСума natural_change (природний фактор):", natural_sum)
print("Сума migration_change (міграційний фактор):", migration_sum)

# перевіряємо, чи змінилась динаміка після 2022 року і period переводимо у дату (інколи pandas читає як текст)
df["period"] = pd.to_datetime(df["period"], errors="coerce")

avg_before_2022 = df[df["period"] < "2022-01-01"]["total_change"].mean()
avg_after_2022 = df[df["period"] >= "2022-01-01"]["total_change"].mean()

print("\nСереднє total_change до 2022:", avg_before_2022)
print("Середнє total_change після 2022:", avg_after_2022)

if avg_after_2022 < avg_before_2022:
    print("\nПісля 2022 року середній показник став нижчий (скорочення посилилось).")
else:
    print("\nПісля 2022 року середній показник не став нижчим або змінився незначно.")

