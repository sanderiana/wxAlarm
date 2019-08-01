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

import os
import json
from datetime import *


class Logger:
    APPEND_MODE = 'a'
    WEEK_NO_US = '%U'
    YEAR = '%Y'
    MONTH = '%m'
    DAY = '%d'
    FILE_LINE = '%Y-%m-%d %H:%M:%S'
    COLUMN_TIME = 'write-time'

    def __init__(self, log_dir):
        self.log_dir = log_dir

    def writeLog(self, mode, dicts=None):
        current = datetime.now()
        diff_day = current.weekday()

        week_start_date = current + timedelta(days=(-1 * diff_day))
        week_no = week_start_date.strftime(self.WEEK_NO_US)
        year = week_start_date.strftime(self.YEAR)
        month = week_start_date.strftime(self.MONTH)
        day = week_start_date.strftime(self.DAY)

        dirpath = self.log_dir + '/' + year + '/'
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        param = (week_no, month, day, mode)
        filepath = dirpath + ("week%s-%s%s-%s.json" % param)
        current_time_text = current.strftime(self.FILE_LINE)
        base = {self.COLUMN_TIME: current_time_text}
        if dicts is not None:
            base.update(dicts)

        line = json.dumps(base, ensure_ascii=False, sort_keys=True) + "\n"
        with open(filepath, self.APPEND_MODE) as file_res:
            file_res.write(line)



