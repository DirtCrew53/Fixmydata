# Fixmydata

Fixmydata is a lightweight helper library built on top of pandas for cleaning, validating, and inspecting tabular datasets. It provides quick, chainable utilities for removing common data issues so you can focus on analysis.

## Installation

- **Python:** 3.7+
- **Required dependencies:** pandas, numpy

The library is currently distributed from source. Clone the repository and install in editable mode:

```bash
pip install -e .
```
### Troubleshooting installation on Windows

If you see a build error for `pandas` (for example: `cl.exe failed with exit code 2`), the installer is trying to compile pandas from source instead of using a pre-built wheel.

1. Make sure you are using a supported Python (3.8–3.12) and have an up-to-date `pip`:
   ```powershell
   python -m pip install --upgrade pip setuptools wheel
   ```
2. Force-install pandas and numpy from official wheels (no compilation):
   ```powershell
   python -m pip install --only-binary=:all: "pandas>=1.5" "numpy>=1.23"
   ```
3. Re-run the library install:
   ```powershell
   pip install -e .
   ```

If a wheel is unavailable for your Python version/architecture, install the **Microsoft C++ Build Tools** and retry, or use a Python version with published pandas wheels.

## Features

- **Cleaning:** Deduplicate rows, drop or fill missing values, remove columns, and trim whitespace with `DataCleaner`.
- **Validation:** Assert value ranges and check for missing or empty data with `DataValidator`.
- **Outlier filtering:** Identify inliers using Z-score or IQR methods while ignoring non-numeric columns via `OutlierDetector`.
- **Utilities:** CSV load/save helpers, column name normalization, null counting, and quick DataFrame introspection.

## Quickstart

```python
import pandas as pd
from Fixmydata import DataCleaner, DataValidator, OutlierDetector

raw = pd.DataFrame({
    "id": [1, 1, 2, 3],
    "city": ["  New York", "Boston  ", "Chicago", None],
    "value": [10.5, 9.7, 11.2, 13.0],
})

# Clean data (methods mutate an internal copy; access the result via .data)
cleaning = DataCleaner(raw)
cleaning.remove_duplicates(subset=["id"])
cleaning.drop_missing(columns=["city"])
cleaning.standardize_whitespace(["city"])
clean = cleaner.data

# Validate data (raises assertion errors on failures)
validator = DataValidator(clean)
validator.validate_range("value", 0, 15)
validator.validate_non_empty()

# Filter outliers (returns an inliers-only DataFrame)
detector = OutlierDetector(clean)
inliers = detector.z_score_outliers(threshold=2.5)
print(inliers)
```

### Using utilities

```python
from Fixmydata import utils

# Save cleaned data for reuse
utils.to_csv(clean, "cleaned.csv")

# Load it later and inspect quickly
reloaded = utils.from_csv("cleaned.csv")
utils.df_info(reloaded)
```

## Modules

- `Fixmydata.cleaning.DataCleaner`: Common cleaning operations that mutate an internal copy and expose the cleaned `data` property for reuse.
- `Fixmydata.data_validator.DataValidator`: Range and completeness checks with clear errors on schema mismatches.
- `Fixmydata.outlier_detector.OutlierDetector`: Z-score and IQR inlier filters with safeguards for missing numeric data.
- `Fixmydata.utils`: CSV I/O helpers, column name normalization, null counting, and DataFrame info display.
- `Fixmydata.stats`: Basic descriptive statistics and standalone outlier helpers.

## Error handling and caveats

- Validation methods raise assertion errors when ranges are violated or required fields are empty.
- Outlier filtering ignores non-numeric columns and may drop rows with missing numeric values depending on the method.
- Cleaning methods mutate internal state; re-instantiate `DataCleaner` if you need to preserve the original DataFrame.

## Documentation

Formal API docs are not yet published. Explore the source modules above for deeper detail.

- Walkthroughs: See [`Fixmydata_demo.md`](Fixmydata_demo.md) for a GitHub-friendly project demo and presentation outline mirroring the companion notebook.

## Contributors

| Name                  | Role / Position | Main Contribution                           |
| --------------------- | --------------- | ------------------------------------------- |
| Johann Lloyd Megalbio | Leader          | Project management and overall coordination |
| Albrien Dealino       | Developer       | Core coding and development tasks           |
| Rafael John Calingin  | Developer       | Coding and implementation of key features   |
| Shawn Bolores Sillote | Developer       | Development of system modules and functions |

## Contributing

Contributions are welcome! Please open an issue to discuss changes, then submit a pull request with relevant tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
