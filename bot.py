from telebot import types

import telebot
import sqlite3


bot = telebot.TeleBot('6894941637:AAGRlm5DyIMGy7kdTt91oCW5o3eL5t60VXs')
name = None
last_name = None
user_id = None


@bot.message_handler(commands=['start', 'reg', 'register'])
def send_welcome(message):
    global user_id
    try:
        conn = sqlite3.connect('db.sql')
        cur = conn.cursor()

        cur.execute('CREATE TABLE IF NOT EXISTS users (chat_id INTEGER PRIMARY KEY, name varchar(50), last_name varchar(50), password varchar(50))')
        conn.commit()
        try:
            user_id = cur.execute("SELECT chat_id FROM users WHERE chat_id = ?", (message.chat.id, )).fetchone()[0]
            if user_id == message.chat.id:
                bot.send_message(message.chat.id, 'Вы уже зарегистрированы')
            else:
                raise ValueError
        except Exception:
            bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрирую!\n'
                                              'Введите свой пароль')
            bot.register_next_step_handler(message, user_pass)
        user_id = None
        cur.close()
        conn.close()
    except ConnectionError:
        bot.send_message(message.chat.id, 'Ошибка с соединением. Попробуйте позже')


def user_pass(message):
    conn = sqlite3.connect('db.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (chat_id, password)"
                " VALUES ('%s', '%s')"
                % (message.chat.id, message.text.strip()))
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, f'Вы зарегистрированы.\nВаш ID: {message.chat.id}\nВаш пароль: {message.text.strip()}')


@bot.message_handler(commands=['setBio'])
def set_bio(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Имя', callback_data='first_name'))
    markup.add(types.InlineKeyboardButton('Фамилия', callback_data='last_name'))
    bot.send_message(message.chat.id, 'Выберите что хотите поменять или добавить', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'first_name':
        bot.send_message(call.message.chat.id, 'Введите имя')
        bot.register_next_step_handler(call.message, user_name)
    elif call.data == 'last_name':
        bot.send_message(call.message.chat.id, 'Введите фамиилию')
        bot.register_next_step_handler(call.message, user_last_name)


def user_last_name(message):
    conn = sqlite3.connect('db.sql')
    cur = conn.cursor()
    cur.execute("UPDATE users SET last_name = '%s' WHERE chat_id = '%s'" % (message.text, message.chat.id))
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Ваша фамилия была изменена')


def user_name(message):
    conn = sqlite3.connect('db.sql')
    cur = conn.cursor()
    cur.execute("UPDATE users SET name = '%s' WHERE chat_id = '%s'" % (message.text, message.chat.id))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Ваше имя было изменено')


bot.infinity_polling()
