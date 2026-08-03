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

# Token to'g'ridan-to'g'ri yozildi
TOKEN = '8922407533:AAGZ5ydMUq_LsLMTjOD0DnRuE05AhevdXAg'
bot = telebot.TeleBot(TOKEN)

try:
    bot.remove_webhook()
except:
    pass

# Excel faylni o'qish (agar mavjud bo'lsa)
EXCEL_FILE = 'data.xlsx'

def load_data():
    try:
        return pd.read_excel(EXCEL_FILE)
    except Exception as e:
        print(f"Faylni o'qishda xatolik: {e}")
        return None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Havas Reglament botiga xush kelibsiz.")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    text = message.text
    df = load_data()
    
    if df is not None:
        # Bu yerda qidiruv yoki boshqa mantiqlarni yozishingiz mumkin
        bot.reply_to(message, f"Siz yubordingiz: {text}")
    else:
        bot.reply_to(message, "Ma'lumotlar bazasi topilmadi.")

if __name__ == "__main__":
    keep_alive()
    print("Bot ishga tushdi...")
    bot.infinity_polling()
