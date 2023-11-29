import telebot
import sqlite3
from telebot import types

firstName = None
lastName = None
phone = None
email = None
groupe = None
role = None
idAdmin = None
nameEvent = None
dataEvent = None
descrEvent = None
countMembers = None

bot = telebot.TeleBot('6403923052:AAHGqUcfTQNzddNfdwu5PArLe4i9BPajIJ0')


# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
@bot.message_handler(commands=['start'])
def start(message):
    connect = sqlite3.connect("usersVolunteer.db")
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
            id INTEGER,
            firstName TEXT,
            lastName TEXT,
            phone TEXT,
            email TEXT,
            tgUrl TEXT,
            groupe TEXT,
            role INTEGER
        )""")
    connect.commit()

    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    data = cursor.fetchone()
    print(data)
    if data is None:
        bot.send_message(message.chat.id, "Введите ваше имя")
        bot.register_next_step_handler(message, user_firstName)
    else:
        bot.send_message(message.chat.id, "Такой пользователь уже существует!")


def user_firstName(message):
    try:
        global firstName
        firstName = message.text.strip()
        bot.send_message(message.chat.id, "Введите вашу фамилию")
        bot.register_next_step_handler(message, user_lastName)
    except:
        bot.send_message(message.chat.id, "Введите ваше имя")
        bot.register_next_step_handler(message, user_firstName)


def user_lastName(message):
    try:
        global lastName
        lastName = message.text.strip()
        bot.send_message(message.chat.id, "Введите ваш телефонный номер")
        bot.register_next_step_handler(message, user_phone)
    except:
        bot.send_message(message.chat.id, "Введите вашу фамилию")
        bot.register_next_step_handler(message, user_lastName)


def user_phone(message):
    try:
        global phone
        phone = message.text.strip()
        bot.send_message(message.chat.id, "Введите ваш email")
        bot.register_next_step_handler(message, user_email)
    except:
        bot.send_message(message.chat.id, "Введите ваш телефонный номер")
        bot.register_next_step_handler(message, user_phone)


def user_email(message):
    try:
        global email
        email = message.text.strip()
        bot.send_message(message.chat.id, "Введите вашу группу")
        bot.register_next_step_handler(message, user_groupe)
    except:
        bot.send_message(message.chat.id, "Введите ваш email")
        bot.register_next_step_handler(message, user_email)


def user_groupe(message):
    try:
        global groupe
        groupe = message.text.strip()
        bot.send_message(message.chat.id, "Если вы волонтер введите '1' Если вы организатор '2'")
        bot.register_next_step_handler(message, user_role)
    except:
        bot.send_message(message.chat.id, "Введите вашу группу")
        bot.register_next_step_handler(message, user_groupe)


def user_role(message):
    global role
    if message.text == '2':
        bot.send_message(message.chat.id,
                         "Введите пароль организатора. Его можно узнать у руководителя волонтерского движения")
        bot.register_next_step_handler(message, user_toPasswordRole)
    elif message.text == '1':
        role = message.text.strip()

        connect = sqlite3.connect("usersVolunteer.db")
        cursor = connect.cursor()

        cursor.execute(f"INSERT INTO login_id VALUES (?, ?, ?, ?, ?, ?, ?);",
                       (message.chat.id, firstName, lastName, phone, email, groupe, role))
        connect.commit()
        cursor.close()
        connect.close()
        bot.send_message(message.chat.id, "Вы зарегистрированы как волонтер")
    else:
        bot.send_message(message.chat.id, "Если вы волонтер введите '1' Если вы организатор '2'")
        bot.register_next_step_handler(message, user_role)


def user_toPasswordRole(message):
    global role
    if message.text == "12345":
        role = '2'

        connect = sqlite3.connect("usersVolunteer.db")
        cursor = connect.cursor()

        cursor.execute(f"INSERT INTO login_id VALUES (?, ?, ?, ?, ?, ?, ?);",
                       (message.chat.id, firstName, lastName, phone, email, groupe, role))
        connect.commit()
        cursor.close()
        connect.close()
    else:
        bot.send_message(message.chat.id, "Неправильный пароль!")
        bot.send_message(message.chat.id, "Если вы волонтер введите '1' Если вы организатор '2'")
        bot.register_next_step_handler(message, user_role)


@bot.message_handler(commands=['reg'])
def reg(message):
    connect = sqlite3.connect("usersVolunteer.db")
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM login_id")
    data = cursor.fetchall()
    print(data[-1])


# Меню выбора

@bot.message_handler(commands=['button'])
def button(message):
    bot.send_message(message.chat.id, 'Выбери действие', reply_markup=returnMarkup())


# ДОБАВЛЕНИЕ МЕРОПРИЯТИЯ

@bot.message_handler(commands=['addEvent', 'addevent'])
def addEvent(message):
    connect = sqlite3.connect("usersVolunteer.db")
    cursor = connect.cursor()

    connectEvent = sqlite3.connect("eventVolunteer.db")
    cursorEvent = connectEvent.cursor()

    cursorEvent.execute("""CREATE TABLE IF NOT EXISTS event_id(
                idAdmin INTEGER,
                idEvent INTEGER,
                nameEvent TEXT,
                data TEXT,
                descr TEXT,
                countMembers INTEGER
            )""")
    connectEvent.commit()

    people_id = message.chat.id
    cursor.execute(f"SELECT role FROM login_id WHERE id = {people_id}")
    check = cursor.fetchone()
    print(check)
    if check[0] == 2:
        bot.send_message(message.chat.id, 'Введите название вашего мероприятия')
        bot.register_next_step_handler(message, event_name)
    else:
        bot.send_message(message.chat.id, 'У вас недостаточно прав')


def event_name(message):
    try:
        global nameEvent
        nameEvent = message.text.strip()
        bot.send_message(message.chat.id, "Введите дату мероприятия (Образец: 01.01.2001)")
        bot.register_next_step_handler(message, event_data)
    except:
        bot.send_message(message.chat.id, "Введите название вашего мероприятия")
        bot.register_next_step_handler(message, event_name)


def event_data(message):
    try:
        global dataEvent
        dataEvent = message.text.strip()
        bot.send_message(message.chat.id, "Напишите задачи волонтеров на вашем мероприятии")
        bot.register_next_step_handler(message, event_descr)
    except:
        bot.send_message(message.chat.id, "Введите дату мероприятия")
        bot.register_next_step_handler(message, event_data)


def event_descr(message):
    try:
        global descrEvent
        descrEvent = message.text.strip()
        bot.send_message(message.chat.id, "Напишите количество участников (Строго число)")
        bot.register_next_step_handler(message, event_members)
    except:
        bot.send_message(message.chat.id, "Напишите задачи волонтеров на вашем мероприятии")
        bot.register_next_step_handler(message, event_descr)


def event_members(message):
    if message:
        global countMembers
        countMembers = message.text.strip()

        connect = sqlite3.connect("eventVolunteer.db")
        cursor = connect.cursor()

        cursor.execute("SELECT idEvent FROM event_id")
        data = cursor.fetchall()
        print(data[-1])

        test = data[-1]
        test = test[0] + 1

        cursor.execute(f"INSERT INTO event_id VALUES (?, ?, ?, ?, ?, ?);",
                       (message.chat.id, test, nameEvent, dataEvent, descrEvent, countMembers))
        connect.commit()
        cursor.close()
        connect.close()

        connect = sqlite3.connect(f"{nameEvent}.db")
        cursor = connect.cursor()

        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {nameEvent}(
                                idAdmin INTEGER,
                                idVolunteers INTEGER,
                                firstName TEXT,
                                lastName TEXT,
                                phoneVolunteer TEXT,
                                VacPos INTEGER
                            )""")
        connect.commit()

        connectAdmin = sqlite3.connect("usersVolunteer.db")
        cursorAdmin = connectAdmin.cursor()

        cursorAdmin.execute(f"SELECT firstName, lastName, phone FROM login_id WHERE id = {message.chat.id}")
        data = cursorAdmin.fetchone()
        print(data)

        cursor.execute(f"INSERT INTO {nameEvent} VALUES (?, ?, ?, ?, ?, ?);",
                       (message.chat.id, message.chat.id, data[0], data[1], data[2], countMembers))
        connectAdmin.commit()
        cursorAdmin.close()
        connectAdmin.close()
        connect.commit()
        cursor.close()
        connect.close()

    else:
        bot.send_message(message.chat.id, "Напишите нужно количество волонтеров1")
        bot.register_next_step_handler(message, event_members)


