import json, datetime

from requests import get

#проверка введенных данных
def group(group_number):
    req = get('https://raspi.ulspu.ru/json/dashboard/groups')
    grsp = json.loads(req.text)
    for item in grsp['rows']:
        if group_number == item:
            return group_number
    else:
        return None

#день недели
def day_week(day):
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

#список с распианием
def group_list_schedule(group_number, day):
    group_number = group_number.replace(' ', '%20')
    day = datetime.datetime.strptime(str(day), "%Y-%m-%d").date()
    req = get(f"https://raspi.ulspu.ru/json/dashboard/events?mode=group&value={group_number}")

    raw_schedudle = json.loads(req.text)
    raw_raspisanie = []
    for item in raw_schedudle['data']:
        dayrspis = datetime.datetime.strptime(item['start'], "%Y-%m-%dT%H:%M:%S.%fZ").date()
        if day == dayrspis:
            raw_raspisanie.append(item)
    return sorted(raw_raspisanie, key=lambda x: datetime.datetime.strptime(x['start'], "%Y-%m-%dT%H:%M:%S.%fZ").time())


def split_title(rlist):
    for item in rlist:
        hlp1=item['title'].split(' - ')
        hlp2=hlp1[2].split(' (')
        hlp2[1]=hlp2[1].replace(')',' ')
        for i in hlp2:
            hlp1.append(i)
        hlp1.pop(2)
        item['title']=hlp1
    return rlist

def format_title(rlist):
    rlist=split_title(rlist)
    for item in rlist:
        item['title'] = '*Дисциплина:* '+ item['title'][0] + ' \n*Тип занятия:* '+ item['title'][1] + ' \n*Преподаватель:*' + item['title'][2] + ' \n*Аудитория:* ' + item['title'][3]
    return rlist


#Вид даты
def date_revers_date(date):
    date = str(date)
    date = date.split('-')
    date[0], date[2] = date[2], date[0]
    return date[0] + '.' + date[1] + '.' + date[2]


def schedule(group_number, day):
    raspis = ['*Расписание на ' + date_revers_date(day) + ' ' + day_week(str(day)) + ':*\n\n']
    rawraspis = group_list_schedule(group_number, str(day))
    date = str(day)
    day = date_revers_date(day)
    para = 1
    prodpara = datetime.timedelta(hours=1, minutes=30)
    lasttime = datetime.timedelta(hours=8, minutes=30)
    nopara = ''
    rawraspis = format_title(rawraspis)
    for item in rawraspis:
        startt = datetime.datetime.strptime(item['start'], "%Y-%m-%dT%H:%M:%S.%fZ").time()
        starttime = datetime.timedelta(hours=startt.hour, minutes=startt.minute, seconds=startt.second, microseconds=startt.microsecond) + datetime.timedelta(hours=4, minutes=0, seconds=0, microseconds=0)
        endt = datetime.datetime.strptime(item['end'], "%Y-%m-%dT%H:%M:%S.%fZ").time()
        endtime = datetime.timedelta(hours=endt.hour, minutes=endt.minute, seconds=endt.second, microseconds=endt.microsecond) + datetime.timedelta(hours=4, minutes=0, seconds=0, microseconds=0)
        if starttime == lasttime:
            raspis.append(item['title'] + ' \n*Время:* ' + str(starttime)[:-3] + '-' + str(endtime)[:-3] + '\n \n')
        else:
            nopara = starttime - lasttime
            if nopara // prodpara > 4:
                para = para + nopara // prodpara - 1
            else:
                para = para + nopara // prodpara
            raspis.append('*'+str(para) + ' пара* \n' + item['title'] + ' \n*Время:* ' + str(starttime)[:-3] + '-' + str(endtime)[:-3] + '\n \n')
            lasttime = starttime
    if len(raspis) <= 1:
        return [f'У {group_number.replace("%20", " ")} нет в занятий в {day}{day_week(date)}\n\n']
    else:
        return raspis


def this_week():
    return [datetime.datetime.today().isocalendar()[0], datetime.datetime.today().isocalendar()[1]]


def next_week():
    return [(datetime.datetime.today()+datetime.timedelta(weeks=1)).isocalendar()[0], (datetime.datetime.today()+datetime.timedelta(weeks=1)).isocalendar()[1]]


def week_date_list(nweek, nyear):
    nweek = str(nyear)+'-W'+str(nweek)
    weekDay = datetime.datetime.strptime(nweek + '-1', "%Y-W%W-%w").date()
    weekList = [weekDay]
    for i in range(1, 6):
        weekDay += datetime.timedelta(days=1)
        weekList.append(weekDay)
    return weekList


def gr_this_week_schedule(group_number):
    raspis = []
    week = week_date_list(this_week()[1], this_week()[0])
    for i in week:
        for x in schedule(group_number, i):
            raspis.append(x)
    return raspis


def gr_next_week_schedule(group_number):
    raspis = []
    week = week_date_list(next_week()[1], next_week()[0])
    for i in week:
        for x in schedule(group_number, i):
            raspis.append(x)
    return raspis

def gr_today_raspis(group_number):
    day = datetime.datetime.today().date()
    return schedule(group_number, day)


def gr_tomorrow_raspis(group_number):
    day = datetime.date.today() + datetime.timedelta(days=1)
    return schedule(group_number, day)