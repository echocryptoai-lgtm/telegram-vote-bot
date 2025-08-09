# 📁 bot.py

import os
import requests
import telebot
from langdetect import detect

# 🔐 Zmienne środowiskowe
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 🔧 Inicjalizacja bota
bot = telebot.TeleBot(BOT_TOKEN)

# 🧠 Funkcja: zapytanie do Groq AI
def ask_groq(prompt, lang="en"):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = {
        "role": "system",
        "content": f"You are a helpful assistant. Reply in {lang.upper()} language."
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            system_prompt,
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ AI error: {str(e)}"

# 🌍 Funkcja: wykrywanie języka
def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return "en"

# 📩 Funkcja: obsługa wiadomości
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    user_lang = detect_language(user_input)
    bot.send_chat_action(message.chat.id, 'typing')
    ai_response = ask_groq(user_input, lang=user_lang)
    bot.send_message(message.chat.id, ai_response)

# 🚀 Funkcja: uruchomienie bota
if __name__ == "__main__":
    print("✅ Bot is running with Groq AI and language detection...")
    bot.polling()
