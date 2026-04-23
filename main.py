import logging
import sys
from datetime import datetime

# =========================
# CONFIG LOGGING
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# =========================
# IMPORT PIPELINE MODULES
# =========================

from extract.scraper import run_scraper
from staging.staging import load_to_staging
from clean.cleaning import clean_data
from warehouse.loader import load_to_warehouse

# =========================
# PIPELINE STEPS
# =========================

def extract_step():
    logging.info("🚀 START EXTRACT (Scraping Avito)")
    data = run_scraper()
    logging.info(f"✅ Extract terminé | {len(data)} records")
    return data


def staging_step(data):
    logging.info("📦 START STAGING")
    load_to_staging(data)
    logging.info("✅ Staging terminé")


def clean_step():
    logging.info("🧹 START CLEANING")
    clean_data()
    logging.info("✅ Clean terminé")


def warehouse_step():
    logging.info("🏗️ START WAREHOUSE LOAD")
    load_to_warehouse()
    logging.info("✅ Warehouse chargé")


# =========================
# MAIN PIPELINE
# =========================

def run_pipeline():
    start_time = datetime.now()
    logging.info("====================================")
    logging.info("🔥 PIPELINE AVITO STARTED")
    logging.info("====================================")

    try:
        # 1. Extract
        data = extract_step()

        if not data:
            logging.warning("⚠️ Aucun data extrait → arrêt pipeline")
            return

        # 2. Staging
        staging_step(data)

        # 3. Clean
        clean_step()

        # 4. Warehouse
        warehouse_step()

        duration = datetime.now() - start_time
        logging.info("====================================")
        logging.info(f"🎉 PIPELINE SUCCESS | Duration: {duration}")
        logging.info("====================================")

    except Exception as e:
        logging.error("❌ PIPELINE FAILED")
        logging.error(str(e))


# =========================
# ENTRYPOINT
# =========================
if __name__ == "__main__":
    run_pipeline()