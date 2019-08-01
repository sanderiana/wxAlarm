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

from wxalarmlib import utils, repository


class WxAlarmDataStore:
    def __init__(self, config):
        # ------------------------------------------------------
        # config logger
        self.config = config
        log_dir = config.GetLogFolder()
        self.logger = utils.Logger(log_dir)

        # ------------------------------------------------------
        # repository
        alarm_ini = config.GetAlarmIni()
        self.alarm_repo = repository.AlarmRepository(alarm_ini)

        # ------------------------------------------------------
        # timer
        from wxalarmlib.application import WxAlarmTimeStore
        self.timer_store = WxAlarmTimeStore(self)

    def GetAlarmRepo(self):
        return self.alarm_repo

    def GetTimerStore(self):
        return self.timer_store

    def GetLogger(self):
        return self.logger

    def GetConfig(self):
        return self.config
