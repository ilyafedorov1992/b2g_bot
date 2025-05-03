from flask import Flask
import os
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello from Render!'

# Команда /start
async def start(update, context):
    await update.message.reply_text('Бот запущен и работает!')

# Команда /help
async def help_command(update, context):
    await update.message.reply_text("Вот чем я могу помочь: /start /update /feedback /love")

# Команда /update
async def update_command(update, context):
    await update.message.reply_text("Пока обновлений нет, но скоро будут 🔄")

# Команда /feedback
async def feedback_command(update, context):
    await update.message.reply_text("Ты можешь оставить отзыв прямо здесь или написать Илье ❤️")

# Команда /love
async def love_command(update, context):
    await update.message.reply_text("Любовь — это всё, что нам нужно. И ты это доказал 💛")

# Основной запуск бота
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
    
    await application.run_polling()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
    asyncio.run(run_bot())
