"""Functions for exploratory data analysis summaries."""

from pathlib import Path

import pandas as pd


def load_analysis_ready_dataset(file_path: Path) -> pd.DataFrame:
    """Load the merged analysis-ready dataset."""
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Analysis-ready dataset was not found: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    dataframe = pd.read_csv(file_path)
    print(
        f"Loaded analysis-ready dataset: "
        f"{dataframe.shape[0]} rows, {dataframe.shape[1]} columns."
    )

    return dataframe


def print_dataset_overview(dataframe: pd.DataFrame) -> None:
    """Print a simple overview of the analysis-ready dataset."""
    print("\n" + "=" * 80)
    print("Phase 5 Dataset Overview")
    print("=" * 80)
    print(f"Rows: {dataframe.shape[0]}")
    print(f"Columns: {dataframe.shape[1]}")
    print("\nColumn list:")
    print(list(dataframe.columns))
    print("\nMissing sentiment values:")
    print(dataframe[["sentiment_value", "sentiment_classification"]].isna().sum())
    print("\nData types:")
    print(dataframe.dtypes)


def create_overall_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Create one-row overall trading summary metrics."""
    total_trades = len(dataframe)
    win_count = int(dataframe["is_profitable"].sum())
    loss_count = int(total_trades - win_count)
    win_rate = _safe_percentage(win_count, total_trades)

    summary = {
        "total_trades": total_trades,
        "unique_accounts": dataframe["account"].nunique(dropna=True),
        "unique_coins": dataframe["coin"].nunique(dropna=True),
        "total_closed_pnl": dataframe["closed_pnl"].sum(),
        "average_closed_pnl": dataframe["closed_pnl"].mean(),
        "median_closed_pnl": dataframe["closed_pnl"].median(),
        "minimum_closed_pnl": dataframe["closed_pnl"].min(),
        "maximum_closed_pnl": dataframe["closed_pnl"].max(),
        "win_count": win_count,
        "loss_count": loss_count,
        "win_rate_percent": win_rate,
        "average_trade_size_usd": dataframe["size_usd"].mean(),
        "total_fees": dataframe["fee"].sum(),
        "missing_sentiment_rows": int(dataframe["sentiment_value"].isna().sum()),
    }

    return pd.DataFrame([summary])


def create_sentiment_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Summarize trading metrics by sentiment classification."""
    return _grouped_summary(dataframe, "sentiment_classification")


def create_direction_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Summarize trading metrics by trade direction."""
    return _grouped_summary(dataframe, "direction")


def create_coin_summary(
    dataframe: pd.DataFrame,
    top_n: int = 20,
) -> pd.DataFrame:
    """Summarize trading metrics for the top coins by trade count."""
    summary = _grouped_summary(dataframe, "coin")

    return summary.sort_values("trade_count", ascending=False).head(top_n)


def create_missing_sentiment_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Create a report for rows that did not match sentiment data."""
    missing_sentiment = dataframe[dataframe["sentiment_value"].isna()].copy()

    if missing_sentiment.empty:
        return pd.DataFrame(
            [
                {
                    "missing_sentiment_rows": 0,
                    "affected_trade_dates": "",
                }
            ]
        )

    grouped = (
        missing_sentiment.groupby("trade_date", dropna=False)
        .agg(
            missing_sentiment_rows=("trade_date", "size"),
            unique_accounts=("account", "nunique"),
            unique_coins=("coin", "nunique"),
            total_closed_pnl=("closed_pnl", "sum"),
        )
        .reset_index()
    )

    return grouped


def create_all_eda_summaries(
    dataframe: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """Create all Phase 5 EDA summary tables."""
    return {
        "overall_summary": create_overall_summary(dataframe),
        "sentiment_summary": create_sentiment_summary(dataframe),
        "direction_summary": create_direction_summary(dataframe),
        "coin_summary": create_coin_summary(dataframe),
        "missing_sentiment_summary": create_missing_sentiment_summary(dataframe),
    }


def save_summary_tables(
    summaries: dict[str, pd.DataFrame],
    reports_dir: Path,
) -> None:
    """Save all EDA summary tables as CSV files."""
    reports_dir = Path(reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    for report_name, summary_dataframe in summaries.items():
        output_path = reports_dir / f"{report_name}.csv"
        summary_dataframe.to_csv(output_path, index=False)
        print(f"Saved report: {output_path}")


def print_summary_tables(summaries: dict[str, pd.DataFrame]) -> None:
    """Print EDA summary tables in a readable way."""
    for report_name, summary_dataframe in summaries.items():
        print("\n" + "=" * 80)
        print(report_name.replace("_", " ").title())
        print("=" * 80)
        print(summary_dataframe)


def _grouped_summary(
    dataframe: pd.DataFrame,
    group_column: str,
) -> pd.DataFrame:
    """Create reusable grouped trading metrics."""
    grouped = (
        dataframe.groupby(group_column, dropna=False)
        .agg(
            trade_count=("closed_pnl", "size"),
            total_closed_pnl=("closed_pnl", "sum"),
            average_closed_pnl=("closed_pnl", "mean"),
            median_closed_pnl=("closed_pnl", "median"),
            win_count=("is_profitable", "sum"),
            average_trade_size_usd=("size_usd", "mean"),
            total_fees=("fee", "sum"),
        )
        .reset_index()
    )

    grouped["win_rate_percent"] = (
        grouped["win_count"] / grouped["trade_count"] * 100
    ).round(2)

    return grouped


def _safe_percentage(numerator: int, denominator: int) -> float:
    """Calculate a percentage while avoiding division by zero."""
    if denominator == 0:
        return 0.0

    return round(numerator / denominator * 100, 2)
