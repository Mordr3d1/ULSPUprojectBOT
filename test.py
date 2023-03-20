import re
#Будет убирать повторения в одном дне

#Создаёт файл даты для сравнения
# Не обязательная функция
def compare():
    f = open('utils/timetable', 'r', encoding='utf-8')
    f2 = open('utils/withoutdate', 'w', encoding='utf-8')
    text = f.read(18)  #Ровное колличество символов первой строки, очень важно!
    f2.write(text)

def final_sort_day():
    dates_to_compare = open('utils/withoutdate', 'r')
    dates = dates_to_compare.readlines()

    dates_in_file = open('utils/timetable', 'r')
    file_dates = dates_in_file.readlines()

    sorted_day = open('utils/sortedday.txt', 'w')

    text = []

    a = 2
    b = 3
    c = 2

    for v in dates:
        for line in file_dates[0:6]:    # Строчка по умолчанию
            text.append(line)

        if dates[0] == file_dates[7] == file_dates[14]:
            text.append('\n')
            for line in file_dates[8:13]:
                text.append(line)

            while dates[0] == file_dates[7 * c]:
                c = c + 1

                text.append('\n')

                for line in file_dates[7*a+1:7*b-1]:
                    text.append(line)

                a = a + 1
                b = b + 1

            else:
                break
        if dates[0] == file_dates[7]:
            text.append('\n')
            for line in file_dates[8:13]:
                text.append(line)


    for line in text:
        sorted_day.write("%s" % line)




def sort_2_days():














#Мусорная тестовая функция
def test2():

    with open('utils/withoutdate', 'r', encoding='utf-8' ) as dates_to_compare:
        dates = dates_to_compare.readlines(1)

    with open('utils/timetable', 'r', encoding='utf-8') as dates_in_file:
        file_dates = dates_in_file.readlines()

    sorted_day =  open('utils/sortedday', 'w', encoding='utf-8')



    for v in dates:
        if v in file_dates:
            text = str(set(file_dates) - set(dates))
            text = str(dates) + text
            sorted_day.write(text)
            print('Работает')
            break
        else:
            print('Не работает')



# отсортировка даты на 1 день

def test3():
    dates_to_compare = open('utils/withoutdate', 'r', encoding='utf-8')
    dates = dates_to_compare.readlines(1)

    dates_in_file = open('utils/timetable', 'r', encoding='utf-8')

    file_dates = dates_in_file.readlines()

    sorted_day =  open('utils/sortedday.txt', 'w', encoding='utf-8')

    text = []
    a = 2
    b = 3

    for v in dates:
        if v in file_dates[0]:

            sorted_day.write(str(file_dates[0:6]))
            sorted_day.write('\n')
            if v in file_dates[7]:
                sorted_day.write('\n')
                sorted_day.write(str(file_dates[8:13]))
                sorted_day.write('\n')
                while  v in file_dates[7*a]:
                    sorted_day.write('\n')
                    sorted_day.write(str(file_dates[7*a+1:7*b-1]))
                    a = a + 1
                    b = b + 1
                    sorted_day.write('\n')

            else:
                break








# Тест фильтра и создание отдельного файла
def sorttest_1():
    with open('utils/sortedday.txt', 'r', encoding='utf-8') as f:
        lines = f.read()
    f2 = open('utils/teststr.txt', 'w', encoding='utf-8')


    regex = '\w+\S*\D+..+:+..'

    list = re.findall(regex,  lines)

    regex = '.n....'

    list = re.sub(regex, ' ', lines)


    print(list)

    f2.write(list)


# Фильтрация мусора
def sort_normal():
    file = open('utils/teststr.txt', 'r', encoding='utf-8')
    read = file.readlines()
    modified = []

    for line in read:
        modified.append(line.strip())

    print(modified)



# Попытка сортировки
def sort_normal2():
    file = open('utils/teststr.txt', 'r', encoding='utf-8')
    read = file.readlines()
    modified = []

    for line in read:
        if line[-1] == '':
            modified.append('\n')
            modified.append(line[:-1])

    print(modified)

# Создание того же списка

def sorted_data():
    strings = ('Дата:','Расположение:','Время:','Предмет:', 'Тип:')
    newlines = []

    with open('utils/teststr.txt') as f:
        try:
            for line in f:
                if any(s in line for s in strings):
                    newlines.append('\n')
                    newlines.append(line)

        except:
            pass

    f.close()

    theFile = open('utils/testsrtfin.txt', 'w')
    for line in newlines:
        theFile.write(line)
    theFile.close()


# Сортировка тест
def sort_normal3():
    file = open('utils/sortedday.txt', 'r', encoding='utf-8')
    theFile = open('utils/testsrtfin.txt', 'w')

    read = file.readlines()
    modified = []

    for line in read:
        what_need = line.split('\n')
        modified.append(what_need)


    print(modified)
    #for line in read:
        #theFile.write(f"{line}\n")

# Создание json файла Тест



'''def jsontest():
    filename = 'utils/teststr.txt'

    dict1 = {}
    with open(filename) as fh:
	    for line in fh:

		    command, description = line.strip().split(None, 1)

		    dict1[command] = description.strip()

    out_file = open("test1.json", "w")
    json.dump(dict1, out_file, indent = 4, sort_keys = False)
    out_file.close()'''


