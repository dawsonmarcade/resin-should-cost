"""
Raw layer: fetch from FRED and store in SQLite exactly as received.
 
Run from the project root:
    py -m src.load
 
Safe to run as often as you like. The primary keys plus INSERT OR REPLACE
mean a re-run updates rows instead of duplicating them.
"""
import sqlite3
from datetime import datetime
 
import pandas as pd
 
from config import DB_PATH, REFRESH_DAYS, SERIES
from src.fetch import fetch_all_metadata, fetch_all_observations
 
 
def connect():
    return sqlite3.connect(DB_PATH)
 
 
def create_tables(con):
    # Data: one row per series per date.
    con.execute("""
        CREATE TABLE IF NOT EXISTS observations (
            series_id TEXT,
            date      TEXT,     -- 'YYYY-MM-DD' (SQLite has no date type)
            value     REAL,
            loaded_at TEXT,     -- when this row was last written
            PRIMARY KEY (series_id, date)
        )
    """)
    # Metadata: one row per series.
    con.execute("""
        CREATE TABLE IF NOT EXISTS series_meta (
            series_id           TEXT PRIMARY KEY,
            role                TEXT,   -- driver / target (ours, not FRED's)
            title               TEXT,
            units               TEXT,
            frequency           TEXT,
            seasonal_adjustment TEXT,
            observation_start   TEXT,
            observation_end     TEXT,
            last_updated        TEXT,
            notes               TEXT
        )
    """)
 
 
def refresh_starts(con):
    """
    For series already in the database, start the pull REFRESH_DAYS before the
    latest date we have. New series aren't in the result, so they get a full pull.
    """
    rows = con.execute("SELECT series_id, MAX(date) FROM observations GROUP BY series_id").fetchall()
    starts = {}
    for series_id, last_date in rows:
        start = pd.Timestamp(last_date) - pd.Timedelta(days=REFRESH_DAYS)
        starts[series_id] = start.strftime("%Y-%m-%d")
    return starts
 
 
def insert_observations(con, df):
    df = df.copy()
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    df["loaded_at"] = datetime.now().isoformat(timespec="seconds")
    rows = list(df[["series_id", "date", "value", "loaded_at"]].itertuples(index=False, name=None))
    con.executemany(
        "INSERT OR REPLACE INTO observations (series_id, date, value, loaded_at) VALUES (?, ?, ?, ?)",
        rows,
    )
    return len(rows)
 
 
def insert_metadata(con, df):
    cols = ["series_id", "role", "title", "units", "frequency", "seasonal_adjustment",
            "observation_start", "observation_end", "last_updated", "notes"]
    rows = list(df[cols].itertuples(index=False, name=None))
    placeholders = ", ".join("?" for _ in cols)
    con.executemany(
        f"INSERT OR REPLACE INTO series_meta ({', '.join(cols)}) VALUES ({placeholders})",
        rows,
    )
    return len(rows)
 
 
def summary(con):
    return pd.read_sql("""
        SELECT o.series_id, m.role, m.units, COUNT(*) AS n_rows,
               MIN(o.date) AS first_date, MAX(o.date) AS last_date
        FROM observations o
        LEFT JOIN series_meta m ON o.series_id = m.series_id
        GROUP BY o.series_id
        ORDER BY m.role, o.series_id
    """, con)
 
 
def main():
    con = connect()
    create_tables(con)
 
    print("Fetching metadata...")
    n_meta = insert_metadata(con, fetch_all_metadata())
 
    print("Fetching observations...")
    obs = fetch_all_observations(starts=refresh_starts(con))
    n_obs = insert_observations(con, obs)
 
    con.commit()
    print(f"\nWrote {n_meta} metadata rows and {n_obs} observation rows to {DB_PATH}\n")
    print(summary(con).to_string(index=False))
    con.close()
 
 
if __name__ == "__main__":
    main()
 