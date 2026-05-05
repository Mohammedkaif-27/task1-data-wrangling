"""
=============================================================
 ApexPlanet Internship - Task 1: Data Immersion & Wrangling
 Author  : [Your Name]
 Dataset : Sales Transactions (raw_sales_data.csv)
 Purpose : Load → Profile → Clean → Transform → Export
=============================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# STEP 1 — LOAD RAW DATA
# ─────────────────────────────────────────────
print("=" * 60)
print("STEP 1: Loading Raw Dataset")
print("=" * 60)

df = pd.read_csv("raw_sales_data.csv")

print(f"Shape       : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Columns     : {list(df.columns)}\n")
print(df.head(5).to_string())


# ─────────────────────────────────────────────
# STEP 2 — DATA QUALITY ASSESSMENT (Profiling)
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 2: Data Quality Assessment")
print("=" * 60)

# 2a. Missing values
print("\n[2a] Missing Values:")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_report = pd.DataFrame({"Missing Count": missing, "Missing %": missing_pct})
print(missing_report[missing_report["Missing Count"] > 0].to_string())

# 2b. Duplicate rows
dup_count = df.duplicated().sum()
print(f"\n[2b] Duplicate Rows: {dup_count}")
print(df[df.duplicated(keep=False)][["order_id", "customer_id", "order_date"]].head())

# 2c. Inconsistent date formats
print("\n[2c] Sample date_of_birth values (multiple formats detected):")
print(df["date_of_birth"].dropna().unique()[:10])

print("\n[2d] Sample order_date values:")
print(df["order_date"].unique()[:5])

# 2e. discount column - mixed types (%, blank)
print("\n[2e] Unique discount values:")
print(df["discount"].unique())

# 2f. Data types
print("\n[2f] Data Types:")
print(df.dtypes.to_string())

# 2g. Region inconsistencies
print("\n[2g] Unique Region values:")
print(df["region"].unique())

# 2h. Category inconsistencies
print("\n[2h] Unique Categories:")
print(df["category"].value_counts().to_string())


# ─────────────────────────────────────────────
# STEP 3 — DATA CLEANING & TRANSFORMATION
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3: Data Cleaning & Transformation")
print("=" * 60)

df_clean = df.copy()

# ── 3a. Remove duplicates
before = len(df_clean)
df_clean.drop_duplicates(inplace=True)
after = len(df_clean)
print(f"\n[3a] Removed {before - after} duplicate row(s). Rows remaining: {after}")

# ── 3b. Standardize date_of_birth (3 different formats → YYYY-MM-DD)
def parse_dob(val):
    if pd.isna(val):
        return np.nan
    formats = ["%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d"]
    for fmt in formats:
        try:
            return datetime.strptime(str(val).strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return np.nan

df_clean["date_of_birth"] = df_clean["date_of_birth"].apply(parse_dob)
print(f"\n[3b] date_of_birth standardized to YYYY-MM-DD format.")

# ── 3c. Standardize order_date
df_clean["order_date"] = pd.to_datetime(df_clean["order_date"]).dt.strftime("%Y-%m-%d")
print(f"[3c] order_date standardized to YYYY-MM-DD format.")

# ── 3d. Clean discount column — remove '%', convert to float (0-1 scale)
def clean_discount(val):
    if pd.isna(val) or str(val).strip() == "":
        return 0.0
    cleaned = str(val).replace("%", "").strip()
    try:
        return float(cleaned) / 100
    except ValueError:
        return 0.0

df_clean["discount"] = df_clean["discount"].apply(clean_discount)
print(f"[3d] discount column cleaned — converted to decimal (0.0–1.0 scale).")

# ── 3e. Standardize region — normalize 'Kerala' → 'South' (it is in South India)
region_map = {"Kerala": "South"}
df_clean["region"] = df_clean["region"].replace(region_map)
print(f"[3e] Region 'Kerala' normalized to 'South'.")

# ── 3f. Standardize category names — title-case
df_clean["category"] = df_clean["category"].str.strip().str.title()
print(f"[3f] Category names standardized to Title Case.")

# ── 3g. Fill missing email with placeholder
df_clean["email"] = df_clean["email"].fillna("not_provided@unknown.com")
print(f"[3g] Missing emails filled with placeholder.")

# ── 3h. Fill missing date_of_birth with median (for age calculation purposes)
# We will flag missing DOB rows separately
df_clean["dob_missing_flag"] = df_clean["date_of_birth"].isna().astype(int)
print(f"[3h] Created 'dob_missing_flag' column (1 = DOB was missing).")

# ── 3i. Recalculate total_amount to verify / fix inconsistencies
#    Formula: total_amount = quantity * unit_price * (1 - discount)
df_clean["total_amount_recalculated"] = (
    df_clean["quantity"] * df_clean["unit_price"] * (1 - df_clean["discount"])
).round(2)

# Flag rows where original total doesn't match recalculated
df_clean["amount_mismatch_flag"] = (
    (df_clean["total_amount"] - df_clean["total_amount_recalculated"]).abs() > 1
).astype(int)
mismatches = df_clean["amount_mismatch_flag"].sum()
print(f"[3i] Found {mismatches} rows where total_amount didn't match formula. Using recalculated value.")

# Replace total_amount with recalculated
df_clean["total_amount"] = df_clean["total_amount_recalculated"]
df_clean.drop(columns=["total_amount_recalculated"], inplace=True)

# ── 3j. Validate numeric columns — no negatives allowed
for col in ["quantity", "unit_price", "total_amount"]:
    neg_count = (df_clean[col] < 0).sum()
    if neg_count > 0:
        df_clean = df_clean[df_clean[col] >= 0]
        print(f"[3j] Removed {neg_count} rows with negative {col}.")
    else:
        print(f"[3j] {col}: No negative values found. ✓")

# ── 3k. Strip whitespace from all string columns
str_cols = df_clean.select_dtypes(include="object").columns
df_clean[str_cols] = df_clean[str_cols].apply(lambda col: col.str.strip())
print(f"[3k] Whitespace stripped from all text columns.")


# ─────────────────────────────────────────────
# STEP 4 — FEATURE ENGINEERING
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4: Feature Engineering")
print("=" * 60)

# 4a. Customer Age (from date_of_birth)
today = pd.Timestamp("2024-06-30")  # using end of dataset period
df_clean["customer_age"] = df_clean["date_of_birth"].apply(
    lambda dob: int((today - pd.Timestamp(dob)).days / 365.25) if pd.notna(dob) else np.nan
)
print(f"[4a] 'customer_age' column created from date_of_birth.")

# 4b. Age group / generation bucket
def age_group(age):
    if pd.isna(age):
        return "Unknown"
    if age < 28:
        return "Gen Z (< 28)"
    elif age < 44:
        return "Millennial (28-43)"
    elif age < 60:
        return "Gen X (44-59)"
    else:
        return "Boomer (60+)"

df_clean["age_group"] = df_clean["customer_age"].apply(age_group)
print(f"[4b] 'age_group' column created.")

# 4c. Order Month and Quarter
df_clean["order_month"] = pd.to_datetime(df_clean["order_date"]).dt.month
df_clean["order_quarter"] = pd.to_datetime(df_clean["order_date"]).dt.quarter
df_clean["order_month_name"] = pd.to_datetime(df_clean["order_date"]).dt.strftime("%b")
print(f"[4c] 'order_month', 'order_quarter', 'order_month_name' columns created.")

# 4d. Discount tier
def discount_tier(d):
    if d == 0:
        return "No Discount"
    elif d <= 0.05:
        return "Low (1-5%)"
    elif d <= 0.10:
        return "Medium (6-10%)"
    else:
        return "High (>10%)"

df_clean["discount_tier"] = df_clean["discount"].apply(discount_tier)
print(f"[4d] 'discount_tier' column created.")

# 4e. Revenue bucket (to classify order size)
def revenue_bucket(amt):
    if amt < 1000:
        return "Micro (<1K)"
    elif amt < 5000:
        return "Small (1K-5K)"
    elif amt < 15000:
        return "Medium (5K-15K)"
    elif amt < 50000:
        return "Large (15K-50K)"
    else:
        return "Enterprise (>50K)"

df_clean["revenue_bucket"] = df_clean["total_amount"].apply(revenue_bucket)
print(f"[4e] 'revenue_bucket' column created.")

# 4f. Is First Purchase flag per customer
df_clean["order_date_dt"] = pd.to_datetime(df_clean["order_date"])
df_clean = df_clean.sort_values(["customer_id", "order_date_dt"])
df_clean["is_first_purchase"] = ~df_clean.duplicated(subset="customer_id", keep="first")
df_clean["is_first_purchase"] = df_clean["is_first_purchase"].astype(int)
df_clean.drop(columns=["order_date_dt"], inplace=True)
print(f"[4f] 'is_first_purchase' flag created.")


# ─────────────────────────────────────────────
# STEP 5 — FINAL COLUMN ORDERING & EXPORT
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 5: Export Cleaned Dataset")
print("=" * 60)

final_columns = [
    "order_id", "customer_id", "customer_name", "email",
    "date_of_birth", "customer_age", "age_group", "dob_missing_flag",
    "order_date", "order_month", "order_month_name", "order_quarter",
    "product_name", "category",
    "quantity", "unit_price", "discount", "discount_tier",
    "total_amount", "revenue_bucket",
    "payment_method", "region", "status",
    "amount_mismatch_flag", "is_first_purchase"
]

df_final = df_clean[final_columns]

df_final.to_csv("cleaned_sales_data.csv", index=False)
print(f"\nCleaned dataset exported: cleaned_sales_data.csv")
print(f"Final Shape: {df_final.shape[0]} rows × {df_final.shape[1]} columns")


# ─────────────────────────────────────────────
# STEP 6 — CLEANING SUMMARY REPORT
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 6: Cleaning Summary Report")
print("=" * 60)

print(f"""
╔══════════════════════════════════════════════════╗
║         DATA CLEANING SUMMARY                  ║
╠══════════════════════════════════════════════════╣
║ Original Records       : {before:<6}                 ║
║ After Deduplication    : {after:<6}                 ║
║ Final Records          : {len(df_final):<6}                 ║
║ Final Columns          : {len(df_final.columns):<6}                 ║
╠══════════════════════════════════════════════════╣
║ Issues Fixed:                                   ║
║  ✓ Duplicate rows removed                       ║
║  ✓ Date formats unified (3 → YYYY-MM-DD)        ║
║  ✓ Discount % → decimal (0.0-1.0)               ║
║  ✓ Region names normalized                      ║
║  ✓ Category names title-cased                   ║
║  ✓ Missing emails flagged & filled              ║
║  ✓ Total amount verified & recalculated         ║
║  ✓ Whitespace stripped from all text fields     ║
╠══════════════════════════════════════════════════╣
║ New Features Engineered:                        ║
║  + customer_age (from date_of_birth)            ║
║  + age_group (generational bucket)              ║
║  + order_month, order_quarter, month_name       ║
║  + discount_tier                                ║
║  + revenue_bucket                               ║
║  + dob_missing_flag                             ║
║  + is_first_purchase                            ║
║  + amount_mismatch_flag                         ║
╚══════════════════════════════════════════════════╝
""")

print("\nSample of Cleaned Dataset:")
print(df_final.head(5).to_string())

print("\nData Types in Cleaned Dataset:")
print(df_final.dtypes.to_string())

print("\nMissing Values in Cleaned Dataset:")
print(df_final.isnull().sum()[df_final.isnull().sum() > 0].to_string() or "None ✓")

print("\n✅ Task 1 Complete! Files ready for GitHub upload.")
