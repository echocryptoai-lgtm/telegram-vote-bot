# 🤖 Telegram Voting Bot with AI (Groq)

A smart Telegram bot that allows users to vote, view results, reset votes, and ask AI-powered questions using Groq's Mixtral model.

---

## 🚀 Features

- 🗳️ Voting system with per-user tracking
- 📊 Live results with total vote count
- 🔄 Reset votes (admin-only)
- 🧠 AI chat powered by Groq API
- 🌐 English interface
- 🔐 Secure token handling via environment variables

---

## 📦 Requirements

Install dependencies using `pip` or include this in `requirements.txt`:

```txt
pyTelegramBotAPI
requests
langdetect
httpx==0.27.0
certifi>=2023.7.22
aiohttp
