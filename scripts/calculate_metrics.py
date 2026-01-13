import csv
import gzip
import json
from pathlib import Path
from datetime import date

ZIP = "31088"
RAW_DIR = Path(f"data/houston-county-ga/{ZIP}/raw")
OUT_DIR = Path(f"data/houston-county-ga/{ZIP}/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

gz_file = RAW_DIR / "redfin.zip.gz"

rows = []
with gzip.open(gz_file, "rt") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        if row["region"] == ZIP:
            rows.append(row)

rows = rows[-4:]  # last 4 weeks

inventory = int(float(rows[-1]["inventory"]))
prev_inventory = int(float(rows[-2]["inventory"]))

market = {
    "market": "Houston County, GA",
    "zip": ZIP,
    "city": "Warner Robins",
    "updated": str(date.today()),
    "period": "weekly",
    "inventory": {
        "active": inventory,
        "change_pct": round((inventory - prev_inventory) / prev_inventory * 100, 1)
    },
    "pricing": {
        "median_list": int(float(rows[-1]["median_list_price"])),
        "median_sale": int(float(rows[-1]["median_sale_price"])),
        "spread_pct": round(
            (float(rows[-1]["median_sale_price"]) -
             float(rows[-1]["median_list_price"])) /
            float(rows[-1]["median_list_price"]) * 100, 1
        ),
        "trend": "cooling" if float(rows[-1]["median_list_price"]) <
                            float(rows[-2]["median_list_price"]) else "heating"
    },
    "velocity": {
        "avg_dom": int(float(rows[-1]["days_on_market"])),
        "dom_change": int(float(rows[-1]["days_on_market"]) -
                          float(rows[-2]["days_on_market"])),
        "absorption_rate": round(
            float(rows[-1]["homes_sold"]) / inventory, 2
        ),
        "months_supply": round(inventory / max(float(rows[-1]["homes_sold"]), 1), 1)
    },
    "signals": {
        "seller_leverage": "neutral",
        "price_reductions_up": float(rows[-1]["price_drops"]) >
                               float(rows[-2]["price_drops"]),
        "inventory_rising": inventory > prev_inventory
    },
    "history": {
        "inventory": [int(float(r["inventory"])) for r in rows],
        "median_list": [int(float(r["median_list_price"])) for r in rows],
        "avg_dom": [int(float(r["days_on_market"])) for r in rows]
    }
}

with open(OUT_DIR / "market.json", "w") as f:
    json.dump(market, f, indent=2)

print("Market metrics generated")

