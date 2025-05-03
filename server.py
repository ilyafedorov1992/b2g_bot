from flask import Flask
import os
import threading
from telegram.ext import ApplicationBuilder, CommandHandler

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello from Render!'

async def start(update, context):
    await update.message.reply_text('Бот запущен и работает!')

def run_bot():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не найден в переменных окружения")

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))

    # Запускаем polling прямо здесь
    application.run_polling()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    # Flask сервер запускается отдельно
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()

    # Запускаем Telegram-бота
    run_bot()
