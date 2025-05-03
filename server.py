from flask import Flask
import os
import asyncio
import threading
from telegram.ext import ApplicationBuilder, CommandHandler

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello from Render!'

# Обработчики команд
async def start(update, context):
    await update.message.reply_text('Бот запущен и работает!')

async def help_command(update, context):
    await update.message.reply_text("Вот чем я могу помочь: /start /update /feedback /love")

async def update_command(update, context):
    await update.message.reply_text("Пока обновлений нет, но скоро будут 🔄")

async def feedback_command(update, context):
    await update.message.reply_text("Ты можешь оставить отзыв прямо здесь или написать Илье ❤️")

async def love_command(update, context):
    await update.message.reply_text("Любовь — это всё, что нам нужно. И ты это доказал 💛")

# Функция запуска Telegram-бота
async def run_bot():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не найден в переменных окружения")

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("update", update_command))
    application.add_handler(CommandHandler("feedback", feedback_command))
    application.add_handler(CommandHandler("love", love_command))
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.updater.idle()

# Запуск Flask и бота
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    # Запускаем Flask в отдельном потоке
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()

    # Запускаем бота в основном потоке
    asyncio.run(run_bot())
