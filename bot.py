import os
import telebot
import requests

# 🔐 Load secrets from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = telebot.TeleBot(BOT_TOKEN)

# 📱 Main menu keyboard
menu_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.row('🗳️ Vote', '📊 Results')
menu_keyboard.row('🔄 Reset Votes', '🧠 Ask AI')

# 📊 Voting storage
votes = {}

# 🧠 AI function using Groq API
def ask_groq(message_text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": message_text}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "❌ AI error: failed to get a response."

# 🚀 Start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Welcome! Choose an option below:", reply_markup=menu_keyboard)

# 🗳️ Voting
@bot.message_handler(func=lambda m: m.text == '🗳️ Vote')
def vote(message):
    user_id = message.from_user.id
    votes[user_id] = votes.get(user_id, 0) + 1
    bot.send_message(message.chat.id, "✅ Your vote has been recorded.")

# 📊 Show results
@bot.message_handler(func=lambda m: m.text == '📊 Results')
def results(message):
    total_votes = sum(votes.values())
    bot.send_message(message.chat.id, f"📊 Total votes: {total_votes}")

# 🔄 Reset votes (admin only)
@bot.message_handler(func=lambda m: m.text == '🔄 Reset Votes')
def reset_votes(message):
    if message.from_user.id == ADMIN_ID:
        votes.clear()
        bot.send_message(message.chat.id, "🔄 All votes have been reset.")
    else:
        bot.send_message(message.chat.id, "⛔ Only the admin can reset votes.")

# 🧠 Ask AI — prompt user to type question
@bot.message_handler(func=lambda m: m.text == '🧠 Ask AI')
def ask_ai(message):
    bot.send_message(message.chat.id, "🧠 Please type your question for the AI:")

# 💬 Handle all other messages as AI questions
@bot.message_handler(func=lambda m: True)
def handle_ai(message):
    if message.text not in ['🗳️ Vote', '📊 Results', '🔄 Reset Votes', '🧠 Ask AI']:
        reply = ask_groq(message.text)
        bot.send_message(message.chat.id, reply)

# ▶️ Run the bot
print("✅ Bot is running... Waiting for messages on Telegram.")
bot.polling()
