from flask import Flask
import os
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello from Render!'

async def start(update, context):
    await update.message.reply_text('Бот запущен и работает!')

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
    # Запускаем Flask-сервер отдельно (не блокирует основной поток)
    import threading
    port = int(os.environ.get("PORT", 5000))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()

    # Запускаем бота в основном потоке событий
    asyncio.run(run_bot())
