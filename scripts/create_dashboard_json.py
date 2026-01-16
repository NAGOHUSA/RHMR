#!/usr/bin/env python3
"""
Create aggregated dashboard JSON from collected data
"""

import json
import glob
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

def create_dashboard_json():
    """Create main dashboard JSON with aggregated data from all ZIPs"""
    print("Creating dashboard JSON files...")
    
    base_dir = Path("data/houston-county-ga")
    dashboard_data = {
        "last_updated": datetime.now().isoformat(),
        "zip_codes": {},
        "market_overview": {},
        "trends": {},
        "alerts": [],
        "recommendations": []
    }
    
    # Find all ZIP code directories
    zip_dirs = [d for d in base_dir.iterdir() if d.is_dir() and d.name.isdigit()]
    
    for zip_dir in zip_dirs:
        zip_code = zip_dir.name
        latest_file = zip_dir / "latest.json"
        summary_file = zip_dir / "market_summary.json"
        properties_file = zip_dir / "properties.json"
        
        if latest_file.exists():
            try:
                with open(latest_file, 'r', encoding='utf-8') as f:
                    zip_data = json.load(f)
                
                # Add ZIP summary to dashboard
                dashboard_data["zip_codes"][zip_code] = {
                    "market_summary": zip_data.get("market_summary", {}),
                    "property_count": len(zip_data.get("properties", [])),
                    "last_updated": zip_data.get("timestamp", ""),
                    "location": {
                        "city": self._get_city_by_zip(zip_code),
                        "county": "Houston",
                        "state": "GA"
                    }
                }
                
                # Process properties for trends
                properties = zip_data.get("properties", [])
                if properties:
                    self._analyze_zip_trends(zip_code, properties, dashboard_data)
                    
            except Exception as e:
                print(f"Error processing {zip_code}: {e}")
                continue
    
    # Calculate overall market overview
    if dashboard_data["zip_codes"]:
        self._calculate_overall_market(dashboard_data)
    
    # Generate alerts and recommendations
    self._generate_alerts(dashboard_data)
    self._generate_recommendations(dashboard_data)
    
    # Save dashboard JSON
    self._save_dashboard_files(dashboard_data, base_dir)
    
    print(f"✅ Dashboard created successfully!")
    print(f"   - Zips processed: {len(dashboard_data['zip_codes'])}")
    print(f"   - Total properties: {dashboard_data['market_overview'].get('total_properties', 0)}")
    print(f"   - Market health: {dashboard_data['market_overview'].get('overall_health_score', 0)}/100")
    
    return dashboard_data

def _get_city_by_zip(self, zip_code):
    """Get city name from ZIP code"""
    city_map = {
        '31088': 'Warner Robins',
        '31093': 'Centerville', 
        '31098': 'Bonaire'
    }
    return city_map.get(zip_code, 'Unknown')

def _analyze_zip_trends(self, zip_code, properties, dashboard_data):
    """Analyze trends for a specific ZIP code"""
    active_properties = [p for p in properties if p.get('status') == 'Active']
    pending_properties = [p for p in properties if p.get('status') == 'Pending']
    sold_properties = [p for p in properties if p.get('status') == 'Sold']
    
    # Price trends
    if active_properties:
        prices = [p.get('price', 0) for p in active_properties]
        avg_price = sum(prices) / len(prices)
        
        # Calculate price changes (simulated)
        price_change_30d = round(random.uniform(-0.03, 0.05) * 100, 1)
        
        dashboard_data["trends"][zip_code] = {
            "avg_price": round(avg_price, 2),
            "price_change_30d": price_change_30d,
            "active_listings": len(active_properties),
            "pending_listings": len(pending_properties),
            "sold_30d": len([p for p in sold_properties if 
                           datetime.fromisoformat(p.get('scraped_date', datetime.now().isoformat())) > 
                           datetime.now() - timedelta(days=30)]),
            "days_on_market_avg": sum(p.get('days_on_market', 0) for p in active_properties) / max(len(active_properties), 1),
            "price_per_sqft_avg": sum(p.get('price', 0) / max(p.get('sqft', 1), 1) for p in active_properties) / max(len(active_properties), 1)
        }

def _calculate_overall_market(self, dashboard_data):
    """Calculate overall market metrics"""
    total_properties = sum(zip_data["property_count"] for zip_data in dashboard_data["zip_codes"].values())
    total_active = sum(zip_data["market_summary"].get("inventory_count", 0) for zip_data in dashboard_data["zip_codes"].values())
    
    health_scores = [zip_data["market_summary"].get("market_health_score", 50) 
                    for zip_data in dashboard_data["zip_codes"].values()]
    avg_health = sum(health_scores) / len(health_scores) if health_scores else 50
    
    # Calculate overall metrics
    dashboard_data["market_overview"] = {
        "total_zip_codes": len(dashboard_data["zip_codes"]),
        "total_properties": total_properties,
        "active_listings": total_active,
        "overall_health_score": round(avg_health, 1),
        "market_condition": self._get_market_condition(avg_health),
        "last_updated": datetime.now().isoformat(),
        "update_frequency": "6 hours",
        "data_sources": ["public_records", "simulated_data", "market_trends"]
    }

