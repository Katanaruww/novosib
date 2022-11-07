import sqlite3

from telebot import *

bot = telebot.TeleBot("5533520772:AAHTAyslH5hxMMMtHrDjC_QWdHSeotuVE28")

conn = sqlite3.connect('nov.db', check_same_thread=False)
cursor = conn.cursor()

chat_id = -1001754479498
admin = 1140638587
admin2 = 5500090672
admin3 = 5246801425
censore = ['мат', 'пизда', 'хуй', 'жопа', 'говно', 'секс', 'иди нахуй']

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id
    user_name = message.from_user.first_name
    username = message.from_user.username
    cursor.execute("INSERT INTO work (user_id, user_name, username) VALUES (?, ?, ?)", (user_id, user_name, username, ))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    profil = types.KeyboardButton(text='Профиль')
    uslugi = types.KeyboardButton(text='Услуги')
    ofic = types.KeyboardButton(text='Официальный Новороссийск')
    faq = types.KeyboardButton(text='FAQ')
    markup.add(profil, uslugi)
    markup.add(ofic)
    markup.add(faq)
    bot.send_message(message.from_user.id, f"Добро Пожаловать, {message.from_user.first_name}",
                            reply_markup=markup)

@bot.message_handler(commands=['help'])
def send(message):
    markup = types.InlineKeyboardMarkup()
    help = types.InlineKeyboardButton(text="Поддержка", url="https://t.me/skysity_er")
    markup.add(help)
    bot.send_message(message.chat.id, "<b>Помощь в использовании бота</b>⬇", parse_mode="HTML", reply_markup=markup)


@bot.message_handler(commands=['send'])
def send(message):
    if message.from_user.id == admin:
        msg = bot.send_message(message.chat.id, "Введите текст рассылки: ")
        bot.register_next_step_handler(msg, sendd)
    else:
        bot.send_message(message.chat.id, "Вы не авторизированы!")

