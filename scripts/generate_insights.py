import json
from pathlib import Path

ZIP = "31088"
JSON_FILE = Path(f"data/houston-county-ga/{ZIP}/processed/market.json")

# Load processed market data
with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

points = []

# Inventory change insight
inv_change = data["inventory"]["change_pct"]
if inv_change > 3:
    points.append("Inventory increased notably this period, giving buyers more options.")
elif inv_change < -3:
    points.append("Inventory dropped significantly, giving sellers more leverage.")
else:
    points.append("Inventory is stable compared to last period.")

# Pricing trend insight
trend = data["pricing"]["trend"]
if trend == "heating":
    points.append("Home prices are trending upward; sellers may get top dollar.")
else:
    points.append("Home prices are trending downward; buyers have more negotiating power.")

# Velocity / DOM insight
dom_change = data["velocity"]["dom_change"]
if dom_change > 2:
    points.append("Homes are taking longer to sell than last period, watch pricing closely.")
elif dom_change < -2:
    points.append("Homes are selling faster than last period, a competitive market for buyers.")

# Signals insight
if data["signals"]["price_reductions_up"]:
    points.append("Price reductions are increasing, indicating seller flexibility.")
if data["signals"]["inventory_rising"]:
    points.append("Inventory is rising, increasing options for buyers.")

# Attach insights to JSON
data["weekly_insights"] = points

# Save updated JSON
with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Weekly insights generated successfully for ZIP {ZIP}")