def returnMarkup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('Показать все мероприятия', callback_data='show_event')
    item2 = types.InlineKeyboardButton('Профиль', callback_data='show_profile')
    item3 = types.InlineKeyboardButton('Зарегистрироваться на волонтерство', callback_data='reg_to_event')
    markup.add(item, item2, item3)
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'back':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "Выберите действие", reply_markup=returnMarkup())

        elif call.data == 'edit':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            item = types.InlineKeyboardButton('Назад', callback_data='back')
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(item)
            bot.send_message(call.message.chat.id, "я еще не сделал", reply_markup=markup)

        elif call.data == 'show_profile':
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                connect = sqlite3.connect("usersVolunteer.db")
                cursor = connect.cursor()

                people_id = call.message.chat.id
                cursor.execute(f'SELECT firstName, lastName, phone, email, groupe FROM login_id WHERE id = {people_id}')
                users = cursor.fetchall()

                info = ''
                for el in users:
                    info += (f'{el[0]} {el[1]}\n'
                             f'Номер телефона: {el[2]}\n'
                             f'Email: {el[3]}\n'
                             f'Ваша группа: {el[4]}')

                cursor.close()
                connect.close()

                markup = types.InlineKeyboardMarkup(row_width=1)
                item2 = types.InlineKeyboardButton('Редактировать', callback_data='edit')
                item = types.InlineKeyboardButton('Назад', callback_data='back')
                markup.add(item, item2)

                bot.send_message(call.message.chat.id, info, reply_markup=markup)
            except:
                bot.send_message(call.message.chat.id, "Вы не зарегистрированы")

        elif call.data == 'show_event':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            connect = sqlite3.connect("eventVolunteer.db")
            cursor = connect.cursor()

            cursor.execute('SELECT idEvent, nameEvent, data, descr, countMembers FROM event_id')
            events = cursor.fetchall()

            info = ''
            for el in events:
                info += (
                    f'<b>ID мероприятия:</b> {el[0]} \n <b>Название мероприятия:</b> {el[1]} \n <b>Дата проведения:</b> {el[2]} \n <b>Описание мероприятия:</b> {el[3]} \n Количество вакантных мест: {el[4]}\n')

            cursor.close()
            connect.close()

            markup = types.InlineKeyboardMarkup(row_width=2)
            item = types.InlineKeyboardButton('Назад', callback_data='back')
            markup.add(item)

            bot.send_message(call.message.chat.id, info, reply_markup=markup, parse_mode='html')

        elif call.data == 'reg_to_event':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "Напишите id мероприятия")
            bot.register_next_step_handler(call.message, reg_user_to_vol)

