import json
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)

TOKEN = 8635397710:AAHclWn7_6pYIa_g9p3wP9ANzBksfzw2_BI

GET_REF = 1

with open("products.json", "r", encoding="utf-8") as f:
    PRODUCTS = json.load(f)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📋 لیست قیمت", callback_data="price")],
        [InlineKeyboardButton("👤 ثبت کد معرف", callback_data="ref")],
    ]

    await update.message.reply_text(
        "به ربات خوش آمدید.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
      elif query.data == "old_peugeot":
        await show_prices(query, "پژو", "پژو قدیم")
elif query.data == "ref":
    return await ask_ref(update, context)

    elif query.data == "new_peugeot":
        await show_prices(query, "پژو", "پژو جدید")

    elif query.data == "full_pride":
        await show_prices(query, "پراید", "پک کامل")

    elif query.data == "normal_pride":
        await show_prices(query, "پراید", "پک معمولی")
    await query.answer()
async def show_prices(query, category, subcategory):
    items = PRODUCTS[category][subcategory]

    text = f"📋 {subcategory}\n\n"

    for name, price in items.items():
        text += f"✅ {name}\n💰 {price}\n\n"

    keyboard = [
        [InlineKeyboardButton("🔙 بازگشت", callback_data=category)]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    if query.data == "price":
        keyboard = [
            [InlineKeyboardButton("🚗 پژو", callback_data="peugeot")],
            [InlineKeyboardButton("🚗 پراید", callback_data="pride")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="home")],
        ]

        await query.edit_message_text(
            "لیست محصولات",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "peugeot":
        keyboard = [
            [InlineKeyboardButton("پژو قدیم", callback_data="old_peugeot")],
            [InlineKeyboardButton("پژو جدید", callback_data="new_peugeot")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="price")],
        ]

        await query.edit_message_text(
            "دسته بندی پژو",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "pride":
        keyboard = [
            [InlineKeyboardButton("پک کامل", callback_data="full_pride")],
            [InlineKeyboardButton("پک معمولی", callback_data="normal_pride")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="price")],
        ]

        await query.edit_message_text(
            "دسته بندی پراید",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

async def get_ref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ref = update.message.text

    with open("referrals.txt", "a", encoding="utf-8") as f:
        f.write(f"{update.effective_user.id} : {ref}\n")

    await update.message.reply_text("✅ کد معرف ثبت شد.")
    return ConversationHandler.END


async def ask_ref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text("لطفاً کد معرف خود را وارد کنید:")
    return GET_REF
def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(ask_ref, pattern="^ref$")],
        states={
            GET_REF: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_ref)
            ]
        },
        fallbacks=[],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(conv)

    print("Bot Started...")
    app.run_polling()


if __name__ == "__main__":
    main()
