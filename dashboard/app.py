"""Streamlit dashboard for trader sentiment analysis."""

from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
CHARTS_DIR = PROJECT_ROOT / "outputs" / "charts"
PUBLIC_CHARTS_DIR = PROJECT_ROOT / "docs" / "assets"

MERGED_DATA_PATH = PROCESSED_DATA_DIR / "trader_sentiment_merged.csv"

REPORT_PATHS = {
    "overall": REPORTS_DIR / "overall_summary.csv",
    "sentiment": REPORTS_DIR / "sentiment_summary.csv",
    "direction": REPORTS_DIR / "direction_summary.csv",
    "coin": REPORTS_DIR / "coin_summary.csv",
    "missing_sentiment": REPORTS_DIR / "missing_sentiment_summary.csv",
}

CHART_PATHS = {
    "sentiment_distribution": CHARTS_DIR / "sentiment_distribution.png",
    "pnl_by_sentiment": CHARTS_DIR / "pnl_by_sentiment.png",
    "average_pnl_by_sentiment": CHARTS_DIR / "average_pnl_by_sentiment.png",
    "win_rate_by_sentiment": CHARTS_DIR / "win_rate_by_sentiment.png",
    "trade_count_by_direction": CHARTS_DIR / "trade_count_by_direction.png",
    "pnl_by_direction": CHARTS_DIR / "pnl_by_direction.png",
    "top_coins_by_trade_count": CHARTS_DIR / "top_coins_by_trade_count.png",
    "top_coins_by_pnl": CHARTS_DIR / "top_coins_by_pnl.png",
    "closed_pnl_distribution": CHARTS_DIR / "closed_pnl_distribution.png",
}


