import asyncio
import logging
import os
from datetime import time
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import aiohttp
from dotenv import load_dotenv

load_dotenv()

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerplexityClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai/chat/completions"
    
    async def get_daily_news(self):
        """Get information from Perplexity"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "pplx-70b-online",
            "messages": [
                {
                    "role": "user",
                    "content": """Write a brief daily digest (3-5 points):
                    - Most important news of the day
                    - Brief, concise points
                    - Maximum 500 characters for Telegram
                    - Use emojis for clarity"""
                }
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.base_url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data['choices'][0]['message']['content']
                    else:
                        logger.error(f"Perplexity API error: {resp.status}")
                        return None
            except asyncio.TimeoutError:
                logger.error("Perplexity API timeout")
                return None
            except Exception as e:
                logger.error(f"Error fetching from Perplexity: {e}")
                return None

class TelegramBotManager:
    def __init__(self, bot_token, channel_id, perplexity_api_key):
        self.bot = Bot(token=bot_token)
        self.channel_id = channel_id
        self.perplexity = PerplexityClient(perplexity_api_key)
    
    async def send_daily_post(self):
        """Send daily post to channel"""
        try:
            logger.info("Fetching information from Perplexity...")
            content = await self.perplexity.get_daily_news()
            
            if not content:
                content = "Failed to get information from Perplexity. Check API key."
            
            message = f"""Daily News Digest

{content}

_Powered by Perplexity AI_"""
            
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode="Markdown"
            )
            
            logger.info(f"Successfully sent post to channel")
            
        except Exception as e:
            logger.error(f"Error sending post: {e}")
    
    async def start_scheduler(self):
        """Start scheduler"""
        scheduler = AsyncIOScheduler()
        
        # Schedule: daily at 08:00 Moscow time
        scheduler.add_job(
            self.send_daily_post,
            CronTrigger(hour=8, minute=0, timezone="Europe/Moscow"),
            id="daily_perplexity_post",
            name="Send daily post"
        )
        
        scheduler.start()
        logger.info("Scheduler started. Bot will send posts daily at 08:00 MSK")
        
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            scheduler.shutdown()
            logger.info("Bot stopped")

async def main():
    if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID, PERPLEXITY_API_KEY]):
        logger.error("Missing environment variables!")
        logger.error("Set: TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID, PERPLEXITY_API_KEY")
        return
    
    manager = TelegramBotManager(
        bot_token=TELEGRAM_BOT_TOKEN,
        channel_id=TELEGRAM_CHANNEL_ID,
        perplexity_api_key=PERPLEXITY_API_KEY
    )
    
    await manager.start_scheduler()

if __name__ == "__main__":
    asyncio.run(main())
