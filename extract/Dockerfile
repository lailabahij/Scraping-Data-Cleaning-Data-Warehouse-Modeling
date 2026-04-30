# ======================
# SCRAPING SERVICE
# ======================
FROM python:3.10

WORKDIR /app

# copy files
COPY . .

# install dependencies (إلا عندك requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt || true

# create logs folder
RUN mkdir -p /app/logs

# run scraping script
CMD ["python", "scraper.py"]