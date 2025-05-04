
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

# --- Меню логика ---

main_menu = [["Возражения"], ["Продукты"]]

submenu = {
    "Возражения": [["Утилизация РКО"], ["БГ"], ["Кредиты"], ["Открытие счёта"]],
    "Продукты": [["БГ"], ["Оборотный кредит"], ["КЛИК"], ["Счёт"]],
}

# --- Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    await update.message.reply_text(
        "Привет! Выбери категорию:", reply_markup=reply_markup
    )

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text in submenu:
        reply_markup = ReplyKeyboardMarkup(submenu[text], resize_keyboard=True)
        await update.message.reply_text(f"Выбери вариант из «{text}»:", reply_markup=reply_markup)

    elif any(text in row for row in submenu.values()):
        await update.message.reply_text(f"🔧 Ответ для «{text}» пока не добавлен. Скоро будет!")

    else:
        reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
        await update.message.reply_text("Пожалуйста, выбери вариант из меню 👇", reply_markup=reply_markup)

# --- Bot setup ---

async def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не найден в переменных окружения")

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    await application.initialize()
    await application.bot.delete_webhook(drop_pending_updates=True)
    await application.start()
    print("🤖 Бот запущен")
    await application.updater.start_polling()

# --- Entry point ---

if __name__ == '__main__':
    import threading

    # Запуск Flask-сервера
    port = int(os.environ.get("PORT", 5000))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()

    # Запуск бота
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
