import psycopg2
import telebot
import datetime
from telebot import types


token = "5983981418:AAETHQbRGFyFlTZN22Bq6qslcUVzZStvg8E"
bot = telebot.TeleBot(token)


conn = psycopg2.connect(database="timetable",
                        user="postgres",
                        password="2104",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


# Получение текущей даты для вычисления текущей недели и получение текущего дня недели
week = int(datetime.datetime.utcnow().isocalendar()[1]) % 2
if week == 0: next_week = 1
else: next_week = 0

def day_timetable(day, message, week):
    cursor.execute(
        "SELECT day, subject_name, room_numb, start_time, end_time, full_name FROM timetable INNER JOIN subject "
        "on timetable.subject = subject.id INNER JOIN teacher on "
        "teacher.subject = subject.id WHERE day=" + str(day) + " AND week='" + str(week) + "'" + "ORDER BY start_time")
    records = list(cursor.fetchall())
    print(records)
    bot.send_message(message.chat.id, records[0][0])
    bot.send_message(message.chat.id, "-------------------------------------------")
    for i in records:
        line = i[1] + "    " + i[2] + "    " + str(i[3]) + "-" + str(i[4]) + "    " + i[5]
        bot.send_message(message.chat.id, line)
    bot.send_message(message.chat.id, "-------------------------------------------")


def week_timetable(week, message):
    cursor.execute(
        "SELECT day, subject_name, room_numb, start_time, end_time, "
        "full_name FROM timetable INNER JOIN subject on timetable.subject = subject.id "
        "INNER JOIN teacher on teacher.subject = subject.id WHERE week=" + str(week))
    records = list(cursor.fetchall())
    for i in records:
        if i[0] == "Понедельник":
            day_timetable("'Понедельник'", message, week)
            break
    for i in records:
        if i[0] == "Вторник":
            day_timetable("'Вторник'", message, week)
            break
    for i in records:
        if i[0] == "Среда":
            day_timetable("'Среда'", message, week)
            break
    for i in records:
        if i[0] == "Четверг":
            day_timetable("'Четверг'", message, week)
            break
    for i in records:
        if i[0] == "Пятница":
            day_timetable("'Пятница'", message, week)
            break








@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Понедельник", "Вторник", "Среда")
    keyboard.row("Четверг", "Пятница")
    keyboard.row("Расписание на текущую неделю", "Расписание на следующую неделю", "/help")
    bot.send_message(message.chat.id, f"Здравствуйте, {message.from_user.first_name}, здесь Вы можете узнать "
                                      "расписание группы БВТ2203."
                                      "\nДля более детальной информации используйте: /help", reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, "Бот предназначен для получения расписания для "
                                      "группы БВТ2203."
                                      "\nТакже в боте есть несколько команд:"
                                      "\n/start - чтобы вернуться к приветствию"
                                      "\n/week - чтобы узнать какая неделя в данный момент;"
                                      "\n/mtuci - чтобы получить ссылку на официальный сайт университета;"
                                      "\n/help - чтобы получить более делательную информацию о боте.")

@bot.message_handler(commands=['week'])
def week_message(message):
    if week == 0:
        bot.send_message(message.chat.id, "На данный момент четная неделя")
    else:
        bot.send_message(message.chat.id, "На данный момент нечетная неделя")

@bot.message_handler(commands=['mtuci'])
def week_message(message):
    bot.send_message(message.chat.id, "Официальный сайт МТУСИ: https://mtuci.ru/")



@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "понедельник":
        day_timetable("'Понедельник'", message, week)
    elif message.text.lower() == "вторник":
        day_timetable("'Вторник'", message, week)
    elif message.text.lower() == "среда":
        day_timetable("'Среда'", message, week)
    elif message.text.lower() == "четверг":
        day_timetable("'Четверг'", message, week)
    elif message.text.lower() == "пятница":
        day_timetable("'Пятница'", message, week)
    elif message.text.lower() == "расписание на текущую неделю":
        week_timetable(week, message)
    elif message.text.lower() == "расписание на следующую неделю":
        week_timetable(next_week, message)
    else:
        bot.send_message(message.chat.id, 'Извините, я Вас не понял')

bot.polling(none_stop=True, interval=0)
