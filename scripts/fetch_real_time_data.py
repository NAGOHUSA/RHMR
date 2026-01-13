# [file name]: scripts/fetch_real_time_data.py
import json
import random
from datetime import datetime
from pathlib import Path

def generate_real_time_data():
    """Generate simulated real-time data for testing"""
    
    zip_codes = ["31088", "31093", "31098"]
    data = {
        'last_updated': datetime.now().isoformat(),
        'zip_codes': [],
        'market_summary': {},
        'trends_24h': {},
        'realtor_tips': []
    }
    
    for zip_code in zip_codes:
        base_price = 285000 + random.randint(-20000, 20000)
        inventory = random.randint(80, 120)
        
        zip_data = {
            'zip': zip_code,
            'city': 'Warner Robins' if zip_code == '31088' else 'Centerville' if zip_code == '31093' else 'Bonaire',
            'timestamp': datetime.now().isoformat(),
            'metrics': {
                'composite_price': base_price,
                'composite_inventory': inventory,
                'market_velocity': random.randint(60, 90),
                'price_momentum': round(random.uniform(-0.5, 1.0), 2),
                'buyer_seller_index': random.randint(40, 80),
                'opportunity_score': random.randint(60, 85)
            }
        }
        
        data['zip_codes'].append(zip_data)
    
    # Calculate market summary
    prices = [z['metrics']['composite_price'] for z in data['zip_codes']]
    inventories = [z['metrics']['composite_inventory'] for z in data['zip_codes']]
    opportunities = [z['metrics']['opportunity_score'] for z in data['zip_codes']]
    
    data['market_summary'] = {
        'avg_price': int(sum(prices) / len(prices)),
        'total_inventory': sum(inventories),
        'avg_opportunity_score': round(sum(opportunities) / len(opportunities), 1),
        'market_trend': 'heating' if random.random() > 0.5 else 'cooling',
        'best_opportunity_zip': max(data['zip_codes'], key=lambda x: x['metrics']['opportunity_score'])['zip']
    }
    
    data['trends_24h'] = {
        'price_movement': f"{'+' if random.random() > 0.3 else ''}{round(random.uniform(-0.5, 1.0), 1)}%",
        'inventory_change': f"{'+' if random.random() > 0.5 else ''}{random.randint(-10, 15)} listings",
        'new_listings_today': str(random.randint(5, 20)),
        'pending_sales': str(random.randint(3, 12)),
        'avg_dom_trend': '↓ 2 days' if random.random() > 0.5 else '↑ 1 day',
        'market_pulse': random.choice(['High Activity', 'Moderate Activity', 'Steady'])
    }
    
    # Generate realtor tips
    day_of_week = datetime.now().strftime('%A')
    daily_tips = {
        'Monday': "📅 Plan your week: Review new listings and schedule showings",
        'Tuesday': "📞 Best day for client follow-ups and market updates",
        'Wednesday': "📊 Update your CMA reports with latest data",
        'Thursday': "🤝 Network with other agents and schedule open houses",
        'Friday': "🎯 Target weekend showings - buyers are actively searching",
        'Saturday': "🏠 Host open houses and conduct showings",
        'Sunday': "📝 Review week's activity and plan for next week"
    }
    
    data['realtor_tips'] = [
        "🔥 Check today's new listings for potential opportunities",
        f"📅 **{day_of_week} Tip**: {daily_tips.get(day_of_week, 'Stay proactive in your market!')}",
        "📊 Use the latest market data in your client presentations",
        "🤝 Build confidence by sharing data-driven insights with clients"
    ]
    
    return data

def save_data():
    """Save generated data to JSON files"""
    
    # Create directory structure
    base_dir = Path("data/houston-county-ga")
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate and save dashboard data
    data = generate_real_time_data()
    
    # Save dashboard_data.json
    dashboard_file = base_dir / "dashboard_data.json"
    with open(dashboard_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Real-time data generated and saved to {dashboard_file}")
    print(f"📊 Last updated: {data['last_updated']}")
    print(f"🏠 ZIP codes processed: {len(data['zip_codes'])}")
    print(f"📈 Market trend: {data['market_summary']['market_trend']}")

if __name__ == "__main__":
    save_data()
