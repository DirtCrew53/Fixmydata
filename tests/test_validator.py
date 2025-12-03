import pandas as pd
import pytest

from fixmydata import DataValidator


def test_validate_range_passes_for_in_range_values():
    df = pd.DataFrame({"age": [25, 30, 35]})

    validated = DataValidator(df).validate_range("age", 20, 40)

    assert validated.equals(df)


def test_validate_non_empty_raises_on_nulls():
    df = pd.DataFrame({"age": [25, None]})

    with pytest.raises(ValueError):
        DataValidator(df).validate_non_empty()
