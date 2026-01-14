# scripts/deepseek_ai_insights.py
import requests
import json
import os
from datetime import datetime
from pathlib import Path

class DeepSeekAI:
    """Free AI insights using DeepSeek API"""
    
    def __init__(self, api_key=None):
        # DeepSeek offers free API with reasonable limits
        # Get your free API key from: https://platform.deepseek.com/
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.model = "deepseek-chat"  # Free model
        
    def generate_market_insight(self, market_data, property_data=None):
        """Generate AI market insight"""
        
        prompt = f"""
        As a real estate market analyst, provide a concise, data-driven insight based on this market data:
        
        Market Overview for ZIP {market_data.get('zip_code', 'Unknown')}:
        - Inventory: {market_data.get('inventory_count', 0)} active listings
        - Median Price: ${market_data.get('median_price', 0):,}
        - Days on Market: {market_data.get('avg_days_on_market', 0)} days
        - Market Trend: {market_data.get('market_trend', 'stable')}
        - Health Score: {market_data.get('market_health_score', 50)}/100
        - New Listings (30d): {market_data.get('new_listings_30d', 0)}
        - Price Reductions (30d): {market_data.get('price_reductions_30d', 0)}
        
        Generate a practical insight for realtors. Focus on:
        1. What this means for buyers vs sellers
        2. One specific opportunity in the current market
        3. One thing to watch out for
        4. Recommended strategy for this week
        
        Keep it under 150 words. Be direct and actionable.
        """
        
        try:
            if not self.api_key:
                return self._get_fallback_insight(market_data)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a real estate market analyst providing concise, actionable insights."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 300,
                "temperature": 0.7
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                insight = result['choices'][0]['message']['content'].strip()
                
                return {
                    "id": f"insight_{int(datetime.now().timestamp())}",
                    "timestamp": datetime.now().isoformat(),
                    "zip_code": market_data.get('zip_code'),
                    "insight": insight,
                    "source": "deepseek_ai",
                    "market_conditions": {
                        "inventory": market_data.get('inventory_count'),
                        "median_price": market_data.get('median_price'),
                        "trend": market_data.get('market_trend')
                    },
                    "action_items": self._extract_action_items(insight),
                    "confidence_score": self._calculate_confidence(market_data)
                }
            else:
                print(f"DeepSeek API error: {response.status_code}")
                return self._get_fallback_insight(market_data)
                
        except Exception as e:
            print(f"Error generating AI insight: {e}")
            return self._get_fallback_insight(market_data)
    
    def generate_daily_tip(self, realtor_experience="new", market_data=None):
        """Generate daily tip for realtors"""
        
        experience_levels = {
            "new": "a brand new realtor just starting out",
            "intermediate": "an experienced realtor with 1-3 years in the business",
            "experienced": "a seasoned realtor with 5+ years of experience"
        }
        
        prompt = f"""
        Generate a daily professional tip for {experience_levels.get(realtor_experience, 'a realtor')}.
        
        Today's date: {datetime.now().strftime('%A, %B %d, %Y')}
        
        The tip should:
        1. Be specific and actionable (something they can do today)
        2. Help build their business or serve clients better
        3. Include one specific conversation starter
        4. Be encouraging and confidence-building
        
        Market Context (if helpful):
        - Day of week: {datetime.now().strftime('%A')}
        - Typical {datetime.now().strftime('%A')} activities in real estate
        
        Format the response as a JSON object with:
        {{
            "title": "Brief title of the tip",
            "tip": "The main tip text (2-3 sentences)",
            "action": "Specific action to take today",
            "conversation_starter": "A phrase to use with clients",
            "confidence_builder": "One thing to remember to build confidence"
        }}
        """
        
        try:
            if not self.api_key:
                return self._get_fallback_tip(realtor_experience)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a real estate coach helping agents succeed."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 400,
                "temperature": 0.8
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                tip_text = result['choices'][0]['message']['content'].strip()
                
                # Try to parse as JSON, if it's plain text, wrap it
                try:
                    tip_data = json.loads(tip_text)
                except:
                    tip_data = {
                        "title": "Daily Professional Tip",
                        "tip": tip_text,
                        "action": "Review this tip and implement one thing today",
                        "conversation_starter": "I was reviewing the latest market data and noticed...",
                        "confidence_builder": "Your knowledge and preparation make you valuable to clients."
                    }
                
                return {
                    "id": f"tip_{int(datetime.now().timestamp())}",
                    "timestamp": datetime.now().isoformat(),
                    "experience_level": realtor_experience,
                    "tip": tip_data,
                    "day_of_week": datetime.now().strftime('%A'),
                    "source": "deepseek_ai"
                }
            else:
                return self._get_fallback_tip(realtor_experience)
                
        except Exception as e:
            print(f"Error generating daily tip: {e}")
            return self._get_fallback_tip(realtor_experience)
    
    def generate_property_analysis(self, property_data):
        """Generate AI analysis for a specific property"""
        
        prompt = f"""
        Analyze this property listing for a realtor:
        
        Property: {property_data.get('address', 'Unknown address')}
        Price: ${property_data.get('price', 0):,}
        Beds/Baths: {property_data.get('bedrooms', 0)}/{property_data.get('bathrooms', 0)}
        Square Feet: {property_data.get('sqft', 0):,}
        Days on Market: {property_data.get('days_on_market', 0)}
        Status: {property_data.get('status', 'Unknown')}
        Property Type: {property_data.get('property_type', 'Unknown')}
        
        Provide a brief analysis covering:
        1. Pricing assessment (fair, over, under)
        2. Target buyer profile
        3. Key selling points to highlight
        4. One potential concern to address
        5. Recommended marketing angle
        
        Be concise and practical.
        """
        
        try:
            if not self.api_key:
                return self._get_fallback_property_analysis(property_data)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a real estate analyst helping agents evaluate properties."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 350,
                "temperature": 0.6
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                analysis = result['choices'][0]['message']['content'].strip()
                
                return {
                    "property_id": property_data.get('id', 'unknown'),
                    "address": property_data.get('address'),
                    "analysis": analysis,
                    "timestamp": datetime.now().isoformat(),
                    "source": "deepseek_ai"
                }
            else:
                return self._get_fallback_property_analysis(property_data)
                
        except Exception as e:
            print(f"Error generating property analysis: {e}")
            return self._get_fallback_property_analysis(property_data)
    
    def _extract_action_items(self, insight_text):
        """Extract action items from insight text"""
        # Simple extraction - in production could use more sophisticated NLP
        action_words = ['focus on', 'consider', 'look for', 'target', 'prioritize', 'recommend', 'suggest']
        actions = []
        
        lines = insight_text.split('.')
        for line in lines:
            line_lower = line.lower()
            for word in action_words:
                if word in line_lower:
                    actions.append(line.strip())
                    break
        
        return actions[:3]  # Return top 3 actions
    
    def _calculate_confidence(self, market_data):
        """Calculate confidence score for insight"""
        # Simple calculation based on data completeness
        score = 50
        
        if market_data.get('inventory_count', 0) > 0:
            score += 10
        
        if market_data.get('median_price', 0) > 0:
            score += 10
        
        if market_data.get('new_listings_30d', 0) > 0:
            score += 10
        
        if market_data.get('market_health_score', 0) > 0:
            score += 10
        
        return min(score, 95)
    
    def _get_fallback_insight(self, market_data):
        """Fallback insight when AI fails"""
        fallbacks = [
            f"With {market_data.get('inventory_count', 0)} active listings and median price of ${market_data.get('median_price', 0):,}, the market shows {market_data.get('market_trend', 'stable')} conditions. Consider focusing on properties that have been on market 30+ days for potential negotiations.",
            f"Market inventory at {market_data.get('inventory_count', 0)} listings suggests a {'seller' if market_data.get('inventory_count', 0) < 80 else 'buyer'} favored market. Price reductions ({market_data.get('price_reductions_30d', 0)}) indicate some seller flexibility.",
            f"Current market shows {market_data.get('avg_days_on_market', 0)} average days on market. {'Properties are moving quickly' if market_data.get('avg_days_on_market', 0) < 30 else 'Consider price adjustments for stagnant listings'}."
        ]
        
        import random
        return {
            "id": f"fallback_{int(datetime.now().timestamp())}",
            "timestamp": datetime.now().isoformat(),
            "zip_code": market_data.get('zip_code'),
            "insight": random.choice(fallbacks),
            "source": "fallback_ai",
            "action_items": ["Review market data daily", "Update client communications", "Adjust pricing strategies"],
            "confidence_score": 75
        }
    
    def _get_fallback_tip(self, experience_level):
        """Fallback tip when AI fails"""
        day_of_week = datetime.now().strftime('%A')
        
        tips_by_day = {
            'Monday': {
                'title': 'Start Strong',
                'tip': 'Review all new listings and price changes from the weekend. Update your CMAs and reach out to 3 past clients with a market update.',
                'action': 'Schedule 2 showings for this week',
                'conversation_starter': 'I noticed some interesting price changes over the weekend...',
                'confidence_builder': 'Your preparation sets you apart from other agents.'
            },
            'Tuesday': {
                'title': 'Client Connection Day',
                'tip': 'Focus on client follow-ups and consultations. Perfect day for market updates and answering questions.',
                'action': 'Call 5 clients with personalized updates',
                'conversation_starter': 'Based on your criteria, I found...',
                'confidence_builder': 'Your knowledge builds client trust instantly.'
            },
            'Wednesday': {
                'title': 'Mid-Week Momentum',
                'tip': 'Update all your listings with fresh photos and descriptions. Check competitor pricing.',
                'action': 'Refresh 2 listing descriptions',
                'conversation_starter': 'The mid-week market shows...',
                'confidence_builder': 'Your attention to detail makes listings stand out.'
            },
            'Thursday': {
                'title': 'Weekend Preparation',
                'tip': 'Prepare for weekend showings and open houses. Confirm all appointments.',
                'action': 'Schedule 3 weekend showings',
                'conversation_starter': 'This weekend presents great opportunities because...',
                'confidence_builder': 'Your organization ensures smooth transactions.'
            },
            'Friday': {
                'title': 'Follow-Up Focus',
                'tip': 'Follow up on all week\'s leads and showings. Prepare weekend showing packets.',
                'action': 'Send 5 follow-up emails from this week',
                'conversation_starter': 'Following up on our conversation about...',
                'confidence_builder': 'Your persistence converts leads to clients.'
            },
            'Saturday': {
                'title': 'Showcase Day',
                'tip': 'Perfect day for open houses and showings. Be prepared with market data for buyer questions.',
                'action': 'Host at least 1 open house',
                'conversation_starter': 'Welcome! Let me show you why this property stands out...',
                'confidence_builder': 'Your expertise shines during showings.'
            },
            'Sunday': {
                'title': 'Strategy Session',
                'tip': 'Review the week\'s activity and plan for next week. Update your business goals.',
                'action': 'Plan next week\'s schedule',
                'conversation_starter': 'Looking ahead to next week...',
                'confidence_builder': 'Your strategic planning drives long-term success.'
            }
        }
        
        tip = tips_by_day.get(day_of_week, tips_by_day['Monday'])
        
        return {
            "id": f"fallback_tip_{int(datetime.now().timestamp())}",
            "timestamp": datetime.now().isoformat(),
            "experience_level": experience_level,
            "tip": tip,
            "day_of_week": day_of_week,
            "source": "fallback"
        }
    
    def _get_fallback_property_analysis(self, property_data):
        """Fallback property analysis"""
        return {
            "property_id": property_data.get('id', 'unknown'),
            "address": property_data.get('address'),
            "analysis": f"This {property_data.get('bedrooms', 0)}-bedroom, {property_data.get('bathrooms', 0)}-bathroom property at ${property_data.get('price', 0):,} presents {'good value' if property_data.get('price_per_sqft', 0) < 150 else 'premium pricing'}. Consider highlighting the {property_data.get('sqft', 0):,} sqft and {property_data.get('property_type', 'property')} features. {'Price appears competitive' if property_data.get('days_on_market', 0) < 30 else 'Consider market comparison given days on market.'}",
            "timestamp": datetime.now().isoformat(),
            "source": "fallback"
        }


