
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import Dispatcher, MessageHandler, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Пример команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот, и я работаю через webhook 💛")

# Добавляем обработчик команды /start
application.add_handler(CommandHandler("start", start))

# Flask endpoint для Telegram Webhook
@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Устанавливаем вебхук при запуске
@app.before_first_request
def set_webhook():
    application.bot.set_webhook(f"{WEBHOOK_URL}/webhook/{BOT_TOKEN}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
