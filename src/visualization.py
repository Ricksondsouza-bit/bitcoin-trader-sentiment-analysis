"""Functions for creating visual analysis charts."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


CHART_STYLE = "whitegrid"


def load_report_tables(reports_dir: Path) -> dict[str, pd.DataFrame]:
    """Load Phase 5 report CSV files used for chart creation."""
    reports_dir = Path(reports_dir)
    report_files = {
        "overall_summary": "overall_summary.csv",
        "sentiment_summary": "sentiment_summary.csv",
        "direction_summary": "direction_summary.csv",
        "coin_summary": "coin_summary.csv",
        "missing_sentiment_summary": "missing_sentiment_summary.csv",
    }

    report_tables = {}

    for report_name, file_name in report_files.items():
        report_path = reports_dir / file_name

        if not report_path.exists():
            raise FileNotFoundError(f"Report file was not found: {report_path}")

        report_tables[report_name] = pd.read_csv(report_path)
        print(f"Loaded report: {report_path}")

    return report_tables


def create_all_charts(
    merged_dataframe: pd.DataFrame,
    report_tables: dict[str, pd.DataFrame],
    charts_dir: Path,
) -> list[Path]:
    """Create and save all Phase 6 charts."""
    charts_dir = Path(charts_dir)
    charts_dir.mkdir(parents=True, exist_ok=True)

    sns.set_theme(style=CHART_STYLE)

    sentiment_summary = _clean_sentiment_summary(
        report_tables["sentiment_summary"]
    )
    direction_summary = report_tables["direction_summary"].copy()
    coin_summary = report_tables["coin_summary"].copy()

    chart_paths = [
        plot_sentiment_distribution(sentiment_summary, charts_dir),
        plot_pnl_by_sentiment(sentiment_summary, charts_dir),
        plot_average_pnl_by_sentiment(sentiment_summary, charts_dir),
        plot_win_rate_by_sentiment(sentiment_summary, charts_dir),
        plot_trade_count_by_direction(direction_summary, charts_dir),
        plot_pnl_by_direction(direction_summary, charts_dir),
        plot_top_coins_by_trade_count(coin_summary, charts_dir),
        plot_top_coins_by_pnl(coin_summary, charts_dir),
        plot_closed_pnl_distribution(merged_dataframe, charts_dir),
    ]

    return chart_paths


def plot_sentiment_distribution(
    sentiment_summary: pd.DataFrame,
    charts_dir: Path,
) -> Path:
    """Save a chart showing trade count by sentiment."""
    output_path = Path(charts_dir) / "sentiment_distribution.png"
    ordered_data = sentiment_summary.sort_values("trade_count", ascending=False)

    _create_bar_chart(
        ordered_data,
        x_column="sentiment_classification",
        y_column="trade_count",
        title="Trade Count by Market Sentiment",
        x_label="Sentiment",
        y_label="Trade Count",
        output_path=output_path,
    )

    return output_path


def plot_pnl_by_sentiment(
    sentiment_summary: pd.DataFrame,
    charts_dir: Path,
) -> Path:
    """Save a chart showing total Closed PnL by sentiment."""
    output_path = Path(charts_dir) / "pnl_by_sentiment.png"

    _create_bar_chart(
        sentiment_summary,
        x_column="sentiment_classification",
        y_column="total_closed_pnl",
        title="Total Closed PnL by Market Sentiment",
        x_label="Sentiment",
        y_label="Total Closed PnL",
        output_path=output_path,
    )

    return output_path


def plot_average_pnl_by_sentiment(
    sentiment_summary: pd.DataFrame,
    charts_dir: Path,
) -> Path:
    """Save a chart showing average Closed PnL by sentiment."""
    output_path = Path(charts_dir) / "average_pnl_by_sentiment.png"

    _create_bar_chart(
        sentiment_summary,
        x_column="sentiment_classification",
        y_column="average_closed_pnl",
        title="Average Closed PnL by Market Sentiment",
        x_label="Sentiment",
        y_label="Average Closed PnL",
        output_path=output_path,
    )

    return output_path


def plot_win_rate_by_sentiment(
    sentiment_summary: pd.DataFrame,
    charts_dir: Path,
) -> Path:
    """Save a chart showing win rate by sentiment."""
    output_path = Path(charts_dir) / "win_rate_by_sentiment.png"

    _create_bar_chart(
        sentiment_summary,
        x_column="sentiment_classification",
        y_column="win_rate_percent",
        title="Win Rate by Market Sentiment",
        x_label="Sentiment",
        y_label="Win Rate (%)",
        output_path=output_path,
    )

    return output_path


def plot_trade_count_by_direction(
    direction_summary: pd.DataFrame,
    charts_dir: Path,
) -> Path:
    """Save a chart showing trade count by direction."""
    output_path = Path(charts_dir) / "trade_count_by_direction.png"
    ordered_data = direction_summary.sort_values("trade_count", ascending=True)

    _create_horizontal_bar_chart(
        ordered_data,
        x_column="trade_count",
        y_column="direction",
        title="Trade Count by Direction",
        x_label="Trade Count",
        y_label="Direction",
        output_path=output_path,
    )

    return output_path


def plot_pnl_by_direction(
    direction_summary: pd.DataFrame,
    charts_dir: Path,
) -> Path:
    """Save a chart showing total Closed PnL by direction."""
    output_path = Path(charts_dir) / "pnl_by_direction.png"
    ordered_data = direction_summary.sort_values("total_closed_pnl", ascending=True)

    _create_horizontal_bar_chart(
        ordered_data,
        x_column="total_closed_pnl",
        y_column="direction",
        title="Total Closed PnL by Direction",
        x_label="Total Closed PnL",
        y_label="Direction",
        output_path=output_path,
    )

    return output_path


def plot_top_coins_by_trade_count(
    coin_summary: pd.DataFrame,
    charts_dir: Path,
) -> Path:
    """Save a chart showing top coins by trade count."""
    output_path = Path(charts_dir) / "top_coins_by_trade_count.png"
    ordered_data = coin_summary.sort_values("trade_count", ascending=True)

    _create_horizontal_bar_chart(
        ordered_data,
        x_column="trade_count",
        y_column="coin",
        title="Top Coins by Trade Count",
        x_label="Trade Count",
        y_label="Coin",
        output_path=output_path,
    )

    return output_path


def plot_top_coins_by_pnl(
    coin_summary: pd.DataFrame,
    charts_dir: Path,
) -> Path:
    """Save a chart showing top coins by total Closed PnL."""
    output_path = Path(charts_dir) / "top_coins_by_pnl.png"
    ordered_data = coin_summary.sort_values("total_closed_pnl", ascending=True)

    _create_horizontal_bar_chart(
        ordered_data,
        x_column="total_closed_pnl",
        y_column="coin",
        title="Top Coins by Total Closed PnL",
        x_label="Total Closed PnL",
        y_label="Coin",
        output_path=output_path,
    )

    return output_path


def plot_closed_pnl_distribution(
    merged_dataframe: pd.DataFrame,
    charts_dir: Path,
) -> Path:
    """Save a simple distribution chart for Closed PnL."""
    output_path = Path(charts_dir) / "closed_pnl_distribution.png"
    clipped_pnl = merged_dataframe["closed_pnl"].clip(
        lower=merged_dataframe["closed_pnl"].quantile(0.01),
        upper=merged_dataframe["closed_pnl"].quantile(0.99),
    )

    fig, axis = plt.subplots(figsize=(10, 6))
    sns.histplot(clipped_pnl, bins=50, kde=False, ax=axis, color="#2F6B8F")
    axis.set_title("Closed PnL Distribution (1st to 99th Percentile)")
    axis.set_xlabel("Closed PnL")
    axis.set_ylabel("Trade Count")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Saved chart: {output_path}")

    return output_path


def _create_bar_chart(
    dataframe: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str,
    x_label: str,
    y_label: str,
    output_path: Path,
) -> None:
    """Create a vertical bar chart."""
    fig, axis = plt.subplots(figsize=(10, 6))
    sns.barplot(data=dataframe, x=x_column, y=y_column, ax=axis, color="#2F6B8F")
    axis.set_title(title)
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    axis.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Saved chart: {output_path}")


def _create_horizontal_bar_chart(
    dataframe: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str,
    x_label: str,
    y_label: str,
    output_path: Path,
) -> None:
    """Create a horizontal bar chart."""
    fig, axis = plt.subplots(figsize=(10, 7))
    sns.barplot(data=dataframe, x=x_column, y=y_column, ax=axis, color="#2F6B8F")
    axis.set_title(title)
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Saved chart: {output_path}")


def _clean_sentiment_summary(sentiment_summary: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of sentiment summary with a readable missing label."""
    cleaned_summary = sentiment_summary.copy()
    cleaned_summary["sentiment_classification"] = cleaned_summary[
        "sentiment_classification"
    ].fillna("Missing sentiment")

    return cleaned_summary
