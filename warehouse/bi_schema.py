import psycopg2
import os
from dotenv import load_dotenv

# ======================
# LOAD ENV FILE
# ======================
load_dotenv()

# ======================
# DB CONFIG FROM ENV
# ======================
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT")
}

# ======================
# CONNECT TO DB
# ======================
def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# ======================
# EXECUTE QUERY
# ======================
def execute_query(query):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(query)
    conn.commit()

    cur.close()
    conn.close()

# ======================
# CREATE BI SCHEMA
# ======================
def create_bi_schema():
    print("🚀 Creating BI schema...")

    queries = [
        "CREATE SCHEMA IF NOT EXISTS bi_schema;",

        """
        CREATE TABLE IF NOT EXISTS bi_schema.dim_location (
            location_id INTEGER PRIMARY KEY,
            location_clean VARCHAR(255),
            city VARCHAR(100),
            district VARCHAR(100)
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS bi_schema.dim_time (
            time_id INTEGER PRIMARY KEY,
            full_date DATE,
            year INT,
            month INT,
            day INT
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS bi_schema.dim_characteristics (
            characteristics_id INTEGER PRIMARY KEY,
            surface FLOAT,
            rooms INT,
            baths INT
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS bi_schema.fact_annonce (
            id INT PRIMARY KEY,
            title VARCHAR(255),
            price FLOAT,
            price_capped FLOAT,
            surface FLOAT,
            rooms INT,
            baths INT,
            link VARCHAR(255),

            location_id INT,
            time_id INT,
            characteristics_id INT,

            FOREIGN KEY (location_id) REFERENCES bi_schema.dim_location(location_id),
            FOREIGN KEY (time_id) REFERENCES bi_schema.dim_time(time_id),
            FOREIGN KEY (characteristics_id) REFERENCES bi_schema.dim_characteristics(characteristics_id)
        );
        """
    ]

    for q in queries:
        execute_query(q)

    print("✅ BI schema created!")