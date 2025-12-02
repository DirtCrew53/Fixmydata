import pandas as pd
import pytest

from Fixmydata.outlier_detector import OutlierDetector


def test_z_score_outliers_ignores_non_numeric_columns():
    df = pd.DataFrame(
        {
            "value": [10, 12, 11, 200],
            "category": ["a", "a", "b", "b"],
        }
    )

    detector = OutlierDetector(df)
    filtered = detector.z_score_outliers(threshold=1)

    assert len(filtered) == 3
    assert "category" in filtered.columns


def test_iqr_outliers_requires_numeric_columns():
    df = pd.DataFrame({"label": ["a", "b", "c"]})
    detector = OutlierDetector(df)

    with pytest.raises(ValueError):
        detector.iqr_outliers()