def generate_all_insights():
    """Generate AI insights for all ZIP codes"""
    base_dir = Path("data/houston-county-ga")
    
    # Initialize DeepSeek AI
    ai = DeepSeekAI()
    
    insights_data = {
        "generated_at": datetime.now().isoformat(),
        "daily_tips": {},
        "market_insights": {},
        "property_analyses": []
    }
    
    for zip_dir in base_dir.iterdir():
        if zip_dir.is_dir():
            zip_code = zip_dir.name
            
            # Load market summary
            summary_file = zip_dir / "market_summary.json"
            if summary_file.exists():
                with open(summary_file, 'r') as f:
                    market_summary = json.load(f)
                    market_summary['zip_code'] = zip_code
                
                # Generate market insight
                insight = ai.generate_market_insight(market_summary)
                insights_data["market_insights"][zip_code] = insight
                
                # Generate daily tip for each experience level
                for level in ["new", "intermediate", "experienced"]:
                    tip = ai.generate_daily_tip(level, market_summary)
                    if zip_code not in insights_data["daily_tips"]:
                        insights_data["daily_tips"][zip_code] = {}
                    insights_data["daily_tips"][zip_code][level] = tip
    
    # Save all insights
    insights_file = base_dir / "ai_insights.json"
    with open(insights_file, 'w', encoding='utf-8') as f:
        json.dump(insights_data, f, indent=2, default=str)
    
    print(f"✅ AI insights generated and saved to {insights_file}")
    
    # Also generate dashboard-specific JSON
    generate_dashboard_json(insights_data)


