
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

# Обработка нажатий на кнопки
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected = query.data

    parts = selected.split(">")
    node = bot_data

    try:
        for part in parts:
            node = node[part]

        # Если node — список формулировок и ответов
        if isinstance(node, list):
            response_text = ""
            for entry in node:
                question = entry.get("formulirovka")
                answers = entry.get("otvety", [])
                if question:
                    response_text += f"❓ <b>{question}</b>\n"
                    for ans in answers:
                        response_text += f"💬 {ans}\n"
                    response_text += "\n"
            await query.edit_message_text(response_text.strip(), parse_mode="HTML")
        elif isinstance(node, dict):
            keyboard = [
                [InlineKeyboardButton(text=k, callback_data=selected + ">" + k)]
                for k in node.keys()
            ]
            await query.edit_message_text("Выбери:", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.edit_message_text("Неизвестный формат данных.")
    except Exception as e:
        await query.edit_message_text("Ошибка при обработке. Проверь данные.")

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
