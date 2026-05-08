FROM python:3.10

WORKDIR /app

# 1. copy requirements 
COPY requirements.txt .

# 2. install dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# 3. copy 
COPY . .

# 4. logs folder
RUN mkdir -p /app/logs

CMD ["python", "scraper.py"]
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*