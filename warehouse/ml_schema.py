import psycopg2
import os
from dotenv import load_dotenv

# ======================
# LOAD ENV
# ======================
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT")
}

# ======================
# CONNECTION
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
# CREATE ML SCHEMA
# ======================
def create_ml_schema():
    print("🚀 Creating ML schema...")

    queries = [

        # SCHEMA
        "CREATE SCHEMA IF NOT EXISTS ml_schema;",

        # TABLE OBT ANNONCE
        """
        CREATE TABLE IF NOT EXISTS ml_schema.obt_annonce (
            id INT PRIMARY KEY,
            title VARCHAR(255),
            price FLOAT,
            price_capped FLOAT,
            surface FLOAT,
            rooms INT,
            baths INT,
            link VARCHAR(255),

            location_clean VARCHAR(255),
            city VARCHAR(100),
            district VARCHAR(100),

            prix_m2 FLOAT,
            is_new BOOLEAN,
            is_luxury BOOLEAN,
            age_estime INT,
            type_bien VARCHAR(100),
            price_category VARCHAR(50),
            city_popularity FLOAT,
            is_premium_city BOOLEAN
        );
        """,

        # INDEXES
        "CREATE INDEX IF NOT EXISTS idx_ml_city ON ml_schema.obt_annonce(city);",
        "CREATE INDEX IF NOT EXISTS idx_ml_price ON ml_schema.obt_annonce(price);",
        "CREATE INDEX IF NOT EXISTS idx_ml_type ON ml_schema.obt_annonce(type_bien);",
        "CREATE INDEX IF NOT EXISTS idx_ml_category ON ml_schema.obt_annonce(price_category);"
    ]

    for q in queries:
        execute_query(q)

    print("✅ ML schema created successfully!")