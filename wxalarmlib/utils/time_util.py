# -*- coding: utf-8 -*-

# ---------------------------------------------------------------
# wxalarm.py
#
# Copyright (c) 2019 sanderiana https://github.com/sanderiana
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
# ---------------------------------------------------------------
# Icon made by Freepik from www.flaticon.com
# ---------------------------------------------------------------

import datetime


def change_time(hour_min):
    date = datetime.datetime.now()
    year = date.year
    month = date.month
    day = date.day
    time = hour_min.split(":")
    hour = int(time[0])
    min = int(time[1])
    return datetime.datetime(year, month, day, hour, min, 0)


def change_delta(delta_time):
    sec = delta_time.total_seconds()
    hour = sec // 3600
    min = (sec - (hour * 3600)) // 60
    return "%02d:%02d" % (hour, min)