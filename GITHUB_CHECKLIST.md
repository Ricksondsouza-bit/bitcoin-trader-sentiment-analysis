# GitHub Upload Checklist

Use this checklist before uploading the project to GitHub.

## Keep

- Source code in `src/`
- Dashboard code in `dashboard/`
- Notebook in `notebooks/`
- README and project summary files
- Final Markdown report
- Small chart preview images in `docs/assets/`
- `.gitkeep` files that preserve empty folders

## Avoid Uploading By Default

Large CSV files are ignored by `.gitignore`:

- `data/raw/*.csv`
- `data/processed/*.csv`

This keeps the repository lightweight and avoids publishing raw trading data by accident.

## Recommended GitHub Steps

```bash
git init
git add .
git status
git commit -m "Add bitcoin trader sentiment analysis project"
```

Then create a new GitHub repository and follow GitHub's instructions to add the remote and push.

## Optional Before Publishing

- Add a dashboard screenshot.
- Replace the generic copyright line in `LICENSE` with your name.
- Add a short project description to the GitHub repository page.
- Add topics such as `data-science`, `bitcoin`, `streamlit`, `sentiment-analysis`, and `python`.
