#!/usr/bin/env python3
"""
Generate AI insights using DeepSeek API
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime
import time

class DeepSeekAIInsights:
    """Generate AI-powered real estate insights using DeepSeek"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('DEEPSEEK_API_KEY')
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.base_dir = Path("data/houston-county-ga")
        
    def generate_insights(self):
        """Generate AI insights for all collected data"""
        print("Generating DeepSeek AI insights...")
        
        if not self.api_key:
            print("⚠️  No DeepSeek API key found. Using simulated insights.")
            return self._generate_simulated_insights()
        
        try:
            # Load dashboard data
            dashboard_file = self.base_dir / "dashboard.json"
            if not dashboard_file.exists():
                print("⚠️  Dashboard data not found. Collect data first.")
                return self._generate_simulated_insights()
            
            with open(dashboard_file, 'r', encoding='utf-8') as f:
                dashboard_data = json.load(f)
            
            # Generate market analysis
            market_analysis = self._analyze_market_with_ai(dashboard_data)
            
            # Generate investment recommendations
            investment_recs = self._generate_investment_recommendations(dashboard_data)
            
            # Generate neighborhood insights
            neighborhood_insights = self._generate_neighborhood_insights(dashboard_data)
            
            # Save insights
            insights_data = {
                "timestamp": datetime.now().isoformat(),
                "market_analysis": market_analysis,
                "investment_recommendations": investment_recs,
                "neighborhood_insights": neighborhood_insights,
                "ai_model": "deepseek-chat",
                "confidence_score": 0.85
            }
            
            self._save_insights(insights_data)
            
            return insights_data
            
        except Exception as e:
            print(f"Error generating AI insights: {e}")
            return self._generate_simulated_insights()
    
    def _analyze_market_with_ai(self, dashboard_data):
        """Analyze market data using AI"""
        
        # Prepare market data summary
        market_summary = dashboard_data.get("market_overview", {})
        zip_data = dashboard_data.get("zip_codes", {})
        
        prompt = f"""
        Analyze this real estate market data and provide insights:
        
        MARKET OVERVIEW:
        - Total Properties: {market_summary.get('total_properties', 0)}
        - Active Listings: {market_summary.get('active_listings', 0)}
        - Market Health Score: {market_summary.get('overall_health_score', 0)}/100
        - Market Condition: {market_summary.get('market_condition', 'Unknown')}
        
        ZIP CODE DATA:
        {json.dumps(zip_data, indent=2)}
        
        Please analyze and provide:
        1. Current market trends
        2. Best opportunities for buyers
        3. Best opportunities for sellers
        4. Risk factors to watch
        5. 3-month market outlook
        
        Keep response concise and data-driven.
        """
        
        return self._call_deepseek_api(prompt)
    
    def _generate_investment_recommendations(self, dashboard_data):
        """Generate AI-powered investment recommendations"""
        
        prompt = f"""
        Based on this real estate data, provide investment recommendations:
        
        DATA: {json.dumps(dashboard_data, indent=2)}
        
        Provide specific investment recommendations including:
        1. Best ZIP codes for flipping houses
        2. Best ZIP codes for rental properties
        3. Risk assessment for each area
        4. Expected ROI for different strategies
        5. Timing recommendations (when to buy/sell)
        
        Format as actionable recommendations with confidence levels.
        """
        
        return self._call_deepseek_api(prompt)
    
    def _generate_neighborhood_insights(self, dashboard_data):
        """Generate neighborhood-level insights"""
        
        prompt = f"""
        Analyze these neighborhood real estate patterns:
        
        DATA: {json.dumps(dashboard_data, indent=2)}
        
        Provide neighborhood insights including:
        1. Up-and-coming areas
        2. Areas with declining values
        3. School district impacts
        4. Development trends
        5. Demographic influences
        
        Focus on specific, actionable insights for investors.
        """
        
        return self._call_deepseek_api(prompt)
    
    def _call_deepseek_api(self, prompt):
        """Call DeepSeek API with prompt"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a real estate market analyst with 20 years of experience."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                print(f"API Error: {response.status_code}")
                return self._get_fallback_response()
                
        except Exception as e:
            print(f"API call failed: {e}")
            return self._get_fallback_response()
    
    def _get_fallback_response(self):
        """Get fallback response when API fails"""
        return {
            "market_analysis": "Market analysis unavailable. Please check API configuration.",
            "recommendations": "Enable DeepSeek API for AI-powered insights.",
            "confidence": "low"
        }
    
    def _generate_simulated_insights(self):
        """Generate simulated insights when API is unavailable"""
        print("Generating simulated AI insights...")
        
        insights = {
            "timestamp": datetime.now().isoformat(),
            "market_analysis": """
            MARKET ANALYSIS:
            - Overall market shows balanced conditions with slight buyer's market tendencies
            - Inventory levels are moderate across all ZIP codes
            - Price growth has stabilized after recent appreciation
            
            KEY OBSERVATIONS:
            1. ZIP 31088 shows strongest seller conditions with low inventory
            2. ZIP 31093 offers best value opportunities for buyers
            3. Market velocity is normal with average DOM of 28 days
            
            OUTLOOK: Stable growth expected over next 3-6 months
            """,
            "investment_recommendations": [
                {
                    "strategy": "House Flipping",
                    "recommended_zip": "31093",
                    "reason": "Lower entry prices with room for appreciation",
                    "estimated_roi": "15-25%",
                    "risk": "Medium"
                },
                {
                    "strategy": "Rental Properties",
                    "recommended_zip": "31088",
                    "reason": "Strong rental demand near military base",
                    "estimated_cap_rate": "6-8%",
                    "risk": "Low"
                }
            ],
            "neighborhood_insights": {
                "warner_robins": "Stable market driven by military employment",
                "centerville": "Growing family-oriented community",
                "bonaire": "Mixed market with both opportunities and risks"
            },
            "ai_model": "simulated",
            "confidence_score": 0.65
        }
        
        self._save_insights(insights)
        return insights
    
    def _save_insights(self, insights_data):
        """Save AI insights to file"""
        insights_dir = self.base_dir / "ai_insights"
        insights_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save full insights
        insights_file = insights_dir / f"ai_insights_{timestamp}.json"
        with open(insights_file, 'w', encoding='utf-8') as f:
            json.dump(insights_data, f, indent=2, default=str)
        
        # Save latest insights
        latest_file = insights_dir / "latest_insights.json"
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(insights_data, f, indent=2, default=str)
        
        # Save summary for dashboard
        summary_file = self.base_dir / "ai_insights_summary.json"
        summary = {
            "last_updated": insights_data["timestamp"],
            "market_sentiment": self._extract_sentiment(insights_data),
            "top_recommendation": insights_data.get("investment_recommendations", [{}])[0] if insights_data.get("investment_recommendations") else {},
            "confidence": insights_data.get("confidence_score", 0)
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print("✅ AI insights saved successfully!")
    
    def _extract_sentiment(self, insights_data):
        """Extract market sentiment from insights"""
        analysis = insights_data.get("market_analysis", "").lower()
        
        if any(word in analysis for word in ["strong", "growing", "opportunity", "positive"]):
            return "bullish"
        elif any(word in analysis for word in ["declining", "risk", "caution", "negative"]):
            return "bearish"
        else:
            return "neutral"

if __name__ == "__main__":
    # Initialize and generate insights
    ai = DeepSeekAIInsights()
    insights = ai.generate_insights()
    
    print("\n" + "="*50)
    print("AI INSIGHTS SUMMARY")
    print("="*50)
    print(f"Generated: {insights.get('timestamp', 'N/A')}")
    print(f"Confidence: {insights.get('confidence_score', 0)*100}%")
    
    # Print key recommendations
    recs = insights.get("investment_recommendations", [])
    if recs:
        print("\nTOP RECOMMENDATIONS:")
        for i, rec in enumerate(recs[:3], 1):
            print(f"{i}. {rec.get('strategy', 'N/A')} in ZIP {rec.get('recommended_zip', 'N/A')}")
            print(f"   ROI: {rec.get('estimated_roi', 'N/A')}")
