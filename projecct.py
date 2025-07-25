import os.path
import random

from googleapiclient.discovery import build
from google.oauth2 import service_account
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import schedule
from impor import *
import datetime as dt
from threading import Thread


def time():
    while True:
        schedule.run_pending()


def job():
    result = sheet.values().get(spreadsheetId=sample_spreadsheet_id,
                                range=sample_range_name).execute()
    for count in range(len(result.get('values', []))):
        lst = str(result.get('values', [])[count - 2][14]).split(';')
        if lst[0] != 'choosen_oly':
            user_id = result.get('values', [])[count - 2][0]
            for j in lst:
                r = oly_by_name(j)
                date = str(r.start)
                if '...' in date:
                    date1 = date.split('...')
                    n = ''
                    h = ''
                    for t in date1[0]:
                        if t != ' ':
                            if t.isdigit():
                                n += t
                            else:
                                h += t
                    if not h:
                        for t in date1[1]:
                            if t != ' ':
                                if t.isdigit():
                                    n += t
                                else:
                                    h += t
                    month = int(mon.index(h))
                    month = 4
                    day = int(n)
                    day = 24
                    mon1 = dt.datetime.now().month
                    day1 = dt.datetime.now().day
                    if month == mon1 and day - 1 == day1:
                        if j:
                            sender(user_id, f'Завтра начнется {j}')
                    elif month == mon1 and day == day1:
                        if j:
                            sender(user_id, f'{j} Началась. Желаем вам удачи')
                else:
                    n = ''
                    h = ''
                    for t in date:
                        if t != ' ':
                            if t.isdigit():
                                n += t
                            else:
                                h += t
                    if not h:
                        for t in date[1]:
                            if t != ' ':
                                if t.isdigit():
                                    n += t
                                else:
                                    h += t
                    month = int(mon.index(h))
                    month = 4
                    day = int(n)
                    day = 24
                    mon1 = dt.datetime.now().month
                    day1 = dt.datetime.now().day
                    if month == mon1 and day - 1 == day1:
                        if j:
                            sender(user_id, f'Завтра начнется {j}')
                    elif month == mon1 and day == day1:
                        if j:
                            sender(user_id, f'{j} Началась. Желаем вам удачи')


def oly_by_name(title):
    obj = db_sess.query(Oly).all()
    for el in obj:
        if title.lower() in str(el.name).lower() or str(el.name).lower() in title.lower():
            return el


token = "token :)"
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
sp = ['Биология', 'География', 'Информатика', 'Математика', 'Физика', 'Химия', 'Астрономия',
      'История', 'Обществознание', 'Экономика', 'Психология']
mon = ['янв', 'фев', 'мар', 'фпр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']

dict1 = {'Биология': '5B11%5D',
         'География': '5B10%5D',
         'Информатика': '5B6%5D',
         'Математика': '5B6%5D',
         'Физика': '5B12%5D',
         'Химия': '5B13%5D',
         'Астрономия': '5B20%5D',
         'История': '5B8%5D',
         'Обществознание': '5B9%5D',
         'Экономика': '5B14%5D',
         'Психология': '5B28%5D'}

scopes = ['https://www.googleapis.com/auth/spreadsheets']
base_dir = os.path.dirname(os.path.abspath(__file__))
service_file = os.path.join(base_dir, "credations.json")
credentials = service_account.Credentials.from_service_account_file(service_file, scopes=scopes)

# The ID and range of a sample spreadsheet.
sample_spreadsheet_id = 'name'
sample_range_name = 'Data'

mobs_spreadsheet_id = 'name'
mobs_range_name = 'mobs'

service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()


def sender(user_id, msg, keyboard=None):
    if keyboard:
        vk.method('messages.send', {'user_id': user_id, 'message': msg, 'random_id': 0,
                                    'keyboard': keyboard.get_keyboard()})
    else:
        vk.method('messages.send', {'user_id': user_id, 'message': msg, 'random_id': 0})


def check_in_game_data(user_id):
    # Call the Sheets API
    result = sheet.values().get(spreadsheetId=sample_spreadsheet_id,
                                range=sample_range_name).execute()
    values = result.get('values', [])
    count = 0
    for row in values:
        count += 1
        if row[0] != 'id':
            if int(user_id) == int(row[0]):
                return count
        else:
            count = 2
    range_ = f'Data!A{count}:Q{count}'
    array = {'values': [
        [user_id, 'нету', 'нету', 1, 0, 100, 100, 1, 1, 1, 1, 1, 100, 100, 100, 0, 'start_1']]}
    service.spreadsheets().values().update(spreadsheetId=sample_spreadsheet_id,
                                           range=range_,
                                           valueInputOption='USER_ENTERED',
                                           body=array).execute()
    return False


