import pandas as pd

from fixmydata import OutlierDetector


def test_z_score_filters_high_outlier():
    df = pd.DataFrame({"value": [10, 10, 11, 9, 12, 100]})

    filtered = OutlierDetector(df).z_score_outliers(threshold=1.5)

    assert len(filtered) == 5
    assert 100 not in filtered["value"].values


def test_iqr_filters_low_outlier():
    df = pd.DataFrame({"value": [-100, 10, 12, 14, 16]})

    filtered = OutlierDetector(df).iqr_outliers()

    assert len(filtered) == 4
    assert -100 not in filtered["value"].values
