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


def ListSchedule(group_number, day):
    prname = group_number.replace(' ', '%20')
    day = datetime.datetime.strptime(str(day), "%Y-%m-%d").date()
    req = get(f"https://raspi.ulspu.ru/json/dashboard/events?mode=group&value={group_number}")
    raw_schedudle = json.loads(req.text)
    raw_raspisanie = []
    for item in raw_schedudle['data']:
        dayrspis = datetime.datetime.strptime(item['start'], "%Y-%m-%dT%H:%M:%S.%fZ").date()
        if day == dayrspis:
            raw_raspisanie.append(item)
    return sorted(raw_raspisanie, key=lambda x: datetime.datetime.strptime(x['start'], "%Y-%m-%dT%H:%M:%S.%fZ").time())


def SplitTitle(rlist):
    for item in rlist:
        hlp1=item['title'].split(' - ')
        hlp2=hlp1[2].split(' (')
        hlp2[1]=hlp2[1].replace(')',' ')
        for i in hlp2:
            hlp1.append(i)
        hlp1.pop(2)
        item['title']=hlp1
    return rlist

def FormatTitle(rlist):
    rlist=SplitTitle((rlist))
    for item in rlist:
        item['title'] = '*Дисциплина:* '+ item['title'][0] + ' \n*Тип занятия:* '+ item['title'][1] + ' \n*Группа:*' + item['title'][2] + ' \n*Аудитория:* ' + item['title'][3]
    return rlist



def schedule(group_number, day):

    if day == 'Сегодня':
        day = datetime.date.today()

    elif day == 'Завтра':
        day = datetime.date.today()
        day = day + datetime.timedelta(days=1)


    if group_number:
        raspis = 'Расписание на ' + str(day) + ' ' + day_week(day) + '\n'
        para = 1
        prodpara = datetime.timedelta(hours=1, minutes=30)
        lasttime = datetime.timedelta(hours=8, minutes=30)
        nopara = ''
        rawraspis = ListSchedule(group_number, day)
        rawraspis = FormatTitle(rawraspis)
        for item in rawraspis:
            startt = datetime.datetime.strptime(item['start'], "%Y-%m-%dT%H:%M:%S.%fZ").time()
            starttime = datetime.timedelta(hours=startt.hour, minutes=startt.minute, seconds=startt.second,
                                           microseconds=startt.microsecond) + datetime.timedelta(hours=4, minutes=0,
                                                                                                 seconds=0,
                                                                                                 microseconds=0)
            endt = datetime.datetime.strptime(item['end'], "%Y-%m-%dT%H:%M:%S.%fZ").time()
            endtime = datetime.timedelta(hours=endt.hour, minutes=endt.minute, seconds=endt.second,
                                         microseconds=endt.microsecond) + datetime.timedelta(hours=4, minutes=0,
                                                                                             seconds=0, microseconds=0)
            if starttime == lasttime:
                raspis = raspis + item['title'] + ' \n*Время:* ' + str(starttime)[:-3] + '-' + str(endtime)[
                                                                                               :-3] + '\n \n'
            else:
                nopara = starttime - lasttime
                if nopara // prodpara > 4:
                    para = para + nopara // prodpara - 1
                else:
                    para = para + nopara // prodpara
                raspis = raspis + str(para) + ' пара \n' + item['title'] + ' \n*Время:* ' + str(starttime)[
                                                                                            :-3] + '-' + str(
                    endtime)[:-3] + '\n \n'
                lasttime = starttime
        if len(raspis) == 0:
            raspis = f'У {group_number.replace("%20", " ")} нет в занятий в этот день.'
            return raspis
        else:
            return raspis
    else:
        return 'На данного преподавателя нет расписания. Убедитесь, что правильно ввели фамилию и инициалы преподавателя. '