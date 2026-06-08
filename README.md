# sharik_bot 🔔

A Telegram bot that reminds you about things.

## Commands

| Command | Description |
|---|---|
| `/start` | Show help |
| `/remind <minutes> <message>` | Set a reminder |
| `/list` | Show active reminders |
| `/delete <id>` | Cancel a reminder |

**Example:**
```
/remind 30 Take a break
/remind 1440 Call mom tomorrow
```

## Setup

1. **Get a bot token** from [@BotFather](https://t.me/BotFather) on Telegram

2. **Clone & install:**
   ```bash
   git clone https://github.com/buholica/sharik_bot.git
   cd sharik_bot
   pip install -r requirements.txt
   ```

3. **Configure:**
   ```bash
   cp .env.example .env
   # edit .env and paste your BOT_TOKEN
   ```

4. **Run:**
   ```bash
   python main.py
   ```
