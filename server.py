from flask import Flask
import os
import asyncio
import threading
from telegram.ext import ApplicationBuilder, CommandHandler

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello from Render!'

# Команда /start
async def start(update, context):
    await update.message.reply_text('Бот запущен и работает!')

# Запуск Telegram-бота
async def run_bot():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не найден в переменных окружения")

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    await application.run_polling()

# Запуск Flask и бота
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    # Flask в отдельном потоке
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()

    # Telegram-бот в основном потоке
    try:
        asyncio.run(run_bot())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
