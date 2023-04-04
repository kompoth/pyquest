# Temporary dummies to emulate interaction with database
import datetime as dt

import config

def check_timer():
    # tmp dummy to send reminders to admins on 20:00.
    # TODO: get a list of users to be reminded
    
    cur_dttm = dt.datetime.now()
    shedule_dttm = dt.datetime.combine(cur_dttm, dt.time(20, 0, 0))
    delta_tm = dt.timedelta(minutes=config.get_value('period'))
    next_dttm = shedule_dttm + delta_tm
    if shedule_dttm <= cur_dttm < next_dttm:
        return config.get_value('admins') 
    else:
        return []
