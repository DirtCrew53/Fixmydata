import sys
import pandas as pd
from pathlib import Path

# -------------------------------------------------
# PROJECT PATH SETUP
# -------------------------------------------------
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

DATA_DIR = ROOT / "datasets"

from Fixmydata import DataCleaner, DataValidator, OutlierDetector


# =================================================
# NORMAL USAGE DEMONSTRATION
# =================================================

print("=== NORMAL USAGE: TITANIC DATASET ===")

titanic_path = DATA_DIR / "tested.csv"
titanic_df = pd.read_csv(titanic_path)

cleaning = DataCleaner(titanic_df)

cleaning.fill_missing("Age", cleaning.data["Age"].median())
cleaning.fill_missing("Fare", cleaning.data["Fare"].median())
cleaning.fill_missing("Cabin", "Unknown")

titanic_clean = cleaning.remove_duplicates()

validator = DataValidator(titanic_clean)
validator.validate_non_empty()
validator.validate_range("Age", 0, 90)

detector = OutlierDetector(titanic_clean)
titanic_iqr = detector.iqr_outliers()

print("Original rows:", len(titanic_clean))
print("Rows after IQR filtering:", len(titanic_iqr))


# =================================================
# SECOND DATASET
# =================================================

print("\n=== NORMAL USAGE: USA HOUSING DATASET ===")

housing_path = DATA_DIR / "USA Housing Dataset.csv"
housing_df = pd.read_csv(housing_path)

housing_cleaner = DataCleaner(housing_df)
housing_base = housing_cleaner.remove_duplicates()

housing_detector = OutlierDetector(housing_base)
housing_no_outliers = housing_detector.z_score_outliers(threshold=3)

price_sqft_corr = housing_no_outliers["price"].corr(
    housing_no_outliers["sqft_living"]
)

print(f"Correlation between price and square footage: {price_sqft_corr:.3f}")


# =================================================
# ERROR HANDLING DEMONSTRATIONS
# =================================================

print("\n=== ERROR HANDLING DEMONSTRATIONS ===")

# 1. Missing column error
try:
    cleaning.fill_missing("Aeg", 30)
except Exception as e:
    print("Missing column error:", e)

# 2. Invalid fill value type
try:
    cleaning.fill_missing("Fare", "Unknown")
except Exception as e:
    print("Invalid fill value error:", e)

# 3. Invalid range validation
try:
    validator.validate_range("Age", 0, 10)
except Exception as e:
    print("Range validation error:", e)

# 4. Invalid outlier threshold
try:
    detector.z_score_outliers(threshold=-1)
except Exception as e:
    print("Invalid threshold error:", e)

# 5. Empty dataset validation
try:
    empty_df = pd.DataFrame()
    empty_validator = DataValidator(empty_df)
    empty_validator.validate_non_empty()
except Exception as e:
    print("Empty dataset error:", e)

print("\nDemo completed.")
