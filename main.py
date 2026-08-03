import os
import threading
import telebot
import pandas as pd
from flask import Flask

# Render port xatosi bermasligi uchun server
app = Flask('')


@app.route('/')
def home():
  return 'Bot ishlayapti!'


def run():
  app.run(host='0.0.0.0', port=10000)


def keep_alive():
  t = threading.Thread(target=run)
  t.start()


# Tokenni Render muhitidan olamiz
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

try:
  bot.remove_webhook()
except Exception:
  pass

file_path = 'REGLAMENT.xlsx'

try:
  df = pd.read_excel(file_path, sheet_name=0)
  df.columns = ['MAXSULOT', 'QAYTARISH']
  df['MAXSULOT'] = df['MAXSULOT'].astype(str).str.strip().str.upper()
  print('Excel fayl muvaffaqiyatli o`qildi!')
except Exception as e:
  print(f'Faylni o`qishda xatolik: {e}')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  bot.reply_to(
      message, 'Assolomu alaykum! Havas reglament botiga xush kelibsiz.'
  )


@bot.message_handler(func=lambda message: True)
def find_product(message):
  query = message.text.strip().upper()

  if 'df' in globals() and not df.empty:
    result = df[df['MAXSULOT'].str.contains(query, na=False)]

    if not result.empty:
      response = ''
      for index, row in result.head(5).iterrows():
        response += f'📦 *{row["MAXSULOT"]}*\n🔄 Qaytarish sharti: `{row["QAYTARISH"]}`\n\n'
      bot.reply_to(message, response, parse_mode='Markdown')
    else:
      bot.reply_to(message, 'Kechirasiz, bu nomdagi mahsulot reglamentdan topilmadi.')
  else:
    bot.reply_to(message, 'Xatolik: Excel fayl topilmadi.')


if __name__ == '__main__':
  keep_alive()
  print('Bot muvaffaqiyatli ishga tushdi!')
  bot.infinity_polling()
  
