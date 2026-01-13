import json
from pathlib import Path

ZIP = "31088"
FILE = Path(f"data/houston-county-ga/{ZIP}/processed/market.json")

data = json.loads(FILE.read_text())
points = []

if data["inventory"]["change_pct"] > 3:
    points.append("Inventory increased notably this week, giving buyers more options.")

if data["velocity"]["dom_change"] > 2:
    points.append("Homes are taking longer to sell, suggesting pricing sensitivity.")

if data["pricing"]["spread_pct"] < -2:
    points.append("Homes are selling below list price on average.")

data["weekly_insights"] = points
FILE.write_text(json.dumps(data, indent=2))

print("Weekly insights generated")

