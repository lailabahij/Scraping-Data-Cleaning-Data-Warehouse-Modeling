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

CMD ["python", "clean_data.py"]