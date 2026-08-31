"""
Retail Customer Insights
02 - Customer & Revenue Analysis

Purpose:
    Transform the cleaned customer dataset into business-focused
    analytical outputs for Power BI.

Outputs:
    - Executive KPIs
    - Customer segments
    - Customer value
    - Age group performance
    - Category performance
    - Subscription performance
    - Discount performance
    - Product performance
    - Payment method analysis
    - Shipping analysis
    - Seasonal analysis
"""

from pathlib import Path

import pandas as pd


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "Data"
    / "processed"
    / "customer_behavior_clean.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "Data"
    / "analysis"
)


# =========================================================
# LOAD DATA
# =========================================================

def load_data():
    """Load the cleaned dataset."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"\nClean dataset not found:\n{INPUT_FILE}\n\n"
            "Run prepare_data.py first."
        )

    df = pd.read_csv(INPUT_FILE)

    print(f"Loaded {len(df):,} records.")

    return df


# =========================================================
# EXECUTIVE KPIs
# =========================================================

def create_executive_kpis(df):

    total_revenue = df["purchase_amount"].sum()

    total_customers = (
        df["customer_id"].nunique()
    )

    average_purchase = (
        df["purchase_amount"].mean()
    )

    average_rating = (
        df["review_rating"].mean()
    )

    subscription_rate = (
        df["subscription_status"]
        .eq("Yes")
        .mean()
        * 100
    )

    discount_rate = (
        df["discount_applied"]
        .eq("Yes")
        .mean()
        * 100
    )

    return pd.DataFrame({
        "metric": [
            "Total Revenue",
            "Total Customers",
            "Average Purchase",
            "Average Rating",
            "Subscription Rate",
            "Discount Usage Rate"
        ],
        "value": [
            total_revenue,
            total_customers,
            average_purchase,
            average_rating,
            subscription_rate,
            discount_rate
        ]
    })


# =========================================================
# CUSTOMER VALUE
# =========================================================

def create_customer_value(df):

    result = (
        df.groupby("customer_id")
        .agg(
            age=("age", "first"),
            gender=("gender", "first"),
            location=("location", "first"),
            total_revenue=(
                "purchase_amount",
                "sum"
            ),
            average_purchase=(
                "purchase_amount",
                "mean"
            ),
            previous_purchases=(
                "previous_purchases",
                "first"
            ),
            subscription_status=(
                "subscription_status",
                "first"
            ),
            discount_applied=(
                "discount_applied",
                "first"
            ),
            average_rating=(
                "review_rating",
                "mean"
            )
        )
        .reset_index()
    )

    # Divide customers into three equal-sized value groups
    result["customer_value_segment"] = pd.qcut(
        result["total_revenue"],
        q=3,
        labels=[
            "Low Value",
            "Medium Value",
            "High Value"
        ]
    )

    return result.sort_values(
        "total_revenue",
        ascending=False
    )


# =========================================================
# CUSTOMER LOYALTY
# =========================================================

def create_customer_segments(df):

    result = df.copy()

    result["customer_segment"] = pd.cut(
        result["previous_purchases"],
        bins=[
            -1,
            1,
            10,
            float("inf")
        ],
        labels=[
            "New",
            "Returning",
            "Loyal"
        ]
    )

    return (
        result.groupby(
            "customer_segment",
            observed=True
        )
        .agg(
            customers=(
                "customer_id",
                "nunique"
            ),
            revenue=(
                "purchase_amount",
                "sum"
            ),
            average_purchase=(
                "purchase_amount",
                "mean"
            ),
            average_previous_purchases=(
                "previous_purchases",
                "mean"
            )
        )
        .reset_index()
    )


# =========================================================
# AGE GROUP ANALYSIS
# =========================================================

def create_age_analysis(df):

    return (
        df.groupby(
            "age_group",
            observed=True
        )
        .agg(
            customers=(
                "customer_id",
                "nunique"
            ),
            revenue=(
                "purchase_amount",
                "sum"
            ),
            average_purchase=(
                "purchase_amount",
                "mean"
            ),
            average_rating=(
                "review_rating",
                "mean"
            )
        )
        .reset_index()
    )


# =========================================================
# CATEGORY ANALYSIS
# =========================================================

def create_category_analysis(df):

    result = (
        df.groupby("category")
        .agg(
            customers=(
                "customer_id",
                "nunique"
            ),
            purchases=(
                "customer_id",
                "count"
            ),
            revenue=(
                "purchase_amount",
                "sum"
            ),
            average_purchase=(
                "purchase_amount",
                "mean"
            ),
            average_rating=(
                "review_rating",
                "mean"
            )
        )
        .reset_index()
    )

    result["revenue_share"] = (
        result["revenue"]
        / result["revenue"].sum()
        * 100
    )

    return result.sort_values(
        "revenue",
        ascending=False
    )


# =========================================================
# SUBSCRIPTION ANALYSIS
# =========================================================

def create_subscription_analysis(df):

    return (
        df.groupby("subscription_status")
        .agg(
            customers=(
                "customer_id",
                "nunique"
            ),
            revenue=(
                "purchase_amount",
                "sum"
            ),
            average_purchase=(
                "purchase_amount",
                "mean"
            ),
            average_previous_purchases=(
                "previous_purchases",
                "mean"
            ),
            average_rating=(
                "review_rating",
                "mean"
            )
        )
        .reset_index()
    )


# =========================================================
# DISCOUNT ANALYSIS
# =========================================================

def create_discount_analysis(df):

    result = (
        df.groupby("discount_applied")
        .agg(
            customers=(
                "customer_id",
                "nunique"
            ),
            revenue=(
                "purchase_amount",
                "sum"
            ),
            average_purchase=(
                "purchase_amount",
                "mean"
            ),
            average_rating=(
                "review_rating",
                "mean"
            )
        )
        .reset_index()
    )

    return result


# =========================================================
# PRODUCT ANALYSIS
# =========================================================

def create_product_analysis(df):

    return (
        df.groupby(
            [
                "category",
                "item_purchased"
            ]
        )
        .agg(
            purchases=(
                "customer_id",
                "count"
            ),
            customers=(
                "customer_id",
                "nunique"
            ),
            revenue=(
                "purchase_amount",
                "sum"
            ),
            average_purchase=(
                "purchase_amount",
                "mean"
            ),
            average_rating=(
                "review_rating",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            "revenue",
            ascending=False
        )
    )


# =========================================================
# PAYMENT ANALYSIS
# =========================================================

def create_payment_analysis(df):

    return (
        df.groupby("payment_method")
        .agg(
            purchases=(
                "customer_id",
                "count"
            ),
            revenue=(
                "purchase_amount",
                "sum"
            ),
            average_purchase=(
                "purchase_amount",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            "revenue",
            ascending=False
        )
    )


# =========================================================
# SHIPPING ANALYSIS
# =========================================================

def create_shipping_analysis(df):

    return (
        df.groupby("shipping_type")
        .agg(
            purchases=(
                "customer_id",
                "count"
            ),
            revenue=(
                "purchase_amount",
                "sum"
            ),
            average_purchase=(
                "purchase_amount",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            "average_purchase",
            ascending=False
        )
    )


# =========================================================
# SEASONAL ANALYSIS
# =========================================================

def create_seasonal_analysis(df):

    return (
        df.groupby("season")
        .agg(
            purchases=(
                "customer_id",
                "count"
            ),
            revenue=(
                "purchase_amount",
                "sum"
            ),
            average_purchase=(
                "purchase_amount",
                "mean"
            ),
            average_rating=(
                "review_rating",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            "revenue",
            ascending=False
        )
    )


# =========================================================
# TOP PRODUCTS
# =========================================================

def create_top_products(df):

    result = (
        df.groupby("item_purchased")
        .agg(
            purchases=(
                "customer_id",
                "count"
            ),
            revenue=(
                "purchase_amount",
                "sum"
            ),
            average_purchase=(
                "purchase_amount",
                "mean"
            ),
            average_rating=(
                "review_rating",
                "mean"
            )
        )
        .reset_index()
    )

    return (
        result
        .sort_values(
            "revenue",
            ascending=False
        )
        .head(10)
    )


# =========================================================
# SAVE OUTPUTS
# =========================================================

def save_outputs(outputs):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("\n" + "=" * 60)
    print("SAVING ANALYSIS OUTPUTS")
    print("=" * 60)

    for name, data in outputs.items():

        file_path = (
            OUTPUT_DIR
            / f"{name}.csv"
        )

        data.to_csv(
            file_path,
            index=False
        )

        print(
            f"✓ {name}.csv"
        )


# =========================================================
# MAIN
# =========================================================

def main():

    print("=" * 60)
    print("RETAIL CUSTOMER INSIGHTS")
    print("CUSTOMER & REVENUE ANALYSIS")
    print("=" * 60)

    df = load_data()

    outputs = {

        "executive_kpis":
            create_executive_kpis(df),

        "customer_value":
            create_customer_value(df),

        "customer_segments":
            create_customer_segments(df),

        "age_analysis":
            create_age_analysis(df),

        "category_analysis":
            create_category_analysis(df),

        "subscription_analysis":
            create_subscription_analysis(df),

        "discount_analysis":
            create_discount_analysis(df),

        "product_analysis":
            create_product_analysis(df),

        "payment_analysis":
            create_payment_analysis(df),

        "shipping_analysis":
            create_shipping_analysis(df),

        "seasonal_analysis":
            create_seasonal_analysis(df),

        "top_products":
            create_top_products(df)
    }

    save_outputs(outputs)

    print("\nAnalysis complete.")
    print(
        f"Output files are located in:\n{OUTPUT_DIR}"
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()