st.set_page_config(
    page_title="Trader Sentiment Analysis",
    page_icon="BTC",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def load_merged_dataset() -> pd.DataFrame:
    """Load the merged analysis-ready dataset."""
    dataframe = pd.read_csv(MERGED_DATA_PATH)
    dataframe["trade_date"] = pd.to_datetime(dataframe["trade_date"], errors="coerce")
    dataframe["sentiment_filter"] = dataframe["sentiment_classification"].fillna(
        "Missing sentiment"
    )

    return dataframe


@st.cache_data(show_spinner=False)
def load_report(path: Path) -> pd.DataFrame:
    """Load a summary report CSV."""
    return pd.read_csv(path)


def validate_required_files() -> list[Path]:
    """Return a list of required summary files that are missing."""
    return [path for path in REPORT_PATHS.values() if not path.exists()]


def format_number(value: float) -> str:
    """Format a number for display."""
    return f"{value:,.2f}"


def format_integer(value: float) -> str:
    """Format an integer-like value for display."""
    return f"{int(value):,}"


def calculate_filtered_metrics(dataframe: pd.DataFrame) -> dict[str, float]:
    """Calculate dashboard metrics from the filtered dataset."""
    total_trades = len(dataframe)
    win_count = int(dataframe["is_profitable"].sum())
    win_rate = (win_count / total_trades * 100) if total_trades else 0.0

    return {
        "total_trades": total_trades,
        "total_closed_pnl": dataframe["closed_pnl"].sum(),
        "win_rate": win_rate,
        "average_trade_size": dataframe["size_usd"].mean() if total_trades else 0.0,
        "total_fees": dataframe["fee"].sum(),
    }


def render_metric_row(metrics: dict[str, float]) -> None:
    """Render top-level filtered metrics."""
    columns = st.columns(5)
    columns[0].metric("Trades", format_integer(metrics["total_trades"]))
    columns[1].metric("Total Closed PnL", format_number(metrics["total_closed_pnl"]))
    columns[2].metric("Win Rate", f"{metrics['win_rate']:.2f}%")
    columns[3].metric(
        "Avg Trade Size USD",
        format_number(metrics["average_trade_size"]),
    )
    columns[4].metric("Total Fees", format_number(metrics["total_fees"]))


def render_chart(path: Path, caption: str) -> None:
    """Render a chart image from full local outputs or public preview assets."""
    public_path = PUBLIC_CHARTS_DIR / path.name

    if path.exists():
        st.image(str(path), caption=caption, width="stretch")
    elif public_path.exists():
        st.image(str(public_path), caption=caption, width="stretch")
    else:
        st.warning(f"Missing chart file: {path.name}")


def apply_dashboard_filters(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Render sidebar filters and return the filtered dataset."""
    with st.sidebar:
        st.header("Filters")

        sentiment_options = sorted(dataframe["sentiment_filter"].unique().tolist())
        selected_sentiments = st.multiselect(
            "Sentiment",
            options=sentiment_options,
            default=sentiment_options,
        )

        coin_options = sorted(dataframe["coin"].dropna().unique().tolist())
        selected_coins = st.multiselect(
            "Coin",
            options=coin_options,
            default=coin_options,
        )

        direction_options = sorted(dataframe["direction"].dropna().unique().tolist())
        selected_directions = st.multiselect(
            "Direction",
            options=direction_options,
            default=direction_options,
        )

        minimum_date = dataframe["trade_date"].min().date()
        maximum_date = dataframe["trade_date"].max().date()
        selected_date_range = st.date_input(
            "Trade Date Range",
            value=(minimum_date, maximum_date),
            min_value=minimum_date,
            max_value=maximum_date,
        )

    filtered_dataframe = dataframe.copy()

    if selected_sentiments:
        filtered_dataframe = filtered_dataframe[
            filtered_dataframe["sentiment_filter"].isin(selected_sentiments)
        ]

    if selected_coins:
        filtered_dataframe = filtered_dataframe[filtered_dataframe["coin"].isin(selected_coins)]

    if selected_directions:
        filtered_dataframe = filtered_dataframe[
            filtered_dataframe["direction"].isin(selected_directions)
        ]

    if len(selected_date_range) == 2:
        start_date, end_date = selected_date_range
        filtered_dataframe = filtered_dataframe[
            (filtered_dataframe["trade_date"].dt.date >= start_date)
            & (filtered_dataframe["trade_date"].dt.date <= end_date)
        ]

    return filtered_dataframe


missing_files = validate_required_files()

st.title("Bitcoin Market Sentiment and Trader Performance Analysis")
st.caption("Interactive dashboard built from processed project outputs.")

if missing_files:
    st.error("Some required dashboard summary files are missing.")
    st.dataframe(
        pd.DataFrame({"missing_file": [str(path) for path in missing_files]}),
        width="stretch",
    )
    st.stop()

overall_summary = load_report(REPORT_PATHS["overall"])
sentiment_summary = load_report(REPORT_PATHS["sentiment"])
direction_summary = load_report(REPORT_PATHS["direction"])
coin_summary = load_report(REPORT_PATHS["coin"])
missing_sentiment_summary = load_report(REPORT_PATHS["missing_sentiment"])
has_merged_dataset = MERGED_DATA_PATH.exists()

st.success("Dashboard inputs loaded successfully.")

if has_merged_dataset:
    merged_df = load_merged_dataset()
    filtered_df = apply_dashboard_filters(merged_df)
else:
    filtered_df = pd.DataFrame()
    st.info(
        "Public deployment mode is using summary reports only. "
        "Add data/processed/trader_sentiment_merged.csv locally for filters and row previews."
    )

st.subheader("Overall Project Metrics")
overall_row = overall_summary.iloc[0]
overall_columns = st.columns(7)
overall_columns[0].metric("Total Trades", format_integer(overall_row["total_trades"]))
overall_columns[1].metric(
    "Unique Accounts",
    format_integer(overall_row["unique_accounts"]),
)
overall_columns[2].metric("Unique Coins", format_integer(overall_row["unique_coins"]))
overall_columns[3].metric(
    "Total Closed PnL",
    format_number(overall_row["total_closed_pnl"]),
)
overall_columns[4].metric("Win Rate", f"{overall_row['win_rate_percent']:.2f}%")
overall_columns[5].metric("Total Fees", format_number(overall_row["total_fees"]))
overall_columns[6].metric(
    "Missing Sentiment",
    format_integer(overall_row["missing_sentiment_rows"]),
)

if has_merged_dataset:
    st.subheader("Filtered Dataset Summary")
    render_metric_row(calculate_filtered_metrics(filtered_df))

    if filtered_df.empty:
        st.warning("No rows match the selected filters.")

sentiment_tab, direction_tab, coin_tab, pnl_tab, missing_tab, data_tab = st.tabs(
    [
        "Sentiment",
        "Direction",
        "Coins",
        "PnL",
        "Missing Sentiment",
        "Data Preview",
    ]
)

with sentiment_tab:
    st.subheader("Sentiment Analysis")
    st.dataframe(sentiment_summary, width="stretch")
    left_column, right_column = st.columns(2)
    with left_column:
        render_chart(
            CHART_PATHS["sentiment_distribution"],
            "Trade count by market sentiment",
        )
        render_chart(
            CHART_PATHS["average_pnl_by_sentiment"],
            "Average Closed PnL by market sentiment",
        )
    with right_column:
        render_chart(CHART_PATHS["pnl_by_sentiment"], "Total Closed PnL by sentiment")
        render_chart(CHART_PATHS["win_rate_by_sentiment"], "Win rate by sentiment")

with direction_tab:
    st.subheader("Direction Analysis")
    st.dataframe(direction_summary, width="stretch")
    left_column, right_column = st.columns(2)
    with left_column:
        render_chart(
            CHART_PATHS["trade_count_by_direction"],
            "Trade count by direction",
        )
    with right_column:
        render_chart(CHART_PATHS["pnl_by_direction"], "Total Closed PnL by direction")

with coin_tab:
    st.subheader("Coin Analysis")
    st.dataframe(coin_summary, width="stretch")
    left_column, right_column = st.columns(2)
    with left_column:
        render_chart(
            CHART_PATHS["top_coins_by_trade_count"],
            "Top coins by trade count",
        )
    with right_column:
        render_chart(CHART_PATHS["top_coins_by_pnl"], "Top coins by total Closed PnL")

with pnl_tab:
    st.subheader("Closed PnL Distribution")
    render_chart(
        CHART_PATHS["closed_pnl_distribution"],
        "Closed PnL distribution clipped to the 1st and 99th percentiles",
    )

with missing_tab:
    st.subheader("Missing Sentiment Report")
    missing_rows = int(overall_row["missing_sentiment_rows"])
    if missing_rows > 0:
        st.warning(f"{missing_rows} rows do not have matching sentiment data.")
    else:
        st.success("No missing sentiment rows found.")
    st.dataframe(missing_sentiment_summary, width="stretch")

with data_tab:
    if has_merged_dataset:
        st.subheader("Filtered Data Preview")
        st.caption("Showing up to 500 filtered rows.")
        preview_columns = [
            "trade_date",
            "coin",
            "direction",
            "side",
            "size_usd",
            "closed_pnl",
            "sentiment_value",
            "sentiment_classification",
            "is_profitable",
        ]
        st.dataframe(filtered_df[preview_columns].head(500), width="stretch")
    else:
        st.subheader("Public Summary Preview")
        st.dataframe(sentiment_summary, width="stretch")
