# outlier_detector.py
import pandas as pd
import numpy as np

class OutlierDetector:
    def __init__(self, data: pd.DataFrame):
        self._data = data  # private attribute to hold the dataframe

    def z_score_outliers(self, threshold=3):
        """Detects outliers using the Z-score method."""
        z_scores = np.abs((self._data - self._data.mean()) / self._data.std())
        return self._data[(z_scores < threshold).all(axis=1)]

    def iqr_outliers(self):
        """Detects outliers using the Interquartile Range (IQR) method."""
        Q1 = self._data.quantile(0.25)
        Q3 = self._data.quantile(0.75)
        IQR = Q3 - Q1
        return self._data[~((self._data < (Q1 - 1.5 * IQR)) | (self._data > (Q3 + 1.5 * IQR))).any(axis=1)]
