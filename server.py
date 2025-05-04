
import os
import json
import asyncio
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

app = Flask(__name__)

@app.route('/')
def home():
    return 'Бот работает (polling)'

# Загрузка структуры кнопок
with open("bot_structure.json", "r", encoding="utf-8") as f:
    BOT_STRUCTURE = json.load(f)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[key] for key in BOT_STRUCTURE.keys()]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привет! Выбери раздел 👇", reply_markup=reply_markup
    )

# Обработка нажатий
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in BOT_STRUCTURE:
        keyboard = [[item] for item in BOT_STRUCTURE[text]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(f"Выбери пункт из «{text}»:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Пожалуйста, выбери вариант из меню 👇")

# Запуск телеграм-бота
async def run_bot():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("Переменная окружения BOT_TOKEN не задана")

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    await application.initialize()
    await application.start()
    print("🤖 Бот запущен через polling")
    await application.updater.start_polling()
    await application.updater.idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
