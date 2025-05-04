
import os
import json
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Загрузка структуры из JSON
with open("bot_structure.json", encoding="utf-8") as f:
    bot_data = json.load(f)

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # например: https://название-сайта.onrender.com/webhook/ТОКЕН

app = Flask(__name__)

@app.route("/")
def index():
    return "Бот на Webhook активен!"

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Возражения → Утилизация РКО", callback_data="Возражения>Утилизация РКО")],
        [InlineKeyboardButton("Возражения → БГ", callback_data="Возражения>БГ")],
        [InlineKeyboardButton("Возражения → Кредиты", callback_data="Возражения>Кредиты")],
        [InlineKeyboardButton("Возражения → Открытие счета", callback_data="Возражения>Открытие счета")],
        [InlineKeyboardButton("Продукт → БГ", callback_data="Продукт>БГ")],
        [InlineKeyboardButton("Продукт → Оборотный кредит", callback_data="Продукт>Оборотный кредит")],
        [InlineKeyboardButton("Продукт → КЛИК", callback_data="Продукт>КЛИК")],
        [InlineKeyboardButton("Продукт → Счет", callback_data="Продукт>Счет")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери раздел:", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected = query.data

    if selected == "BACK_TO_MAIN":
        await start(update, context)
        return

    parts = selected.split(">")
    node = bot_data
    try:
        for part in parts:
            node = node[part]

        if isinstance(node, list):
            text = ""
            for entry in node:
                text += f"❓ <b>{entry.get('formulirovka')}</b>\n"
                for answer in entry.get("otvety", []):
                    text += f"💬 {answer}\n"
                text += "\n"
            await query.edit_message_text(text.strip(), parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="BACK_TO_MAIN")]]))
        elif isinstance(node, dict):
            keyboard = [
                [InlineKeyboardButton(text=k, callback_data=selected + ">" + k)]
                for k in node.keys()
            ]
            keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="BACK_TO_MAIN")])
            await query.edit_message_text("Выбери:", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.edit_message_text("Неизвестный формат.")
    except:
        await query.edit_message_text("Ошибка обработки. Проверь структуру.")

# --- Flask endpoint для Telegram ---
@app.post(WEBHOOK_PATH)
def webhook() -> str:
    application.update_queue.put_nowait(Update.de_json(request.get_json(force=True), application.bot))
    return "ok"

# --- Инициализация и Webhook ---
async def setup():
    await application.bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}")

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(handle_callback))

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
