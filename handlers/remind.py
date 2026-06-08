from telegram import Update
from telegram.ext import ContextTypes

# reminder_id -> {"chat_id": ..., "text": ..., "job": ...}
_reminders: dict[int, dict] = {}
_counter = 0


async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Usage: /remind <minutes> <message>"""
    global _counter

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Please use the format: /remind <minutes> <message>\n"
            "Example: /remind 30 Call mom"
        )
        return

    try:
        minutes = float(context.args[0])
        if minutes <= 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text("Minutes must be a positive number.")
        return

    text = " ".join(context.args[1:])
    _counter += 1
    reminder_id = _counter
    chat_id = update.effective_chat.id

    async def fire(ctx: ContextTypes.DEFAULT_TYPE) -> None:
        await ctx.bot.send_message(chat_id=chat_id, text=f"🔔 Reminder #{reminder_id}: {text}")
        _reminders.pop(reminder_id, None)

    job = context.job_queue.run_once(fire, when=minutes * 60, name=str(reminder_id))
    _reminders[reminder_id] = {"chat_id": chat_id, "text": text, "job": job}

    await update.message.reply_text(
        f"Got it! I'll remind you in {minutes:.0f} minute(s): \"{text}\"\n"
        f"Reminder ID: #{reminder_id}"
    )


async def list_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List all active reminders for this chat."""
    chat_id = update.effective_chat.id
    active = {rid: r for rid, r in _reminders.items() if r["chat_id"] == chat_id}

    if not active:
        await update.message.reply_text("You have no active reminders.")
        return

    lines = [f"#{rid}: {r['text']}" for rid, r in active.items()]
    await update.message.reply_text("Your active reminders:\n" + "\n".join(lines))


async def delete_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Usage: /delete <id>"""
    if not context.args:
        await update.message.reply_text("Please provide a reminder ID: /delete <id>")
        return

    try:
        reminder_id = int(context.args[0].lstrip("#"))
    except ValueError:
        await update.message.reply_text("Invalid ID. Use /list to see your reminder IDs.")
        return

    reminder = _reminders.pop(reminder_id, None)
    if reminder is None or reminder["chat_id"] != update.effective_chat.id:
        await update.message.reply_text(f"No active reminder #{reminder_id} found.")
        return

    reminder["job"].schedule_removal()
    await update.message.reply_text(f"Reminder #{reminder_id} deleted.")
