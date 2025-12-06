import pandas as pd
from Fixmydata import DataCleaner, DataValidator, OutlierDetector

def test_fixmydata():
    print("=== Starting Fixmydata tests ===\n")
    

    df = pd.DataFrame({
        "A": [1, 2, None, 3, 1000],
        "B": [10, 20, 30, None, 400],
        "C": ["foo", "bar", None, "baz", "qux"]
    })
    
    print("Original DataFrame:")
    print(df, "\n")

    cleaner = DataCleaner(df)
    cleaned = cleaner.drop_missing()
    print("After drop_missing():")
    print(cleaned, "\n")
    
    cleaned = cleaner.fill_missing("C", "missing")
    print("After fill_missing('C'):")
    print(cleaned, "\n")
    
    cleaned = cleaner.standardize_whitespace(["C"])
    print("After standardize_whitespace(['C']):")
    print(cleaned, "\n")
    
    validator = DataValidator(cleaned)
    try:
        validator.validate_non_empty()
        print("validate_non_empty() passed.\n")
    except ValueError as e:
        print(f"validate_non_empty() failed: {e}\n")
    
    try:
        validator.validate_range("A", 0, 1000)
        print("validate_range('A', 0, 1000) passed.\n")
    except Exception as e:
        print(f"validate_range('A', 0, 1000) failed: {e}\n")
    
    # --- Test OutlierDetector ---
    od = OutlierDetector(cleaned)
    outliers_removed = od.z_score_outliers()
    print("After z_score_outliers():")
    print(outliers_removed, "\n")
    
    outliers_removed = od.iqr_outliers()
    print("After iqr_outliers():")
    print(outliers_removed, "\n")
    
    print("=== All tests completed ===")

if __name__ == "__main__":
    test_fixmydata()
