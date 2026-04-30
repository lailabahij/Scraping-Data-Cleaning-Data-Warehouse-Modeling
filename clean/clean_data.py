import pandas as pd
import matplotlib.pyplot as plt
import logging
import os,re

# -----------------------
# SETUP LOGS
# -----------------------
os.makedirs("../logs", exist_ok=True)

logging.basicConfig(
    filename="../logs/eda.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("🚀 Script started")

# -----------------------
# LOAD DATA
# -----------------------
df = pd.read_csv("../staging/row_data.csv")
logging.info(f"Data loaded: {df.shape}")

print(df.head())
print(df.info())
print(df.describe(include="all"))
print(df["rooms"].head())
print(df["baths"].head())
print(df["surface"].head())

# DATA TYPES CLEANING
# -----------------------
# Convert price to numeric (int64)
df["price"] = (
    df["price"]
    .astype(str)
    .str.replace(r"[^\d]", "", regex=True)
)
df["price"] = pd.to_numeric(df["price"], errors="coerce").astype("Int64")

# Convert surface to numeric but keep as string in raw then clean
df["surface"] = (
    df["surface"]
    .astype("string")  # better than astype(str)
    .str.replace(r"[^\d.]", "", regex=True)
)

df["surface"] = pd.to_numeric(df["surface"], errors="coerce")

# Convert rooms & baths to numeric (if exist numbers inside strings)
for col in ["rooms", "baths"]:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(r"[^\d]", "", regex=True)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

# Convert text columns to string type
text_cols = ["title", "location", "link"]
for col in text_cols:
    if col in df.columns:
        df[col] = df[col].astype("string")

# -----------------------
# DUPLICATES
# -----------------------
duplicates = df.duplicated().sum()
logging.info(f"Duplicates found: {duplicates}")

df.drop_duplicates(inplace=True)
logging.info(f"After removing duplicates: {df.shape}")

df["title"] = df["title"].str.replace(
    r"^(À.*?|Vente|Location)\s*",
    "",
    regex=True,
    flags=re.IGNORECASE
)
logging.info("Prefixes (À VENDRE / VENTE / LOCATION) removed from title")
# Detect fake missing values
df.replace(["", " ", "N/A", "None"], pd.NA, inplace=True)

missing_report = pd.DataFrame({
    "missing": df.isnull().sum(),
    "percent": (df.isnull().sum() / len(df)) * 100
})

print(missing_report)
logging.info("missing_report")
print(df.columns)
#Standardisation des villes et quartiers
print(df["location"].unique())
# Clean location
df["location_clean"] = df["location"].str.replace(
    r"appartements dans",
    "",
    case=False,
    regex=True
).str.strip()

logging.info("Location prefix removed successfully")

# Split
df[["city", "district"]] = df["location_clean"].str.split(",", expand=True)
logging.info("Location split into city and district")

# Clean text
df["city"] = df["city"].str.lower().str.strip()
df["district"] = df["district"].str.lower().str.strip()

logging.info("City and district normalized (lower + strip)")




# Standardize cities
city_mapping = {
    "casa": "casablanca",
    "tanger": "tangier"
}

df["city"] = df["city"].replace(city_mapping)

logging.info("City names standardized using mapping")

# Validation logs
logging.info(f"Unique cities: {df['city'].unique()}")
logging.info(f"Unique districts sample: {df['district'].dropna().unique()[:10]}")

# Print for debugging
print(df["city"].unique())
print(df["district"].unique())

import matplotlib.pyplot as plt

plt.boxplot(df["price"])
plt.title("Price Outliers Check")
plt.show()
# -----------------------
# OUTLIERS DETECTION
# -----------------------
Q1 = df["price"].quantile(0.25)
Q3 = df["price"].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = df[(df["price"] < lower) | (df["price"] > upper)]

outliers_count = len(outliers)
total_rows = len(df)
ratio = outliers_count / total_rows * 100

print("Outliers count:", outliers_count)
print("Total rows:", total_rows)
print("Ratio %:", ratio)

# ✅ LOGGING
logging.info(f"Price Q1: {Q1}, Q3: {Q3}, IQR: {IQR}")
logging.info(f"Outliers bounds → lower: {lower}, upper: {upper}")
logging.info(f"Outliers count: {outliers_count}")
logging.info(f"Outliers ratio: {ratio:.2f}%")
df["price_capped"] = df["price"].clip(lower, upper)
logging.info("Capping applied on price column")

logging.info(f"Original max price: {df['price'].max()}")
logging.info(f"Capped max price: {df['price_capped'].max()}")

logging.info(f"Original min price: {df['price'].min()}")
logging.info(f"Capped min price: {df['price_capped'].min()}")

#new boxplot# 🔥 Distribution check (IMPORTANT)
logging.info(f"Price mean (before): {df['price'].mean()}")
logging.info(f"Price median (before): {df['price'].median()}")

logging.info(f"Price mean (after): {df['price_capped'].mean()}")
logging.info(f"Price median (after): {df['price_capped'].median()}")
import matplotlib.pyplot as plt

plt.boxplot(df["price_capped"].dropna())
plt.title("Price After Capping")
plt.show()
#save data clean
df.to_csv("../staging/clean_data.csv", index=False, encoding="utf-8")
logging.info("Clean data saved successfully to clean_data.csv")
