# 📊 Task 1 — Data Immersion & Wrangling
### ApexPlanet Software Pvt. Ltd. | 60-Day Data Analytics Internship

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0-green?logo=pandas)
![Status](https://img.shields.io/badge/Task-Completed-brightgreen)
![Timeline](https://img.shields.io/badge/Timeline-10%20Days-orange)

---

## 🎯 Objective

Rapidly acquaint with the dataset and master the critical first step of any data project: **acquiring, profiling, cleaning, and preparing data** for downstream analysis.

---

## 📁 Repository Structure

```
task1-data-wrangling/
│
├── raw_sales_data.csv          ← Original messy dataset (61 rows × 15 cols)
├── cleaned_sales_data.csv      ← Analysis-ready cleaned dataset (60 rows × 25 cols)
├── data_cleaning.py            ← Full Python cleaning & transformation script
├── data_dictionary.md          ← Documentation for all variables
└── README.md                   ← This file
```

---

## 📦 Dataset Overview

**Domain:** Retail Sales Transactions  
**Period:** January 2024 – June 2024  
**Source:** Internal simulated dataset (ApexPlanet internship)

### Raw Dataset Issues Identified:

| Issue | Detail |
|-------|--------|
| 🔴 Duplicate rows | 1 exact duplicate found (ORD001) |
| 🟡 Missing values | `email` (4 rows), `date_of_birth` (6 rows), `discount` (1 row) |
| 🟡 Inconsistent date formats | 3 formats in `date_of_birth`: `DD-MM-YYYY`, `DD/MM/YYYY`, `YYYY-MM-DD` |
| 🟡 Discount as string | Stored as `"10%"` instead of numeric `0.10` |
| 🟡 Non-standard region | `"Kerala"` should be `"South"` |
| 🟡 Category casing | Mixed casing in category names |

---

## 🔧 Steps Performed

### Step 1 — Load & Inspect
- Loaded CSV with Pandas
- Checked shape, dtypes, and initial sample

### Step 2 — Data Quality Assessment
- Identified missing values per column
- Found duplicate rows
- Detected 3 inconsistent date formats
- Discovered % symbol in discount column
- Found non-standard region value (`Kerala`)

### Step 3 — Data Cleaning
- ✅ Removed 1 duplicate row
- ✅ Standardized all date formats → `YYYY-MM-DD`
- ✅ Cleaned discount → converted to `float` (0.0 – 1.0)
- ✅ Normalized region: `Kerala` → `South`
- ✅ Title-cased all category names
- ✅ Filled missing emails with placeholder
- ✅ Flagged missing DOB rows with `dob_missing_flag`
- ✅ Verified and recalculated `total_amount` using formula
- ✅ Stripped whitespace from all string columns

### Step 4 — Feature Engineering
| New Column | Logic |
|------------|-------|
| `customer_age` | Derived from `date_of_birth` |
| `age_group` | Gen Z / Millennial / Gen X / Boomer |
| `order_month`, `order_quarter`, `order_month_name` | From `order_date` |
| `discount_tier` | No Discount / Low / Medium / High |
| `revenue_bucket` | Micro / Small / Medium / Large / Enterprise |
| `dob_missing_flag` | 1 if DOB was originally missing |
| `is_first_purchase` | 1 if customer's first ever order |
| `amount_mismatch_flag` | 1 if original total ≠ recalculated total |

---

## 📊 Before vs After

| Metric | Before | After |
|--------|--------|-------|
| Rows | 61 | 60 |
| Columns | 15 | 25 |
| Missing values | 11 | 6 (DOB only, flagged) |
| Duplicates | 1 | 0 |
| Date formats | 3 | 1 (YYYY-MM-DD) |
| Discount type | String (`%`) | Float (0.0–1.0) |

---

## 🚀 How to Run

```bash
# 1. Clone this repository
git clone https://github.com/[YourUsername]/task1-data-wrangling.git
cd task1-data-wrangling

# 2. Install dependencies
pip install pandas numpy

# 3. Run the cleaning script
python data_cleaning.py

# Output: cleaned_sales_data.csv is generated in the same folder
```

**Requirements:**
- Python 3.10+
- pandas >= 1.5
- numpy >= 1.23

---

## 📽️ LinkedIn Video Walkthrough

🎬 [Watch the 3–5 min Task 1 walkthrough on LinkedIn](#)  
*(Link to be updated after upload)*

---

## 👨‍💻 Author

**Shaik Mohammed Kaif**  
B.Tech CSE (AI & ML) | G. Pulla Reddy Engineering College, Kurnool  
Data Analytics Intern @ ApexPlanet Software Pvt. Ltd.  

---

*Part of the ApexPlanet 60-Day Data Analytics Internship Program*
