import os
import pandas as pd
import matplotlib.pyplot as plt


# шлях до вже оброблених даних
DATA_PATH = "data/processed/population_change_regions.csv"

# папка для збереження графіків
FIG_DIR = "reports/figures"

os.makedirs(FIG_DIR, exist_ok=True)
df = pd.read_csv(DATA_PATH)

print("Візуалізація даних")


# топ-10 регіонів за найбільшим скороченням населення (total_change)
region_total = df.groupby("region")["total_change"].sum().sort_values()

top20 = region_total.head(20)

plt.figure()
top20.plot(kind="bar")
plt.title("Топ-20 регіонів з найбільшим скороченням населення")
plt.xlabel("Регіон")
plt.ylabel("Сума total_change")
plt.tight_layout()

out1 = os.path.join(FIG_DIR, "regions_total_change.png")
plt.savefig(out1, dpi=200)
plt.close()

print("Збережено графік:", out1)

# порівняння природного та міграційного факторів (сума по всіх записах)
natural_sum = df["natural_change"].sum()
migration_sum = df["migration_change"].sum()

plt.figure()
plt.bar(["natural_change", "migration_change"], [natural_sum, migration_sum])
plt.title("Порівняння природного та міграційного факторів")
plt.xlabel("Показник")
plt.ylabel("Сума значень")
plt.tight_layout()

out2 = os.path.join(FIG_DIR, "natural_vs_migration.png")
plt.savefig(out2, dpi=200)
plt.close()

print("Збережено графік:", out2)