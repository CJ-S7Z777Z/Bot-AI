import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Замените 'YOUR_TELEGRAM_BOT_TOKEN' на ваш токен Telegram-бота
TELEGRAM_BOT_TOKEN = '8136304812:AAF7dJH2tfQMsblb481ZhpK8MhLp3S8eIC0'
# Замените 'PROXY_API_KEY' на ваш ключ доступа к Proxy API
PROXY_API_KEY = 'sk-DBko1ahyuH9VtaixhTFQ6qPvbfouPcOW'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text('Привет👋! Я бот на основе ChatGPT, который поможет в написании сценариев для видео!')

async def chatgpt_response(message: str) -> str:
  url = "https://api.proxyapi.ru/openai/v1/chat/completions"
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {PROXY_API_KEY}"
  }
  data = {
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": message}]
  }
  response = requests.post(url, headers=headers, json=data)
  if response.status_code == 200:
    response_json = response.json()
    return response_json['choices'][0]['message']['content']
  else:
    return "Произошла ошибка при получении ответа от ChatGPT."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  user_message = update.message.text
  
  # Отправляем статус "печатает..."
  await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

  # Получаем ответ от ChatGPT
  bot_response = await chatgpt_response(user_message)
  await update.message.reply_text(bot_response)

def main() -> None:
  app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

  app.add_handler(CommandHandler("start", start))
  app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

  app.run_polling()

if __name__ == '__main__':
  main()
