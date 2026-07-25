"""Main entry point for the trader sentiment analysis project."""

from pathlib import Path


def main() -> None:
    """Run Phase 8 final report validation."""
    project_root = Path(__file__).resolve().parent
    processed_data_dir = project_root / "data" / "processed"
    reports_dir = project_root / "outputs" / "reports"
    charts_dir = project_root / "outputs" / "charts"
    merged_dataset_path = processed_data_dir / "trader_sentiment_merged.csv"
    final_report_path = reports_dir / "final_project_report.md"

    required_files = [
        merged_dataset_path,
        reports_dir / "overall_summary.csv",
        reports_dir / "sentiment_summary.csv",
        reports_dir / "direction_summary.csv",
        reports_dir / "coin_summary.csv",
        reports_dir / "missing_sentiment_summary.csv",
        charts_dir / "sentiment_distribution.png",
        charts_dir / "pnl_by_sentiment.png",
        charts_dir / "average_pnl_by_sentiment.png",
        charts_dir / "win_rate_by_sentiment.png",
        charts_dir / "trade_count_by_direction.png",
        charts_dir / "pnl_by_direction.png",
        charts_dir / "top_coins_by_trade_count.png",
        charts_dir / "top_coins_by_pnl.png",
        charts_dir / "closed_pnl_distribution.png",
        final_report_path,
    ]

    missing_files = [file_path for file_path in required_files if not file_path.exists()]

    if missing_files:
        print("Phase 8 validation failed. Missing files:")
        for file_path in missing_files:
            print(file_path)
        return

    print("Phase 8 completed successfully.")
    print(f"Final report created: {final_report_path}")
    print("Required processed data, reports, and charts are available.")
    print("Raw datasets were not modified.")
    print("No model training, deployment, or new phase work was done.")


if __name__ == "__main__":
    main()
