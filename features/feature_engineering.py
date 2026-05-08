import pandas as pd
import logging

# -----------------------------
# LOGGING SETUP
# -----------------------------
logging.basicConfig(
    filename="../logs/feature_engineering.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("🚀 Script started")

# -----------------------------
# 1. LOAD DATA
# -----------------------------
df = pd.read_csv("../staging/clean_data.csv")
logging.info(f"Data loaded: {df.shape}")

print(df.columns)
print(df["title"].unique())

# -----------------------------
# 2. CLEANING
# -----------------------------
df = df[df["surface"] > 0]
logging.info("Filtered surface > 0")

# -----------------------------
# 3. FEATURE 1: Prix par m²
# -----------------------------
df["prix_m2"] = df["price"] / df["surface"]
logging.info("Created feature: prix_m2")

# -----------------------------
# 4. FEATURE 2: is_new / is_luxury
# -----------------------------
df["is_new"] = df["title"].str.contains("neuf", case=False, na=False)

df["is_luxury"] = df["title"].str.contains(
    "penthouse|duplex|villa|marina|vue mer|haut standing|magnifique|superbe",
    case=False,
    na=False
)

logging.info("Created features: is_new, is_luxury")

# -----------------------------
# 5. FEATURE 3: âge estimé (proxy)
# -----------------------------
df["age_estime"] = 15  # default

df.loc[df["is_new"] == True, "age_estime"] = 0
df.loc[df["is_luxury"] == True, "age_estime"] = 5

logging.info("Created feature: age_estime")

# -----------------------------
# 6. FEATURE 4: TYPE DE BIEN
# -----------------------------
df["type_bien"] = "appartement"

df.loc[df["title"].str.contains("studio", case=False, na=False), "type_bien"] = "studio"
df.loc[df["title"].str.contains("duplex", case=False, na=False), "type_bien"] = "duplex"
df.loc[df["title"].str.contains("villa", case=False, na=False), "type_bien"] = "villa"
df.loc[df["title"].str.contains("penthouse", case=False, na=False), "type_bien"] = "penthouse"

logging.info("Created feature: type_bien")

# -----------------------------
# 7. FEATURE 5: PRICE CATEGORY
# -----------------------------
df["price_category"] = pd.cut(
    df["price"],
    bins=[0, 100000, 300000, 600000, 1000000, float("inf")],
    labels=["low", "medium", "high", "very_high", "luxury"]
)

logging.info("Created feature: price_category")

# -----------------------------
# 8. FEATURE 6: CITY POPULARITY
# -----------------------------
df["city_popularity"] = df["city"].map(df["city"].value_counts())

logging.info("Created feature: city_popularity")

# -----------------------------
# 9. FEATURE 7: PREMIUM CITY
# -----------------------------
premium_cities = ["marrakech", "rabat", "casablanca"]

df["is_premium_city"] = df["city"].isin(premium_cities)

logging.info("Created feature: is_premium_city")

# -----------------------------
# 10. FINAL CLEAN
# -----------------------------
df["age_estime"] = df["age_estime"].clip(lower=0)

logging.info("Final cleaning done")

# -----------------------------
# 11. SAVE RESULT (optional)
# -----------------------------
df.to_csv("../staging/features_data.csv", index=False)

logging.info("File saved: features_data.csv")

print("✅ Feature engineering completed")