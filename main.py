import os
from dotenv import load_dotenv

load_dotenv()
FRED_API = os.getenv("FRED_API_KEY")

print(FRED_API)


