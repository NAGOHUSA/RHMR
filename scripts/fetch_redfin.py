import requests
from pathlib import Path
import time

ZIP = "31088"
BASE_DIR = Path(f"data/houston-county-ga/{ZIP}/raw")
BASE_DIR.mkdir(parents=True, exist_ok=True)

URL = (
    "https://files.zillowstatic.com/research/public_csvs/zhvi/"
    "Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
)

out_file = BASE_DIR / "zillow_zhvi.csv"

MAX_RETRIES = 3

for attempt in range(1, MAX_RETRIES + 1):
    try:
        response = requests.get(URL, timeout=60)
        response.raise_for_status()
        out_file.write_text(response.text, encoding="utf-8")
        print("Zillow data downloaded successfully")
        break
    except Exception as e:
        print(f"Attempt {attempt} failed: {e}")
        if attempt == MAX_RETRIES:
            raise
        time.sleep(5)
