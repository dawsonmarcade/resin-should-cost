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
BASE_URL = "https://api.stlouisfed.org/fred/"
def get_series(series_id, start = START_DATE):
    
    series_endpoint = BASE_URL + "series/observations"

    params = {
        "series_id" : series_id,
        "api_key" : os.getenv("FRED_API_KEY"),
        "file_type": "json",
        "observation_start": start
    }
    resp = requests.get(series_endpoint, params = params)
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


def get_descriptions(series_id, start = START_DATE):
    
    descriptions_endpoint = BASE_URL + "series"

    params = {
        "series_id" : series_id,
        "api_key" : os.getenv("FRED_API_KEY"),
        "file_type": "json",
        "observation_start": start
    }
    
    resp = requests.get(descriptions_endpoint, params = params)
    resp.raise_for_status()
    seriess_list = resp.json()['seriess']
    
    return seriess_list

print(get_descriptions(SERIES))
    