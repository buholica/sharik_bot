import logging
import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

from handlers.start import start
from handlers.remind import remind, list_reminders, delete_reminder

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN is not set. Copy .env.example to .env and fill it in.")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("remind", remind))
    app.add_handler(CommandHandler("list", list_reminders))
    app.add_handler(CommandHandler("delete", delete_reminder))

    print("Bot is running. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
