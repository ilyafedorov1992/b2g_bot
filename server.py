import os
import threading
from flask import Flask
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = os.getenv("BOT_TOKEN")  # Добавь переменную окружения на Railway

app = Flask(__name__)

@app.route('/')
def home():
    return 'Бот работает! 🤖'

# Telegram-бот
async def start(update, context):
    await update.message.reply_text("Привет, я живу на Railway!")

def run_telegram_bot():
    app_builder = ApplicationBuilder().token(TOKEN).build()
    app_builder.add_handler(CommandHandler("start", start))
    app_builder.run_polling()

if __name__ == '__main__':
    # Запуск бота в отдельном потоке
    threading.Thread(target=run_telegram_bot).start()

    # Flask-сервер, чтобы Railway не ругался
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