def what_is_your_location(user_id, msg, count):
    # Call the Sheets API
    result = sheet.values().get(spreadsheetId=sample_spreadsheet_id,
                                range=sample_range_name).execute()
    loc = result.get('values', [])[count - 2][16]
    if msg == 'меню':
        keyboard = VkKeyboard()
        keyboard.add_button("Выбрать предмет олимпиады", VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button("Ваши олимпиады", VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("Новости", VkKeyboardColor.NEGATIVE)
        array = {'values': [['starter_loc']]}
        range_ = f'Data!Q{count - 1}:Q{count - 1}'
        service.spreadsheets().values().update(spreadsheetId=sample_spreadsheet_id,
                                               range=range_,
                                               valueInputOption='USER_ENTERED',
                                               body=array).execute()
        sender(user_id, 'Вы в меню', keyboard=keyboard)
    elif loc == 'start_1':
        name_1(user_id, msg, count - 2)
    elif loc == 'start_2' and msg == 'нет':
        name_3(user_id, msg, count)
    elif loc == 'start_2':
        name_2(user_id, msg, count)
    elif loc == 'year_1':
        year_1(user_id, msg, count)
    elif loc == 'starter_loc' or msg == 'выбрать предмет олимпиады' or \
            msg == 'ваши олимпиады' or msg == 'ближайшие олимпиады' or msg == 'меню':
        starter_loc(user_id, msg, count)
    elif loc == 'village':
        village(user_id, msg, count)
    elif loc == 'change_oly':
        change(user_id, msg, count)
    elif loc == 'choose':
        choose(user_id, msg, count)
    elif loc == 'action':
        action(user_id, msg, count)


def name_1(user_id, msg, count):
    keyboard = VkKeyboard()
    keyboard.add_button("Да", VkKeyboardColor.PRIMARY)
    keyboard.add_button("Нет", VkKeyboardColor.PRIMARY)
    sender(user_id, f'Ваc зовут - {msg.capitalize()}? Я верно расслышал?', keyboard)
    range_ = f'Data!A{count + 1}:Q{count + 1}'
    array = {'values': [[user_id, msg.capitalize(), 'нету', 1, 0, 10, 10, 1, 1, 1, 1, 1,
                         100, 10, 10, 0, 'start_2']]}
    service.spreadsheets().values().update(spreadsheetId=sample_spreadsheet_id,
                                           range=range_,
                                           valueInputOption='USER_ENTERED',
                                           body=array).execute()


def name_2(user_id, msg, count):
    result = sheet.values().get(spreadsheetId=sample_spreadsheet_id,
                                range=sample_range_name).execute()
    res = result.get('values', [])[count - 2][1]
    sender(user_id, f'Принято, {res}! Да прибудет с вами Сила!')
    range_ = f'Data!Q{count - 1}:Q{count - 1}'
    array = {'values': [['year_1']]}
    service.spreadsheets().values().update(spreadsheetId=sample_spreadsheet_id,
                                           range=range_,
                                           valueInputOption='USER_ENTERED',
                                           body=array).execute()
    sender(user_id, 'В каком классе вы учитесь?')


def name_3(user_id, msg, count):
    result = sheet.values().get(spreadsheetId=sample_spreadsheet_id,
                                range=sample_range_name).execute()
    res = result.get('values', [])[count - 2][1]
    sender(user_id, 'Тогда назовите свое имя')
    range_ = f'Data!A{count - 1}:Q{count - 1}'
    array = {
        'values': [[user_id, res, 'нету', 1, 0, 10, 10, 1, 1, 1, 1, 1, 100, 10, 10, 0, 'start_1']]}
    service.spreadsheets().values().update(spreadsheetId=sample_spreadsheet_id,
                                           range=range_,
                                           valueInputOption='USER_ENTERED',
                                           body=array).execute()


def year_1(user_id, msg, count):
    result = sheet.values().get(spreadsheetId=sample_spreadsheet_id,
                                range=sample_range_name).execute()
    res = result.get('values', [])[count - 2][2]
    if msg.isdigit():
        if 1 <= int(msg) <= 11:
            keyboard = VkKeyboard()
            keyboard.add_button("Выбрать предмет олимпиады", VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("Ваши олимпиады", VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button("Новости", VkKeyboardColor.NEGATIVE)
            array = {'values': [[user_id, res, int(msg), 1, 0, 10, 10, 1, 1, 1, 1, 1, 100, 10, 10, 0,
                                 'starter_loc']]}
            sender(user_id, 'сообщение', keyboard=keyboard)
            range_ = f'Data!A{count - 1}:Q{count - 1}'
            service.spreadsheets().values().update(spreadsheetId=sample_spreadsheet_id,
                                                   range=range_,
                                                   valueInputOption='USER_ENTERED',
                                                   body=array).execute()

        else:
            sender(user_id, 'Введите число от 1 до 11')
    else:
        sender(user_id, 'Введите число от 1 до 11', keyboard=False)


def year_2(user_id, msg, count):
    keyboard = VkKeyboard()
    keyboard.add_button("Выбрать предмет олимпиады", VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Ваши олимпиады", VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Новости", VkKeyboardColor.NEGATIVE)
    result = sheet.values().get(spreadsheetId=sample_spreadsheet_id,
                                range=sample_range_name).execute()
    res = result.get('values', [])[count - 2][2]
    if msg.isdigit():
        if 1 <= int(msg) <= 11:
            array = {'values': [[user_id, res, int(msg), 1, 0, 10, 10, 1, 1, 1, 1, 1, 100, 10, 10, 0,
                                 'starter_loc']]}
        else:
            sender(user_id, 'Введите число от 1 до 11', keyboard=keyboard)
            array = {'values': [
                [user_id, res, int(msg), 1, 0, 10, 10, 1, 1, 1, 1, 1, 100, 10, 10, 0, 'year_1']]}
    else:
        sender(user_id, 'Введите число от 1 до 11', keyboard=False)
        array = {'values': [
            [user_id, res, int(msg), 1, 0, 10, 10, 1, 1, 1, 1, 1, 100, 10, 10, 0, 'year_1']]}

    range_ = f'Data!A{count - 1}:Q{count - 1}'
    service.spreadsheets().values().update(spreadsheetId=sample_spreadsheet_id,
                                           range=range_,
                                           valueInputOption='USER_ENTERED',
                                           body=array).execute()


def village(user_id, msg, count):
    if msg != 'назад':
        sender(user_id, 'Список олимпиад')
        range_ = f'Data!Q{count - 1}:Q{count - 1}'
        array = {'values': [['starter_loc']]}
        service.spreadsheets().values().update(spreadsheetId=sample_spreadsheet_id,
                                               range=range_,
                                               valueInputOption='USER_ENTERED',
                                               body=array).execute()
    else:
        keyboard = VkKeyboard()
        keyboard.add_button("Назад", VkKeyboardColor.PRIMARY)
        range_ = f'Data!Q{count - 1}:Q{count - 1}'
        array = {'values': [['change_oly']]}
        service.spreadsheets().values().update(spreadsheetId=sample_spreadsheet_id,
                                               range=range_,
                                               valueInputOption='USER_ENTERED',
                                               body=array).execute()
        sender(user_id, 'Напишите название предмета')


def starter_loc(user_id, msg, count):
    if msg == 'выбрать предмет олимпиады':
        keyboard = VkKeyboard()
        keyboard.add_button("Назад", VkKeyboardColor.PRIMARY)
        sender(user_id, 'Напишите название предмета', keyboard=keyboard)
        range_ = f'Data!Q{count - 1}:Q{count - 1}'
        array = {'values': [['change_oly']]}
        service.spreadsheets().values().update(spreadsheetId=sample_spreadsheet_id,
                                               range=range_,
                                               valueInputOption='USER_ENTERED',
                                               body=array).execute()
    elif msg == 'ваши олимпиады':
        sender(user_id, 'Ваш список олимпиад')
        result = sheet.values().get(spreadsheetId=sample_spreadsheet_id,
                                    range=sample_range_name).execute()
        lst = str(result.get('values', [])[count - 2][14]).split(';')
        for j in lst:
            if j:
                obj = oly_by_name(j)
                e = ''
                e += str(obj.name) + '\n'
                e += 'Начало: ' + '\t' + str(obj.start) + '\n'
                e += 'Рейтинг: ' + '\t' + str(obj.rate)
                sender(user_id, e)

    elif msg == 'новости':
        result = sheet.values().get(spreadsheetId=sample_spreadsheet_id,
                                    range=sample_range_name).execute()
        res = result.get('values', [])[count - 2][2]
        u = Parser(sp[random.randint(0, len(sp))], res, 'year')
        t = ''
        for i in range(5):
            t += u.oly(i).last_news + '\n'
        sender(user_id, t)
        range_ = f'Data!Q{count - 1}:Q{count - 1}'
        array = {'values': [['starter_loc']]}
        service.spreadsheets().values().update(spreadsheetId=sample_spreadsheet_id,
                                               range=range_,
                                               valueInputOption='USER_ENTERED',
                                               body=array).execute()


def change(user_id, msg, count):
    if msg.capitalize() in dict1:
        result = sheet.values().get(spreadsheetId=sample_spreadsheet_id,
                                    range=sample_range_name).execute()
        res = result.get('values', [])[count - 2][2]
        g = dict1[msg.capitalize()]
        a = Parser(g, res, 'year')
        e = ''
        keyboard = VkKeyboard()
        t = str(a.oly(0).name)[:40]
        e += str(a.oly(0).name) + "\n"
        keyboard.add_button(t, VkKeyboardColor.PRIMARY)
        for i in range(1, 5):
            t = str(a.oly(i).name)[:40]
            e += str(a.oly(i).name) + "\n"
            keyboard.add_line()
            keyboard.add_button(t, VkKeyboardColor.PRIMARY)
        sender(user_id, f'{e}', keyboard=keyboard)
        range_ = f'Data!Q{count - 1}:Q{count - 1}'
        array = {'values': [['choose']]}
        service.spreadsheets().values().update(spreadsheetId=sample_spreadsheet_id,
                                               range=range_,
                                               valueInputOption='USER_ENTERED',
                                               body=array).execute()
    elif msg == 'назад':
        keyboard = VkKeyboard()
        keyboard.add_button("Выбрать предмет олимпиады", VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button("Ваши олимпиады", VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("Новости", VkKeyboardColor.NEGATIVE)
        range_ = f'Data!Q{count - 1}:Q{count - 1}'
        array = {'values': [['starter_loc']]}
        service.spreadsheets().values().update(spreadsheetId=sample_spreadsheet_id,
                                               range=range_,
                                               valueInputOption='USER_ENTERED',
                                               body=array).execute()
        sender(user_id, 'Вы вернулись', keyboard=keyboard)


def choose(user_id, msg, count):
    obj = oly_by_name(msg)
    e = ''
    keyboard = VkKeyboard()
    e += str(obj.name) + '\n'
    e += 'Начало: ' + '\t' + str(obj.start) + '\n'
    e += 'Рейтинг: ' + '\t' + str(obj.rate)
    keyboard.add_button('Добавить в мои')
    keyboard.add_line()
    keyboard.add_button('Последняя новость')
    keyboard.add_line()
    keyboard.add_button('Материалы для подготовки')
    keyboard.add_line()
    keyboard.add_button('Меню')
    sender(user_id, str(e), keyboard=keyboard)
    range_ = f'Data!Q{count - 1}:Q{count - 1}'
    array = {'values': [['action']]}
    service.spreadsheets().values().update(spreadsheetId=sample_spreadsheet_id,
                                           range=range_,
                                           valueInputOption='USER_ENTERED',
                                           body=array).execute()
    range_ = f'Data!P{count - 1}:P{count - 1}'
    array = {'values': [[obj.name]]}
    service.spreadsheets().values().update(spreadsheetId=sample_spreadsheet_id,
                                           range=range_,
                                           valueInputOption='USER_ENTERED',
                                           body=array).execute()


def action(user_id, msg, count):
    result = sheet.values().get(spreadsheetId=sample_spreadsheet_id,
                                range=sample_range_name).execute()
    lst = str(result.get('values', [])[count - 2][14])
    chosen = str(result.get('values', [])[count - 2][15])
    e = ''
    if msg == 'добавить в мои':
        if chosen not in lst:
            lst += ';' + str(chosen)
            range_ = f'Data!O{count - 1}:O{count - 1}'
            array = {'values': [[lst]]}
            service.spreadsheets().values().update(spreadsheetId=sample_spreadsheet_id,
                                                   range=range_,
                                                   valueInputOption='USER_ENTERED',
                                                   body=array).execute()
            e = f'{chosen} была добавлена в ваши олимпиады'
        else:
            e = 'Эта олимпиада уже в вашем списке'
    elif msg == 'последняя новость':
        obj = oly_by_name(chosen)
        e = str(obj.last_news)
        e += '\n' + 'https://olimpiada.ru' + obj.last_news_link
    elif msg == 'материалы для подготовки':
        try:
            if obj := oly_by_name(chosen).materilas:
                e = obj
            else:
                e = 'Эта олимпиада не предоставила материалов для подготовки!'
        except Exception:
            e = 'Эта олимпиада не предоставила материалов для подготовки!'
    sender(user_id, e)


def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                user_id = event.user_id
                msg = event.text.lower()
                in_game = check_in_game_data(user_id)
                if in_game:
                    what_is_your_location(user_id, msg, in_game)
                else:
                    sender(user_id, "Приветствую. Как мне к вам обращатся?")


if __name__ == '__main__':
    db_session.global_init("db/oly0.db")
    db_sess = db_session.create_session()
    schedule.every().day.at("09:00").do(job)
    Thread(target=main).start()
    Thread(target=time).start()
