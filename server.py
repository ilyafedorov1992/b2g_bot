import json
import logging
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN.split(':')[0]}"

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Инициализация Telegram приложения
application = Application.builder().token(BOT_TOKEN).build()

# Загрузка структуры кнопок из JSON-файла
with open("bot_structure.json", "r", encoding="utf-8") as f:
    structure = json.load(f)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(text=item["text"], callback_data=item["callback"])]
        for item in structure
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите продукт:", reply_markup=reply_markup)

# Обработка нажатий на кнопки
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    for item in structure:
        if item["callback"] == query.data:
            await query.edit_message_text(text=item["response"])
            return

# Регистрация хендлеров
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(handle_callback))

# Обработка входящих Webhook-запросов от Telegram
@app.post(WEBHOOK_PATH)
async def webhook(request_flask):
    data = await request_flask.get_data()
    update = Update.de_json(json.loads(data), application.bot)
    await application.process_update(update)
    return "ok"

# Ручной запуск сервера
@app.get("/")
def root():
    return "Бот работает через Webhook", 200

if __name__ == "__main__":
    import asyncio
    asyncio.run(application.initialize())
    app.run(host="0.0.0.0", port=10000)
