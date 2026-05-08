# 🏗️ Projet Data Pipeline - Avito.ma (BI & Machine Learning)

---

## 📌 Contexte du projet

Avito.ma est une plateforme de petites annonces immobilières au Maroc.  
Les données issues du scraping sont hétérogènes, non structurées et bruitées, ce qui nécessite un **pipeline industriel complet** pour les transformer en données exploitables.

---

## 🎯 Objectif du projet

Construire un pipeline de données end-to-end permettant de transformer des données brutes en un système prêt pour :

- 📊 Analyse décisionnelle (BI - Power BI)
- 🤖 Modèles de Machine Learning
- 📈 Analyse avancée des données

---

## 🏛️ Architecture globale du pipeline

```
Source (Avito.ma)
        ↓
Extract (Scraping)
        ↓
Staging (Raw Data)
        ↓
Clean Layer (Nettoyage)
        ↓
Data Warehouse
        ↓
 ┌───────────────┬────────────────┐
 │               │                │
 BI Schema     ML Schema (OBT)
```

---

## 📁 Structure du projet

```
SCRAP/
│
├── extract/               # Scraping des données
├── staging/               # Données brutes (RAW)
├── clean/                 # Nettoyage des données
├── features/              # Feature Engineering
├── warehouse/             # Data Warehouse (BI + ML)
├── data/                  # Données intermédiaires
├── logs/                  # Logs du pipeline
│
├── docker-compose.yml     # Orchestration complète
├── .env                   # Variables d’environnement

```

---

## ⚙️ Stack technique

- 🐍 Python
- 🕷️ Selenium / Requests (Scraping)
- 🐘 PostgreSQL / SQL Server (Docker)
- 🐼 Pandas / SQLAlchemy
- 🐳 Docker & Docker Compose
- 📊 Power BI
- 🤖 Machine Learning (future étape)

---

## 🔄 Étapes du pipeline

### 1️⃣ Extract (Scraping)

- Titre de l’annonce  
- Prix  
- Ville / Quartier  
- Surface (m²)  
- Chambres  
- Salles de bain  
- Étage  
- Lien annonce  

🚫 Exclusion :
- Noms
- Emails
- Téléphones

---

### 2️⃣ Staging Layer

- Stockage RAW
- Pagination
- Logs scraping
- Gestion erreurs

---

### 3️⃣ Clean Layer

- Suppression doublons
- Valeurs manquantes
- Normalisation villes
- Correction types
- Outliers

---

### 4️⃣ Feature Engineering

- 💰 Prix/m²  
- 🏠 Âge du bien  
- 📍 Encodage géographique  
- 🔢 Variables analytiques  

---

### 5️⃣ Data Warehouse

#### 📊 BI Schema (Star Schema)

- Fact_Annonce  
- Dim_Localisation  
- Dim_Caractéristiques  

➡️ Power BI

#### 🤖 ML Schema (OBT)

- Table unique
- Dataset ML prêt

---

## 🚀 Automatisation avec Docker

```
scraping → staging → clean → warehouse
```

- Docker Compose orchestration
- Logs centralisés
- Retry automatique

---

## 🧹 Staging

- Nettoyage automatique
- Réutilisation possible

---

## 📊 Validation des données

- Cohérence tables
- Intégrité relations
- Complétude données
- Validation BI & ML

---

## 🔐 Conformité & RGPD

- Aucune donnée personnelle
- Anonymisation
- Respect Avito.ma
- Logs traçabilité

---

## 📌 Résultat attendu

✔ Pipeline industriel complet  
✔ Data Warehouse BI + ML  
✔ Dataset Power BI  
✔ Dataset Machine Learning  
✔ Architecture Docker automatisée  
```
