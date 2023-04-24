import telebot
import sqlite3
from aiogram import Bot, Dispatcher, executor, types

#Настройка бд
conn = sqlite3.connect('DeadLineBot', check_same_thread=False)
cursor = conn.cursor()

def db_table_val(task_name: str, task_deadline: str, task_person: str):
    cursor.execute('INSERT INTO tasks (name, deadline, person) VALUES (?, ?, ?)', (task_name, task_deadline, task_person))
    conn.commit()

#Настройка бота
API_TOKEN = '6194104756:AAGMLy2K78jiRBrIZRMFObIvLiAQ72q4m_4'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

#Блок со всеми командами
global last_command
global current_message

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ бот по твоим дедлайнам!\nОтправь мне любое сообщение, а я тебе отправлю инструкции.")


@dp.message_handler(commands=['new_task'])
async def cmd_reply(message: types.Message):
    global last_command
    await message.reply('Введите параметры задачи в следующем виде:\nНазвание, срок сдачи, ответственный')
    last_command = 'new_task'


@dp.message_handler(commands=['check_tasks'])
async def cmd_reply(message: types.Message):
    global last_command
    await message.reply('Вот все ваши задачи:\n ')
    last_command = 'check_tasks'
    all_records = get_all_records()
    await message.answer(all_records)

@dp.message_handler(commands=['delete_task'])
async def cmd_reply(message: types.Message):
    global last_command
    await message.reply('Введите номер (айди) задачи, которую необходимо удалить')
    last_command = 'delete_task'


#Функция считывания параметров команд и вывода ответов для каждого из них
@dp.message_handler()
async def send_answer_to_command(message: types.Message):
    global last_command
    global current_message
    if last_command == 'new_task':
        current_message = message.text

        answer = 'Добавил новую задачу: ' + message.text + '\n' + 'Айди этой задачи: '
        await message.answer(answer)
        add_record(current_message)


#Здесь ничего нет для last_command == 'cheack_tasks', т.к. у нас нет доп. параметров для этой команды и отвечаем сразу




    if last_command == 'delete_task':
        current_message = message.text
        delete_record(current_message)
        answer = 'Удалил задачу под номером ' + message.text
        await message.answer(answer)

#Функция добавления записи в базу данных
def add_record(task):
    task_to_database = task.split()
    t_name = task_to_database[0]
    t_deadline = task_to_database[1]
    t_person = task_to_database[2]
    db_table_val(task_name=t_name, task_deadline=t_deadline, task_person=t_person)

#Функция удаления записи в базе данных
def delete_record(task_id):
    try:
        sqlite_connection = sqlite3.connect('DeadLineBot')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_delete_query = """DELETE from tasks where id = """ + task_id
        cursor.execute(sql_delete_query)
        sqlite_connection.commit()
        print("Запись успешно удалена")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


# class record(object):
#     def __init__(self, id, name, deadline, human):
#         """Constructor"""
#         self.id = id
#         self.name = name
#         self.deadline = deadline
#         self.human = human
#
#     def convert_record_to_str(self):
#         record_str = f'{self.id} {self.name} {self.deadline} {self.human}'
#         return record_str

def get_all_records():
    try:
        sqlite_connection = sqlite3.connect('DeadLineBot')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT * from tasks"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        all_records = ''

        for row in records:
            all_records += f'{row[0]} | {row[1]} | {row[2]} | {row[3]}\n\n'

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

    return all_records







if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



