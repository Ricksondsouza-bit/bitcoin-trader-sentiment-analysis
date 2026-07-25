"""Functions for cleaning and preparing project datasets."""

from pathlib import Path
import re

import pandas as pd


HISTORICAL_DATETIME_COLUMNS = {
    "timestamp_ist": {"dayfirst": True},
    "timestamp": {"unit": "ms"},
}

HISTORICAL_NUMERIC_COLUMNS = [
    "execution_price",
    "size_tokens",
    "size_usd",
    "start_position",
    "closed_pnl",
    "fee",
]

SENTIMENT_DATETIME_COLUMNS = {
    "date": {},
    "timestamp": {"unit": "s"},
}

SENTIMENT_NUMERIC_COLUMNS = [
    "value",
]


def standardize_column_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of a DataFrame with clean snake_case column names."""
    cleaned_dataframe = dataframe.copy()
    cleaned_dataframe.columns = [
        _to_snake_case(column) for column in cleaned_dataframe.columns
    ]

    return cleaned_dataframe


def remove_duplicate_rows(
    dataframe: pd.DataFrame,
    dataset_name: str,
) -> pd.DataFrame:
    """Return a copy of a DataFrame with exact duplicate rows removed."""
    duplicate_count = int(dataframe.duplicated().sum())
    print(f"{dataset_name} duplicate rows before cleaning: {duplicate_count}")

    cleaned_dataframe = dataframe.drop_duplicates().copy()
    removed_count = dataframe.shape[0] - cleaned_dataframe.shape[0]
    print(f"{dataset_name} duplicate rows removed: {removed_count}")

    return cleaned_dataframe


def convert_datetime_columns(
    dataframe: pd.DataFrame,
    datetime_columns: dict[str, dict[str, object]],
    dataset_name: str,
) -> pd.DataFrame:
    """Return a copy of a DataFrame with selected columns converted to datetime."""
    cleaned_dataframe = dataframe.copy()

    for column_name, options in datetime_columns.items():
        if column_name not in cleaned_dataframe.columns:
            print(f"Warning: {dataset_name} missing datetime column: {column_name}")
            continue

        cleaned_dataframe[column_name] = pd.to_datetime(
            cleaned_dataframe[column_name],
            errors="coerce",
            **options,
        )
        missing_after_conversion = int(cleaned_dataframe[column_name].isna().sum())
        print(
            f"{dataset_name} datetime column converted: {column_name} "
            f"({missing_after_conversion} missing values after conversion)"
        )

    return cleaned_dataframe


def convert_numeric_columns(
    dataframe: pd.DataFrame,
    numeric_columns: list[str],
    dataset_name: str,
) -> pd.DataFrame:
    """Return a copy of a DataFrame with selected columns converted to numeric."""
    cleaned_dataframe = dataframe.copy()

    for column_name in numeric_columns:
        if column_name not in cleaned_dataframe.columns:
            print(f"Warning: {dataset_name} missing numeric column: {column_name}")
            continue

        cleaned_dataframe[column_name] = pd.to_numeric(
            cleaned_dataframe[column_name],
            errors="coerce",
        )
        missing_after_conversion = int(cleaned_dataframe[column_name].isna().sum())
        print(
            f"{dataset_name} numeric column converted: {column_name} "
            f"({missing_after_conversion} missing values after conversion)"
        )

    return cleaned_dataframe


def validate_categorical_values(
    dataframe: pd.DataFrame,
    categorical_columns: list[str],
    dataset_name: str,
) -> None:
    """Print unique values for selected categorical columns without modifying data."""
    print("\n" + "=" * 80)
    print(f"Categorical Value Check: {dataset_name}")
    print("=" * 80)

    for column_name in categorical_columns:
        if column_name not in dataframe.columns:
            print(f"Warning: {dataset_name} missing categorical column: {column_name}")
            continue

        unique_values = dataframe[column_name].drop_duplicates().head(20).to_list()
        unique_count = int(dataframe[column_name].nunique(dropna=False))
        print(f"\n{column_name}: {unique_count} unique values")
        print(unique_values)


def clean_historical_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean a copy of the historical trader dataset for later analysis."""
    dataset_name = "Historical Trader Data"
    print("\n" + "=" * 80)
    print(f"Cleaning Dataset: {dataset_name}")
    print("=" * 80)
    print(f"Shape before cleaning: {dataframe.shape}")

    cleaned_dataframe = standardize_column_names(dataframe)
    cleaned_dataframe = remove_duplicate_rows(cleaned_dataframe, dataset_name)
    cleaned_dataframe = convert_datetime_columns(
        cleaned_dataframe,
        HISTORICAL_DATETIME_COLUMNS,
        dataset_name,
    )
    cleaned_dataframe = convert_numeric_columns(
        cleaned_dataframe,
        HISTORICAL_NUMERIC_COLUMNS,
        dataset_name,
    )
    validate_categorical_values(
        cleaned_dataframe,
        ["coin", "side", "direction", "crossed"],
        dataset_name,
    )

    print(f"\nShape after cleaning: {cleaned_dataframe.shape}")
    print("\nMissing values after cleaning:")
    print(cleaned_dataframe.isna().sum())
    print("\nData types after cleaning:")
    print(cleaned_dataframe.dtypes)

    return cleaned_dataframe


def clean_sentiment_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean a copy of the Fear and Greed Index dataset for later analysis."""
    dataset_name = "Fear and Greed Index"
    print("\n" + "=" * 80)
    print(f"Cleaning Dataset: {dataset_name}")
    print("=" * 80)
    print(f"Shape before cleaning: {dataframe.shape}")

    cleaned_dataframe = standardize_column_names(dataframe)
    cleaned_dataframe = remove_duplicate_rows(cleaned_dataframe, dataset_name)
    cleaned_dataframe = convert_datetime_columns(
        cleaned_dataframe,
        SENTIMENT_DATETIME_COLUMNS,
        dataset_name,
    )
    cleaned_dataframe = convert_numeric_columns(
        cleaned_dataframe,
        SENTIMENT_NUMERIC_COLUMNS,
        dataset_name,
    )
    validate_categorical_values(
        cleaned_dataframe,
        ["classification"],
        dataset_name,
    )

    print(f"\nShape after cleaning: {cleaned_dataframe.shape}")
    print("\nMissing values after cleaning:")
    print(cleaned_dataframe.isna().sum())
    print("\nData types after cleaning:")
    print(cleaned_dataframe.dtypes)

    return cleaned_dataframe


def save_processed_dataset(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """Save a processed dataset as a CSV file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_path, index=False)
    print(f"Saved processed dataset: {output_path}")


def _to_snake_case(column_name: str) -> str:
    """Convert a column name into snake_case."""
    cleaned_name = column_name.strip().lower()
    cleaned_name = re.sub(r"[^a-z0-9]+", "_", cleaned_name)
    cleaned_name = re.sub(r"_+", "_", cleaned_name)

    return cleaned_name.strip("_")
