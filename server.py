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

async def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не найден в переменных окружения")

    app_builder = ApplicationBuilder().token(token).build()
    app_builder.add_handler(CommandHandler("start", start))

    await app_builder.initialize()
    await app_builder.start()
    await app_builder.updater.start_polling()
    await app_builder.updater.idle()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    # Запускаем Flask в отдельном потоке
    from threading import Thread
    Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()

    # Запускаем Telegram-бота в event loop
    asyncio.run(main())
