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
    observation_df = observation_df[2, 3]

    return observation_df

test = get_series("DCOILWTICO")

print(test)