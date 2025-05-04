
import os
import json
import asyncio
from flask import Flask
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# Загрузка структуры из JSON
with open("bot_structure.json", encoding="utf-8") as f:
    bot_data = json.load(f)

# Flask-сервер для Render
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello from Render!'

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(text=key, callback_data=key)]
        for key in bot_data.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я — помощник команды Почти Божественные. Выбери раздел:",
        reply_markup=reply_markup
    )

# Обработка переходов по кнопкам
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected = query.data

    parts = selected.split(">")
    node = bot_data
    for part in parts:
        if part in node:
            node = node[part]
        else:
            await query.edit_message_text("Что-то пошло не так.")
            return

    if isinstance(node, dict):
        keyboard = [
            [InlineKeyboardButton(text=k, callback_data=selected + ">" + k)]
            for k in node.keys()
        ]
        await query.edit_message_text("Выбери:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif isinstance(node, list):
        text = ""
        for entry in node:
            text += f"❓ {entry['formulirovka']}\n"
            for answer in entry['otvety']:
                text += f"💬 {answer}\n"
            text += "\n"
        await query.edit_message_text(text.strip())

# Запуск бота
async def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не найден в переменных окружения")

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))

    await application.initialize()
    await application.start()
    print("🤖 Бот запущен")
    await application.updater.start_polling()

# Точка входа
if __name__ == '__main__':
    import threading
    port = int(os.environ.get("PORT", 5000))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()

    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
