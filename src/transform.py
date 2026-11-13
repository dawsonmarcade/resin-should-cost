"""
Read from observations, average to monthly

"""
import pandas as pd
from src.load import connect
from config import SERIES

def get_monthly_average(df):
    monthly_rows = []          # FIX: collect rows in a list, build the DataFrame once at the end
    total = 0                  # sum of values in the current month
    count = 0                  # FIX: number of values in the current month (not i)
    current_series = None
    current_month = None
    for i in range(0, len(df)):
        # Convert the single series and month into a value to be checked
        series_id = df["series_id"][i]
        month = df["date"][i].to_period("M")

        # Check if current index is the same or not
        if (series_id, month) != (current_series, current_month):
            if count > 0:
                monthly_rows.append({
                "series_id" : current_series,
                "month": current_month,
                "value" : total/count
                })

            current_series, current_month = series_id, month
            total, count = 0, 0
        total += df["value"][i]
        count += 1
    
    if count > 0:
        monthly_rows.append({
                        "series_id" : current_series,
                        "month": current_month,
                        "value" : total/count
                        }) 
    monthly_df = pd.DataFrame(monthly_rows)
    
    return monthly_df

def main():
    con = connect()

    #Pulling dataframe, adjusting date information to be a date_time datatype, and sorting the dataframe by date
    observation_df = pd.read_sql_query("SELECT * FROM observations", con)
    observation_df["date"] = pd.to_datetime(observation_df["date"])
    observation_df = observation_df.sort_values(["series_id", "date"]).reset_index(drop = True)
    
    print(get_monthly_average(observation_df))


if __name__ == "__main__":
    main()