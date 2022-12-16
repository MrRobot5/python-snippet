
from datetime import date
import time

today = date.today()

for x in range(0, 30 * 12):

    # Formatting datetime
    suffix = today.strftime("%Y%m%d")
    print("request day:", suffix)
    if today.day == 1:
        today = today.replace(month=today.month - 1, day=30)
    today = today.replace(day=today.day - 1)


