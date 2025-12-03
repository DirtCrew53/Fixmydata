import pandas as pd

from fixmydata import DataCleaner


def test_remove_duplicates_and_fill_missing_mean():
    df = pd.DataFrame({"a": [1, 1, None], "b": [1, 1, 1]})
    cleaner = DataCleaner(df)

    cleaned = cleaner.remove_duplicates().fill_missing(strategy="mean").data

    assert cleaned.shape == (2, 2)
    assert cleaned["a"].iloc[1] == 1


def test_standardize_columns_lowercases_and_snake_cases():
    df = pd.DataFrame({"First Name": ["Ann"], "Last Name": ["Lee"]})

    standardized = DataCleaner(df).standardize_columns().data

    assert list(standardized.columns) == ["first_name", "last_name"]