@bot.message_handler(commands=['admin'])
def send(message):
    if message.from_user.id == admin or message.from_user.id == admin2 or message.from_user.id == admin3:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        rework = types.KeyboardButton(text="Изменение Данных")
        naz = types.KeyboardButton(text="Вернуться")
        markup.add(rework)
        markup.add(naz)
        bot.send_message(message.chat.id, "Вы вошли в меню администратора!", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Вы не авторизированы!")


@bot.message_handler(commands=['back'])
def send_message(message):
    markup = types.InlineKeyboardMarkup()
    fioo = types.InlineKeyboardButton(text="Введите ФИО", callback_data="fio")
    number = types.InlineKeyboardButton(text="Введите номер телефона", callback_data="number")
    adress = types.InlineKeyboardButton(text="Введите адрес", callback_data="adress")
    raion = types.InlineKeyboardButton(text="Введите район", callback_data="raion")
    data = types.InlineKeyboardButton(text="Введите дату", callback_data="data")
    markup.add(fioo, number)
    markup.add(adress, raion, data)

    row = cursor.execute(f"SELECT * FROM work WHERE user_id = {message.from_user.id}").fetchone()

    bot.send_message(message.chat.id,
                     f"<b>🔑ID</b>: {row[0]}"
                     f"\n<b>👤Username</b>: @{row[2]}"
                     f"\n<b>📝Ф.И.О</b>: {row[3]}"
                     f"\n<b>🎉Дата рождения</b>: {row[4]}"
                     f"\n<b>📱Номер телефона</b>: {row[5]}"
                     f"\n<b>📬Адрес</b>: {row[6]}"
                     f"\n<b>📍Район</b>: {row[7]}",
                     parse_mode="HTML", reply_markup=markup)




@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'jitel':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        cursor.execute(f'UPDATE work SET who = "Житель", user_id = {call.from_user.id}')
        conn.commit()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        profil = types.KeyboardButton(text='Профиль')
        uslugi = types.KeyboardButton(text='Услуги')
        ref = types.KeyboardButton(text='Реферальная Система')
        ofic = types.KeyboardButton(text='Официальный Новороссийск')
        faq = types.KeyboardButton(text='FAQ')
        pay = types.KeyboardButton(text='Купить бота')
        markup.add(profil, uslugi)
        markup.add(ref)
        markup.add(ofic)
        markup.add(faq)
        markup.add(pay)
        bot.send_message(call.from_user.id, "Выберите функцию:", reply_markup=markup)

    elif call.data == 'turist':
        bot.send_message(call.from_user.id, " В разработке... ")
        cursor.execute(f'UPDATE work SET who = "Турист", user_id = {call.from_user.id}')
        conn.commit()
    elif call.data == 'fio':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = bot.send_message(call.message.chat.id, "Введите Ф.И.О.(Иванов Иван Иванович): ")
        bot.register_next_step_handler(msg, fioo)
    elif call.data == 'data':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = bot.send_message(call.message.chat.id, "Введите дату рождения(ДД.ММ.ГГГГ): ")
        bot.register_next_step_handler(msg, data)
    elif call.data == 'number':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = bot.send_message(call.message.chat.id, "Введите номер телефона(+7 XXX XXX XX XX): ")
        bot.register_next_step_handler(msg, number)
    elif call.data == 'adress':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = bot.send_message(call.message.chat.id, "Введите адрес проживания(Улица, дом/кв): ")
        bot.register_next_step_handler(msg, adress)
    elif call.data == 'avto':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = bot.send_message(call.message.chat.id, "Введите номер вашего автомобиля(A001AA25): ")
        bot.register_next_step_handler(msg, avto)
    elif call.data == 'raion':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Приморский Район", callback_data="prim")
        item2 = types.InlineKeyboardButton(text="Новороссийский район", callback_data="novor")
        item3 = types.InlineKeyboardButton(text="Восточный район", callback_data="vost")
        item4 = types.InlineKeyboardButton(text="Южный район", callback_data="ug")
        item5 = types.InlineKeyboardButton(text="Центральный район", callback_data="cent")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)

        bot.send_message(call.from_user.id, "Выберите ваш район: ", reply_markup=markup)
    elif call.data == "feedback":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Благоустройство территории", callback_data="blagustr")
        item2 = types.InlineKeyboardButton(text="Вентиляция", callback_data="ventil")
        item3 = types.InlineKeyboardButton(text="Мусор", callback_data="musor")
        item4 = types.InlineKeyboardButton(text="Горячее теплоснабжение", callback_data="upsnab")
        item5 = types.InlineKeyboardButton(text="Канализация", callback_data="gavno")
        item6 = types.InlineKeyboardButton(text="Кровля", callback_data="krovl")
        item7 = types.InlineKeyboardButton(text="Лифт", callback_data="lift")
        item8 = types.InlineKeyboardButton(text="Теплоснабжение", callback_data="tepl")
        item9 = types.InlineKeyboardButton(text="Общестроительные работы", callback_data="stroirab")
        item10 = types.InlineKeyboardButton(text="Содержание домового имущества", callback_data="soddomim")
        item11 = types.InlineKeyboardButton(text="Холодное водоснабжение", callback_data="downsnab")
        item12 = types.InlineKeyboardButton(text="Электроснабжение", callback_data="electrosnab")
        item13 = types.InlineKeyboardButton(text="Отлов агрессивных животных", callback_data="otlov")
        item14 = types.InlineKeyboardButton(text="Незаконные надписи", callback_data="nadpisi")
        item15 = types.InlineKeyboardButton(text="Адресные указатели", callback_data="adresuk")
        markup.add(item1, item2)
        markup.add(item3, item4)
        markup.add(item5, item6)
        markup.add(item7, item8)
        markup.add(item9, item10)
        markup.add(item11, item12)
        markup.add(item13, item14)
        markup.add(item15)
        bot.send_message(call.from_user.id, "Выберите категорию обращения: ", reply_markup=markup)
    elif call.data == "blagustr":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        us_id = call.message.chat.id
        tema = "Благоустройство территории"
        row = cursor.execute(f"SELECT * FROM work WHERE user_id = {call.message.chat.id}").fetchone()
        fio = row[3]
        nomer = row[4]
        adres = row[5]
        cursor.execute('INSERT INTO feedback (user_id, tema, fio, nomer, adres) VALUES (?, ?, ?, ?, ?)',
                       (us_id, tema, fio, nomer, adres))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="feedback")
        markup.add(item1)
        msg = bot.send_message(call.message.chat.id, "Напишите ваше обращение: ", reply_markup=markup)
        bot.register_next_step_handler(msg, feedback)
    elif call.data == "ventil":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        us_id = call.message.chat.id
        tema = "Вентиляция"
        row = cursor.execute(f"SELECT * FROM work WHERE user_id = {call.message.chat.id}").fetchone()
        fio = row[3]
        nomer = row[4]
        adres = row[5]
        cursor.execute('INSERT INTO feedback (user_id, tema, fio, nomer, adres) VALUES (?, ?, ?, ?, ?)',
                       (us_id, tema, fio, nomer, adres))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="feedback")
        markup.add(item1)
        msg = bot.send_message(call.message.chat.id, "Напишите ваше обращение: ", reply_markup=markup)
        bot.register_next_step_handler(msg, feedback)
    elif call.data == "musor":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        us_id = call.message.chat.id
        tema = "Мусор"
        row = cursor.execute(f"SELECT * FROM work WHERE user_id = {call.message.chat.id}").fetchone()
        fio = row[3]
        nomer = row[4]
        adres = row[5]
        cursor.execute('INSERT INTO feedback (user_id, tema, fio, nomer, adres) VALUES (?, ?, ?, ?, ?)',
                       (us_id, tema, fio, nomer, adres))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="feedback")
        markup.add(item1)
        msg = bot.send_message(call.message.chat.id, "Напишите ваше обращение: ", reply_markup=markup)
        bot.register_next_step_handler(msg, feedback)
    elif call.data == "upsnab":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        us_id = call.message.chat.id
        tema = "Горячее водоснабжение"
        row = cursor.execute(f"SELECT * FROM work WHERE user_id = {call.message.chat.id}").fetchone()
        fio = row[3]
        nomer = row[4]
        adres = row[5]
        cursor.execute('INSERT INTO feedback (user_id, tema, fio, nomer, adres) VALUES (?, ?, ?, ?, ?)',
                       (us_id, tema, fio, nomer, adres))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="feedback")
        markup.add(item1)
        msg = bot.send_message(call.message.chat.id, "Напишите ваше обращение: ", reply_markup=markup)
        bot.register_next_step_handler(msg, feedback)
    elif call.data == "gavno":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        us_id = call.message.chat.id
        tema = "Канализация"
        row = cursor.execute(f"SELECT * FROM work WHERE user_id = {call.message.chat.id}").fetchone()
        fio = row[3]
        nomer = row[4]
        adres = row[5]
        cursor.execute('INSERT INTO feedback (user_id, tema, fio, nomer, adres) VALUES (?, ?, ?, ?, ?)',
                       (us_id, tema, fio, nomer, adres))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="feedback")
        markup.add(item1)
        msg = bot.send_message(call.message.chat.id, "Напишите ваше обращение: ", reply_markup=markup)
        bot.register_next_step_handler(msg, feedback)
    elif call.data == "krovl":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        us_id = call.message.chat.id
        tema = "Кровля"
        row = cursor.execute(f"SELECT * FROM work WHERE user_id = {call.message.chat.id}").fetchone()
        fio = row[3]
        nomer = row[4]
        adres = row[5]
        cursor.execute('INSERT INTO feedback (user_id, tema, fio, nomer, adres) VALUES (?, ?, ?, ?, ?)',
                       (us_id, tema, fio, nomer, adres))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="feedback")
        markup.add(item1)
        msg = bot.send_message(call.message.chat.id, "Напишите ваше обращение: ", reply_markup=markup)
        bot.register_next_step_handler(msg, feedback)
    elif call.data == "lift":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        us_id = call.message.chat.id
        tema = "Лифт"
        row = cursor.execute(f"SELECT * FROM work WHERE user_id = {call.message.chat.id}").fetchone()
        fio = row[3]
        nomer = row[4]
        adres = row[5]
        cursor.execute('INSERT INTO feedback (user_id, tema, fio, nomer, adres) VALUES (?, ?, ?, ?, ?)',
                       (us_id, tema, fio, nomer, adres))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="feedback")
        markup.add(item1)
        msg = bot.send_message(call.message.chat.id, "Напишите ваше обращение: ", reply_markup=markup)
        bot.register_next_step_handler(msg, feedback)
    elif call.data == "tepl":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        us_id = call.message.chat.id
        tema = "Теплоснабжение"
        row = cursor.execute(f"SELECT * FROM work WHERE user_id = {call.message.chat.id}").fetchone()
        fio = row[3]
        nomer = row[4]
        adres = row[5]
        cursor.execute('INSERT INTO feedback (user_id, tema, fio, nomer, adres) VALUES (?, ?, ?, ?, ?)',
                       (us_id, tema, fio, nomer, adres))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="feedback")
        markup.add(item1)
        msg = bot.send_message(call.message.chat.id, "Напишите ваше обращение: ", reply_markup=markup)
        bot.register_next_step_handler(msg, feedback)
    elif call.data == "stroirab":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        us_id = call.message.chat.id
        tema = "Общестроительные работы"
        row = cursor.execute(f"SELECT * FROM work WHERE user_id = {call.message.chat.id}").fetchone()
        fio = row[3]
        nomer = row[4]
        adres = row[5]
        cursor.execute('INSERT INTO feedback (user_id, tema, fio, nomer, adres) VALUES (?, ?, ?, ?, ?)',
                       (us_id, tema, fio, nomer, adres))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="feedback")
        markup.add(item1)
        msg = bot.send_message(call.message.chat.id, "Напишите ваше обращение: ", reply_markup=markup)
        bot.register_next_step_handler(msg, feedback)
    elif call.data == "soddomim":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        us_id = call.message.chat.id
        tema = "Содержание домового имущества"
        row = cursor.execute(f"SELECT * FROM work WHERE user_id = {call.message.chat.id}").fetchone()
        fio = row[3]
        nomer = row[4]
        adres = row[5]
        cursor.execute('INSERT INTO feedback (user_id, tema, fio, nomer, adres) VALUES (?, ?, ?, ?, ?)',
                       (us_id, tema, fio, nomer, adres))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="feedback")
        markup.add(item1)
        msg = bot.send_message(call.message.chat.id, "Напишите ваше обращение: ", reply_markup=markup)
        bot.register_next_step_handler(msg, feedback)
    elif call.data == "downsnab":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        us_id = call.message.chat.id
        tema = "Холодное водоснабжение"
        row = cursor.execute(f"SELECT * FROM work WHERE user_id = {call.message.chat.id}").fetchone()
        fio = row[3]
        nomer = row[4]
        adres = row[5]
        cursor.execute('INSERT INTO feedback (user_id, tema, fio, nomer, adres) VALUES (?, ?, ?, ?, ?)',
                       (us_id, tema, fio, nomer, adres))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="feedback")
        markup.add(item1)
        msg = bot.send_message(call.message.chat.id, "Напишите ваше обращение: ", reply_markup=markup)
        bot.register_next_step_handler(msg, feedback)
    elif call.data == "electrosnab":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        us_id = call.message.chat.id
        tema = "Электроснабжение"
        row = cursor.execute(f"SELECT * FROM work WHERE user_id = {call.message.chat.id}").fetchone()
        fio = row[3]
        nomer = row[4]
        adres = row[5]
        cursor.execute('INSERT INTO feedback (user_id, tema, fio, nomer, adres) VALUES (?, ?, ?, ?, ?)',
                       (us_id, tema, fio, nomer, adres))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="feedback")
        markup.add(item1)
        msg = bot.send_message(call.message.chat.id, "Напишите ваше обращение: ", reply_markup=markup)
        bot.register_next_step_handler(msg, feedback)
    elif call.data == "otlov":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        us_id = call.message.chat.id
        tema = "Отлов агрессивных животных"
        row = cursor.execute(f"SELECT * FROM work WHERE user_id = {call.message.chat.id}").fetchone()
        fio = row[3]
        nomer = row[4]
        adres = row[5]
        cursor.execute('INSERT INTO feedback (user_id, tema, fio, nomer, adres) VALUES (?, ?, ?, ?, ?)',
                       (us_id, tema, fio, nomer, adres))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="feedback")
        markup.add(item1)
        msg = bot.send_message(call.message.chat.id, "Напишите ваше обращение: ", reply_markup=markup)
        bot.register_next_step_handler(msg, feedback)
    elif call.data == "nadpisi":

        us_id = call.message.chat.id
        tema = "Незаконные надписи"
        row = cursor.execute(f"SELECT * FROM work WHERE user_id = {call.message.chat.id}").fetchone()
        fio = row[3]
        nomer = row[4]
        adres = row[5]
        cursor.execute('INSERT INTO feedback (user_id, tema, fio, nomer, adres) VALUES (?, ?, ?, ?, ?)',
                       (us_id, tema, fio, nomer, adres))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="feedback")
        markup.add(item1)
        msg = bot.send_message(call.message.chat.id, "Напишите ваше обращение: ", reply_markup=markup)
        bot.register_next_step_handler(msg, feedback)
    elif call.data == "adresuk":

        us_id = call.message.chat.id
        tema = "Адресные указатели"
        row = cursor.execute(f"SELECT * FROM work WHERE user_id = {call.message.chat.id}").fetchone()
        fio = row[3]
        nomer = row[4]
        adres = row[5]
        cursor.execute('INSERT INTO feedback (user_id, tema, fio, nomer, adres) VALUES (?, ?, ?, ?, ?)',
                       (us_id, tema, fio, nomer, adres))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="feedback")
        markup.add(item1)
        msg = bot.send_message(call.message.chat.id, "Напишите ваше обращение: ", reply_markup=markup)
        bot.register_next_step_handler(msg, feedback)
    elif call.data == "yes":

        row = cursor.execute(f"SELECT * FROM feedback ORDER BY id DESC LIMIT 1").fetchone()
        bot.send_message(-1001678855406, f"\n<b>Заявка №{row[0]}</b>"
                                         f"\n<b>Тема заявки:</b> {row[2]}"
                                         "\n"
                                         f"\n<b>Контактные данные:</b>"
                                         "\n"
                                         f"\n<b>Ф.И.О.:</b> {row[3]}"
                                         f"\n<b>Контактный номер телефона:</b> {row[4]}"
                                         f"\n<b>Адрес:</b> {row[5]}"
                                         "\n"
                                         f"\n<b>Обращение: {row[6]}</b>", parse_mode="HTML")
    elif call.data == "no":
        cursor.execute(f"DELETE * FROM feedback WHERE user_id = {call.message.chat.id}")

        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "prim":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        cursor.execute(f'UPDATE work SET raion = "Приморский район", user_id = {call.from_user.id}')
        conn.commit()
        bot.send_message(call.from_user.id, "Район успешно добавлен!")
    elif call.data == "novor":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        cursor.execute(f'UPDATE work SET raion = "Новороссийский район", user_id = {call.from_user.id}')
        conn.commit()
        bot.send_message(call.from_user.id, "Район успешно добавлен!")
    elif call.data == "vost":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        cursor.execute(f'UPDATE work SET raion = "Восточный район", user_id = {call.from_user.id}')
        conn.commit()
        bot.send_message(call.from_user.id, "Район успешно добавлен!")
    elif call.data == "ug":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        cursor.execute(f'UPDATE work SET raion = "Южный район", user_id = {call.from_user.id}')
        conn.commit()
        bot.send_message(call.from_user.id, "Район успешно добавлен!")
    elif call.data == "cent":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        cursor.execute(f'UPDATE work SET raion = "Центральный район", user_id = {call.from_user.id}')
        conn.commit()
        bot.send_message(call.from_user.id, "Район успешно добавлен!")
    elif call.data == "chats":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        glav = types.InlineKeyboardButton(text="ОСНОВНОЙ КАНАЛ", url="https://t.me/your_NVRSK")
        ug = types.InlineKeyboardButton(text="Южный Район", url="https://t.me/+olXiWgqSb58wOTli")
        nov = types.InlineKeyboardButton(text="Новороссийский Район", url="https://t.me/+Q4OqW4XbseozZjUy")
        vost = types.InlineKeyboardButton(text="Восточный Район", url="https://t.me/+DqjPH4bAzMhjOTgy")
        cent = types.InlineKeyboardButton(text="Центральный Район", url="https://t.me/+olhPSCf3mVA1OWYy")
        prim = types.InlineKeyboardButton(text="Приморский Район", url="https://t.me/+BGoIMSjEhgAzYTky")
        markup.add(glav)
        markup.add(ug)
        markup.add(nov)
        markup.add(vost)
        markup.add(cent)
        markup.add(prim)
        bot.send_message(call.from_user.id, "<b>Выберите район: </b>", parse_mode="HTML", reply_markup=markup)
    elif call.data == "food":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        prim = types.InlineKeyboardButton(text="Приморский Район", callback_data="primfood")
        cent = types.InlineKeyboardButton(text="Центральный Район", callback_data="centfood")
        vost = types.InlineKeyboardButton(text="Восточный Район", callback_data="vostfood")
        nov = types.InlineKeyboardButton(text="Новороссийский Район", callback_data="novfood")
        ug = types.InlineKeyboardButton(text="Южный Район", callback_data="ugfood")
        all = types.InlineKeyboardButton(text="Неважно", callback_data="allfood")
        markup.add(all)
        markup.add(cent)
        markup.add(ug)
        markup.add(prim)
        markup.add(vost)
        markup.add(nov)


        bot.send_message(call.from_user.id, "<b>Выберите район: </b>", parse_mode="HTML", reply_markup=markup)
    elif call.data == "primfood":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        prim = types.InlineKeyboardButton(text="Доставка", callback_data="dostprimfood")
        cent = types.InlineKeyboardButton(text="Рестораны", callback_data="restprimfood")
        vost = types.InlineKeyboardButton(text="Кафе", callback_data="cafeprimfood")
        nov = types.InlineKeyboardButton(text="Фаст-Фуд", callback_data="fastprimfood")
        ug = types.InlineKeyboardButton(text="Любое", callback_data="allprim")
        markup.add(prim)
        markup.add(cent)
        markup.add(vost)
        markup.add(nov)
        markup.add(ug)
        bot.send_message(call.from_user.id, "<b>Выберите где поесть: </b>", parse_mode="HTML", reply_markup=markup)
    elif call.data == "dostprimfood":
        food(call, "Приморский", "dostavka", 1)
    elif call.data == "restprimfood":
        food(call, "Приморский", "restaurant", 1)
    elif call.data == "cafeprimfood":
        food(call, "Приморский", "cafe", 1)
    elif call.data == "fastprimfood":
        food(call, "Приморский", "fastfood", 1)
    elif call.data == "allprim":
        food(call, "Приморский", "dostavka", 1)


    elif call.data == "centfood":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        prim = types.InlineKeyboardButton(text="Доставка", callback_data="dostcentfood")
        cent = types.InlineKeyboardButton(text="Рестораны", callback_data="restcentfood")
        vost = types.InlineKeyboardButton(text="Кафе", callback_data="cafecentfood")
        nov = types.InlineKeyboardButton(text="Фаст-Фуд", callback_data="fastcentfood")
        ug = types.InlineKeyboardButton(text="Любое", callback_data="allcent")
        markup.add(prim)
        markup.add(cent)
        markup.add(vost)
        markup.add(nov)
        markup.add(ug)
        bot.send_message(call.from_user.id, "<b>Выберите где поесть: </b>", parse_mode="HTML", reply_markup=markup)
    elif call.data == "dostcentfood":
        food(call, "Центральный", "dostavka", 1)
    elif call.data == "restcentfood":
        food(call, "Центральный", "restaurant", 1)
    elif call.data == "cafecentfood":
        food(call, "Центральный", "cafe", 1)
    elif call.data == "fastcentfood":
        food(call, "Центральный", "fastfood", 1)
    elif call.data == "allcent":
        food(call, "Центральный", "dostavka", 1)


    elif call.data == "vostfood":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        prim = types.InlineKeyboardButton(text="Доставка", callback_data="dostvostfood")
        cent = types.InlineKeyboardButton(text="Рестораны", callback_data="restvostfood")
        vost = types.InlineKeyboardButton(text="Кафе", callback_data="cafevostfood")
        nov = types.InlineKeyboardButton(text="Фаст-Фуд", callback_data="fastvostfood")
        ug = types.InlineKeyboardButton(text="Любое", callback_data="allvost")
        markup.add(prim)
        markup.add(cent)
        markup.add(vost)
        markup.add(nov)
        markup.add(ug)
        bot.send_message(call.from_user.id, "<b>Выберите где поесть: </b>", parse_mode="HTML", reply_markup=markup)
    elif call.data == "dostvostfood":
        food(call, "Восточный", "dostavka", 1)
    elif call.data == "restvostfood":
        food(call, "Восточный", "restaurant", 1)
    elif call.data == "cafevostfood":
        food(call, "Восточный", "cafe", 1)
    elif call.data == "fastvostfood":
        food(call, "Восточный", "fastfood", 1)
    elif call.data == "allvost":
        food(call, "Восточный", "dostavka", 1)


    elif call.data == "novfood":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        prim = types.InlineKeyboardButton(text="Доставка", callback_data="dostnovfood")
        cent = types.InlineKeyboardButton(text="Рестораны", callback_data="restnovfood")
        vost = types.InlineKeyboardButton(text="Кафе", callback_data="cafenovfood")
        nov = types.InlineKeyboardButton(text="Фаст-Фуд", callback_data="fastnovfood")
        ug = types.InlineKeyboardButton(text="Любое", callback_data="allnov")
        markup.add(prim)
        markup.add(cent)
        markup.add(vost)
        markup.add(nov)
        markup.add(ug)
        bot.send_message(call.from_user.id, "<b>Выберите где поесть: </b>", parse_mode="HTML", reply_markup=markup)
    elif call.data == "dostnovfood":
        food(call, "Новороссийский", "dostavka", 1)
    elif call.data == "restnovfood":
        food(call, "Новороссийский", "restaurant", 1)
    elif call.data == "cafevostfood":
        food(call, "Новороссийский", "cafe", 1)
    elif call.data == "fastnovfood":
        food(call, "Новороссийский", "fastfood", 1)
    elif call.data == "allnov":
        food(call, "Новороссийский", "dostavka", 1)

    elif call.data == "ugfood":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        prim = types.InlineKeyboardButton(text="Доставка", callback_data="dostugfood")
        cent = types.InlineKeyboardButton(text="Рестораны", callback_data="restugfood")
        vost = types.InlineKeyboardButton(text="Кафе", callback_data="cafeugfood")
        nov = types.InlineKeyboardButton(text="Фаст-Фуд", callback_data="fastugfood")
        ug = types.InlineKeyboardButton(text="Любое", callback_data="allug")
        markup.add(prim)
        markup.add(cent)
        markup.add(vost)
        markup.add(nov)
        markup.add(ug)
        bot.send_message(call.from_user.id, "<b>Выберите где поесть: </b>", parse_mode="HTML", reply_markup=markup)
    elif call.data == "dostugfood":
        food(call, "Южный", "dostavka", 1)
    elif call.data == "restugfood":
        food(call, "Южный", "restaurant", 1)
    elif call.data == "cafeugfood":
        food(call, "Южный", "cafe", 1)
    elif call.data == "fastugfood":
        food(call, "Южный", "fastfood", 1)
    elif call.data == "allug":
        food(call, "Южный", "dostavka", 1)


    elif call.data == "allfood":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        prim = types.InlineKeyboardButton(text="Доставка", callback_data="dostallfood")
        cent = types.InlineKeyboardButton(text="Рестораны", callback_data="restallfood")
        vost = types.InlineKeyboardButton(text="Кафе", callback_data="cafeallfood")
        nov = types.InlineKeyboardButton(text="Фаст-Фуд", callback_data="fastallfood")
        ug = types.InlineKeyboardButton(text="Любое", callback_data="all")
        markup.add(prim)
        markup.add(cent)
        markup.add(vost)
        markup.add(nov)
        markup.add(ug)
        bot.send_message(call.from_user.id, "<b>Выберите где поесть: </b>", parse_mode="HTML", reply_markup=markup)
    elif call.data == "dostallfood":
        food(call, "Южный", "dostavka", 1)
    elif call.data == "restallfood":
        food(call, "Южный", "restaurant", 1)
    elif call.data == "cafeallfood":
        food(call, "Южный", "cafe", 1)
    elif call.data == "fastallfood":
        food(call, "Южный", "fastfood", 1)
    elif call.data == "all":
        food(call, "Южный", "dostavka", 1)
    elif call.data == "jal":
        markup = types.InlineKeyboardMarkup()
        bron = types.InlineKeyboardButton(text="Забронировать", callback_data="bron")
        online = types.InlineKeyboardButton(text="Заказать Онлайн", callback_data="online")
        jaloba = types.InlineKeyboardButton(text="Отзыв", callback_data="jaloba")
        markup.add(bron)
        markup.add(online)
        markup.add(jaloba)
        bot.send_message(call.message.chat.id, "Выберите действие: ", reply_markup=markup)
    elif call.data == "bron":
        bot.send_message(call.message.chat.id, "Cкоро...")
    elif call.data == "online":
        bot.send_message(call.message.chat.id, "Cкоро...")
    elif call.data == "jaloba":
        bot.send_message(call.message.chat.id, "Cкоро...")
    elif call.data == "like":
        row = cursor.execute("SELECT * FROM yprav").fetchone()
        s = f"{call.message.text}"
        print(s)
    elif call.data == "dislike":

        row = cursor.execute("SELECT * FROM uslugi").fetchone()
        s = f"{call.message.caption}"
        fak = s.split("\n")
        cursor.execute(f'UPDATE uslugi SET dislike ={row[10]} + 1 WHERE name = "{fak[0]}"')
        conn.commit()

    elif call.data == "back":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Благоустройство территории", callback_data="blagustr")
        item2 = types.InlineKeyboardButton(text="Вентиляция", callback_data="ventil")
        item3 = types.InlineKeyboardButton(text="Мусор", callback_data="musor")
        item4 = types.InlineKeyboardButton(text="Горячее теплоснабжение", callback_data="upsnab")
        item5 = types.InlineKeyboardButton(text="Канализация", callback_data="gavno")
        item6 = types.InlineKeyboardButton(text="Кровля", callback_data="krovl")
        item7 = types.InlineKeyboardButton(text="Лифт", callback_data="lift")
        item8 = types.InlineKeyboardButton(text="Теплоснабжение", callback_data="tepl")
        item9 = types.InlineKeyboardButton(text="Общестроительные работы", callback_data="stroirab")
        item10 = types.InlineKeyboardButton(text="Содержание домового имущества", callback_data="soddomim")
        item11 = types.InlineKeyboardButton(text="Холодное водоснабжение", callback_data="downsnab")
        item12 = types.InlineKeyboardButton(text="Электроснабжение", callback_data="electrosnab")
        item13 = types.InlineKeyboardButton(text="Отлов агрессивных животных", callback_data="otlov")
        item14 = types.InlineKeyboardButton(text="Незаконные надписи", callback_data="nadpisi")
        item15 = types.InlineKeyboardButton(text="Адресные указатели", callback_data="adresuk")
        markup.add(item1, item2)
        markup.add(item3, item4)
        markup.add(item5, item6)
        markup.add(item7, item8)
        markup.add(item9, item10)
        markup.add(item11, item12)
        markup.add(item13, item14)
        markup.add(item15)
        bot.send_message(call.from_user.id, "Выберите категорию обращения: ", reply_markup=markup)
    elif call.data == "admin":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Администрация", callback_data="administ")
        item2 = types.InlineKeyboardButton(text="Управление", callback_data="yprav")
        item3 = types.InlineKeyboardButton(text="Аварийные службы", callback_data="avarslyjb")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(call.message.chat.id, "<b>Структура Города: </b>", parse_mode="HTML", reply_markup=markup)
    elif call.data == "administ":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Глава Города", callback_data="glavgor")
        item2 = types.InlineKeyboardButton(text="Заместители", callback_data="zam")
        item3 = types.InlineKeyboardButton(text="Назад", callback_data="admin")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(call.message.chat.id, "<b>Администрация: </b>", parse_mode="HTML", reply_markup=markup)
    elif call.data == "glavgor":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM administ WHERE id = 1").fetchone()
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text="Назад", callback_data="administ")
        markup.add(back)
        bot.send_photo(call.message.chat.id, row[1], caption=f"<b>{row[2]}</b>\n"
                                                             "\n"
                                                             f"<b>{row[3]}</b>\n"
                                                             "\n"
                                                             "<b>Контакты:</b>\n"
                                                             "\n"
                                                             f"{row[4]}\n"
                                                             f"{row[5]}\n", parse_mode="HTML", reply_markup=markup)
    elif call.data == "zam":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM administ WHERE id = 2").fetchone()
        markup = types.InlineKeyboardMarkup()
        next = types.InlineKeyboardButton(text="➡", callback_data="mac")
        naz = types.InlineKeyboardButton(text=" ", callback_data="eeeee")
        back = types.InlineKeyboardButton(text="Назад", callback_data="administ")
        markup.add(naz, next)
        markup.add(back)
        bot.send_photo(call.message.chat.id, row[1], caption=f"<b>{row[2]}</b>\n"
                                                             "\n"
                                                             f"<b>{row[3]}</b>\n"
                                                             "\n"
                                                             "<b>Контакты:</b>\n"
                                                             "\n"
                                                             f"{row[4]}\n"
                                                             f"{row[5]}\n"
                                                             "\n"
                                                             f"<b>{row[6]}</b>\n", parse_mode="HTML",
                       reply_markup=markup)
    elif call.data == "mac":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM administ WHERE id = 3").fetchone()
        markup = types.InlineKeyboardMarkup()
        next = types.InlineKeyboardButton(text="➡", callback_data="alf")
        naz = types.InlineKeyboardButton(text="⬅", callback_data="zam")
        back = types.InlineKeyboardButton(text="Назад", callback_data="administ")
        markup.add(naz, next)
        markup.add(back)
        bot.send_photo(call.message.chat.id, row[1], caption=f"<b>{row[2]}</b>\n"
                                                             "\n"
                                                             f"<b>{row[3]}</b>\n"
                                                             "\n"
                                                             "<b>Контакты:</b>\n"
                                                             "\n"
                                                             f"{row[4]}\n"
                                                             f"{row[5]}\n"
                                                             "\n"
                                                             f"<b>{row[6]}</b>\n", parse_mode="HTML",
                       reply_markup=markup)
    elif call.data == "alf":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM administ WHERE id = 4").fetchone()
        markup = types.InlineKeyboardMarkup()
        next = types.InlineKeyboardButton(text="➡", callback_data="amen")
        naz = types.InlineKeyboardButton(text="⬅", callback_data="mac")
        back = types.InlineKeyboardButton(text="Назад", callback_data="administ")
        markup.add(naz, next)
        markup.add(back)
        bot.send_photo(call.message.chat.id, row[1], caption=f"<b>{row[2]}</b>\n"
                                                             "\n"
                                                             f"<b>{row[3]}</b>\n"
                                                             "\n"
                                                             "<b>Контакты:</b>\n"
                                                             "\n"
                                                             f"{row[4]}\n"
                                                             f"{row[5]}\n"
                                                             "\n"
                                                             f"<b>{row[6]}</b>\n", parse_mode="HTML",
                       reply_markup=markup)
    elif call.data == "amen":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM administ WHERE id = 5").fetchone()
        markup = types.InlineKeyboardMarkup()
        next = types.InlineKeyboardButton(text="➡", callback_data="mai")
        naz = types.InlineKeyboardButton(text="⬅", callback_data="alf")
        back = types.InlineKeyboardButton(text="Назад", callback_data="administ")
        markup.add(naz, next)
        markup.add(back)
        bot.send_photo(call.message.chat.id, row[1], caption=f"<b>{row[2]}</b>\n"
                                                             "\n"
                                                             f"<b>{row[3]}</b>\n"
                                                             "\n"
                                                             "<b>Контакты:</b>\n"
                                                             "\n"
                                                             f"{row[4]}\n"
                                                             f"{row[5]}\n"
                                                             "\n"
                                                             f"<b>{row[6]}</b>\n", parse_mode="HTML",
                       reply_markup=markup)
    elif call.data == "mai":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM administ WHERE id = 6").fetchone()
        markup = types.InlineKeyboardMarkup()
        next = types.InlineKeyboardButton(text="➡", callback_data="voron")
        naz = types.InlineKeyboardButton(text="⬅", callback_data="amen")
        back = types.InlineKeyboardButton(text="Назад", callback_data="administ")
        markup.add(naz, next)
        markup.add(back)
        bot.send_photo(call.message.chat.id, row[1], caption=f"<b>{row[2]}</b>\n"
                                                             "\n"
                                                             f"<b>{row[3]}</b>\n"
                                                             "\n"
                                                             "<b>Контакты:</b>\n"
                                                             "\n"
                                                             f"{row[4]}\n"
                                                             f"{row[5]}\n"
                                                             "\n"
                                                             f"<b>{row[6]}</b>\n", parse_mode="HTML",
                       reply_markup=markup)

    elif call.data == "voron":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM administ WHERE id = 7").fetchone()
        markup = types.InlineKeyboardMarkup()
        next = types.InlineKeyboardButton(text="➡", callback_data="breys")
        naz = types.InlineKeyboardButton(text="⬅", callback_data="mai")
        back = types.InlineKeyboardButton(text="Назад", callback_data="administ")
        markup.add(naz, next)
        markup.add(back)
        bot.send_photo(call.message.chat.id, row[1], caption=f"<b>{row[2]}</b>\n"
                                                             "\n"
                                                             f"<b>{row[3]}</b>\n"
                                                             "\n"
                                                             "<b>Контакты:</b>\n"
                                                             "\n"
                                                             f"{row[4]}\n"
                                                             f"{row[5]}\n"
                                                             "\n"
                                                             f"<b>{row[6]}</b>\n", parse_mode="HTML",
                       reply_markup=markup)
    elif call.data == "breys":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM administ WHERE id = 8").fetchone()
        markup = types.InlineKeyboardMarkup()
        next = types.InlineKeyboardButton(text="➡", callback_data="melan")
        naz = types.InlineKeyboardButton(text="⬅", callback_data="voron")
        back = types.InlineKeyboardButton(text="Назад", callback_data="administ")
        markup.add(naz, next)
        markup.add(back)
        bot.send_photo(call.message.chat.id, row[1], caption=f"<b>{row[2]}</b>\n"
                                                             "\n"
                                                             f"<b>{row[3]}</b>\n"
                                                             "\n"
                                                             "<b>Контакты:</b>\n"
                                                             "\n"
                                                             f"{row[4]}\n"
                                                             f"{row[5]}\n"
                                                             "\n"
                                                             f"<b>{row[6]}</b>\n", parse_mode="HTML",
                       reply_markup=markup)
    elif call.data == "melan":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM administ WHERE id = 9").fetchone()
        markup = types.InlineKeyboardMarkup()
        next = types.InlineKeyboardButton(text="➡", callback_data="azyz")
        naz = types.InlineKeyboardButton(text="⬅", callback_data="breys")
        back = types.InlineKeyboardButton(text="Назад", callback_data="administ")
        markup.add(naz, next)
        markup.add(back)
        bot.send_photo(call.message.chat.id, row[1], caption=f"<b>{row[2]}</b>\n"
                                                             "\n"
                                                             f"<b>{row[3]}</b>\n"
                                                             "\n"
                                                             "<b>Контакты:</b>\n"
                                                             "\n"
                                                             f"{row[4]}\n"
                                                             f"{row[5]}\n"
                                                             "\n"
                                                             f"<b>{row[6]}</b>\n", parse_mode="HTML",
                       reply_markup=markup)
    elif call.data == "azyz":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM administ WHERE id = 10").fetchone()
        markup = types.InlineKeyboardMarkup()
        next = types.InlineKeyboardButton(text="➡", callback_data="car")
        naz = types.InlineKeyboardButton(text="⬅", callback_data="melan")
        back = types.InlineKeyboardButton(text="Назад", callback_data="administ")
        markup.add(naz, next)
        markup.add(back)
        bot.send_photo(call.message.chat.id, row[1], caption=f"<b>{row[2]}</b>\n"
                                                             "\n"
                                                             f"<b>{row[3]}</b>\n"
                                                             "\n"
                                                             "<b>Контакты:</b>\n"
                                                             "\n"
                                                             f"{row[4]}\n"
                                                             f"{row[5]}\n"
                                                             "\n"
                                                             f"<b>{row[6]}</b>\n", parse_mode="HTML",
                       reply_markup=markup)
    elif call.data == "car":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM administ WHERE id = 11").fetchone()
        markup = types.InlineKeyboardMarkup()
        next = types.InlineKeyboardButton(text="➡", callback_data="koz")
        naz = types.InlineKeyboardButton(text="⬅", callback_data="azyz")
        back = types.InlineKeyboardButton(text="Назад", callback_data="administ")
        markup.add(naz, next)
        markup.add(back)
        bot.send_photo(call.message.chat.id, row[1], caption=f"<b>{row[2]}</b>\n"
                                                             "\n"
                                                             f"<b>{row[3]}</b>\n"
                                                             "\n"
                                                             "<b>Контакты:</b>\n"
                                                             "\n"
                                                             f"{row[4]}\n"
                                                             f"{row[5]}\n"
                                                             "\n"
                                                             f"<b>{row[6]}</b>\n", parse_mode="HTML",
                       reply_markup=markup)
    elif call.data == "koz":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM administ WHERE id = 12").fetchone()
        markup = types.InlineKeyboardMarkup()
        next = types.InlineKeyboardButton(text=" ", callback_data="tytyt")
        naz = types.InlineKeyboardButton(text="⬅", callback_data="car")
        back = types.InlineKeyboardButton(text="Назад", callback_data="administ")
        markup.add(naz, next)
        markup.add(back)
        bot.send_photo(call.message.chat.id, row[1], caption=f"<b>{row[2]}</b>\n"
                                                             "\n"
                                                             f"<b>{row[3]}</b>\n"
                                                             "\n"
                                                             "<b>Контакты:</b>\n"
                                                             "\n"
                                                             f"{row[4]}\n"
                                                             f"{row[5]}\n"
                                                             "\n"
                                                             f"<b>{row[6]}</b>\n", parse_mode="HTML",
                       reply_markup=markup)
    elif call.data == "yprav":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ ПО ВОПРОСАМ СЕМЬИ И ДЕТСТВА", callback_data="ypfamily")
        item2 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ ФИНАНСОВОГО КОНТРОЛЯ", callback_data="ypfincon")
        item3 = types.InlineKeyboardButton(text="ФИНАНСОВОЕ УПРАВЛЕНИЕ", callback_data="finyp")
        item4 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ КАДРОВОЙ ПОЛИТИКИ", callback_data="ypcadpol")
        item5 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ ПО МУНИЦИПАЛЬНЫМ ПРОЕКТАМ И ПРОГРАММАМ – ПРОЕКТНЫЙ ОФИС",
                                           callback_data="ypmynpro")
        item6 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ ГОРОДСКОГО ХОЗЯЙСТВА (УГХ)", callback_data="ypgorhoz")
        item7 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ ФИЗИЧЕСКОЙ КУЛЬТУРЫ И СПОРТА", callback_data="ypfizkul")
        item8 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ КУЛЬТУРЫ", callback_data="ypkul")
        item9 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ ОБРАЗОВАНИЯ", callback_data="ypobr")
        item10 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ ПО ДЕЛАМ НЕСОВЕРШЕННОЛЕТНИХ", callback_data="yppodelnes")
        item11 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ АРХИВА", callback_data="yparx")
        item12 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ ДЕЛОПРОИЗВОДСТВА", callback_data="ypdelo")
        item13 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ ТРАНСПОРТА И ДОРОЖНОГО ХОЗЯЙСТВА",
                                            callback_data="yptrandorhoz")
        item14 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ ПО ВЗАИМОДЕЙСТВИЮ С ПРАВООХРАНИТЕЛЬНЫМИ ОРГАНАМИ",
                                            callback_data="ypvzpravorg")
        item15 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ ВНУТРЕННЕЙ ПОЛИТИКИ", callback_data="ypvnutpol")
        item16 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ ТОРГОВЛИ И ПОТРЕБИТЕЛЬСКОГО РЫНКА",
                                            callback_data="yptorpot")
        item17 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ АРХИТЕКТУРЫ И ГРАДОСТРОИТЕЛЬСТВА",
                                            callback_data="yparxgrad")
        item18 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ ИМУЩЕСТВЕННЫХ И ЗЕМЕЛЬНЫХ ОТНОШЕНИЙ",
                                            callback_data="ypimzem")
        item19 = types.InlineKeyboardButton(text="ПРАВОВОЕ УПРАВЛЕНИЕ", callback_data="ypprav")
        item20 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ КОНТРОЛЯ ГОРОДСКОГО ХОЗЯЙСТВА (УКГХ)",
                                            callback_data="ypcongorxoz")
        item21 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ МУНИЦИПАЛЬНОГО КОНТРОЛЯ", callback_data="ypmyncon")
        item22 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ МУНИЦИПАЛЬНОГО ЗАКАЗА", callback_data="ypmynzak")
        item23 = types.InlineKeyboardButton(text="УПРАВЛЕНИЕ ЭКОНОМИЧЕСКОГО РАЗВИТИЯ", callback_data="ypemraz")
        item24 = types.InlineKeyboardButton(text="Назад", callback_data="admin")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)
        markup.add(item7)
        markup.add(item8)
        markup.add(item9)
        markup.add(item10)
        markup.add(item11)
        markup.add(item12)
        markup.add(item13)
        markup.add(item14)
        markup.add(item15)
        markup.add(item16)
        markup.add(item17)
        markup.add(item18)
        markup.add(item19)
        markup.add(item20)
        markup.add(item21)
        markup.add(item22)
        markup.add(item23)
        markup.add(item24)
        bot.send_message(call.message.chat.id, "<b>Управление:</b>", parse_mode="HTML", reply_markup=markup)

    elif call.data == "ypfamily":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 1").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text=f"👍({row[6]})", callback_data="like")
        item2 = types.InlineKeyboardButton(text=f"👎({row[7]})", callback_data="dislike")
        item3 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1, item2)
        markup.add(item3)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "ypfincon":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 2").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "finyp":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 3").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "ypcadpol":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 4").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "ypmynpro":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 5").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "ypgorhoz":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 6").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "ypfizkul":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 7").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "ypkul":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 8").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "ypobr":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 9").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "yppodelnes":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 10").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "yparx":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 11").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "ypdelo":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 12").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "yptrandorhoz":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 13").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "ypvzpravorg":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 14").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "ypvnutpol":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 15").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "yptorpot":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 16").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "yparxgrad":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 17").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "ypimzem":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 18").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "ypprav":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 19").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "ypcongorxoz":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 20").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "ypmyncon":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 21").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "ypmynzak":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 22").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "ypemraz":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        row = cursor.execute(f"SELECT * FROM yprav WHERE id = 23").fetchone()
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Назад", callback_data="yprav")
        markup.add(item1)
        bot.send_message(call.message.chat.id, f"\n{row[1]}"
                                               f"\n"
                                               f"\n<b>Контакты: </b>"
                                               f"\n"
                                               f"\n{row[2]}"
                                               f"\n{row[3]}"
                                               f"\n"
                                               f"\n<b>Начальник Управления</b>"
                                               f"\n"
                                               f"\n{row[5]}", parse_mode="HTML", reply_markup=markup)
    elif call.data == "insert":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Где поесть?", callback_data="foodins")
        item2 = types.InlineKeyboardButton(text="Ночной Новороссийск", callback_data="funnyins")
        item3 = types.InlineKeyboardButton(text="Активный Отдых", callback_data="activeins")
        item4 = types.InlineKeyboardButton(text="Культурные мероприятия", callback_data="cultureins")
        item5 = types.InlineKeyboardButton(text="Объявления", callback_data="advertins")
        item6 = types.InlineKeyboardButton(text="Где Остановиться?", callback_data="stateins")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)
        bot.send_message(call.message.chat.id, "<b>Выберите нужную категорию:</b> ", parse_mode="HTML", reply_markup=markup)
    elif call.data == "foodins":
        msg = bot.send_message(call.message.chat.id, "Введите данные для добавления в таблицу\n"
                                           "<b><u>Пример ввода:</u>  \nКЛАСС(кафе, рестораны) : РАЙОН : НАЗВАНИЕ ЗАВЕДЕНИЯ : ССЫЛКА НА ФОТО : НОМЕР ТЕЛЕФОНА : АДРЕС : ВРЕМЯ РАБОТЫ : ССЫЛКА НА САЙТ(если есть)</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, foodins)
    elif call.data == "delete":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Где поесть?", callback_data="fooddel")
        item2 = types.InlineKeyboardButton(text="Ночной Новороссийск", callback_data="funnydel")
        item3 = types.InlineKeyboardButton(text="Активный Отдых", callback_data="activedel")
        item4 = types.InlineKeyboardButton(text="Культурные мероприятия", callback_data="culturedel")
        item5 = types.InlineKeyboardButton(text="Объявления", callback_data="advertdel")
        item6 = types.InlineKeyboardButton(text="Где Остановиться?", callback_data="statedel")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)
        bot.send_message(call.message.chat.id, "<b>Выберите нужную категорию:</b> ", parse_mode="HTML", reply_markup= markup)



