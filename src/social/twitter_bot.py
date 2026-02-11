"""
Twitter Bot - Automated daily predictions
Posts daily crypto predictions to Twitter/X
"""

import asyncio
import os
from datetime import datetime
from typing import Optional
import tweepy
from src.utils.logger import setup_logger
from src.utils.config import settings
from src.ml.data_collector import DataCollector
from src.ml.predictor import Predictor

logger = setup_logger(__name__)


class TwitterBot:
    """Automated Twitter bot for posting predictions"""
    
    def __init__(self):
        """Initialize Twitter API client"""
        # Twitter API credentials (add to .env)
        api_key = os.getenv("TWITTER_API_KEY")
        api_secret = os.getenv("TWITTER_API_SECRET")
        access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        access_secret = os.getenv("TWITTER_ACCESS_SECRET")
        
        if not all([api_key, api_secret, access_token, access_secret]):
            logger.warning("Twitter credentials not configured")
            self.client = None
            return
        
        # Initialize Tweepy client (v2 API)
        self.client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )
        
        logger.info("✅ Twitter bot initialized")
    
    async def post_daily_prediction(self, asset: str = "Bitcoin") -> Optional[str]:
        """
        Post daily prediction to Twitter
        
        Args:
            asset: Asset to predict (default: Bitcoin)
        
        Returns:
            Tweet ID if successful
        """
        if not self.client:
            logger.warning("Twitter client not initialized - skipping post")
            return None
        
        try:
            logger.info(f"Generating prediction for {asset}...")
            
            # Fetch data and predict
            collector = DataCollector()
            data = await collector.fetch_bitcoin_data(days=30)
            
            predictor = Predictor()
            predictor.train(data)
            
            current_price = data[-1]
            predicted_price = predictor.predict_next_day()
            confidence = predictor.get_confidence()
            
            # Calculate change
            price_change = predicted_price - current_price
            price_change_pct = (price_change / current_price) * 100
            
            # Determine emoji based on prediction
            if price_change_pct > 2:
                trend_emoji = "🚀"
                trend_text = "bullish"
            elif price_change_pct > 0:
                trend_emoji = "📈"
                trend_text = "slightly up"
            elif price_change_pct > -2:
                trend_emoji = "📉"
                trend_text = "slightly down"
            else:
                trend_emoji = "🔻"
                trend_text = "bearish"
            
            # Confidence emoji
            if confidence > 0.8:
                conf_emoji = "🟢"
            elif confidence > 0.6:
                conf_emoji = "🟡"
            else:
                conf_emoji = "🔴"
            
            # Compose tweet
            tweet = f"""🔮 DecAI Oracle Daily Prediction

{asset} {trend_emoji}

Current: ${current_price:,.2f}
24h Prediction: ${predicted_price:,.2f}
Change: {price_change_pct:+.2f}%

Trend: {trend_text}
Confidence: {conf_emoji} {confidence:.0%}

Powered by AI + Blockchain
#Bitcoin #Crypto #AI #Web3"""
            
            # Post tweet
            response = self.client.create_tweet(text=tweet)
            tweet_id = response.data['id']
            
            logger.info(f"✅ Posted tweet: {tweet_id}")
            logger.info(f"Tweet content: {tweet}")
            
            return tweet_id
            
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return None
    
    async def post_gas_fees_alert(self) -> Optional[str]:
        """Post gas fees optimization alert"""
        if not self.client:
            return None
        
        try:
            from src.ml.gas_fees_predictor import GasFeesPredictor
            
            predictor = GasFeesPredictor()
            gas_data = await predictor.fetch_gas_history(hours=24)
            predictor.train(gas_data)
            
            current_fee = gas_data[0]['base_fee']
            optimal = predictor.get_optimal_time(gas_data, hours_ahead=24)
            
            savings_pct = (optimal['potential_savings'] / current_fee) * 100
            
            tweet = f"""⛽ Gas Fees Alert

Current: {current_fee:.1f} gwei
Optimal (in {optimal['hours_from_now']}h): {optimal['optimal_fee']:.1f} gwei

💰 Potential Savings: {savings_pct:.0f}%

Wait for lower fees or send now?
Let AI decide.

#Ethereum #GasFees #Web3"""
            
            response = self.client.create_tweet(text=tweet)
            tweet_id = response.data['id']
            
            logger.info(f"✅ Posted gas fees alert: {tweet_id}")
            
            return tweet_id
            
        except Exception as e:
            logger.error(f"Error posting gas alert: {e}")
            return None
    
    async def post_accuracy_update(self) -> Optional[str]:
        """Post accuracy statistics update"""
        if not self.client:
            return None
        
        try:
            from src.ml.accuracy_tracker import AccuracyTracker
            
            tracker = AccuracyTracker()
            stats = tracker.get_statistics()
            
            if stats['verified_predictions'] == 0:
                logger.info("No verified predictions yet - skipping accuracy post")
                return None
            
            tweet = f"""📊 DecAI Oracle Accuracy Report

Total Predictions: {stats['total_predictions']}
Verified: {stats['verified_predictions']}
Average Accuracy: {stats['average_accuracy']:.1f}%
Best Prediction: {stats['best_accuracy']:.1f}%

Transparent. Verifiable. On-chain.

#AI #Blockchain #MachineLearning"""
            
            response = self.client.create_tweet(text=tweet)
            tweet_id = response.data['id']
            
            logger.info(f"✅ Posted accuracy update: {tweet_id}")
            
            return tweet_id
            
        except Exception as e:
            logger.error(f"Error posting accuracy update: {e}")
            return None
    
    def simulate_tweet(self, tweet_text: str):
        """Simulate tweet posting (for testing without API)"""
        print("\n" + "="*60)
        print("🐦 SIMULATED TWEET")
        print("="*60)
        print(tweet_text)
        print("="*60)
        print(f"Length: {len(tweet_text)} characters")
        print("="*60 + "\n")


async def main():
    """Demo Twitter bot"""
    logger.info("🐦 Starting Twitter Bot Demo...")
    
    bot = TwitterBot()
    
    # If no credentials, simulate
    if not bot.client:
        logger.info("Running in simulation mode (no Twitter credentials)")
        
        # Simulate daily prediction
        collector = DataCollector()
        data = await collector.fetch_bitcoin_data(days=30)
        
        predictor = Predictor()
        predictor.train(data)
        
        current_price = data[-1]
        predicted_price = predictor.predict_next_day()
        confidence = predictor.get_confidence()
        price_change_pct = ((predicted_price - current_price) / current_price) * 100
        
        tweet = f"""🔮 DecAI Oracle Daily Prediction

Bitcoin 📈

Current: ${current_price:,.2f}
24h Prediction: ${predicted_price:,.2f}
Change: {price_change_pct:+.2f}%

Confidence: 🟢 {confidence:.0%}

Powered by AI + Blockchain
#Bitcoin #Crypto #AI #Web3"""
        
        bot.simulate_tweet(tweet)
    else:
        # Post real tweet
        tweet_id = await bot.post_daily_prediction("Bitcoin")
        
        if tweet_id:
            print(f"\n✅ Tweet posted successfully!")
            print(f"View at: https://twitter.com/user/status/{tweet_id}")


if __name__ == "__main__":
    asyncio.run(main())
