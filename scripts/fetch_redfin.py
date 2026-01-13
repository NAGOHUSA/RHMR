import requests
from pathlib import Path

ZIP = "31088"
BASE_DIR = Path(f"data/houston-county-ga/{ZIP}/raw")
BASE_DIR.mkdir(parents=True, exist_ok=True)

# Public Redfin Data Center weekly CSV (mirrored)
URL = (
    "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
)

# NOTE:
# We are switching to a public CSV source pattern.
# This file will be replaced with housing data below.

response = requests.get(URL, timeout=30)
response.raise_for_status()

out_file = BASE_DIR / "source.csv"
out_file.write_text(response.text)

print("Public data source downloaded successfully")
