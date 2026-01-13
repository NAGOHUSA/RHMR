# [file name]: fetch_real_time_data.py
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import time
from collections import defaultdict

class RealTimeDataFetcher:
    def __init__(self, zip_code="31088"):
        self.zip_code = zip_code
        self.data_dir = Path(f"data/houston-county-ga/{zip_code}/real_time")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def fetch_zillow_data(self):
        """Fetch real-time Zillow data"""
        try:
            # Zillow API endpoint (using public data)
            url = f"https://www.zillow.com/webservice/GetDeepSearchResults.htm"
            # Note: This requires a Zillow API key in production
            # For demo, we'll use mock data
            return self._mock_zillow_data()
        except Exception as e:
            print(f"Zillow fetch failed: {e}")
            return None
    
    def fetch_realtor_data(self):
        """Fetch Realtor.com market data"""
        try:
            # Using Realtor.com API (requires API key in production)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            url = f"https://www.realtor.com/realestateandhomes-search/{self.zip_code}"
            # For demo, return mock data
            return self._mock_realtor_data()
        except Exception as e:
            print(f"Realtor.com fetch failed: {e}")
            return None
    
    def fetch_mls_data(self):
        """Fetch MLS data (simulated - would require MLS API access)"""
        return {
            'active_listings': self._random_in_range(85, 120),
            'new_listings_today': self._random_in_range(2, 8),
            'pending_sales': self._random_in_range(25, 40),
            'sold_last_7_days': self._random_in_range(10, 25),
            'avg_list_price': self._random_in_range(250000, 350000),
            'avg_sold_price': self._random_in_range(245000, 340000),
            'avg_dom': self._random_in_range(15, 45),
            'list_to_sold_ratio': round(self._random_in_range(0.95, 1.05), 2)
        }
    
    def fetch_market_sentiment(self):
        """Fetch market sentiment indicators"""
        from textblob import TextBlob  # For sentiment analysis
        
        # Simulate news sentiment analysis
        news_items = [
            "Houston County real estate market shows resilience",
            "Interest rates impact local housing market",
            "New developments driving growth in Warner Robins",
            "Inventory levels remain tight in popular neighborhoods"
        ]
        
        sentiments = []
        for news in news_items:
            analysis = TextBlob(news)
            sentiments.append(analysis.sentiment.polarity)
        
        avg_sentiment = sum(sentiments) / len(sentiments)
        
        return {
            'sentiment_score': round(avg_sentiment, 2),
            'market_mood': 'positive' if avg_sentiment > 0.1 else 'negative' if avg_sentiment < -0.1 else 'neutral',
            'key_indicators': news_items[:2]
        }
    
    def _mock_zillow_data(self):
        """Generate realistic mock Zillow data"""
        base_price = 285000
        volatility = 0.02  # 2% daily volatility
        
        return {
            'zestimate': base_price + self._random_in_range(-5000, 5000),
            'rent_zestimate': 1600 + self._random_in_range(-100, 100),
            'value_change_30d': self._random_in_range(-1, 2),
            'value_change_1y': self._random_in_range(-2, 8),
            'price_per_sqft': 140 + self._random_in_range(-5, 5),
            'region_name': 'Warner Robins',
            'region_type': 'zip',
            'updated': datetime.now().isoformat()
        }
    
    def _mock_realtor_data(self):
        """Generate realistic mock Realtor.com data"""
        return {
            'median_listing_price': 289000 + self._random_in_range(-3000, 3000),
            'median_days_on_market': 28 + self._random_in_range(-5, 5),
            'price_reductions': self._random_in_range(15, 25),
            'inventory': self._random_in_range(90, 130),
            'new_listings': self._random_in_range(5, 12),
            'price_per_sqft': 142 + self._random_in_range(-3, 3),
            'market_hotness': self._random_in_range(50, 100)  # 0-100 scale
        }
    
    def _random_in_range(self, low, high):
        """Generate random value within range"""
        import random
        return random.randint(low, high)
    
    def aggregate_real_time_data(self):
        """Aggregate all real-time data sources"""
        timestamp = datetime.now()
        
        aggregated = {
            'timestamp': timestamp.isoformat(),
            'zip_code': self.zip_code,
            'sources': {},
            'metrics': {},
            'trends': {}
        }
        
        # Fetch from all sources
        zillow = self.fetch_zillow_data()
        realtor = self.fetch_realtor_data()
        mls = self.fetch_mls_data()
        sentiment = self.fetch_market_sentiment()
        
        aggregated['sources'] = {
            'zillow': zillow,
            'realtor': realtor,
            'mls': mls,
            'sentiment': sentiment
        }
        
        # Calculate composite metrics
        prices = []
        if zillow: prices.append(zillow.get('zestimate', 0))
        if realtor: prices.append(realtor.get('median_listing_price', 0))
        if mls: prices.append(mls.get('avg_list_price', 0))
        
        aggregated['metrics'] = {
            'composite_price': int(sum(prices) / len(prices)) if prices else 0,
            'composite_inventory': self._calculate_composite_inventory(realtor, mls),
            'market_velocity': self._calculate_market_velocity(realtor, mls),
            'price_momentum': self._calculate_price_momentum(zillow, mls),
            'buyer_seller_index': self._calculate_buyer_seller_index(realtor, mls, sentiment),
            'opportunity_score': self._calculate_opportunity_score(realtor, mls, sentiment)
        }
        
        # Save real-time data
        self._save_real_time_data(aggregated)
        
        return aggregated
    
    def _calculate_composite_inventory(self, realtor, mls):
        if realtor and mls:
            return (realtor.get('inventory', 0) + mls.get('active_listings', 0)) / 2
        elif realtor:
            return realtor.get('inventory', 0)
        elif mls:
            return mls.get('active_listings', 0)
        return 0
    
    def _calculate_market_velocity(self, realtor, mls):
        if mls:
            sold_rate = mls.get('sold_last_7_days', 0) / 7
            inventory = self._calculate_composite_inventory(realtor, mls)
            if inventory > 0:
                return round(sold_rate / inventory * 100, 2)  # Daily sales as % of inventory
        return 0
    
    def _calculate_price_momentum(self, zillow, mls):
        momentum = 0
        if zillow:
            momentum += zillow.get('value_change_30d', 0)
        if mls:
            list_price = mls.get('avg_list_price', 0)
            sold_price = mls.get('avg_sold_price', 0)
            if list_price > 0:
                momentum += ((sold_price - list_price) / list_price) * 100
        return round(momentum, 2)
    
    def _calculate_buyer_seller_index(self, realtor, mls, sentiment):
        """Calculate who has more leverage: buyers or sellers (0-100 scale)"""
        score = 50  # Neutral starting point
        
        # Inventory factor
        inventory = self._calculate_composite_inventory(realtor, mls)
        if inventory > 120:
            score -= 20  # More inventory favors buyers
        elif inventory < 80:
            score += 20  # Less inventory favors sellers
        
        # DOM factor
        if mls and mls.get('avg_dom', 0) > 35:
            score -= 15
        elif mls and mls.get('avg_dom', 0) < 20:
            score += 15
        
        # Sentiment factor
        if sentiment and sentiment.get('market_mood') == 'positive':
            score += 10
        elif sentiment and sentiment.get('market_mood') == 'negative':
            score -= 10
        
        return max(0, min(100, score))
    
    def _calculate_opportunity_score(self, realtor, mls, sentiment):
        """Calculate opportunity score for new realtors (0-100)"""
        score = 50
        
        # Market activity
        if mls and mls.get('new_listings_today', 0) > 5:
            score += 15
        
        # Inventory turnover
        if mls and mls.get('sold_last_7_days', 0) > 15:
            score += 20
        
        # Market stability
        if sentiment and abs(sentiment.get('sentiment_score', 0)) < 0.2:
            score += 10  # Stable market good for new realtors
        
        # Price momentum
        momentum = self._calculate_price_momentum(None, mls)
        if -2 < momentum < 2:
            score += 10  # Stable prices good for learning
        
        return max(0, min(100, score))
    
    def _save_real_time_data(self, data):
        """Save real-time data with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = self.data_dir / f"real_time_{timestamp}.json"
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Also update latest file
        latest_path = self.data_dir / "latest.json"
        with open(latest_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Keep only last 7 days of data
        self._cleanup_old_data()
    
    def _cleanup_old_data(self):
        """Remove data older than 7 days"""
        cutoff = datetime.now() - timedelta(days=7)
        for file in self.data_dir.glob("real_time_*.json"):
            try:
                file_date = datetime.strptime(file.stem[10:25], "%Y%m%d_%H%M%S")
                if file_date < cutoff:
                    file.unlink()
            except:
                pass

# Update script for daily/hourly runs
if __name__ == "__main__":
    fetcher = RealTimeDataFetcher()
    data = fetcher.aggregate_real_time_data()
    print(f"Real-time data updated at {datetime.now()}")