def _get_market_condition(self, health_score):
    """Convert health score to market condition"""
    if health_score >= 70:
        return "Seller's Market"
    elif health_score >= 60:
        return "Balanced Market"
    elif health_score >= 40:
        return "Buyer's Market"
    else:
        return "Depressed Market"

def _generate_alerts(self, dashboard_data):
    """Generate market alerts"""
    alerts = []
    
    for zip_code, zip_data in dashboard_data["zip_codes"].items():
        summary = zip_data["market_summary"]
        
        # Low inventory alert
        if summary.get("inventory_count", 0) < 20:
            alerts.append({
                "type": "warning",
                "zip": zip_code,
                "title": "Low Inventory Alert",
                "message": f"Only {summary['inventory_count']} active listings in {zip_code}",
                "severity": "medium"
            })
        
        # High DOM alert
        if summary.get("avg_days_on_market", 0) > 60:
            alerts.append({
                "type": "warning",
                "zip": zip_code,
                "title": "Slow Market Alert",
                "message": f"Average DOM is {summary['avg_days_on_market']} days in {zip_code}",
                "severity": "low"
            })
        
        # Good buying opportunity
        if summary.get("market_health_score", 0) < 40:
            alerts.append({
                "type": "opportunity",
                "zip": zip_code,
                "title": "Buyer's Market Opportunity",
                "message": f"Strong buyer's market detected in {zip_code}",
                "severity": "high"
            })
    
    dashboard_data["alerts"] = alerts

def _generate_recommendations(self, dashboard_data):
    """Generate investment recommendations"""
    recommendations = []
    
    # Find best ZIP for investment (lowest health score = buyer's market)
    worst_zip = min(dashboard_data["zip_codes"].items(), 
                   key=lambda x: x[1]["market_summary"].get("market_health_score", 100),
                   default=(None, None))
    
    if worst_zip[0]:
        recommendations.append({
            "type": "investment",
            "title": "Consider Buying in " + worst_zip[0],
            "reason": "This area shows strong buyer's market conditions",
            "confidence": "high"
        })
    
    # Find best ZIP for selling (highest health score)
    best_zip = max(dashboard_data["zip_codes"].items(),
                  key=lambda x: x[1]["market_summary"].get("market_health_score", 0),
                  default=(None, None))
    
    if best_zip[0]:
        recommendations.append({
            "type": "selling",
            "title": "Consider Selling in " + best_zip[0],
            "reason": "This area shows strong seller's market conditions",
            "confidence": "medium"
        })
    
    dashboard_data["recommendations"] = recommendations

def _save_dashboard_files(self, dashboard_data, base_dir):
    """Save dashboard files in various formats"""
    
    # Main dashboard file
    dashboard_file = base_dir / "dashboard.json"
    with open(dashboard_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2, default=str)
    
    # Simplified version for web
    simple_dashboard = {
        "last_updated": dashboard_data["last_updated"],
        "market_overview": dashboard_data["market_overview"],
        "alerts": dashboard_data["alerts"],
        "recommendations": dashboard_data["recommendations"]
    }
    
    simple_file = base_dir / "dashboard_simple.json"
    with open(simple_file, 'w', encoding='utf-8') as f:
        json.dump(simple_dashboard, f, indent=2)
    
    # Market trends file
    trends_file = base_dir / "market_trends.json"
    with open(trends_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data["trends"], f, indent=2)
    
    # Create CSV version for spreadsheets
    self._create_csv_dashboard(dashboard_data, base_dir)

def _create_csv_dashboard(self, dashboard_data, base_dir):
    """Create CSV version of dashboard data"""
    csv_data = []
    
    for zip_code, zip_data in dashboard_data["zip_codes"].items():
        summary = zip_data["market_summary"]
        row = {
            "zip_code": zip_code,
            "city": self._get_city_by_zip(zip_code),
            "inventory_count": summary.get("inventory_count", 0),
            "median_price": summary.get("median_price", 0),
            "avg_days_on_market": summary.get("avg_days_on_market", 0),
            "market_health_score": summary.get("market_health_score", 0),
            "market_trend": summary.get("market_trend", ""),
            "property_count": zip_data["property_count"],
            "last_updated": zip_data["last_updated"]
        }
        csv_data.append(row)
    
    if csv_data:
        df = pd.DataFrame(csv_data)
        csv_file = base_dir / "dashboard.csv"
        df.to_csv(csv_file, index=False)

if __name__ == "__main__":
    # Add necessary imports
    import random
    
    # Create dashboard
    dashboard = create_dashboard_json()
