import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

votes = {"yes": 0, "no": 0, "abstain": 0}

menu_keyboard = [
    ['🗳️ Vote', '📊 Results'],
    ['🔄 Reset Votes', '🤖 Ask AI'],
    ['💰 Token Price']
]
menu_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)

vote_keyboard = [['✅ YES', '❌ NO'], ['🤔 ABSTAIN']]
vote_markup = ReplyKeyboardMarkup(vote_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to EchoAI Bot! Please choose an option:", reply_markup=menu_markup)

async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🗳️ Please cast your vote:", reply_markup=vote_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == '🗳️ Vote':
        await vote(update, context)
    elif text == '📊 Results':
        await update.message.reply_text(
            f"📊 Current results:\n✅ YES: {votes['yes']}\n❌ NO: {votes['no']}\n🤔 ABSTAIN: {votes['abstain']}"
        )
    elif text == '🔄 Reset Votes':
        votes["yes"] = 0
        votes["no"] = 0
        votes["abstain"] = 0
        await update.message.reply_text("🔄 All votes have been reset.")
    elif text == '🤖 Ask AI':
        await update.message.reply_text("🧠 Please type your question for the AI. (Feature coming soon!)")
    elif text == '💰 Token Price':
        await update.message.reply_text("💰 Token price feature coming soon!")
    elif text == '✅ YES':
        votes["yes"] += 1
        await update.message.reply_text("✅ You voted YES.")
    elif text == '❌ NO':
        votes["no"] += 1
        await update.message.reply_text("❌ You voted NO.")
    elif text == '🤔 ABSTAIN':
        votes["abstain"] += 1
        await update.message.reply_text("🤔 You chose to abstain.")
    else:
        await update.message.reply_text("❓ I didn't understand that. Please use the menu.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vote", vote))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot is running...")
    app.run_polling()
