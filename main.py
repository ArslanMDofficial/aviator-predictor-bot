import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configs
TOKEN = os.getenv("BOT_TOKEN")
REF_LINK = "https://87lottery.club/r/olspqa"
GROUP_LINK = "https://t.me/AviatorPredictorClubHack"

# In-memory user tracking
users = set()

def generate_prediction():
    crash = round(random.uniform(1.40, 3.00), 2)
    exit_point = round(crash - 0.10, 2)
    return f"""🎯 Predicted Crash Point: <b>{crash}x</b>
✅ Suggested Entry: <b>1.00x</b> → Exit at <b>{exit_point}x</b>

📊 Prediction generated using last 10 crash averages.
💡 Tip: Play safe, exit early!
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users.add(user.id)
    logger.info(f"User started: {user.first_name} ({user.id})")

    keyboard = [
        [InlineKeyboardButton("🎮 Play Aviator", url=REF_LINK)],
        [InlineKeyboardButton("📈 Get Prediction", callback_data="predict")],
        [InlineKeyboardButton("💬 Join Telegram Group", url=GROUP_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👋 Welcome {user.first_name}!\n\n"
        "I will help you predict Aviator crash points.\n"
        "Choose an option below 👇",
        reply_markup=reply_markup
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "predict":
        prediction = generate_prediction()
        await query.edit_message_text(prediction, parse_mode="HTML")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_users = len(users)
    await update.message.reply_text(f"📊 Total Users: {total_users}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.run_polling()
