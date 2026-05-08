import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# ======================
# LOAD ENV
# ======================
load_dotenv()

# ======================
# CREATE ENGINE
# ======================
engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# ======================
# EXECUTE QUERY
# ======================
def execute_query(query):
    with engine.begin() as conn:
        conn.execute(text(query))

# ======================
# CREATE ML SCHEMA
# ======================
def create_ml_schema():

    print("🚀 Creating ML schema...")

    queries = [

        # ======================
        # CREATE SCHEMA
        # ======================
        """
        CREATE SCHEMA IF NOT EXISTS ml_schema;
        """,

        # ======================
        # CREATE OBT TABLE
        # ======================
        """
        CREATE TABLE IF NOT EXISTS ml_schema.feature_store (

            id BIGINT PRIMARY KEY,

            title TEXT,
            price FLOAT,
            location TEXT,
            surface FLOAT,
            rooms INT,
            baths INT,
            link TEXT,

            location_clean TEXT,
            city TEXT,
            district TEXT,

            price_capped FLOAT,
            prix_m2 FLOAT,

            is_new BOOLEAN,
            is_luxury BOOLEAN,

            age_estime INT,

            type_bien TEXT,

            price_category TEXT,

            city_popularity INT,

            is_premium_city BOOLEAN
        );
        """
    ]

    for q in queries:
        execute_query(q)

    print("✅ ML schema created successfully!")


# ======================
# LOAD DATA INTO OBT
# ======================
def load_ml_data(df):

    print("🚀 Loading data into ML feature store...")

    df = df.copy()

    # ======================
    # SAFE ID
    # ======================
    if "id" not in df.columns:
        df["id"] = pd.factorize(df["link"])[0] + 1

    # ======================
    # SAFE COLUMN SELECT
    # ======================
    obt = df.reindex(columns=[
        'id',
        'title',
        'price',
        'location',
        'surface',
        'rooms',
        'baths',
        'link',
        'location_clean',
        'city',
        'district',
        'price_capped',
        'prix_m2',
        'is_new',
        'is_luxury',
        'age_estime',
        'type_bien',
        'price_category',
        'city_popularity',
        'is_premium_city'
    ])

    # ======================
    # LOAD TO POSTGRES
    # ======================
    obt.to_sql(
        'feature_store',
        engine,
        schema='ml_schema',
        if_exists='append',
        index=False,
        method='multi'
    )

    print("✅ Data loaded successfully into ML schema!")