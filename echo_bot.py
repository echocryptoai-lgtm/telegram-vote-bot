from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Replace this with your actual token from BotFather
TOKEN = '8470297424:AAH58XwcSsULMUd4X5MG_496FbUpOlVSZiE'

# Voting data
votes = {"yes": 0, "no": 0, "abstain": 0}

# Main menu keyboard
menu_keyboard = [
    ['🗳️ Vote', '📊 Results'],
    ['🔄 Reset Votes', '🤖 Ask AI'],
    ['💰 Token Price']
]
menu_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)

# Vote keyboard
vote_keyboard = [['✅ YES', '❌ NO'], ['🤔 ABSTAIN']]
vote_markup = ReplyKeyboardMarkup(vote_keyboard, resize_keyboard=True)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ /start triggered")
    await update.message.reply_text("👋 Welcome to EchoAI Bot! Please choose an option:", reply_markup=menu_markup)

# /vote command or Vote button
async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🗳️ Please cast your vote:", reply_markup=vote_markup)

# Handle menu button clicks
async def handle_menu_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

# Handle vote button clicks
async def handle_vote_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == '✅ YES':
        votes["yes"] += 1
        await update.message.reply_text("✅ You voted YES.")
    elif text == '❌ NO':
        votes["no"] += 1
        await update.message.reply_text("❌ You voted NO.")
    elif text == '🤔 ABSTAIN':
        votes["abstain"] += 1
        await update.message.reply_text("🤔 You chose to abstain.")

# Run the bot
if __name__ == '__main__':
    app = ApplicationBuilder().token("8470297424:AAH58XwcSsULMUd4X5MG_496FbUpOlVSZiE").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vote", vote))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_choice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_vote_choice))

    print("✅ Bot is running...")
    app.run_polling()
