import csv
import requests
from pathlib import Path

ZIP = "31088"
BASE_DIR = Path(f"data/houston-county-ga/{ZIP}/raw")
BASE_DIR.mkdir(parents=True, exist_ok=True)

URL = "https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/zip_market_tracker.tsv000.gz"

response = requests.get(URL)
response.raise_for_status()

gz_path = BASE_DIR / "redfin.zip.gz"
gz_path.write_bytes(response.content)

print(f"Downloaded Redfin data for ZIP {ZIP}")

