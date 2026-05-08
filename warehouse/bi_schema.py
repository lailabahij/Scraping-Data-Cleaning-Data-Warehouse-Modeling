import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# ======================
# LOAD ENV
# ======================
load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# ======================
# EXEC QUERY
# ======================
def execute_query(query):
    with engine.begin() as conn:
        conn.execute(text(query))

# ======================
# VALIDATION
# ======================
def validate(df):
    df = df.copy()

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["surface"] = pd.to_numeric(df["surface"], errors="coerce")

    df["rooms"] = pd.to_numeric(df["rooms"], errors="coerce")
    df["baths"] = pd.to_numeric(df["baths"], errors="coerce")

    df = df.dropna(subset=["price", "surface"])

    # rounding fix float issue
    df["surface"] = df["surface"].round(2)

    return df

# ======================
# HELPERS
# ======================
def to_int(x):
    return int(x) if pd.notnull(x) else None

def to_float(x):
    return float(x) if pd.notnull(x) else None

# ======================
# CREATE SCHEMA
# ======================
def create_bi_schema():
    print("🚀 Creating BI schema...")

    execute_query("DROP SCHEMA IF EXISTS bi_schema CASCADE;")
    execute_query("CREATE SCHEMA bi_schema;")

    execute_query("""
        CREATE TABLE IF NOT EXISTS bi_schema.dim_location (
            location_id BIGSERIAL PRIMARY KEY,
            location_clean TEXT,
            city TEXT,
            district TEXT,
            UNIQUE(location_clean, city, district)
        );
    """)

    execute_query("""
        CREATE TABLE IF NOT EXISTS bi_schema.dim_characteristics (
            characteristics_id BIGSERIAL PRIMARY KEY,
            surface FLOAT,
            rooms INT,
            baths INT,
            UNIQUE(surface, rooms, baths)
        );
    """)

    execute_query("""
        CREATE TABLE IF NOT EXISTS bi_schema.fact_annonce (
            link TEXT PRIMARY KEY,
            title TEXT,
            price FLOAT,
            price_capped FLOAT,
            surface FLOAT,
            rooms INT,
            baths INT,
            location_id BIGINT,
            characteristics_id BIGINT,
            FOREIGN KEY (location_id) REFERENCES bi_schema.dim_location(location_id),
            FOREIGN KEY (characteristics_id) REFERENCES bi_schema.dim_characteristics(characteristics_id)
        );
    """)

    print("✅ BI schema ready!")

# ======================
# INSERT LOCATION
# ======================
def insert_locations(df):
    print("📍 Loading dim_location...")

    loc = df[["location_clean", "city", "district"]].copy()

    loc["location_clean"] = loc["location_clean"].astype(str).str.strip().str.lower()
    loc["city"] = loc["city"].astype(str).str.strip().str.lower()
    loc["district"] = loc["district"].astype(str).str.strip().str.lower()

    loc = loc.dropna().drop_duplicates()

    with engine.begin() as conn:
        for _, row in loc.iterrows():
            conn.execute(text("""
                INSERT INTO bi_schema.dim_location 
                (location_clean, city, district)
                VALUES (:location_clean, :city, :district)
                ON CONFLICT DO NOTHING;
            """), row.to_dict())

# ======================
# INSERT CHARACTERISTICS
# ======================
def insert_characteristics(df):
    print("📊 Loading dim_characteristics...")

    char = df[["surface", "rooms", "baths"]].copy()

    char["surface"] = pd.to_numeric(char["surface"], errors="coerce").round(2)
    char["rooms"] = pd.to_numeric(char["rooms"], errors="coerce")
    char["baths"] = pd.to_numeric(char["baths"], errors="coerce")

    char = char.drop_duplicates()

    with engine.begin() as conn:
        for _, row in char.iterrows():
            conn.execute(text("""
                INSERT INTO bi_schema.dim_characteristics 
                (surface, rooms, baths)
                VALUES (:surface, :rooms, :baths)
                ON CONFLICT DO NOTHING;
            """), {
                "surface": to_float(row["surface"]),
                "rooms": to_int(row["rooms"]),
                "baths": to_int(row["baths"])
            })

# ======================
# INSERT FACT (FIXED + BULK SAFE)
# ======================
def insert_fact(fact_df):
    print("📥 Loading fact_annonce...")

    records = fact_df.to_dict(orient="records")

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO bi_schema.fact_annonce (
                link, title, price, price_capped,
                surface, rooms, baths,
                location_id, characteristics_id
            )
            VALUES (
                :link, :title, :price, :price_capped,
                :surface, :rooms, :baths,
                :location_id, :characteristics_id
            )
            ON CONFLICT (link) DO NOTHING;
        """), records)

# ======================
# LOAD BI DATA
# ======================
def load_bi_data(df):
    print("🚀 Loading BI data...")

    df = validate(df)
    df = df.copy()

    # insert dimensions
    insert_locations(df)
    insert_characteristics(df)

    # reload maps
    loc_map = pd.read_sql("""
        SELECT location_id, location_clean, city, district
        FROM bi_schema.dim_location
    """, engine)

    char_map = pd.read_sql("""
        SELECT characteristics_id, surface, rooms, baths
        FROM bi_schema.dim_characteristics
    """, engine)

    # normalize again for safe merge
    df["location_clean"] = df["location_clean"].astype(str).str.strip().str.lower()
    df["city"] = df["city"].astype(str).str.strip().str.lower()
    df["district"] = df["district"].astype(str).str.strip().str.lower()

    df["surface"] = df["surface"].round(2)
    char_map["surface"] = char_map["surface"].round(2)

    # merge
    df = df.merge(loc_map, on=["location_clean", "city", "district"], how="left")
    df = df.merge(char_map, on=["surface", "rooms", "baths"], how="left")

    df = df.dropna(subset=["location_id", "characteristics_id"])

    # FACT TABLE
    fact = df[[
        "link",
        "title",
        "price",
        "price_capped",
        "surface",
        "rooms",
        "baths",
        "location_id",
        "characteristics_id"
    ]].copy()

    # type safety
    fact["price"] = fact["price"].apply(to_float)
    fact["price_capped"] = fact["price_capped"].apply(to_float)
    fact["surface"] = fact["surface"].apply(to_float)
    fact["rooms"] = fact["rooms"].apply(to_int)
    fact["baths"] = fact["baths"].apply(to_int)

    fact = fact.where(pd.notnull(fact), None)

    insert_fact(fact)

    print("✅ BI load completed!")