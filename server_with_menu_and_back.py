
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
    await send_main_menu(update.message.reply_text)

# Главное меню
async def send_main_menu(reply_func):
    main_buttons = [
        [InlineKeyboardButton("Возражения → Утилизация РКО", callback_data="Возражения>Утилизация РКО")],
        [InlineKeyboardButton("Возражения → БГ", callback_data="Возражения>БГ")],
        [InlineKeyboardButton("Возражения → Кредиты", callback_data="Возражения>Кредиты")],
        [InlineKeyboardButton("Возражения → Открытие счета", callback_data="Возражения>Открытие счета")],
        [InlineKeyboardButton("Продукт → БГ", callback_data="Продукт>БГ")],
        [InlineKeyboardButton("Продукт → Оборотный кредит", callback_data="Продукт>Оборотный кредит")],
        [InlineKeyboardButton("Продукт → КЛИК", callback_data="Продукт>КЛИК")],
        [InlineKeyboardButton("Продукт → Счет", callback_data="Продукт>Счет")],
    ]
    reply_markup = InlineKeyboardMarkup(main_buttons)
    await reply_func("Выбери раздел:", reply_markup=reply_markup)

# Обработка кнопок
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected = query.data

    if selected == "BACK_TO_MAIN":
        await send_main_menu(query.edit_message_text)
        return

    parts = selected.split(">")
    node = bot_data

    try:
        for part in parts:
            node = node[part]

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
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="BACK_TO_MAIN")]]
            await query.edit_message_text(response_text.strip(), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

        elif isinstance(node, dict):
            keyboard = [
                [InlineKeyboardButton(text=k, callback_data=selected + ">" + k)]
                for k in node.keys()
            ]
            keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="BACK_TO_MAIN")])
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
