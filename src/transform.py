"""
Read from observations, average to monthly

"""
import pandas as pd
from src.load import connect
from config import SERIES

# def get_monthly_average(data, series_id):



def main():
    con = connect()
    observation_df = pd.read_sql_query("SELECT * FROM observations", con)
    meta_data = pd.read_sql_query("SELECT * FROM series_meta", con)
    observation_df["date"] = pd.to_datetime(observation_df["date"])
    new_observation_df = pd.DataFrame(columns=observation_df.columns)
    
    
    
    total_counter = 0
    for i in range(0, len(observation_df)):
        
        series_from_observation_df = observation_df["series_id"][i]
        frequency = meta_data[meta_data["series_id"] == series_from_observation_df]["frequency"].item()
        
        if frequency == "Daily":
            if observation_df["date"][i].month == observation_df["date"][i].month - 1:
                average_value = total_counter / i
                new_observation_df["value"][i] = average_value
                new_observation_df["series_id"][i] = observation_df["series_id"][i]
                total_counter = 0
            total_counter += observation_df["value"][i]

    print(new_observation_df)
      
if __name__ == "__main__":
    main()