def reg_user_to_vol(message):
    try:
        connect = sqlite3.connect("eventVolunteer.db")
        cursor = connect.cursor()

        print(message.text)

        connectUser = sqlite3.connect("usersVolunteer.db")
        cursorUser = connectUser.cursor()
        cursorUser.execute(f'SELECT id, firstName, lastName, phone FROM login_id WHERE id={message.chat.id}')
        dataUser = cursorUser.fetchone()

        cursor.execute(f'SELECT nameEvent FROM event_id WHERE idEvent={message.text}')
        data = cursor.fetchone()
        cursor.execute(f'SELECT descr FROM event_id WHERE idEvent={message.text}')
        dataDescr = cursor.fetchone()
        print(data[0])
        cursor.execute(f'SELECT countMembers FROM event_id WHERE idEvent={message.text}')
        vacPos = cursor.fetchone()
        print(vacPos[0])
        connectEvent = sqlite3.connect(data[0]+".db")
        cursorEvent = connectEvent.cursor()

        cursorEvent.execute(f'SELECT idVolunteers FROM {data[0]}')
        dataTest = cursorEvent.fetchall()

        test1 = 0
        test = len(dataTest)
        print(test)
        for i in range(len(dataTest)):
            res = dataTest[i]
            check = res[0]
            print(check)
            if (message.chat.id != check):
                test1+=1
            else:
                print('2929293')

        print(test1)
        if (test1 == test):
            sql = f"""UPDATE event_id SET countMembers = countMembers-1 WHERE idEvent={message.text}"""
            cursor.execute(sql)
            connect.commit()

            cursorEvent.execute(f"INSERT INTO {data[0]} VALUES(?, ?, ?, ?, ?, ?);",
                                (0, dataUser[0], dataUser[1], dataUser[2], dataUser[3], int(vacPos[0]) - 1))
            connectEvent.commit()
            bot.send_message(message.chat.id, f"Вы зарегистрировались на мероприятие - {data[0]}")
            bot.send_message(message.chat.id, f"{dataDescr[0]}")
            print('11111')
        elif (test1 != test):
            bot.send_message(message.chat.id, f"Судя по всему, вы уже зарегистрированы на мероприятии - {data[0]}")
            print(('319319931'))

    except:
        print('02')


bot.polling()