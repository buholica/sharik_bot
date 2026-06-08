import logging
import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from handlers.start import start
from handlers.remind import remind, list_reminders, delete_reminder
from handlers.nlp import handle_text

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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    webhook_url = os.getenv("WEBHOOK_URL")  # set this on Render

    if webhook_url:
        # Production: webhook mode (required for Render web service)
        port = int(os.getenv("PORT", 8443))
        print(f"Starting webhook on port {port}...")
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            secret_token=os.getenv("WEBHOOK_SECRET", ""),
            webhook_url=f"{webhook_url}/{token}",
        )
    else:
        # Local: polling mode (no config needed)
        print("Bot is running locally. Press Ctrl+C to stop.")
        app.run_polling()


if __name__ == "__main__":
    main()
