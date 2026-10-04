# Streamlit Deployment Guide

This project can be deployed on Streamlit Community Cloud as a portfolio dashboard.

## Recommended Free Deployment

1. Push this repository to GitHub.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io).
3. Sign in with GitHub.
4. Click **Create app**.
5. Select the repository and branch.
6. Set the main file path:

```text
app/streamlit_app.py
```

7. Deploy.

The deployed dashboard will use the small demo loan-level sample included in `data/demo/` plus the committed summary tables.

## Full Data Deployment

The full loan-level file is approximately 1 GB:

```text
data/processed/loans_with_pd_lgd_ead_v1.csv
```

GitHub regular Git does not support files over 100 MB. To deploy the full dataset, use Git LFS or external object storage. The app will automatically use the full file if it exists at the path above.

## Local Run

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the dashboard:

```bash
python3 -m streamlit run app/streamlit_app.py
```

## Scope

The dashboard is an interactive presentation layer over saved project outputs. It does not retrain models, approve loans, or produce production credit decisions.
