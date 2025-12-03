# fixmydata – A Python Library for Data Cleaning

`fixmydata` is a lightweight toolkit for preparing tabular data before analysis or modeling. It wraps common cleaning, validation, and outlier detection routines behind a small, object-oriented API so you can standardize data quality steps across notebooks and projects.

## Features
- **Remove duplicates**: Drop duplicate rows with a single call.
- **Fill missing values**: Impute with mean, median, or mode across selected columns.
- **Normalize column names**: Standardize headers by lowercasing and collapsing whitespace.
- **Validate datasets**: Guard against empty frames and enforce numeric ranges.
- **Outlier detection**: Filter rows using Z-score or IQR rules while ignoring non-numeric columns.
- **Statistics helpers**: Compute descriptive statistics (mean, median, mode, standard deviation, correlations) for quick exploration.

## Installation
Install the latest release from PyPI:

```bash
pip install fixmydata
```

To work from a clone of this repository instead:

```bash
git clone https://github.com/DirtCrew53/Fixmydata.git
cd Fixmydata
pip install -e .
```

## Quick start
Create a `pandas` DataFrame, clean it, validate it, and check for outliers:

```python
import pandas as pd
from fixmydata import DataCleaner, DataValidator, OutlierDetector

# Sample data
raw = pd.DataFrame({
    "Age": [22, 25, 27, 30, 28, None, 29, 27, 27],
    "Salary": [50000, 55000, None, 60000, 62000, 64000, 58000, 57000, None],
    "Department": ["HR", "IT", "Finance", "HR", "IT", "Finance", "HR", "IT", "HR"],
})

# Cleaning
cleaner = DataCleaner(raw)
cleaned = (
    cleaner
    .remove_duplicates()
    .fill_missing(strategy="mean")
    .standardize_columns()
)

print("Cleaned data:\n", cleaned)

# Validation
validator = DataValidator(cleaned)
validator.validate_non_empty()
validator.validate_range("age", 20, 60)

# Outlier detection
outliers_removed = OutlierDetector(cleaned).z_score_outliers(threshold=2)
print("\nRows kept after outlier check:\n", outliers_removed)
```

## Core classes
- **`DataCleaner`** (`Fixmydata/cleaning.py`)
  - `remove_duplicates()` drops duplicate rows.
  - `fill_missing(strategy="mean", columns=None)` fills missing values using mean, median, or mode; you can target specific columns.
  - `standardize_columns()` lowercases and normalizes column names.
- **`DataValidator`** (`Fixmydata/data_validator.py`)
  - `validate_non_empty()` raises if the DataFrame is empty or contains nulls.
  - `validate_range(column, min_val, max_val)` ensures numeric values stay within bounds.
- **`OutlierDetector`** (`Fixmydata/outlier_detector.py`)
  - `z_score_outliers(threshold=3)` keeps rows whose numeric columns fall within the Z-score threshold.
  - `iqr_outliers()` filters rows outside the interquartile range fence.
- **Statistics helpers** (`Fixmydata/stats.py`)
  - Utility functions such as `calculate_mean`, `calculate_median`, `calculate_mode`, `calculate_std_dev`, and `correlation` for quick descriptive analysis.

## Project structure
- `Fixmydata/`: Library source code organized by feature (cleaning, validation, outlier detection, statistics).
- `datasets/`: Example datasets you can use while experimenting.
- `demo.ipynb`: A walkthrough notebook that demonstrates the API end-to-end.
- `test/`: Automated tests that mirror the public API.

## Contributing
Contributions and bug reports are welcome. Please open an issue or pull request on GitHub describing the change you’d like to make. Make sure to add or update tests alongside code changes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
