import pandas as pd

print("🚀 DÉBUT DU STAGING")

# 📥 Lecture des données propres (clean_data)
df = pd.read_csv("clean_data.csv")

# 📊 Afficher la taille des données avant traitement
print("AVANT:", df.shape)

# 🧹 Nettoyage des noms de colonnes
# - suppression des espaces
# - conversion en minuscules
df.columns = df.columns.str.strip().str.lower()

# 🔢 Conversion des types de données

# Conversion de la colonne price en numérique
# (les valeurs invalides deviennent NaN)
if "price" in df.columns:
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Conversion de la colonne surface en numérique
if "surface" in df.columns:
    df["surface"] = pd.to_numeric(df["surface"], errors="coerce")

# 🚨 Suppression uniquement des lignes importantes manquantes
# On garde seulement les lignes où price ET surface existent
df = df.dropna(subset=["price", "surface"])

# 📊 Afficher la taille après nettoyage
print("APRÈS:", df.shape)

# 💾 Sauvegarde des données staging
df.to_csv("staging_data.csv", index=False)

print("✅ STAGING TERMINÉ")