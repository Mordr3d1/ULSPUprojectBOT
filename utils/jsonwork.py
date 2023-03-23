import json, datetime
from urllib.request import Request, urlopen

from requests import get

from requests import get


'''Дни недели'''
def day_week(day):
    if day == 'Сегодня':
        day = datetime.date.today()

    elif day == 'Завтра':
        day = datetime.date.today()
        day = day + datetime.timedelta(days=1)

    day = datetime.datetime.strptime(str(day), "%Y-%m-%d").date()
    day = day.weekday()
    if day == 0:
        return ' (Понедельник)'
    elif day == 1:
        return ' (Вторник)'
    elif day == 2:
        return ' (Среда)'
    elif day == 3:
        return ' (Четверг)'
    elif day == 4:
        return ' (Пятница)'
    elif day == 5:
        return ' (Суббота)'
    elif day == 6:
        return ' (Воскресенье)'



'''Создаёт файл со всем расписанием'''




def schedule(group_number, day):

    if day == 'Сегодня':
        day = datetime.date.today()

    elif day == 'Завтра':
        day = datetime.date.today()
        day = day + datetime.timedelta(days=1)


    req = get(f'https://raspi.ulspu.ru/json/dashboard/events?mode=group&value={group_number}')


    raw_schedudle = json.loads(req.text)
    raw_raspisanie = []


    raspis =  raspis = 'Расписание на ' + str(day) + day_week(day) + ':\n'+ '\n'


    day = datetime.datetime.strptime(str(day), "%Y-%m-%d").date()


    para = 1

    prodpara = datetime.timedelta(hours=1, minutes=30)
    lasttime = datetime.timedelta(hours=8, minutes=30)
    nopara = ''

    for item in raw_schedudle['data']:
        dayrspis = datetime.datetime.strptime(item['start'], "%Y-%m-%dT%H:%M:%S.%fZ").date()
        if day == dayrspis:
            raw_raspisanie.append(item)
        raw_raspisanie = sorted(raw_raspisanie,
                           key=lambda x: datetime.datetime.strptime(x['start'], "%Y-%m-%dT%H:%M:%S.%fZ").time())

    for item in raw_raspisanie:
        startt = datetime.datetime.strptime(item['start'], "%Y-%m-%dT%H:%M:%S.%fZ").time()
        starttime = datetime.timedelta(hours=startt.hour, minutes=startt.minute, seconds=startt.second,microseconds=startt.microsecond) + datetime.timedelta(hours=4, minutes=0,seconds=0, microseconds=0)
        endt = datetime.datetime.strptime(item['end'], "%Y-%m-%dT%H:%M:%S.%fZ").time()
        endtime = datetime.timedelta(hours=endt.hour, minutes=endt.minute, seconds=endt.second,microseconds=endt.microsecond) + datetime.timedelta(hours=4, minutes=0, seconds=0,microseconds=0)

        if starttime == lasttime:
            raspis = raspis + item['title'] + '\n' + 'Время: ' +'\n' + str(starttime)[:-3] + '-' + str(endtime)[:-3] + '\n'
        else:
            nopara = starttime - lasttime
            if nopara // prodpara > 4:
                para = para + nopara // prodpara - 1
            else:
                para = para + nopara // prodpara
            raspis ='\n' + raspis + str(para) + ' Пара \n' + item['title'] + ' Время: ' + str(starttime)[:-3] + '-' + str(
                endtime)[:-3] + '\n'
            lasttime = starttime
    if len(raspis) <= 40:
        raspis = f'У {group_number.replace("%20", " ")} нет в занятий в этот день.'
        return raspis
    else:
        return raspis










'''def get_json(group_number):
    f = open('utils/timetable', "w")
    f2 = open('utils/jsonhere', 'r')
    id = f2.read()
    req = Request(
        url=f'https://raspi.ulspu.ru/json/dashboard/events?mode=group&value={group_number}',
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
        f.write('\n')'''