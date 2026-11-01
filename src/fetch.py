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
from config import SERIES, START_DATE

dotenv.load_dotenv()

def get_series(series_id, start = "2010-01-01"):
    
    base_endpoint = "https://api.stlouisfed.org/fred/series/observations"

    params = {
        "series_id" : series_id,
        "api_key" : os.getenv("FRED_API_KEY"),
        "file_type": "json",
        "observation_start": start
    }
    resp = requests.get(base_endpoint, params = params)
    resp.raise_for_status()
    observation_list = resp.json()["observations"]
    observation_df = pd.DataFrame(observation_list)
    observation_df = observation_df.loc[:,["date", "value"] ]


    # Cleaning data, converting date to datetime and values to numbers/NaN
    # Tagging with series name
    observation_df["date"] = pd.to_datetime(observation_df["date"])
    observation_df["value"] = pd.to_numeric(observation_df["value"], errors="coerce")
    observation_df["series_id"] = series_id

    

    return observation_df


def fetch_all():
    frames = []
    for series_id in SERIES:
        frames.append(get_series(series_id))
    concat_frames = pd.concat(frames, ignore_index= True)

    return concat_frames


if __name__ == "__main__":
    df = fetch_all()
    print(df.head())
    print(df.tail())
    print(df["series_id"].value_counts())