import json, datetime
from urllib.request import Request, urlopen

from requests import get

from jsonwork import day_week

#group_number, day Переменные которые необходимо задать

#day Сегодня или завтра

#Group number ИИЯ-19-01-01

def schedule():
    group_number ='ИИЯ-19-01-01'
    day = 'Сегодня'

    if day == 'Сегодня':
        day = datetime.date.today()

    elif day == 'Завтра':
        day = datetime.date.today()
        day = day + datetime.timedelta(days=1)

    req = get(f"https://raspi.ulspu.ru/json/dashboard/events?mode=group&value={group_number}")


    raw_schedudle = json.loads(req.text)

    raw_raspisanie = []

    raspis = raspis = 'Расписание на ' + str(day) + day_week(day) + ':\n'

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
        starttime = datetime.timedelta(hours=startt.hour, minutes=startt.minute, seconds=startt.second,
                                       microseconds=startt.microsecond) + datetime.timedelta(hours=4, minutes=0,
                                                                                             seconds=0, microseconds=0)
        endt = datetime.datetime.strptime(item['end'], "%Y-%m-%dT%H:%M:%S.%fZ").time()
        endtime = datetime.timedelta(hours=endt.hour, minutes=endt.minute, seconds=endt.second,
                                     microseconds=endt.microsecond) + datetime.timedelta(hours=4, minutes=0, seconds=0,
                                                                                         microseconds=0)

        if starttime == lasttime:
            raspis = raspis + item['title'] + ' Время: ' + str(starttime)[:-3] + '-' + str(endtime)[:-3] + '\n'
        else:
            nopara = starttime - lasttime
            if nopara // prodpara > 4:
                para = para + nopara // prodpara - 1
            else:
                para = para + nopara // prodpara
            raspis = raspis + str(para) + ' пара \n' + item['title'] + ' Время: ' + str(starttime)[:-3] + '-' + str(
                endtime)[:-3] + '\n'
            lasttime = starttime
    if len(raspis) <= 40:
        raspis = f'У {group_number.replace("%20", " ")} нет в занятий в этот день.'
        return raspis
    else:
        return raspis


schedule()