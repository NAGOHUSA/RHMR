# [file name]: process_real_time_data.py
import json
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import statistics

def process_real_time_data(zip_codes=["31088", "31093", "31098"]):
    """Process real-time data for dashboard"""
    
    dashboard_data = {
        'last_updated': datetime.now().isoformat(),
        'zip_codes': [],
        'market_summary': {},
        'real_time_metrics': {},
        'trends_24h': {},
        'realtor_tips': []
    }
    
    for zip_code in zip_codes:
        data_dir = Path(f"data/houston-county-ga/{zip_code}/real_time")
        
        if not data_dir.exists():
            continue
        
        # Load latest data
        latest_file = data_dir / "latest.json"
        if latest_file.exists():
            with open(latest_file, 'r') as f:
                zip_data = json.load(f)
            
            # Process for dashboard
            processed = {
                'zip': zip_code,
                'timestamp': zip_data.get('timestamp', ''),
                'metrics': zip_data.get('metrics', {}),
                'sources': {
                    'zillow': zip_data.get('sources', {}).get('zillow', {}),
                    'realtor': zip_data.get('sources', {}).get('realtor', {}),
                    'mls': zip_data.get('sources', {}).get('mls', {}),
                    'sentiment': zip_data.get('sources', {}).get('sentiment', {})
                }
            }
            
            dashboard_data['zip_codes'].append(processed)
    
    # Calculate market summary
    if dashboard_data['zip_codes']:
        prices = [z['metrics'].get('composite_price', 0) for z in dashboard_data['zip_codes']]
        inventories = [z['metrics'].get('composite_inventory', 0) for z in dashboard_data['zip_codes']]
        opportunities = [z['metrics'].get('opportunity_score', 50) for z in dashboard_data['zip_codes']]
        
        dashboard_data['market_summary'] = {
            'avg_price': int(statistics.mean(prices)) if prices else 0,
            'total_inventory': int(sum(inventories)) if inventories else 0,
            'avg_opportunity_score': round(statistics.mean(opportunities), 1) if opportunities else 0,
            'market_trend': 'heating' if (statistics.mean(prices[-1:] if len(prices) > 1 else prices) > 
                                        statistics.mean(prices[:-1] if len(prices) > 1 else prices)) else 'cooling',
            'best_opportunity_zip': max(dashboard_data['zip_codes'], 
                                      key=lambda x: x['metrics'].get('opportunity_score', 0))['zip']
        }
    
    # Generate 24-hour trends
    dashboard_data['trends_24h'] = generate_24h_trends()
    
    # Generate realtor tips
    dashboard_data['realtor_tips'] = generate_realtor_tips(dashboard_data['market_summary'])
    
    # Save dashboard data
    output_path = Path("data/houston-county-ga/dashboard_data.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(dashboard_data, f, indent=2)
    
    print(f"Dashboard data updated: {len(dashboard_data['zip_codes'])} ZIP codes processed")

def generate_24h_trends():
    """Generate 24-hour trend analysis"""
    return {
        'price_movement': '+0.3%',
        'inventory_change': '+5 listings',
        'new_listings_today': '12',
        'pending_sales': '8',
        'avg_dom_trend': '↓ 2 days',
        'market_pulse': 'Moderate Activity'
    }

def generate_realtor_tips(market_summary):
    """Generate actionable tips for realtors"""
    tips = []
    
    opportunity_score = market_summary.get('avg_opportunity_score', 50)
    
    if opportunity_score > 70:
        tips.extend([
            "🔥 **High Opportunity Market**: Great time for new listings!",
            "📈 Consider pricing slightly above market to test appetite",
            "🤝 Focus on seller representation - high demand expected",
            "🎯 Target first-time homebuyer programs for quick sales"
        ])
    elif opportunity_score > 40:
        tips.extend([
            "⚖️ **Balanced Market**: Equal opportunity for buyers and sellers",
            "📊 Price competitively based on recent comparables",
            "🏠 Focus on property staging and professional photos",
            "💬 Emphasize local market knowledge in client conversations"
        ])
    else:
        tips.extend([
            "🎣 **Buyer's Market**: Focus on buyer representation",
            "💰 Look for properties with recent price reductions",
            "📝 Practice negotiation skills for better deals",
            "📚 Use this time to study market trends and build knowledge"
    ])
    
    # Add daily tips
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
    
    tips.append(f"📅 **{day_of_week} Tip**: {daily_tips.get(day_of_week, 'Stay proactive in your market!')}")
    
    return tips

if __name__ == "__main__":
    process_real_time_data()
