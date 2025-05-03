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
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.updater.idle()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    # Flask-сервер в отдельном потоке
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()

    # Telegram-бот в основном потоке, но без asyncio.run()
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    loop.run_forever()
