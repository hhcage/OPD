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
        except:
            bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрирую!\n'
                                              'Введите своё имя')
            bot.register_next_step_handler(message, user_name)
        user_id = None
        cur.close()
        conn.close()
    except ConnectionError:
        bot.send_message()


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Отлично!\n'
                                      'Подскажи пожалуйства свою фамилию')
    bot.register_next_step_handler(message, user_last_name)


def user_last_name(message):
    global last_name
    last_name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    chat_id = message.chat.id
    password = message.text.strip()

    conn = sqlite3.connect('db.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO users"
                " (name, last_name, password, chat_id)"
                " VALUES ('%s', '%s', '%s', '%s')"
                % (name, last_name, password, chat_id))
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Вы зарегистрированы' + '\n' + f'Ваш ID: {chat_id}' + '\n' + f'Вас зовут: \
    {last_name} {name}' + '\n' + f'Ваш профиль: ||{password}||', parse_mode='MarkdownV2')


bot.infinity_polling()
