import pandas as pd
from bi_schema import create_bi_schema, load_bi_data
from ml_schema import create_ml_schema, load_ml_data


def main():

    print("🚀 Starting Pipeline...")

    # ======================
    # LOAD DATA
    # ======================
    df = pd.read_csv("/app/staging/clean_data.csv")
    df2 = pd.read_csv("/app/staging/features_data.csv")

    # ======================
    # BI PIPELINE
    # ======================
    print("📊 Running BI pipeline...")
    create_bi_schema()
    load_bi_data(df)

    # ======================
    # ML PIPELINE
    # ======================
    print("🤖 Running ML pipeline...")
    create_ml_schema()
    load_ml_data(df2)

    print("🎯 All pipelines finished successfully!")


# ======================
# ENTRY POINT
# ======================
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("❌ Pipeline failed:", str(e))