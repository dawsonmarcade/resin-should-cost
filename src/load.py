import sqlite3 
from pathlib import Path   
import pandas as pd
from src.fetch import fetch_all

con = sqlite3.connect("FRED.db")

cur = con.cursor()

df = fetch_all()

cur.execute("""
    CREATE TABLE IF NOT EXISTS fred_api_data(
        series_id TEXT,
        date TEXT, 
        value REAL,
        primary key (series_id, date)
    )
""")

#Need to change date format since sqlite cant take date DT
df["date"] = df["date"].dt.strftime("%Y-%m-%d")

#converting dataframe data type into a list since that is how sqlite ingests it
rows = list(df[["series_id", "date", "value"]].itertuples(index= False, name = None))

# executemany runs the INSERT once per tuple; each ? is filled from the tuple in order 
cur.executemany("INSERT OR REPLACE INTO fred_api_data(series_id, date, value) VALUES (?,?,?)", rows)

con.commit()
con.close()