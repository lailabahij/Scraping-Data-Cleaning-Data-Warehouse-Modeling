import time
import csv
import re
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# -----------------------
# PATH CONFIG
# -----------------------
BASE_DIR = r"C:\Users\user\Desktop\scrap"
LOG_DIR = os.path.join(BASE_DIR, "logs")
STAGING_DIR = os.path.join(BASE_DIR, "staging")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(STAGING_DIR, exist_ok=True)


# -----------------------
# LOGGING SETUP
# -----------------------
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "scraping.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("🚀 Scraping script started")


# -----------------------
# INIT DRIVER
# -----------------------
def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre?bathrooms=1&rooms=1&has_price=true&price=100000-&size=10-")

    return driver


# -----------------------
# SCROLL PAGE
# -----------------------
def scroll_page(driver, times=3):
    for i in range(times):
        driver.execute_script("window.scrollBy(0,1000)")
        time.sleep(1)
        logging.info(f"📜 Scrolled page ({i+1}/{times})")


# -----------------------
# GET CARDS
# -----------------------
def get_cards(driver):
    cards = driver.find_elements(By.CSS_SELECTOR, "a[href*='/appartements/']")
    logging.info(f"🔎 Cards found: {len(cards)}")
    return cards


# -----------------------
# EXTRACT PRICE
# -----------------------
def extract_price(card):
    try:
        price_element = card.find_element(By.CSS_SELECTOR, "span.sc-3286ebc5-2.PuYkS")
        price_text = price_element.get_attribute("textContent")
        price_text = re.sub(r"[^\d]", "", price_text)
        return int(price_text) if price_text else None
    except Exception as e:
        logging.warning(f"⚠️ Price extraction failed: {e}")
        return None


# -----------------------
# EXTRACT TITLE
# -----------------------
def extract_title(card):
    try:
        return card.find_element(By.CSS_SELECTOR, "p[title]").text
    except Exception as e:
        logging.warning(f"⚠️ Title extraction failed: {e}")
        return None


# -----------------------
# EXTRACT DETAILS
# -----------------------
def extract_details(text):
    location = surface = rooms = baths = None

    if "dans" in text:
        loc = [l for l in text.split("\n") if "dans" in l]
        location = loc[0] if loc else None

    for l in text.lower().split("\n"):
        if "m²" in l:
            surface = l
        if "chambre" in l:
            rooms = l
        if "sdb" in l or "bain" in l:
            baths = l

    return location, surface, rooms, baths


# -----------------------
# PARSE CARD
# -----------------------
def parse_card(card):
    try:
        text = card.text

        title = extract_title(card)
        price = extract_price(card)
        location, surface, rooms, baths = extract_details(text)
        link = card.get_attribute("href")

        logging.info(f"📦 Parsed card: {title}")

        return [title, price, location, surface, rooms, baths, link]

    except Exception as e:
        logging.error(f"❌ Card parsing failed: {e}")
        return None


# -----------------------
# SAVE CSV (STAGING)
# -----------------------
def save_csv(data, filename="row_data.csv"):
    filepath = os.path.join(STAGING_DIR, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "price", "location", "surface", "rooms", "baths", "link"])
        writer.writerows(data)

    logging.info(f"💾 Data saved to {filepath}")
    print(f"✅ File saved in: {filepath}")


# -----------------------
# NEXT PAGE
# -----------------------
def go_next_page(driver):
    try:
        buttons = driver.find_elements(By.CSS_SELECTOR, "a[href*='?o=']")
        buttons[-1].click()
        time.sleep(2)

        logging.info("➡️ Moved to next page")
        return True

    except Exception as e:
        logging.warning(f"⚠️ Next page failed: {e}")
        return False


# -----------------------
# MAIN SCRAPER
# -----------------------
def scrape():
    driver = init_driver()
    results = []

    for page in range(10):
        logging.info(f"📄 Scraping page {page + 1}")
        print(f"📄 Page {page + 1}")

        scroll_page(driver, 3)
        cards = get_cards(driver)

        for card in cards:
            data = parse_card(card)
            if data:
                results.append(data)

        if not go_next_page(driver):
            logging.info("No more pages - stopping")
            break

    driver.quit()

    save_csv(results)
    logging.info(" Scraping finished successfully")
    print(" DONE")


# RUN
scrape()