"""
Retail Customer Insights
01 - Data Preparation

Loads the raw customer shopping dataset, cleans the data,
creates analytical features, and saves a clean dataset.
"""

from pathlib import Path
import pandas as pd


# =========================================================
# PROJECT PATHS
# =========================================================

# Project root = folder containing Python, Data, SQL
PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA = PROJECT_ROOT / "customer_shopping_behavior.csv"

DATA_DIR = PROJECT_ROOT / "Data"
PROCESSED_DIR = DATA_DIR / "processed"

CLEAN_DATA = PROCESSED_DIR / "customer_behavior_clean.csv"


# =========================================================
# LOAD DATA
# =========================================================

def load_data():
    """Load the raw customer shopping dataset."""

    if not RAW_DATA.exists():
        raise FileNotFoundError(
            f"\nDataset not found:\n{RAW_DATA}\n\n"
            "Make sure customer_shopping_behavior.csv "
            "is in the main project folder."
        )

    df = pd.read_csv(RAW_DATA)

    print(f"Loaded {len(df):,} records.")
    print(f"Original columns: {len(df.columns)}")

    return df


# =========================================================
# CLEAN DATA
# =========================================================

def clean_data(df):
    """Clean and standardize the dataset."""

    # -----------------------------------------------------
    # Standardize column names
    # -----------------------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    # Rename purchase amount column
    if "purchase_amount_(usd)" in df.columns:
        df = df.rename(
            columns={
                "purchase_amount_(usd)": "purchase_amount"
            }
        )

    # -----------------------------------------------------
    # Fill missing review ratings
    # -----------------------------------------------------

    if "review_rating" in df.columns:

        df["review_rating"] = (
            df.groupby("category")["review_rating"]
            .transform(
                lambda x: x.fillna(x.median())
            )
        )

    # -----------------------------------------------------
    # Create age groups
    # -----------------------------------------------------

    if "age" in df.columns:

        df["age_group"] = pd.cut(
            df["age"],
            bins=[0, 25, 35, 50, 100],
            labels=[
                "Young Adult",
                "Adult",
                "Middle-aged",
                "Senior"
            ]
        )

    # -----------------------------------------------------
    # Convert purchase frequency into days
    # -----------------------------------------------------

    if "frequency_of_purchases" in df.columns:

        frequency_mapping = {
            "Weekly": 7,
            "Fortnightly": 14,
            "Bi-Weekly": 14,
            "Monthly": 30,
            "Quarterly": 90,
            "Every 3 Months": 90,
            "Annually": 365
        }

        df["purchase_frequency_days"] = (
            df["frequency_of_purchases"]
            .map(frequency_mapping)
        )

    # -----------------------------------------------------
    # Remove redundant column
    # -----------------------------------------------------

    if "promo_code_used" in df.columns:
        df = df.drop(
            columns=["promo_code_used"]
        )

    return df


# =========================================================
# DATA QUALITY CHECK
# =========================================================

def validate_data(df):
    """Run basic data-quality checks."""

    print("\n" + "=" * 50)
    print("DATA QUALITY CHECK")
    print("=" * 50)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    # Missing values
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if missing.empty:
        print("Missing values: None")
    else:
        print("\nRemaining missing values:")
        print(missing)

    # Duplicates
    print(
        f"\nDuplicate rows: "
        f"{df.duplicated().sum():,}"
    )

    # Customers
    if "customer_id" in df.columns:
        print(
            f"Unique customers: "
            f"{df['customer_id'].nunique():,}"
        )

    # Revenue
    if "purchase_amount" in df.columns:

        print(
            f"Total revenue: "
            f"${df['purchase_amount'].sum():,.2f}"
        )

        print(
            f"Average purchase: "
            f"${df['purchase_amount'].mean():,.2f}"
        )


# =========================================================
# SAVE CLEAN DATA
# =========================================================

def save_data(df):
    """Save cleaned data to the Data/processed folder."""

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        CLEAN_DATA,
        index=False
    )

    print(
        f"\nClean dataset saved to:\n"
        f"{CLEAN_DATA}"
    )


# =========================================================
# MAIN
# =========================================================

def main():

    print("=" * 60)
    print("RETAIL CUSTOMER INSIGHTS")
    print("DATA PREPARATION")
    print("=" * 60)

    df = load_data()

    df = clean_data(df)

    validate_data(df)

    save_data(df)

    print("\nData preparation complete.")


# =========================================================
# RUN PROGRAM
# =========================================================

if __name__ == "__main__":
    main()
