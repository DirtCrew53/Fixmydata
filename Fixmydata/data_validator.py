# data_validator.py
import pandas as pd

class DataValidator:
    def __init__(self, data: pd.DataFrame):
        self._data = data  # private attribute to hold the dataframe

    def validate_range(self, column, min_val, max_val):
        """Ensures values in a column are within the specified range."""
        if not self._data[column].between(min_val, max_val).all():
            raise ValueError(f"Values in {column} are out of the specified range.")
        return self._data

    def validate_non_empty(self):
        """Ensures there are no empty or null values in the dataframe."""
        if self._data.isnull().any().any():
            raise ValueError("Data contains missing values.")
        return self._data
