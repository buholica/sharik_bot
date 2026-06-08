from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Hi! I'm your reminder bot 🔔\n\n"
        "Here's what I can do:\n"
        "/remind <minutes> <message> — set a reminder\n"
        "  Example: /remind 30 Take a break\n\n"
        "/list — show all your active reminders\n"
        "/delete <id> — cancel a reminder by its ID"
    )
    await update.message.reply_text(text)
