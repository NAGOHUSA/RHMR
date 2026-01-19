#!/usr/bin/env python3
"""
Create aggregated dashboard JSON from collected data
"""

import json
import glob
from pathlib import Path
from datetime import datetime, timedelta
import random

def get_city_by_zip(zip_code):
    """Get city name from ZIP code"""
    city_map = {
        '31088': 'Warner Robins',
        '31093': 'Centerville', 
        '31098': 'Bonaire'
    }
    return city_map.get(zip_code, 'Unknown')

def analyze_zip_trends(zip_code, properties, dashboard_data):
    """Analyze trends for a specific ZIP code"""
    active_properties = [p for p in properties if p.get('status') == 'Active']
    pending_properties = [p for p in properties if p.get('status') == 'Pending']
    sold_properties = [p for p in properties if p.get('status') == 'Sold']
    
    # Price trends
    if active_properties:
        prices = [p.get('price', 0) for p in active_properties]
        avg_price = sum(prices) / len(prices) if prices else 0
        
        # Calculate price changes (simulated)
        price_change_30d = round(random.uniform(-0.03, 0.05) * 100, 1)
        
        dashboard_data["trends"][zip_code] = {
            "avg_price": round(avg_price, 2),
            "price_change_30d": price_change_30d,
            "active_listings": len(active_properties),
            "pending_listings": len(pending_properties),
            "sold_30d": len([p for p in sold_properties]),
            "days_on_market_avg": sum(p.get('days_on_market', 0) for p in active_properties) / max(len(active_properties), 1),
            "price_per_sqft_avg": sum(p.get('price', 0) / max(p.get('square_feet', 1), 1) for p in active_properties) / max(len(active_properties), 1)
        }

def calculate_overall_market(dashboard_data):
    """Calculate overall market metrics"""
    total_properties = sum(zip_data.get("property_count", 0) for zip_data in dashboard_data["zip_codes"].values())
    
    health_scores = [zip_data.get("market_summary", {}).get("market_health", 50) 
                    for zip_data in dashboard_data["zip_codes"].values() if zip_data.get("market_summary")]
    avg_health = sum(health_scores) / len(health_scores) if health_scores else 50
    
    # Calculate overall metrics
    dashboard_data["market_overview"] = {
        "total_zip_codes": len(dashboard_data["zip_codes"]),
        "total_properties": total_properties,
        "overall_health_score": round(avg_health, 1),
        "market_condition": get_market_condition(avg_health),
        "last_updated": datetime.now().isoformat(),
        "update_frequency": "6 hours",
        "data_sources": ["free_data_collector", "simulated_data"]
    }

def get_market_condition(health_score):
    """Convert health score to market condition"""
    if health_score >= 70:
        return "Seller's Market"
    elif health_score >= 60:
        return "Balanced Market"
    elif health_score >= 40:
        return "Buyer's Market"
    else:
        return "Depressed Market"

def generate_alerts(dashboard_data):
    """Generate market alerts"""
    alerts = []
    
    for zip_code, zip_data in dashboard_data["zip_codes"].items():
        summary = zip_data.get("market_summary", {})
        
        # Low inventory alert
        inventory = summary.get("inventory", 0)
        if inventory > 0 and inventory < 20:
            alerts.append({
                "type": "warning",
                "zip": zip_code,
                "title": "Low Inventory Alert",
                "message": f"Only {inventory} active listings in {zip_code}",
                "severity": "medium"
            })
        
        # Good buying opportunity
        market_health = summary.get("market_health", 0)
        if market_health < 40:
            alerts.append({
                "type": "opportunity",
                "zip": zip_code,
                "title": "Buyer's Market Opportunity",
                "message": f"Strong buyer's market detected in {zip_code}",
                "severity": "high"
            })
    
    dashboard_data["alerts"] = alerts

def generate_recommendations(dashboard_data):
    """Generate investment recommendations"""
    recommendations = []
    
    if dashboard_data["zip_codes"]:
        # Find best ZIP for investment (lowest health score = buyer's market)
        zip_items = list(dashboard_data["zip_codes"].items())
        if zip_items:
            worst_zip = min(zip_items, 
                          key=lambda x: x[1].get("market_summary", {}).get("market_health", 100))
            
            recommendations.append({
                "type": "investment",
                "title": f"Consider Buying in {worst_zip[0]}",
                "reason": "This area shows buyer's market conditions",
                "confidence": "medium"
            })
            
            # Find best ZIP for selling (highest health score)
            best_zip = max(zip_items,
                          key=lambda x: x[1].get("market_summary", {}).get("market_health", 0))
            
            recommendations.append({
                "type": "selling",
                "title": f"Consider Selling in {best_zip[0]}",
                "reason": "This area shows seller's market conditions",
                "confidence": "medium"
            })
    
    dashboard_data["recommendations"] = recommendations

def save_dashboard_files(dashboard_data, base_dir):
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
    if dashboard_data.get("trends"):
        trends_file = base_dir / "market_trends.json"
        with open(trends_file, 'w', encoding='utf-8') as f:
            json.dump(dashboard_data["trends"], f, indent=2)
    
    print(f"📊 Dashboard files saved to {base_dir}")

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
    zip_codes = ['31088', '31093', '31098']
    
    for zip_code in zip_codes:
        zip_dir = base_dir / zip_code
        latest_file = zip_dir / "latest.json"
        summary_file = zip_dir / "market_summary.json"
        properties_file = zip_dir / "properties.json"
        
        try:
            if latest_file.exists():
                with open(latest_file, 'r', encoding='utf-8') as f:
                    zip_data = json.load(f)
                
                # Add ZIP summary to dashboard
                dashboard_data["zip_codes"][zip_code] = {
                    "market_summary": zip_data.get("market_stats", {}),
                    "property_count": len(zip_data.get("properties", [])),
                    "last_updated": zip_data.get("timestamp", ""),
                    "location": {
                        "city": get_city_by_zip(zip_code),
                        "county": "Houston",
                        "state": "GA"
                    }
                }
                
                # Process properties for trends
                properties = zip_data.get("properties", [])
                if properties:
                    analyze_zip_trends(zip_code, properties, dashboard_data)
                    
            elif summary_file.exists():
                # Fallback to summary file if latest.json doesn't exist
                with open(summary_file, 'r', encoding='utf-8') as f:
                    summary = json.load(f)
                
                dashboard_data["zip_codes"][zip_code] = {
                    "market_summary": summary,
                    "property_count": summary.get("total_properties", 0),
                    "last_updated": datetime.now().isoformat(),
                    "location": {
                        "city": get_city_by_zip(zip_code),
                        "county": "Houston",
                        "state": "GA"
                    }
                }
                
        except Exception as e:
            print(f"Error processing {zip_code}: {e}")
            continue
    
    # Calculate overall market overview
    if dashboard_data["zip_codes"]:
        calculate_overall_market(dashboard_data)
    
    # Generate alerts and recommendations
    generate_alerts(dashboard_data)
    generate_recommendations(dashboard_data)
    
    # Save dashboard JSON
    save_dashboard_files(dashboard_data, base_dir)
    
    print(f"✅ Dashboard created successfully!")
    print(f"   - Zips processed: {len(dashboard_data['zip_codes'])}")
    print(f"   - Total properties: {dashboard_data['market_overview'].get('total_properties', 0)}")
    print(f"   - Market health: {dashboard_data['market_overview'].get('overall_health_score', 0)}/100")
    
    return dashboard_data

if __name__ == "__main__":
    # Create dashboard
    dashboard = create_dashboard_json()
