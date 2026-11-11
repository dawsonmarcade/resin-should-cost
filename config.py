"""
Tracking used series:
DCOILWTICO: WTI crude oil, daily
DCOILBRENTEU: Brent crude oil, daily
DHHNGSP: Henry Hub natural gas, daily. Include it because US polyethylene is made mostly from natural-gas ethane.
WPU066: PPI for plastic resins and materials, monthly
WPU0662: PPI for thermoplastic resins, monthly. Thermoplastics are the category that covers PE, PP, PS and PET.

"""

BASE_URL = "https://api.stlouisfed.org/fred/"
START_DATE = "2000-01-01"
DB_PATH = "FRED.db"

# How many days to re-pull on each run. FRED revises recent values
# (PPI especially), so we refresh the tail instead of only adding new dates.
REFRESH_DAYS = 90

SERIES = {
    "DCOILWTICO": "driver",       # WTI crude, $/bbl, daily
    "DCOILBRENTEU": "driver",     # Brent crude, $/bbl, daily
    "DHHNGSP": "driver",          # Henry Hub natural gas, $/MMBtu, daily
    "WPU0662": "target",          # PPI thermoplastic resins, index, monthly
    "PCU325211325211": "target",  # PPI plastics material & resin mfg, index, monthly
}

LAGS = [0, 1, 2, 3]