@bot.message_handler(content_types=["text"])
def get_messages(message):
    if message.text == "Профиль" or message.text == "Вернуться":
        bot.delete_message(message.chat.id, message.message_id)
        markup = types.InlineKeyboardMarkup()
        fioo = types.InlineKeyboardButton(text="Введите ФИО", callback_data="fio")
        number = types.InlineKeyboardButton(text="Введите номер телефона", callback_data="number")
        adress = types.InlineKeyboardButton(text="Введите адрес", callback_data="adress")
        raion = types.InlineKeyboardButton(text="Введите район", callback_data="raion")
        data = types.InlineKeyboardButton(text="Введите дату", callback_data="data")
        avto = types.InlineKeyboardButton(text="Введите номер автомобиля", callback_data="avto")
        markup.add(fioo, number)
        markup.add(adress, raion, data)
        markup.add(avto)

        row = cursor.execute(f"SELECT * FROM work WHERE user_id = {message.chat.id}").fetchone()

        bot.send_message(message.chat.id,
                         f"<b>🔑ID</b>: {row[0]}"
                         f"\n<b>👤Username</b>: @{row[2]}"
                         f"\n<b>📝Ф.И.О</b>: {row[3]}"
                         f"\n<b>🎉Дата Рождения</b>: {row[4]}"
                         f"\n<b>📱Номер Tелефона</b>: {row[5]}"
                         f"\n<b>📬Адрес</b>: {row[6]}"
                         f"\n<b>📍Район</b>: {row[7]}"
                         f"\n<b>🚗Номер Автомобиля</b>: {row[9]}",
                         parse_mode="HTML", reply_markup=markup)

    elif message.text == "Официальный Новороссийск":
        bot.delete_message(message.chat.id, message.message_id)
        markup = types.InlineKeyboardMarkup()
        news = types.InlineKeyboardButton(text="Новости", url="https://admnvrsk.ru/novosti/")
        avar = types.InlineKeyboardButton(text="Аварийные и Плановые отключения", url="https://t.me/+occSCgbkgvRiNzhi")
        item2 = types.InlineKeyboardButton(text="Оставь обращение", callback_data="feedback")
        admin = types.InlineKeyboardButton(text="Структура Города", callback_data="admin")
        markup.add(news)
        markup.add(avar)
        markup.add(item2)
        markup.add(admin)
        bot.send_message(message.chat.id, "<b>Выберите функцию</b>", parse_mode="HTML", reply_markup=markup)
    elif message.text == "Услуги":
        bot.delete_message(message.chat.id, message.message_id)
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Где Поесть?", callback_data="food")
        item2 = types.InlineKeyboardButton(text="Ночной Новороссийск", callback_data="night")
        item3 = types.InlineKeyboardButton(text="Активный Отдых", callback_data="active")
        item4 = types.InlineKeyboardButton(text="Культурные мероприятия", callback_data="culture")
        item5 = types.InlineKeyboardButton(text="Объявления", callback_data="adv")
        item6 = types.InlineKeyboardButton(text="Где Остановиться?", callback_data="stop")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)
        bot.send_message(message.chat.id, "<b>Выберите нужную кнопку:</b> ", parse_mode="HTML", reply_markup=markup)
    elif message.text == "FAQ":
        bot.delete_message(message.chat.id, message.message_id)
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Поддержка", callback_data="food")
        item2 = types.InlineKeyboardButton(text="Документы", callback_data="funny")
        item3 = types.InlineKeyboardButton(text="Голосование", callback_data="advert")
        item4 = types.InlineKeyboardButton(text="О Нас", callback_data="fashion")
        item5 = types.InlineKeyboardButton(text="Реферальная система", callback_data="refka")
        item6 = types.InlineKeyboardButton(text="Купить Бота", callback_data="paybot")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)
        bot.send_message(message.chat.id, "<b>Выберите нужную кнопку:</b> ", parse_mode="HTML", reply_markup=markup)
    elif message.text == "Изменение Данных":
        bot.delete_message(message.chat.id, message.message_id)
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Добавление", callback_data="insert")
        item2 = types.InlineKeyboardButton(text="Удаление", callback_data="delete")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id, "<b>Выберите нужное действие:</b> ", parse_mode="HTML", reply_markup=markup)
