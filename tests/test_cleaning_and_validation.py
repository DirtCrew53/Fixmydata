import pandas as pd
import pytest

from Fixmydata.cleaning import DataCleaner
from Fixmydata.data_validator import DataValidator


def test_fill_missing_mean_uses_numeric_columns_only():
    df = pd.DataFrame({"age": [20, None, 30], "dept": ["a", "b", None]})
    cleaner = DataCleaner(df)

    result = cleaner.fill_missing("mean")

    assert result.loc[1, "age"] == pytest.approx(25)
    assert pd.isna(result.loc[2, "dept"])


def test_fill_missing_mode_handles_non_numeric_columns():
    df = pd.DataFrame({"age": [20, None, 20], "dept": ["a", "b", None]})
    cleaner = DataCleaner(df)

    result = cleaner.fill_missing("mode", columns=["dept"])

    assert result.loc[2, "dept"] == "a"
    # age remains untouched since only dept requested
    assert pd.isna(result.loc[1, "age"])


def test_fill_missing_non_numeric_mean_raises():
    df = pd.DataFrame({"dept": ["a", None, "b"]})
    cleaner = DataCleaner(df)

    with pytest.raises(TypeError):
        cleaner.fill_missing("mean")


def test_validate_range_checks_type_and_bounds():
    df = pd.DataFrame({"age": [25, 30, 40]})
    validator = DataValidator(df)

    validated = validator.validate_range("age", 20, 50)

    assert validated.equals(df)


def test_validate_range_rejects_missing_column_and_non_numeric():
    df = pd.DataFrame({"dept": ["sales", "hr"]})
    validator = DataValidator(df)

    with pytest.raises(KeyError):
        validator.validate_range("missing", 0, 1)

    with pytest.raises(TypeError):
        validator.validate_range("dept", 0, 1)


def test_validate_non_empty_fails_on_missing_values_or_empty_frame():
    df_with_null = pd.DataFrame({"age": [1, None]})
    validator = DataValidator(df_with_null)
    with pytest.raises(ValueError):
        validator.validate_non_empty()

    empty = pd.DataFrame()
    validator = DataValidator(empty)
    with pytest.raises(ValueError):
        validator.validate_non_empty()
