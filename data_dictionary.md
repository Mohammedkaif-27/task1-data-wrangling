# 📖 Data Dictionary — Sales Transactions Dataset

**Dataset:** `raw_sales_data.csv` / `cleaned_sales_data.csv`  
**Domain:** Retail Sales  
**Time Period:** January 2024 – June 2024  
**Records (raw):** 61 rows | **Records (cleaned):** 60 rows  
**Prepared by:** [Your Name] | ApexPlanet Data Analytics Internship — Task 1

---

## 🔵 Original Columns (Raw Dataset)

| # | Column Name | Data Type | Description | Example Value | Business Relevance |
|---|-------------|-----------|-------------|---------------|--------------------|
| 1 | `order_id` | String | Unique identifier for each order | ORD001 | Primary key for order tracking |
| 2 | `customer_id` | String | Unique identifier for each customer | C101 | Used to track repeat customers |
| 3 | `customer_name` | String | Full name of the customer | Rahul Sharma | Customer identification |
| 4 | `email` | String | Customer email address | rahul@gmail.com | Contact and CRM use |
| 5 | `date_of_birth` | String (mixed formats) | Customer's date of birth — found in 3 formats: `DD-MM-YYYY`, `DD/MM/YYYY`, `YYYY-MM-DD` | 15-03-1990 | Used to derive customer age |
| 6 | `order_date` | String (YYYY-MM-DD) | Date when the order was placed | 2024-01-05 | Trend and time-series analysis |
| 7 | `product_name` | String | Name of the product purchased | Laptop Pro 15 | Product performance tracking |
| 8 | `category` | String | Product category | Electronics | Category-level sales analysis |
| 9 | `quantity` | Integer | Number of units ordered | 2 | Volume analysis |
| 10 | `unit_price` | Integer (₹) | Price per single unit in INR | 75000 | Revenue per unit |
| 11 | `discount` | String (mixed: `%` or `0`) | Discount applied to order — stored as percentage string or 0 | 10% / 0 | **Issue:** inconsistent format, needs cleaning |
| 12 | `total_amount` | Integer (₹) | Final order amount in INR | 67500 | Primary revenue metric |
| 13 | `payment_method` | String | Mode of payment used | Credit Card | Payment preference analysis |
| 14 | `region` | String | Geographic region of customer | North | Regional performance analysis |
| 15 | `status` | String | Order completion status | Completed | Fulfilment tracking |

---

## 🟢 New Columns (Added After Cleaning & Feature Engineering)

| # | Column Name | Data Type | Description | Example Value | Engineering Logic |
|---|-------------|-----------|-------------|---------------|-------------------|
| 16 | `customer_age` | Float | Customer's age in years at June 2024 | 34.0 | Derived from `date_of_birth` |
| 17 | `age_group` | String | Generational bucket based on age | Millennial (28-43) | Categorical age segmentation |
| 18 | `dob_missing_flag` | Integer (0/1) | 1 if DOB was originally missing | 0 | Data quality tracking |
| 19 | `order_month` | Integer | Month number of order date | 1 | Monthly trend analysis |
| 20 | `order_month_name` | String | Short month name | Jan | Human-readable month label |
| 21 | `order_quarter` | Integer | Quarter of the year (1-4) | 1 | Quarterly reporting |
| 22 | `discount_tier` | String | Categorical bucket for discount level | Medium (6-10%) | Discount impact segmentation |
| 23 | `revenue_bucket` | String | Order size classification by revenue | Large (15K-50K) | Order value segmentation |
| 24 | `amount_mismatch_flag` | Integer (0/1) | 1 if original total didn't match recalculated | 0 | Data integrity check |
| 25 | `is_first_purchase` | Integer (0/1) | 1 if this is the customer's first order | 1 | New vs returning customer |

---

## ⚠️ Data Quality Issues Found

| Issue | Column(s) Affected | Count | Action Taken |
|-------|-------------------|-------|--------------|
| Duplicate rows | All columns | 1 row | Removed |
| Missing values | `email` | 4 rows | Filled with `not_provided@unknown.com` |
| Missing values | `date_of_birth` | 6 rows | Flagged with `dob_missing_flag = 1` |
| Missing values | `discount` | 1 row | Treated as 0% discount |
| Inconsistent date formats | `date_of_birth` | Multiple | Standardized to `YYYY-MM-DD` |
| Discount stored as string `%` | `discount` | 17 rows | Converted to decimal (e.g. `10%` → `0.10`) |
| Non-standard region value | `region` | 1 row (`Kerala`) | Mapped to `South` |
| Inconsistent category casing | `category` | All rows | Standardized to Title Case |

---

## 📊 Cleaned Column Data Types

| Column | Type | Valid Range / Values |
|--------|------|----------------------|
| `order_id` | str | ORD001 – ORD060 |
| `customer_id` | str | C101 – C158 |
| `discount` | float | 0.00 – 1.00 |
| `total_amount` | float | > 0 |
| `customer_age` | float | 18 – 80 |
| `order_month` | int | 1 – 6 |
| `order_quarter` | int | 1 – 2 |
| `region` | str | North / South / East / West |
| `status` | str | Completed / Cancelled / Pending |
| `payment_method` | str | Credit Card / Debit Card / UPI / Cash |
| `age_group` | str | Gen Z / Millennial / Gen X / Boomer |
| `discount_tier` | str | No Discount / Low / Medium / High |
| `revenue_bucket` | str | Micro / Small / Medium / Large / Enterprise |
