import datetime
import json, re
from urllib.request import Request, urlopen

from datetime import date

def get_date():
    d1 = date(2022, 8, 26)
    d2 = date(2023, 3, 29)
    #d2 = datetime.date.today()
    result = (d1 - d2).days//7

    result = result * (-1)

    print(result)
    if result == 53:
        print(result)

get_date()

'''Берёт Id группы по неделе'''
def student_json(group_number, day):

    f = open('utils/jsonhere', 'w')
    req = Request(
        url=f'https://www.ulspu.ru/students/schedule/groups-{day}.json?0.0148182787736022',
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
    f = open('utils/timetable', "w")
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

