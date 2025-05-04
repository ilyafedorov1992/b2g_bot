
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import asyncio

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = Flask(__name__)
bot = Bot(BOT_TOKEN)

# Create the Application
application = Application.builder().token(BOT_TOKEN).build()

# Define a simple command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот работает через Webhook 🌐")

application.add_handler(CommandHandler("start", start))

# Set webhook route
@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    if request.method == "POST":
        data = request.get_json(force=True)
        update = Update.de_json(data, bot)
        await application.process_update(update)
        return "ok"
    return "not ok"

# Root route (optional)
@app.route("/", methods=["GET"])
def root():
    return "Бот работает. Webhook ожидает сообщения."

# Register webhook on startup
async def set_webhook():
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook/{BOT_TOKEN}")

if __name__ == "__main__":
    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=10000)