def foodins(message):
    text = message.text
    a = text.split("|")
    print(a)
    cursor.execute('INSERT INTO uslugi (class, raion, name, image, num, addr, time, site) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7],))
    conn.commit()
def food(call, raion, classs, pag):
    row = cursor.execute("SELECT * FROM uslugi WHERE raion = ? AND class = ? AND id_id = ?",
                         (raion, classs, pag)).fetchone()
    markup = types.InlineKeyboardMarkup()
    voskl = types.InlineKeyboardButton(text="❗", callback_data="jal")
    info = types.InlineKeyboardButton(text="🧾Инфо", url="http://nvrsk.com/")
    izb = types.InlineKeyboardButton(text="⭐", callback_data="izb")
    naz = types.InlineKeyboardButton(text="⬅", callback_data="naz:")
    one = types.InlineKeyboardButton(text=f"1/1", callback_data="fdgdf")
    vp = types.InlineKeyboardButton(text="➡", callback_data="vp:")
    markup.add(voskl, info, izb)
    markup.add(naz, one, vp)
    bot.send_photo(call.message.chat.id, row[6], caption=f"<b>{row[5]}</b>\n"
                                                    f"<b>{row[7]}</b>\n"
                                                    f"{row[8]}\n"
                                                    f"{row[9]}\n", parse_mode="HTML",  reply_markup=markup)




def fioo(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    cursor.execute(f'UPDATE work SET fio = "{message.text}", user_id = {message.chat.id}')
    conn.commit()

    markup = types.InlineKeyboardMarkup()
    fioo = types.InlineKeyboardButton(text="Введите ФИО", callback_data="fio")
    number = types.InlineKeyboardButton(text="Введите номер телефона", callback_data="number")
    adress = types.InlineKeyboardButton(text="Введите адрес", callback_data="adress")
    raion = types.InlineKeyboardButton(text="Введите район", callback_data="raion")
    data = types.InlineKeyboardButton(text="Введите дату", callback_data="data")
    markup.add(fioo, number)
    markup.add(adress, raion, data)

    row = cursor.execute(f"SELECT * FROM work WHERE user_id = {message.from_user.id}").fetchone()

    bot.send_message(message.chat.id,
                         f"<b>🔑ID</b>: {row[0]}"
                         f"\n<b>👤Username</b>: @{row[2]}"
                         f"\n<b>📝Ф.И.О</b>: {row[3]}"
                         f"\n<b>🎉Дата Рождения</b>: {row[4]}"
                         f"\n<b>📱Номер Tелефона</b>: {row[5]}"
                         f"\n<b>📬Адрес</b>: {row[6]}"
                         f"\n<b>📍Район</b>: {row[7]}"
                         f"\n<b>🚗Номер Автомобиля</b>: {row[9]}",
                         parse_mode="HTML", reply_markup=markup)

def data(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    cursor.execute(f'UPDATE work SET data = "{message.text}", user_id = {message.from_user.id}')
    conn.commit()

    markup = types.InlineKeyboardMarkup()
    fioo = types.InlineKeyboardButton(text="Введите ФИО", callback_data="fio")
    number = types.InlineKeyboardButton(text="Введите номер телефона", callback_data="number")
    adress = types.InlineKeyboardButton(text="Введите адрес", callback_data="adress")
    raion = types.InlineKeyboardButton(text="Введите район", callback_data="raion")
    data = types.InlineKeyboardButton(text="Введите дату", callback_data="data")
    markup.add(fioo, number)
    markup.add(adress, raion, data)

    row = cursor.execute(f"SELECT * FROM work WHERE user_id = {message.from_user.id}").fetchone()

    bot.send_message(message.chat.id,
                         f"<b>🔑ID</b>: {row[0]}"
                         f"\n<b>👤Username</b>: @{row[2]}"
                         f"\n<b>📝Ф.И.О</b>: {row[3]}"
                         f"\n<b>🎉Дата Рождения</b>: {row[4]}"
                         f"\n<b>📱Номер Tелефона</b>: {row[5]}"
                         f"\n<b>📬Адрес</b>: {row[6]}"
                         f"\n<b>📍Район</b>: {row[7]}"
                         f"\n<b>🚗Номер Автомобиля</b>: {row[9]}",
                         parse_mode="HTML", reply_markup=markup)

def number(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    cursor.execute(f'UPDATE work SET numberr = "{message.text}", user_id = {message.from_user.id}')
    conn.commit()

    markup = types.InlineKeyboardMarkup()
    fioo = types.InlineKeyboardButton(text="Введите ФИО", callback_data="fio")
    number = types.InlineKeyboardButton(text="Введите номер телефона", callback_data="number")
    adress = types.InlineKeyboardButton(text="Введите адрес", callback_data="adress")
    raion = types.InlineKeyboardButton(text="Введите район", callback_data="raion")
    data = types.InlineKeyboardButton(text="Введите дату", callback_data="data")
    markup.add(fioo, number)
    markup.add(adress, raion, data)

    row = cursor.execute(f"SELECT * FROM work WHERE user_id = {message.from_user.id}").fetchone()

    bot.send_message(message.chat.id,
                     f"<b>🔑ID</b>: {row[0]}"
                     f"\n<b>👤Username</b>: @{row[2]}"
                     f"\n<b>📝Ф.И.О</b>: {row[3]}"
                     f"\n<b>🎉Дата Рождения</b>: {row[4]}"
                     f"\n<b>📱Номер Tелефона</b>: {row[5]}"
                     f"\n<b>📬Адрес</b>: {row[6]}"
                     f"\n<b>📍Район</b>: {row[7]}"
                     f"\n<b>🚗Номер Автомобиля</b>: {row[9]}",
                     parse_mode="HTML", reply_markup=markup)


def adress(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    cursor.execute(f'UPDATE work SET adress = "{message.text}", user_id = {message.from_user.id}')
    conn.commit()

    markup = types.InlineKeyboardMarkup()
    fioo = types.InlineKeyboardButton(text="Введите ФИО", callback_data="fio")
    number = types.InlineKeyboardButton(text="Введите номер телефона", callback_data="number")
    adress = types.InlineKeyboardButton(text="Введите адрес", callback_data="adress")
    raion = types.InlineKeyboardButton(text="Введите район", callback_data="raion")
    data = types.InlineKeyboardButton(text="Введите дату", callback_data="data")
    markup.add(fioo, number)
    markup.add(adress, raion, data)

    row = cursor.execute(f"SELECT * FROM work WHERE user_id = {message.from_user.id}").fetchone()

    bot.send_message(message.chat.id,
                     f"<b>🔑ID</b>: {row[0]}"
                     f"\n<b>👤Username</b>: @{row[2]}"
                     f"\n<b>📝Ф.И.О</b>: {row[3]}"
                     f"\n<b>🎉Дата Рождения</b>: {row[4]}"
                     f"\n<b>📱Номер Tелефона</b>: {row[5]}"
                     f"\n<b>📬Адрес</b>: {row[6]}"
                     f"\n<b>📍Район</b>: {row[7]}"
                     f"\n<b>🚗Номер Автомобиля</b>: {row[9]}",
                     parse_mode="HTML", reply_markup=markup)



def feedback(message):
    bot.delete_message(message.chat.id, message.message_id)
    cursor.execute(f'UPDATE feedback SET feedback = "{message.text}" WHERE id = (SELECT max(id) FROM feedback)')
    conn.commit()
    row = cursor.execute(f"SELECT * FROM feedback ORDER BY id DESC LIMIT 1").fetchone()
    markup = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Отправить", callback_data="yes")
    no = types.InlineKeyboardButton(text="Отменить", callback_data="no")
    markup.add(yes, no)
    bot.send_message(message.chat.id, "<b>Проверьте свои данные...</b>"
                                      "\n"
                                      f"\n<b>Заявка №{row[0]}</b>"
                                      f"\n<b>Тема заявки:</b> {row[2]}"
                                      "\n"
                                      f"\n<b>Контактные данные:</b>"
                                      "\n"
                                      f"\n<b>Ф.И.О.:</b> {row[3]}"
                                      f"\n<b>Контактный номер телефона:</b> {row[4]}"
                                      f"\n<b>Адрес:</b> {row[5]}"
                                      "\n"
                                      f"\n<b>Обращение: {row[6]}</b>", parse_mode="HTML", reply_markup=markup)


def avto(message):
    if message.text in censore:
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)
        bot.send_message(message.chat.id, "Нецензурная лексика в нашем боте строго запрещена!")
        msg = bot.send_message(message.chat.id, "Введите номер вашего автомобиля(A001AA25): ")
        bot.register_next_step_handler(msg, avto)
    else:
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
        cursor.execute(f'UPDATE work SET avto = "{message.text}", user_id = {message.from_user.id}')
        conn.commit()


        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        profil = types.KeyboardButton(text='Профиль')
        uslugi = types.KeyboardButton(text='Услуги')
        ofic = types.KeyboardButton(text='Официальный Новороссийск')
        faq = types.KeyboardButton(text='FAQ')
        markup.add(profil, uslugi)
        markup.add(ofic)
        markup.add(faq)
        bot.send_message(message.from_user.id, f"Добро Пожаловать, {message.from_user.first_name}", reply_markup=markup)


def admin_message(text):
    cursor.execute(f'SELECT user_id FROM work')
    row = cursor.fetchall()
    return row


def sendd(message):
    text = message.text
    info = admin_message(text)
    bot.send_message(message.chat.id, '✅ Рассылка начата!')
    for i in range(len(info)):
        try:
            time.sleep(1)
            bot.send_message(info[i][0], str(text))
        except:
            pass
if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(15)
        print(e)
