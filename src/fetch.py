"""
Tracking used series:
DCOILWTICO: WTI crude oil, daily
DCOILBRENTEU: Brent crude oil, daily
DHHNGSP: Henry Hub natural gas, daily. Include it because US polyethylene is made mostly from natural-gas ethane.
WPU066: PPI for plastic resins and materials, monthly
WPU0662: PPI for thermoplastic resins, monthly. Thermoplastics are the category that covers PE, PP, PS and PET.

"""


import os
import dotenv
import requests
import pandas as pd
from config import SERIES, START_DATE, BASE_URL

dotenv.load_dotenv()

META_FIELDS = [
    "title",
    "units",
    "frequency",
    "seasonal_adjustment",
    "observation_start",
    "observation_end",
    "last_updated",
    "notes",
]

def _get(path, params):
    """One GET request to FRED. Adds the key and format so callers don't repeat them."""
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        raise RuntimeError("FRED_API_KEY is not set. Put it in your .env file.")
    full_params = {"api_key": api_key, "file_type": "json", **params}
    resp = requests.get(BASE_URL + path, params=full_params, timeout=30)
    resp.raise_for_status()
    return resp.json()
 
 
# ---------- data ----------
 
def fetch_observations(series_id, start=START_DATE):
    """Data for one series as a DataFrame: series_id, date, value."""
    payload = _get("series/observations", {"series_id": series_id, "observation_start": start})
    df = pd.DataFrame(payload["observations"], columns=["date", "value"])
 
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")  # FRED uses "." for missing
    df = df.dropna(subset=["value"])  # a row with no value carries no information
    df["series_id"] = series_id
    return df[["series_id", "date", "value"]]
 
 
def fetch_all_observations(starts=None):
    """
    Data for every series in config, stacked into one long DataFrame.
 
    starts: optional {series_id: "YYYY-MM-DD"} to pull only recent data for
    series we already have (see load.py). Missing ids use START_DATE.
    """
    starts = starts or {}
    frames = []
    for series_id in SERIES:
        start = starts.get(series_id, START_DATE)
        df = fetch_observations(series_id, start)
        print(f"  {series_id:<16} {len(df):>6} rows from {start}")
        frames.append(df)
    return pd.concat(frames, ignore_index=True)
 
 
# ---------- metadata ----------
 
def fetch_metadata(series_id):
    """Description of one series as a dict (one record)."""
    payload = _get("series", {"series_id": series_id})
    meta = payload["seriess"][0]  # one series asked for -> one description back
    record = {"series_id": series_id, "role": SERIES[series_id]}
    record.update({field: meta.get(field) for field in META_FIELDS})
    return record
 
 
def fetch_all_metadata():
    """Descriptions of every series in config, one row per series."""
    return pd.DataFrame([fetch_metadata(series_id) for series_id in SERIES])