from flask import Flask
import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello from Render!'

# --- Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Сопротивление"], ["Возражения"], ["Продукты"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привет, друг! Я — помощник команды Почти Божественные.",
        reply_markup=reply_markup
    )

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Продукты":
        keyboard = [["Счет"], ["Утиль РКО"], ["БГ"], ["ОК"], ["КЛИК"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Выбери продукт:", reply_markup=reply_markup)

    elif text == "Сопротивление":
        keyboard = [["Холодный_Продажа"], ["Холодный_КП"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Выбери сценарий сопротивления:", reply_markup=reply_markup)

    elif text == "Возражения":
        keyboard = [
            ["Счет"],
            ["Утиль РКО"],
            ["БГ"],
            ["ОК", "маленькая сумма", "не одобрят"],
            ["КЛИК", "маленькая сумма", "не одобрят"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Выбери продукт и возражение:", reply_markup=reply_markup)

    else:
        await update.message.reply_text("Пожалуйста, выбери вариант из меню 👇")

# --- Bot setup ---

async def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не найден в переменных окружения")

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    await application.initialize()
    await application.start()
    print("🤖 Бот запущен")
    await application.updater.start_polling()

# --- Entry point ---

if __name__ == '__main__':
    import threading

    # Запуск Flask-сервера
    port = int(os.environ.get("PORT", 5000))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()

    # Запуск бота через фоновую задачу
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
