"""
Read from observations, average to monthly

"""
import pandas as pd
from src.load import connect
from config import SERIES

# def get_monthly_average(data, series_id):



def main():
    con = connect()
    observation_data = pd.read_sql_query("SELECT * FROM observations", con)
    table_meta_data = pd.read_sql_query("SELECT * FROM series_meta", con)
    observation_data["date"] = pd.to_datetime(observation_data["date"])
    new_observation_df = pd.DataFrame(columns=observation_data.columns)

    for i in range(0, len(observation_data)):
        average_price_counter = 0 
        
        if table_meta_data[observation_data["series_id"][i]][i] == "Daily":
            average_price_counter += observation_data["value"][i]
            
            if observation_data['date'][i].dt.month == observation_data['date'][i-1].dt.month + 1:
                monthly_price_price_counter = average_price_counter / i 
                average_price_counter = 0
                
            
             
    
    print(new_observation_df.head())    
if __name__ == "__main__":
    main()