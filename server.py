from flask import Flask
import os
import asyncio
import threading
from telegram.ext import ApplicationBuilder, CommandHandler

# Инициализируем Flask
app = Flask(__name__)

# Корневая страница (для проверки Render'ом)
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

    # Flask запускается в отдельном потоке
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()

    # Telegram-бот запускается в основном потоке
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    loop.run_forever()
