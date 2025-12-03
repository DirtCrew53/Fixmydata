# fixmydata - A Python Library for Data Cleaning

`fixmydata` is a Python library designed for cleaning and preprocessing data. It includes essential data cleaning tasks like handling missing values, removing duplicates, detecting outliers, and validating datasets. Built using Object-Oriented Programming (OOP) principles, it is modular, reusable, and easy to extend.

## Features:
- **Remove Duplicates**: Remove duplicate rows from your data.
- **Fill Missing Values**: Fill missing values using mean, median, or mode.
- **Detect and Remove Outliers**: Detect outliers using Z-score and IQR methods.
- **Data Validation**: Ensure data is within specified ranges and non-empty.
- **Modular OOP Design**: Utilizes encapsulation, inheritance, and polymorphism.

## Installation
```bash
pip install fixmydata
````
# Usage

```python
from fixmydata import DataCleaner, DataValidator, OutlierDetector
import pandas as pd


data = pd.DataFrame({
    'Age': [22, 25, 27, 30, 28, None, 29, 27, 27],
    'Salary': [50000, 55000, None, 60000, 62000, 64000, 58000, 57000, None],
    'Department': ['HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR', 'IT', 'HR']
})


cleaner = DataCleaner(data)
cleaned_data = cleaner.remove_duplicates().fill_missing(strategy="mean").standardize_columns()

print("Cleaned Data:")
print(cleaned_data)

validator = DataValidator(cleaned_data)
validated_data = validator.validate_non_empty()
validated_data = validator.validate_range('Age', 20, 60)

print("\nValidated Data:")
print(validated_data)

outlier_detector = OutlierDetector(cleaned_data)
outliers = outlier_detector.z_score_outliers(threshold=2)

print("\nOutliers Removed:")
print(outliers)
