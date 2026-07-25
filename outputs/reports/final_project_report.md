# Bitcoin Market Sentiment and Trader Performance Analysis

## Final Project Report

## Project Objective

The objective of this project is to analyse the relationship between Bitcoin market sentiment and trader performance.

The project combines historical trading data from Hyperliquid with the Bitcoin Fear and Greed Index. The analysis focuses on trader profitability, win rate, trade direction, traded coins, fees, trade size, and market sentiment conditions.

## Data Used

The project uses two raw datasets:

- `historical_data.csv`
- `fear_greed_index.csv`

The final analysis uses the merged processed dataset:

```text
data/processed/trader_sentiment_merged.csv
```

The merged dataset contains trader data joined with daily Fear and Greed sentiment information.

## Project Workflow Summary

### Phase 1: Project Setup

The project folder structure, notebook, source files, dashboard placeholder, README, requirements file, and `.gitignore` were created.

### Phase 2: Dataset Loading and Inspection

Both raw datasets were loaded and inspected. Column names, data types, missing values, duplicate rows, and categorical values were reviewed.

### Phase 3: Data Cleaning and Preparation

Cleaned copies of both datasets were created and saved in `data/processed/`. Raw datasets were not modified.

### Phase 4: Dataset Merging

The cleaned trader dataset was merged with the cleaned sentiment dataset by trade date.

The final merged dataset contains:

- 211,224 rows
- 21 columns
- Sentiment value and sentiment classification for each matched trade date

There were 6 rows without matching sentiment data, all on `2024-10-26`.

### Phase 5: Exploratory Data Analysis

Summary report CSV files were generated in:

```text
outputs/reports/
```

The reports include overall performance, sentiment-level summaries, direction-level summaries, coin-level summaries, and missing sentiment checks.

### Phase 6: Visual Analysis

Visual charts were generated and saved in:

```text
outputs/charts/
```

The charts cover sentiment distribution, PnL by sentiment, win rate by sentiment, direction summaries, top coins, and Closed PnL distribution.

### Phase 7: Streamlit Dashboard

A local Streamlit dashboard was created in:

```text
dashboard/app.py
```

The dashboard displays metrics, filters, summary tables, charts, missing sentiment warnings, and a filtered data preview.

## Overall Trading Summary

The final merged dataset contains:

- Total trades: 211,224
- Unique accounts: 32
- Unique coins: 246
- Total Closed PnL: 10,296,958.94
- Average Closed PnL: 48.75
- Median Closed PnL: 0.00
- Minimum Closed PnL: -117,990.10
- Maximum Closed PnL: 135,329.09
- Win count: 86,869
- Loss count: 124,355
- Win rate: 41.13%
- Average trade size: 5,639.45 USD
- Total fees: 245,857.72

## Sentiment-Based Observations

The highest trade count occurred during `Fear` conditions:

- Fear trades: 61,837
- Fear total Closed PnL: 3,357,155.44
- Fear win rate: 42.08%

The highest win rate among matched sentiment groups occurred during `Extreme Greed`:

- Extreme Greed trades: 39,992
- Extreme Greed total Closed PnL: 2,715,171.31
- Extreme Greed average Closed PnL: 67.89
- Extreme Greed win rate: 46.49%

The lowest win rate among matched sentiment groups occurred during `Extreme Fear`:

- Extreme Fear trades: 21,400
- Extreme Fear total Closed PnL: 739,110.25
- Extreme Fear average Closed PnL: 34.54
- Extreme Fear win rate: 37.06%

These results are descriptive. They show how this dataset behaved across sentiment groups, but they do not prove that sentiment caused the trading results.

## Direction-Based Observations

The largest realized Closed PnL values came from closing and selling actions.

Important direction summaries:

- `Close Short`: 36,013 trades, total Closed PnL of 3,709,800.10, win rate of 77.94%
- `Close Long`: 48,678 trades, total Closed PnL of 3,622,929.39, win rate of 87.69%
- `Sell`: 19,902 trades, total Closed PnL of 2,906,748.42, win rate of 80.42%

Some directions, such as `Open Long`, `Open Short`, `Buy`, and `Spot Dust Conversion`, show zero total Closed PnL in the summary. This is expected for opening or non-realizing transaction types because Closed PnL is usually realized when positions are closed.

## Coin-Level Observations

The most actively traded coin in the top-coin summary was `HYPE`:

- HYPE trades: 68,005
- HYPE total Closed PnL: 1,948,484.60
- HYPE win rate: 41.50%

The top coins by total Closed PnL among the top-traded coins include:

- `@107`: 2,783,912.92
- `HYPE`: 1,948,484.60
- `SOL`: 1,639,555.93
- `ETH`: 1,319,978.84
- `BTC`: 868,044.73

Some heavily traded coins had negative total Closed PnL in the top-coin summary:

- `TRUMP`: -364,824.91
- `FARTCOIN`: -100,687.21
- `PAXG`: -18,688.87

These results describe historical performance in this dataset only. They should not be treated as trading recommendations.

## Missing Sentiment Data

There were 6 rows with missing sentiment values after merging.

All missing sentiment rows occurred on:

```text
2024-10-26
```

The missing sentiment rows affected:

- 1 account
- 1 coin
- Total Closed PnL of 42,471.99

The rows were not removed or filled. They are preserved in the merged dataset.

## Dashboard Summary

The Streamlit dashboard provides an interactive way to review:

- Overall project metrics
- Filtered trade metrics
- Sentiment summaries
- Direction summaries
- Coin summaries
- Closed PnL distribution
- Missing sentiment rows
- Filtered trade previews

Run the dashboard from the project root:

```bash
streamlit run dashboard/app.py
```

## Limitations

This project has several important limitations:

- The analysis is descriptive, not predictive.
- The analysis does not prove that sentiment caused trader performance.
- Sentiment data is daily, while trades can happen many times within a day.
- Six trader rows did not match a sentiment date.
- The quality of conclusions depends on the quality and completeness of the provided datasets.
- No machine learning model was trained.
- No external market variables beyond the Fear and Greed Index were included.

## Conclusion

The project successfully created a complete data science workflow from setup to dashboard.

The analysis shows that trader performance varies across sentiment conditions, directions, and coins. In this dataset, `Extreme Greed` had the highest matched-sentiment win rate, while `Fear` had the highest total trade count and total Closed PnL. Realized PnL was mainly associated with closing and selling transaction types.

These findings should be treated as descriptive project insights, not financial advice or trading recommendations.
