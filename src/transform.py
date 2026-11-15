"""
Staging + features: read raw observations, average to monthly, build model features.
"""
import pandas as pd

from src.load import connect

from datetime import date


def get_monthly_average(df):
    """One row per series per month: the average of that month's values."""
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M").astype(str)   # "2026-09"
    return df.groupby(["series_id", "month"], as_index=False)["value"].mean()

def drop_current_month(monthly_df):

    #needs to be in string type
    current_month = pd.Timestamp.today().strftime("%Y-%m")   # "2026-11"
    #more masking
    monthly_df = monthly_df[monthly_df["month"] < current_month]
    return monthly_df

def pivot_wide(monthly_df):
    wide_df = monthly_df.pivot(index="month", columns="series_id", values="value")
    return wide_df

def add_pct_changes(monthly_df):
    hanges_df = monthly_df.pct_change(fill_method=None) * 100

def main():
    con = connect()
    observation_df = pd.read_sql_query("SELECT * FROM observations", con)
    observation_df["date"] = pd.to_datetime(observation_df["date"])
    monthly_df = get_monthly_average(observation_df)
    updated_df = drop_current_month(monthly_df)
    wide_df = pivot_wide(updated_df)
    pct_df = add_pct_changes(wide_df)

    


if __name__ == "__main__":
    main()