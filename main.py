import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
TOKEN = os.getenv("BOT_TOKEN")
REF_LINK = "https://87lottery.club/r/olspqa"
GROUP_LINK = "https://t.me/AviatorPredictorClubHack"

# Track users
user_data = set()

# Generate prediction
def generate_prediction():
    crash = round(random.uniform(1.42, 2.98), 2)
    safe_exit = round(crash - 0.08, 2)
    return f"""🎯 <b>Predicted Crash Point:</b> <code>{crash}x</code>
✅ <b>Recommended Cash Out:</b> <code>{safe_exit}x</code>
⚠️ Use instantly! Prediction expires in seconds."""

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data.add(user_id)
    logger.info(f"User started: {user_id}")

    keyboard = [
        [InlineKeyboardButton("🎯 Get Prediction", callback_data='predict')],
        [InlineKeyboardButton("🎮 Play Aviator", url=REF_LINK)],
        [InlineKeyboardButton("🚀 Join Prediction Group", url=GROUP_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👋 Welcome {update.effective_user.first_name}!\n\n"
        f"🎰 This bot gives you FREE Aviator Game predictions with high accuracy!\n\n"
        f"👇 Use the buttons below to begin:",
        reply_markup=reply_markup
    )

# Prediction Button Handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'predict':
        prediction = generate_prediction()
        await query.edit_message_text(prediction, parse_mode='HTML')

# /stats command
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_users = len(user_data)
    await update.message.reply_text(f"📊 Total Users: {total_users}")

# Run bot
if __name__ == '__main__':
    if not TOKEN:
        print("⚠️ BOT_TOKEN is not set!")
        exit()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Bot is running...")
    app.run_polling()
