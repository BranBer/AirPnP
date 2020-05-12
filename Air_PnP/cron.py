from Air_PnP.models import *
from datetime import datetime

def clear_users_today():
    week_day_today = datetime.today().weekday()
    week_day = ''

    if (week_day_today == 6):
        week_day = 'Sunday'
    if (week_day_today == 0):
        week_day = 'Monday'
    if (week_day_today == 1):
        week_day = 'Tuesday'
    if (week_day_today == 2):
        week_day = 'Wednesday'
    if (week_day_today == 3):
        week_day = 'Thursday'
    if (week_day_today == 4):
        week_day = 'Friday'
    if (week_day_today == 5):
        week_day = 'Saturday'

    days = DayAvailable.objects.filter(week_day = week_day).values('id')
    times = TimesAvailable.objects.filter(week_day__in = days)

    for t in times:
        if (datetime.now().time() >= t.close_time):
            t.relations.clear()
        