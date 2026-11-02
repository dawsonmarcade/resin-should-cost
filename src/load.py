import sqlite3 
from pathlib import Path   
import pandas as pd

con = sqlite3.connect("FRED_DB")

cur = con.cursor()

