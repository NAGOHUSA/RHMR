# [file name]: scripts/calculate_metrics.py
import csv
import json
from pathlib import Path
from datetime import date
import sys
import os

# Get ZIP from command line argument or use default
ZIP = sys.argv[1] if len(sys.argv) > 1 else "31088"

BASE_DIR = Path(__file__).parent.parent

# Try to find CSV file in multiple locations
possible_csv_locations = [
    BASE_DIR / "tmp" / "zillow_zhvi.csv",
    BASE_DIR / "zillow_zhvi.csv",
    Path("/tmp/houston_zhvi/zillow_zhvi.csv")
]

CSV_FILE = None
for location in possible_csv_locations:
    if location.exists():
        CSV_FILE = location
        print(f"Found CSV at: {CSV_FILE}")
        break

# Output folder
OUT_DIR = BASE_DIR / f"data/houston-county-ga/{ZIP}/processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def calculate_metrics():
    if CSV_FILE and CSV_FILE.exists():
        # --- Load Zillow CSV ---
        rows = []
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("RegionName") == ZIP:
                    rows.append(row)
        
        if rows:
            row = rows[0]
            
            # --- Extract last 4 months dynamically ---
            date_columns = [c for c in row.keys() if c[:4].isdigit()]
            date_columns.sort()
            last_periods = date_columns[-4:]
            values = [float(row[c]) for c in last_periods if row[c]]
            
            if len(values) < 2:
                print(f"⚠️ Not enough historical data for ZIP {ZIP}, using default values")
                values = [280000, 282000, 285000, 289500]
            
            latest = values[-1]
            previous = values[-2]
            
            # --- Derived Metrics ---
            price_change_pct = round((latest - previous) / previous * 100, 2)
            trend = "heating" if price_change_pct > 0 else "cooling"
            
            # Inventory proxy
            inventory_proxy = max(1, int(100 / max(abs(price_change_pct), 0.1)))
            
            market = {
                "market": "Houston County, GA",
                "zip": ZIP,
                "city": "Warner Robins",
                "updated": str(date.today()),
                "period": "monthly",
                "inventory": {
                    "active": inventory_proxy,
                    "change_pct": round(price_change_pct * -1, 1)
                },
                "pricing": {
                    "median_list": int(latest),
                    "median_sale": int(latest * 0.97),
                    "spread_pct": -3.0,
                    "trend": trend
                },
                "velocity": {
                    "avg_dom": 30 if trend == "cooling" else 22,
                    "dom_change": 3 if trend == "cooling" else -2,
                    "absorption_rate": 0.75 if trend == "cooling" else 1.1,
                    "months_supply": 4.2 if trend == "cooling" else 2.8
                },
                "signals": {
                    "seller_leverage": "buyer" if trend == "cooling" else "seller",
                    "price_reductions_up": trend == "cooling",
                    "inventory_rising": trend == "cooling"
                },
                "history": {
                    "median_list": values
                }
            }
            
            output_file = OUT_DIR / "market.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(market, f, indent=2)
            
            print(f"✅ Market metrics generated successfully for ZIP {ZIP}")
            return market
        else:
            print(f"⚠️ No data found for ZIP {ZIP} in CSV, creating default data")
    else:
        print("⚠️ CSV file not found, creating default data")
    
    # Create default data
    market = {
        "market": "Houston County, GA",
        "zip": ZIP,
        "city": "Warner Robins",
        "updated": str(date.today()),
        "period": "monthly",
        "inventory": {
            "active": 105,
            "change_pct": 2.5
        },
        "pricing": {
            "median_list": 289500,
            "median_sale": 281000,
            "spread_pct": -3.0,
            "trend": "heating"
        },
        "velocity": {
            "avg_dom": 28,
            "dom_change": -2,
            "absorption_rate": 1.1,
            "months_supply": 2.8
        },
        "signals": {
            "seller_leverage": "seller",
            "price_reductions_up": False,
            "inventory_rising": False
        },
        "history": {
            "median_list": [285000, 287500, 289500, 291000]
        }
    }
    
    output_file = OUT_DIR / "market.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(market, f, indent=2)
    
    print(f"✅ Default market metrics generated for ZIP {ZIP}")
    return market

if __name__ == "__main__":
    calculate_metrics()
