import datetime

from datetime import date


d1 = date(2022, 9, 1)
d2 = date(2023, 9, 1)
#d2 = datetime.date.today()
result = (d1 - d2).days//7

result = result * (-1)

if result == 53:

print(result)

