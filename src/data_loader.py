"""Functions for loading and inspecting project datasets."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


HISTORICAL_EXPECTED_COLUMNS = [
    "Account",
    "Coin",
    "Execution Price",
    "Size Tokens",
    "Size USD",
    "Side",
    "Timestamp IST",
    "Start Position",
    "Direction",
    "Closed PnL",
    "Transaction Hash",
    "Order ID",
    "Crossed",
    "Fee",
    "Trade ID",
    "Timestamp",
]

SENTIMENT_EXPECTED_COLUMNS = [
    "timestamp",
    "value",
    "classification",
    "date",
]


def load_csv(file_path: Path) -> pd.DataFrame:
    """Load a CSV file after validating that the path is usable."""
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"CSV file was not found: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    try:
        dataframe = pd.read_csv(file_path)
    except pd.errors.EmptyDataError as error:
        raise ValueError(f"CSV file is empty and cannot be loaded: {file_path}") from error
    except pd.errors.ParserError as error:
        raise ValueError(
            f"CSV file could not be parsed. It may be invalid or corrupted: "
            f"{file_path}"
        ) from error
    except UnicodeDecodeError as error:
        raise ValueError(
            f"CSV file could not be decoded. Check the file encoding: {file_path}"
        ) from error
    except OSError as error:
        raise OSError(f"CSV file could not be opened: {file_path}") from error

    print(
        f"Loaded {file_path.name} successfully: "
        f"{dataframe.shape[0]} rows, {dataframe.shape[1]} columns."
    )

    if dataframe.empty:
        print(f"Warning: {file_path.name} loaded successfully but is empty.")

    return dataframe


def load_project_datasets(
    historical_path: Path,
    sentiment_path: Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load the historical trader and sentiment datasets."""
    historical_dataframe = load_csv(historical_path)
    sentiment_dataframe = load_csv(sentiment_path)

    return historical_dataframe, sentiment_dataframe


def inspect_dataframe(
    dataframe: pd.DataFrame,
    dataset_name: str,
) -> None:
    """Print a read-only inspection summary for a DataFrame."""
    print("\n" + "=" * 80)
    print(f"Dataset Inspection: {dataset_name}")
    print("=" * 80)

    print("\nFirst five rows:")
    print(dataframe.head())

    print("\nLast five rows:")
    print(dataframe.tail())

    print("\nDataset size:")
    print(f"Rows: {dataframe.shape[0]}")
    print(f"Columns: {dataframe.shape[1]}")

    print("\nComplete column list:")
    print(list(dataframe.columns))

    print("\nData types:")
    print(dataframe.dtypes)

    print("\nMissing-value count:")
    print(dataframe.isna().sum())

    print("\nMissing-value percentage:")
    missing_percentage = dataframe.isna().mean().mul(100).round(2)
    print(missing_percentage)

    duplicate_rows = dataframe.duplicated().sum()
    print("\nDuplicate rows:")
    print(duplicate_rows)

    print("\nSummary statistics for numerical columns:")
    numerical_columns = dataframe.select_dtypes(include="number")
    if numerical_columns.empty:
        print("No numerical columns found.")
    else:
        print(numerical_columns.describe())

    print("\nSummary statistics for text columns:")
    text_columns = dataframe.select_dtypes(include=["object", "string", "category"])
    if text_columns.empty:
        print("No text columns found.")
    else:
        print(text_columns.describe())

    memory_usage_mb = dataframe.memory_usage(deep=True).sum() / (1024**2)
    print("\nMemory usage:")
    print(f"{memory_usage_mb:.2f} MB")

    print("\nIs the DataFrame empty?")
    print(dataframe.empty)


def validate_columns(
    dataframe: pd.DataFrame,
    expected_columns: list[str],
    dataset_name: str,
) -> None:
    """Compare actual DataFrame columns with expected columns."""
    actual_columns = list(dataframe.columns)
    missing_columns = [
        column for column in expected_columns if column not in actual_columns
    ]
    additional_columns = [
        column for column in actual_columns if column not in expected_columns
    ]

    print("\n" + "=" * 80)
    print(f"Column Validation: {dataset_name}")
    print("=" * 80)

    print("\nExpected columns:")
    print(expected_columns)

    print("\nActual columns:")
    print(actual_columns)

    print("\nMissing expected columns:")
    if missing_columns:
        print(missing_columns)
        print("Warning: Some expected columns are missing.")
    else:
        print("None")

    print("\nAdditional unexpected columns:")
    if additional_columns:
        print(additional_columns)
    else:
        print("None")

    if not missing_columns:
        print("\nAll expected columns are present.")


def show_unique_values(
    dataframe: pd.DataFrame,
    column_name: str,
    maximum_values: int = 20,
) -> None:
    """Print a short unique-value summary for a selected column."""
    print("\n" + "=" * 80)
    print(f"Unique Values: {column_name}")
    print("=" * 80)

    if column_name not in dataframe.columns:
        print(f"Warning: Column not found: {column_name}")
        return

    unique_count = dataframe[column_name].nunique(dropna=False)
    unique_values = dataframe[column_name].drop_duplicates().head(maximum_values)

    print(f"\nNumber of unique values including missing values: {unique_count}")
    print(f"\nFirst {maximum_values} unique values:")
    print(unique_values.to_list())

    print(f"\nValue counts, including missing values, limited to {maximum_values}:")
    print(dataframe[column_name].value_counts(dropna=False).head(maximum_values))
