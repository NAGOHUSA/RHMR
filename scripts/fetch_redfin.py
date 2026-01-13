import requests
from pathlib import Path
import time

ZIP = "31088"

# TEMP location in workflow runner, not in repo
TMP_DIR = Path("/tmp/houston_zhvi")
TMP_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = TMP_DIR / "zillow_zhvi.csv"

URL = (
    "https://files.zillowstatic.com/research/public_csvs/zhvi/"
    "Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
)

MAX_RETRIES = 3

for attempt in range(1, MAX_RETRIES + 1):
    try:
        response = requests.get(URL, timeout=60)
        response.raise_for_status()
        CSV_FILE.write_text(response.text, encoding="utf-8")
        print(f"Zillow CSV downloaded to {CSV_FILE}")
        break
    except Exception as e:
        print(f"Attempt {attempt} failed: {e}")
        if attempt == MAX_RETRIES:
            raise
        time.sleep(5)
