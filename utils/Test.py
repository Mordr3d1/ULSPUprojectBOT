import datetime

from datetime import date


d1 = date(2022, 9, 1)
d2 = datetime.date.today()
result = (d1-d2).days//7

print(result)