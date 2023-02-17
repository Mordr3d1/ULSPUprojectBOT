import json, re
from urllib.request import Request, urlopen


def student_json(group_number, week):
    group_number = group_number
    f = open('utils/jsonhere', 'w')
    req = Request(
        url=f'https://www.ulspu.ru/students/schedule/groups-{week}.json?0.0148182787736022',
        headers={'User-Agent': 'Mozila/5.0'}
    )
    site = urlopen(req)
    data = json.load(site)
    for item in data['data']:
        if group_number == item['text']:
            id = item['id']
            f.write(id)
            break


def get_json():
    """" Файл тайм тайбл """
    f = open('utils/timetable', "w")
    """" Айди студентов который был создан с помощью костыля"""
    f2 = open('utils/jsonhere', 'r')
    id = f2.read()
    req = Request(
        url=f'https://www.ulspu.ru/students/schedule/{id}.json',
        headers={'User-Agent': 'Mozila/5.0'})
    site = urlopen(req)
    data = json.load(site)
    for item in data:
        for i in data[item]:
            text = f' Дата: {item[0:10]}\n Расположение: {i["location"]},\n Преподаватель: {i["teachers"]},\n Время: {i["time"]},\n Предмет: {i["subject"]},\n Тип: {i["type"]}\n\n'
            text = re.sub('T13:00:00', '', text)
            f.write(text)



def take_info():
    f = open('utils/timetable', 'r')
    text = f.read()
    return text


def get_dates():
    f = open('utils/dateslist', 'w')
    req = Request(
        url='https://www.ulspu.ru/students/schedule/weeks.json',
        headers={'User-Agent': 'Mozila/5.0'}
    )

    site = urlopen(req)
    data = json.load(site)
    for item in data:
        f.write(str(item))
        f.write('\n')