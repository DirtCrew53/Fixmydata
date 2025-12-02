# cleaning.py
from __future__ import annotations

from typing import List, Optional

import pandas as pd
from pandas.api import types as pd_types


class DataCleaner:
    def __init__(self, data: pd.DataFrame):
        self._data = data.copy()  # private attribute to hold the dataframe

    def remove_duplicates(self) -> pd.DataFrame:
        """Remove duplicate rows from the dataframe."""
        self._data = self._data.drop_duplicates()
        return self._data

    def fill_missing(self, strategy: str = "mean", columns: Optional[List[str]] = None) -> pd.DataFrame:
        """Fill missing values using the chosen strategy.

        Parameters
        ----------
        strategy:
            One of ``"mean"``, ``"median"`` or ``"mode"``.
        columns:
            Optional subset of columns to apply the strategy to. When ``None`` all
            columns are considered; numeric-only columns are used for mean/median.
        """

        available_columns = self._data.columns
        target_columns = list(available_columns if columns is None else columns)

        missing_columns = [col for col in target_columns if col not in available_columns]
        if missing_columns:
            raise KeyError(f"Columns not found in dataframe: {', '.join(missing_columns)}")

        if strategy not in {"mean", "median", "mode"}:
            raise ValueError("Invalid strategy. Choose 'mean', 'median', or 'mode'.")

        if strategy == "mode":
            fills = self._data[target_columns].mode(dropna=True).iloc[0]
            self._data[target_columns] = self._data[target_columns].fillna(fills)
            return self._data

        numeric_columns = [col for col in target_columns if pd_types.is_numeric_dtype(self._data[col])]
        if not numeric_columns:
            raise TypeError("Mean and median strategies require at least one numeric column.")

        if strategy == "mean":
            fills = self._data[numeric_columns].mean()
        else:
            fills = self._data[numeric_columns].median()

        self._data[numeric_columns] = self._data[numeric_columns].fillna(fills)
        return self._data

    def standardize_columns(self) -> pd.DataFrame:
        """Normalize column names by lower-casing and collapsing whitespace."""

        def _clean_column(col: str) -> str:
            return "_".join(str(col).strip().lower().split())

        self._data = self._data.rename(columns=_clean_column)
        return self._data
