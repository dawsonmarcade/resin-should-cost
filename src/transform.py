"""
Staging + features: read raw observations, average to monthly, build model features.
"""
import pandas as pd

from src.load import connect


def get_monthly_average(df):
    """One row per series per month: the average of that month's values."""
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M").astype(str)   # "2026-09"
    return df.groupby(["series_id", "month"], as_index=False)["value"].mean()


def main():
    con = connect()
    observation_df = pd.read_sql_query("SELECT * FROM observations", con)
    observation_df["date"] = pd.to_datetime(observation_df["date"])

    monthly_df = get_monthly_average(observation_df)
    print(monthly_df)
    con.close()


if __name__ == "__main__":
    main()