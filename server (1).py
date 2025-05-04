
import os
import json
from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import asyncio

app = Flask(__name__)

# Загрузка структуры кнопок
with open("bot_structure.json", "r", encoding="utf-8") as f:
    BOT_STRUCTURE = json.load(f)

# Команда старт
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
async def main():
    token = os.environ.get("BOT_TOKEN")
    webhook_url = os.environ.get("WEBHOOK_URL")

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    await application.initialize()
    await application.bot.set_webhook(webhook_url)
    await application.start()
    print("🤖 Бот запущен через Webhook")

# Webhook endpoint
@app.route(f'/webhook/{os.environ.get("BOT_TOKEN")}', methods=["POST"])
async def telegram_webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "OK"

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