def generate_dashboard_json(insights_data):
    """Generate simplified JSON for dashboard"""
    dashboard_data = {
        "last_updated": datetime.now().isoformat(),
        "ai_generated": True,
        "tips": [],
        "insights": [],
        "properties": []
    }
    
    # Process tips
    for zip_code, zip_tips in insights_data.get("daily_tips", {}).items():
        for level, tip_data in zip_tips.items():
            if tip_data.get('tip'):
                dashboard_data["tips"].append({
                    "zip": zip_code,
                    "level": level,
                    "title": tip_data['tip'].get('title', 'Daily Tip'),
                    "content": tip_data['tip'].get('tip', ''),
                    "action": tip_data['tip'].get('action', ''),
                    "time": tip_data['timestamp']
                })
    
    # Process market insights
    for zip_code, insight in insights_data.get("market_insights", {}).items():
        if insight.get('insight'):
            dashboard_data["insights"].append({
                "zip": zip_code,
                "insight": insight['insight'],
                "confidence": insight.get('confidence_score', 75),
                "actions": insight.get('action_items', []),
                "time": insight['timestamp']
            })
    
    # Save dashboard JSON
    dashboard_file = Path("data/houston-county-ga/dashboard_data.json")
    with open(dashboard_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2, default=str)
    
    print(f"✅ Dashboard data saved to {dashboard_file}")


if __name__ == "__main__":
    generate_all_insights()
