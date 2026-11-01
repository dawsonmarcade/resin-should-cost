"""
Tracking used series:
DCOILWTICO: WTI crude oil, daily
DCOILBRENTEU: Brent crude oil, daily
DHHNGSP: Henry Hub natural gas, daily. Include it because US polyethylene is made mostly from natural-gas ethane.
WPU066: PPI for plastic resins and materials, monthly
WPU0662: PPI for thermoplastic resins, monthly. Thermoplastics are the category that covers PE, PP, PS and PET.

"""

SERIES = {
    "DCOILWTICO": "WTI crude oil",
    "DCOILBRENTEU": "Brent crude oil",
    "DHHNGSP": "HH natural gas",
    "WPU066": "PPI for plastic",
    "WPU0662": "PPI for thermoplastic"
    }

START_DATE = "2010-01-01"