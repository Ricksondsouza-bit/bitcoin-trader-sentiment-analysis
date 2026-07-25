"""Functions for creating analysis-ready datasets and features."""

from pathlib import Path

import pandas as pd


def load_cleaned_datasets(
    historical_path: Path,
    sentiment_path: Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load the cleaned historical and sentiment datasets."""
    historical_path = Path(historical_path)
    sentiment_path = Path(sentiment_path)

    _validate_file_path(historical_path)
    _validate_file_path(sentiment_path)

    historical_dataframe = pd.read_csv(historical_path)
    sentiment_dataframe = pd.read_csv(sentiment_path)

    print(
        f"Loaded cleaned historical dataset: "
        f"{historical_dataframe.shape[0]} rows, "
        f"{historical_dataframe.shape[1]} columns."
    )
    print(
        f"Loaded cleaned sentiment dataset: "
        f"{sentiment_dataframe.shape[0]} rows, "
        f"{sentiment_dataframe.shape[1]} columns."
    )

    return historical_dataframe, sentiment_dataframe


def prepare_historical_for_merge(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Create a trade date column in a copy of the historical dataset."""
    prepared_dataframe = dataframe.copy()

    if "timestamp_ist" not in prepared_dataframe.columns:
        raise KeyError("Historical dataset must contain 'timestamp_ist'.")

    prepared_dataframe["timestamp_ist"] = pd.to_datetime(
        prepared_dataframe["timestamp_ist"],
        errors="coerce",
    )
    prepared_dataframe["trade_date"] = prepared_dataframe[
        "timestamp_ist"
    ].dt.normalize()

    missing_trade_dates = int(prepared_dataframe["trade_date"].isna().sum())
    print(f"Historical rows with missing trade_date: {missing_trade_dates}")
    print(
        "Historical trade date range: "
        f"{prepared_dataframe['trade_date'].min()} to "
        f"{prepared_dataframe['trade_date'].max()}"
    )

    return prepared_dataframe


def prepare_sentiment_for_merge(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Create a sentiment date column in a copy of the sentiment dataset."""
    prepared_dataframe = dataframe.copy()

    if "date" not in prepared_dataframe.columns:
        raise KeyError("Sentiment dataset must contain 'date'.")

    prepared_dataframe["sentiment_date"] = pd.to_datetime(
        prepared_dataframe["date"],
        errors="coerce",
    ).dt.normalize()
    prepared_dataframe = prepared_dataframe.rename(
        columns={
            "value": "sentiment_value",
            "classification": "sentiment_classification",
            "timestamp": "sentiment_timestamp",
        }
    )

    missing_sentiment_dates = int(prepared_dataframe["sentiment_date"].isna().sum())
    print(f"Sentiment rows with missing sentiment_date: {missing_sentiment_dates}")
    print(
        "Sentiment date range: "
        f"{prepared_dataframe['sentiment_date'].min()} to "
        f"{prepared_dataframe['sentiment_date'].max()}"
    )

    return prepared_dataframe


def merge_trader_sentiment_data(
    historical_dataframe: pd.DataFrame,
    sentiment_dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Merge cleaned trader data with daily sentiment data by date."""
    merged_dataframe = historical_dataframe.merge(
        sentiment_dataframe[
            [
                "sentiment_date",
                "sentiment_value",
                "sentiment_classification",
            ]
        ],
        how="left",
        left_on="trade_date",
        right_on="sentiment_date",
    )

    print(f"Historical rows before merge: {historical_dataframe.shape[0]}")
    print(f"Merged rows after merge: {merged_dataframe.shape[0]}")

    unmatched_rows = int(merged_dataframe["sentiment_value"].isna().sum())
    print(f"Rows without matching sentiment data: {unmatched_rows}")

    return merged_dataframe


def create_analysis_ready_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Create simple helper columns for later analysis."""
    analysis_dataframe = dataframe.copy()

    if "closed_pnl" not in analysis_dataframe.columns:
        raise KeyError("Merged dataset must contain 'closed_pnl'.")

    analysis_dataframe["is_profitable"] = analysis_dataframe["closed_pnl"] > 0

    return analysis_dataframe


def validate_analysis_ready_dataset(
    dataframe: pd.DataFrame,
) -> None:
    """Print basic validation checks for the analysis-ready dataset."""
    print("\n" + "=" * 80)
    print("Analysis-Ready Dataset Validation")
    print("=" * 80)
    print(f"Rows: {dataframe.shape[0]}")
    print(f"Columns: {dataframe.shape[1]}")
    print("\nColumn list:")
    print(list(dataframe.columns))
    print("\nMissing sentiment values:")
    print(dataframe[["sentiment_value", "sentiment_classification"]].isna().sum())
    print("\nDuplicate rows:")
    print(int(dataframe.duplicated().sum()))
    print("\nHelper columns created:")
    print(["trade_date", "sentiment_value", "sentiment_classification", "is_profitable"])


def save_analysis_ready_dataset(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """Save the analysis-ready merged dataset as a CSV file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_path, index=False)
    print(f"Saved analysis-ready dataset: {output_path}")


def create_analysis_ready_dataset(
    historical_dataframe: pd.DataFrame,
    sentiment_dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Create the final merged dataset for later analysis phases."""
    prepared_historical = prepare_historical_for_merge(historical_dataframe)
    prepared_sentiment = prepare_sentiment_for_merge(sentiment_dataframe)
    merged_dataframe = merge_trader_sentiment_data(
        prepared_historical,
        prepared_sentiment,
    )
    analysis_ready_dataframe = create_analysis_ready_columns(merged_dataframe)
    validate_analysis_ready_dataset(analysis_ready_dataframe)

    return analysis_ready_dataframe


def _validate_file_path(file_path: Path) -> None:
    """Validate that a path exists and points to a file."""
    if not file_path.exists():
        raise FileNotFoundError(f"File was not found: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
