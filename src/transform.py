"""
Read from observations, average to monthly

"""
import pandas as pd
from src.load import connect

#def get_monthly_average(data, series_id):



def main():
    con = connect()
    date , value = pd.read_sql("SELECT date, value FROM fred_api_data"
    , con)
    print(date.dtype(), value)

if __name__ == "__main__":
    main()