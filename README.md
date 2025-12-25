# Telegram Perplexity Bot 🤖

Telegram bot that sends daily news digest from Perplexity AI to your channel every morning at 8:00 AM (Moscow Time).

## Features

✅ Automatically fetches daily news from Perplexity AI
✅ Sends formatted posts to your Telegram channel
✅ Runs on schedule (8:00 AM Moscow Time by default)
✅ Easy setup with environment variables
✅ Python async/await for efficient operations

## Quick Start

### 1. Get Your Credentials

**Telegram Bot Token:**
- Open Telegram and find [@BotFather](https://t.me/botfather)
- Send `/newbot`
- Follow the instructions
- Copy your bot token (format: `7123456789:ABCDefGHIJKlmnopqrstuvwxyz`)

**Telegram Channel ID:**
- Create a Telegram channel (private or public)
- Add your bot as administrator
- Send a test message to the channel
- Your channel ID will be in the format `-1001234567890` (with minus sign)

**Perplexity API Key:**
- Go to [Perplexity AI](https://www.perplexity.ai/)
- Sign up or login
- Go to Settings → API
- Generate and copy your API key (format: `pplx-xxxxxxxxxxxxxxxx`)

### 2. Clone the Repository

```bash
git clone https://github.com/lena111222333/telegram-perplexity-bot
cd telegram-perplexity-bot
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create .env File

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHANNEL_ID=-your_channel_id_here
PERPLEXITY_API_KEY=your_api_key_here
```

### 5. Run the Bot

```bash
python bot.py
```

You should see:
```
Scheduler started. Bot will send posts daily at 08:00 MSK
```

## Configuration

### Change Posting Time

Edit `bot.py` and find this line:

```python
CronTrigger(hour=8, minute=0, timezone="Europe/Moscow")
```

Change `hour=8` and `minute=0` to your preferred time.

### Change News Topic

Edit the prompt in `bot.py` at the `get_daily_news()` method:

```python
"content": """Write a brief daily digest about:
- Technology news
- Cybersecurity
- etc."""
```

## Files

- `bot.py` - Main bot code
- `requirements.txt` - Python dependencies
- `.env.example` - Example environment variables
- `README.md` - This file
- `.gitignore` - Git ignore file (Python)

## Troubleshooting

**Bot not sending messages:**
- Check that the bot is an admin in the channel
- Verify your API keys are correct
- Check the logs for error messages

**API errors:**
- Verify your Perplexity API key is active
- Check your API quota
- Ensure you have internet connection

## Deployment

To run the bot 24/7, consider deploying to:

- **Railway**: Easy free tier, supports Python
- **Heroku**: Paid, but reliable
- **DigitalOcean**: Affordable VPS option
- **Your own server**: Most control, need to manage

## License

MIT

## Support

For issues and questions, open an issue on GitHub.
