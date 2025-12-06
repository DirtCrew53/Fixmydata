import os
import pandas as pd
from Fixmydata import DataCleaner, DataValidator, OutlierDetector, utils

def test_datasets():
    print("=== Starting Fixmydata dataset tests ===\n")

    datasets_path = os.path.join(os.path.dirname(__file__), "..", "datasets")
    csv_files = [f for f in os.listdir(datasets_path) if f.endswith(".csv")]

    if not csv_files:
        print("No CSV files found in datasets/")
        return

    for file in csv_files:
        file_path = os.path.join(datasets_path, file)
        print(f"--- Testing dataset: {file} ---")

        df = utils.load_csv(file_path)
        print("Original DataFrame shape:", df.shape)

        df = utils.clean_column_names(df)

        cleaner = DataCleaner(df)
        try:
            cleaned = cleaner.drop_missing()
            print("drop_missing() successful, shape:", cleaned.shape)
        except Exception as e:
            print(f"drop_missing() error: {e}")
            continue

        for col in cleaned.select_dtypes(include='object').columns:
            cleaned = cleaner.fill_missing(col, "missing")

        validator = DataValidator(cleaned)
        try:
            validator.validate_non_empty()
            print("validate_non_empty() passed")
        except Exception as e:
            print(f"validate_non_empty() failed: {e}")

        numeric_cols = cleaned.select_dtypes(include='number').columns
        for col in numeric_cols:
            try:
                validator.validate_range(col, cleaned[col].min(), cleaned[col].max())
            except Exception as e:
                print(f"validate_range() failed for {col}: {e}")

        od = OutlierDetector(cleaned)
        try:
            outliers_removed_z = od.z_score_outliers()
            print("z_score_outliers() removed rows, new shape:", outliers_removed_z.shape)
        except Exception as e:
            print(f"z_score_outliers() error: {e}")

        try:
            outliers_removed_iqr = od.iqr_outliers()
            print("iqr_outliers() removed rows, new shape:", outliers_removed_iqr.shape)
        except Exception as e:
            print(f"iqr_outliers() error: {e}")

        print("\n")

    print("=== Dataset tests completed ===")

if __name__ == "__main__":
    test_datasets()
