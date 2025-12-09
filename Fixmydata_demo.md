# Fixmydata Walkthrough (GitHub-friendly)

This Markdown guide mirrors the `Fixmydata_demo.ipynb` notebook so you can read and present it directly on GitHub without opening a notebook viewer.

## 1. Overview
Fixmydata wraps common pandas cleaning and validation patterns in small, composable helpers:
- **`DataCleaner`**: remove duplicates, drop/fill missing data, trim whitespace, and drop columns.
- **`DataValidator`**: assert numeric ranges and check for empty datasets.
- **`OutlierDetector`**: filter outliers with Z-score or IQR methods while ignoring non-numeric fields.

The typical workflow is: **load → clean → validate → filter outliers → summarize**.

## 2. Load a messy sample dataset
The sample data intentionally includes duplicate IDs, trailing whitespace, missing values, and a price outlier.

```python
import pandas as pd
from Fixmydata import DataCleaner, DataValidator, OutlierDetector

raw = pd.DataFrame({
    "id": [1, 1, 2, 3, 4, 5],
    "city": ["  New York", "Boston  ", "Chicago", None, "San Francisco", "Houston"],
    "price": [10.5, 9.7, 11.2, 13.0, None, 99.0],
})
raw
```

## 3. Clean the data
- Remove duplicate IDs (keep the first occurrence).
- Drop rows missing a `city` value.
- Standardize whitespace for the `city` column.
- Fill missing prices with the column median for analysis.

```python
cleaner = DataCleaner(raw)
cleaner.remove_duplicates(subset=["id"])
cleaner.drop_missing(columns=["city"])
cleaner.standardize_whitespace(["city"])
median_price = cleaner.data["price"].median()
cleaner.fill_missing("price", median_price)
clean = cleaner.data
clean
```

## 4. Validate the cleaned dataset
Confirm the dataframe is non-empty, free of nulls, and that `price` falls within a practical range (0–50).

```python
validator = DataValidator(clean)
validator.validate_non_empty()
validator.validate_range("price", 0, 50)
clean
```

## 5. Filter outliers
Use Z-score filtering (threshold 2.5) to keep only inlier rows while safely ignoring non-numeric columns.

```python
outlier_detector = OutlierDetector(clean)
inliers = outlier_detector.z_score_outliers(threshold=2.5)
inliers
```

## 6. Summary of results
- Started with duplicate IDs, whitespace issues, missing values, and a price outlier.
- Cleaned dataset now has standardized city names and imputed prices.
- Validation confirms completeness and realistic price ranges.
- Outlier detection isolates reliable rows for downstream analysis.

## 7. Presentation outline (5–7 minutes)
Use this as a talk track—each bullet should take ~30–60 seconds.

1. **Problem & goal (45s)**: Data quality slows analysis; Fixmydata packages repeatable fixes on top of pandas.
2. **Library overview (60s)**: Briefly introduce `DataCleaner`, `DataValidator`, `OutlierDetector`, and helper utilities.
3. **Workflow demo (2–3m)**:
   - Load messy sample data and describe its issues.
   - Run cleaning steps and show before/after.
   - Run validation to prove completeness and sensible ranges.
   - Apply outlier filtering and highlight the remaining rows.
4. **Why it matters (60–90s)**: Consistent cleaning improves reliability, reduces manual rework, and keeps pipelines reproducible.
5. **Extensibility (45–60s)**: Mention that you can swap in IQR outlier detection, customize ranges, or add domain-specific checks.
6. **Next steps (30–45s)**: Show where to find the code, how to run `pip install -e .`, and invite contributions.

## 8. How to run locally
1. Install dependencies: `pip install -e .`
2. Open the notebook (`Fixmydata_demo.ipynb`) or run the code snippets above in a Python shell/IDE.
3. Optional: export the notebook to HTML for sharing using `jupyter nbconvert --to html Fixmydata_demo.ipynb`.

Happy presenting!
