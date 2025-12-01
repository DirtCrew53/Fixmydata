# cleaning.py
import pandas as pd

class DataCleaner:
    def __init__(self, data: pd.DataFrame):
        self._data = data  # private attribute to hold the dataframe

    def remove_duplicates(self):
        """Removes duplicate rows from the dataframe."""
        self._data = self._data.drop_duplicates()
        return self._data

    def fill_missing(self, strategy="mean"):
        """Fills missing values with the chosen strategy: mean, median, or mode."""
        if strategy == "mean":
            self._data.fillna(self._data.mean(), inplace=True)
        elif strategy == "median":
            self._data.fillna(self._data.median(), inplace=True)
        elif strategy == "mode":
            self._data.fillna(self._data.mode().iloc[0], inplace=True)
        else:
            raise ValueError("Invalid strategy. Choose 'mean', 'median', or 'mode'.")
        return self._data

    def standardize_columns(self):
        """Standardizes column names by converting them to lowercase and replacing spaces with underscores."""
        self._data.columns = [col.lower().replace(" ", "_") for col in self._data.columns]
        return self._data
