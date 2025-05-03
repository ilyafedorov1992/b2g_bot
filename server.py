from flask import Flask
import os
import asyncio
from threading import Thread

from telegram.ext import ApplicationBuilder, CommandHandler  # Импортируй, если еще не импортировал

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello from Render!'

# Базовая команда для проверки, что бот работает
async def start(update, context):
    await update.message.reply_text('Бот запущен и работает!')

async def run_telegram_bot():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не найден в переменных окружения")

    app_builder = ApplicationBuilder().token(token).build()
    app_builder.add_handler(CommandHandler("start", start))

    await app_builder.run_polling()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    # Запуск Flask в отдельном потоке
    Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()

    # Запуск Telegram-бота в главном потоке через asyncio
    asyncio.run(run_telegram_bot())
