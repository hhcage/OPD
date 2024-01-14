import telebot


bot = telebot.TeleBot('6894941637:AAGRlm5DyIMGy7kdTt91oCW5o3eL5t60VXs')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
