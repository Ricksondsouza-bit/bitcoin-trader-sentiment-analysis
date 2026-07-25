# Data Folder

This project expects the original CSV files to be placed locally in:

```text
data/raw/
```

Required raw files:

- `historical_data.csv`
- `fear_greed_index.csv`

Processed files are created in:

```text
data/processed/
```

Large CSV files are ignored by Git by default in this portfolio package. This keeps the repository lightweight and avoids accidentally publishing raw trading data.

If you want to publish sample data later, add small anonymized files instead of the full raw datasets.
