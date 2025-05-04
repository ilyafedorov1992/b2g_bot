import os
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

app = Flask(__name__)

@app.route('/')
def home():
    return 'Бот живой!'

# --- Команда /start ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Получено сообщение: {update.message.text}")
    await update.message.reply_text("Привет! Бот работает! 🎉")

# --- Основной запуск ---

async def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не найден в переменных окружения")

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))

    await application.initialize()
    await application.start()
    print("🤖 Бот запущен и готов к команде /start")
    await application.updater.start_polling()

if __name__ == '__main__':
    import threading

    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))).start()

    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
