import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return 'Бот работает!'

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, друг! Я — помощник команды Почти Божественные.")

def start_bot():
    token = os.environ.get("BOT_TOKEN")
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == '__main__':
    # Запуск Flask отдельно
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    # Запуск Telegram-бота
    start_bot()
