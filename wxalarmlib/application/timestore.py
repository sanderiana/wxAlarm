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
from wxalarmlib.application import *
from wxalarmlib.utils.time_util import change_delta
from wxalarmlib.repository import AlarmElement, AlarmStatusElement


class WxAlarmTimeStore:
    def __init__(self, data_store):
        # data store
        self.data_store = data_store

        # target
        self.element_list = {}
        self.today_alarm = None
        self.wake_up = None

    # ---------------------------------------------------------
    # Timer Target

    def GetTodayAlarm(self):
        return self.today_alarm

    def SetTodayAlarm(self, alarm):
        self.today_alarm = alarm.CreateStatus()
        self.today_alarm.StartEnable()

    # ---------------------------------------------------------
    # Timer Event

    def CheckAllStatus(self, top_window):
        print "alarm_event"
        alarm = self.today_alarm
        if alarm is None:
            return

        base_element = alarm.GetBaseElement()
        from wxalarmlib.views import AlarmNoticeView

        # select enable
        group_dict = {}
        for index, status_element in alarm.GetElementDict().items():
            group = status_element.GetFieldBy(AlarmElement.FIELD_GROUP)
            if status_element.IsEnable():
                group_dict[group] = status_element

        # notice
        for group, status_element in group_dict.items():
            now = datetime.datetime.now()

            status_text = status_element.GetStatusText()
            if not status_element.IsOverTime(now):
                print status_text + " -> YET TIME"
                continue

            view = AlarmNoticeView(top_window, base_element, status_element, None)
            view.ShowModal()
            opt = view.GetSelectOpt()
            print status_text + " -> IS OVER TIME -> " + opt[AlarmStatusElement.OPT_TITLE]
            if opt is not None:
                current_base = True
                self.AdjustStatus(base_element, status_element, opt, current_base)

    def SearchStatusBy(self, group_id, want_element_type):
        alarm = self.today_alarm
        for index, status_element in alarm.GetElementDict().items():
            group = status_element.GetFieldBy(AlarmElement.FIELD_GROUP)
            if group != group_id:
                continue

            element_type = status_element.GetFieldBy(AlarmElement.FIELD_ELEMENT_TYPE)
            if element_type != want_element_type:
                continue

            return status_element
        return None

    def AdjustStatus(self, base_element, status_element, opt, current_base):
        work_log = False
        opt_command = opt[AlarmStatusElement.OPT_COMMAND]

        # base_element.SearchStatusBy(1, 1)
        if opt_command == AlarmStatusElement.COMMAND_TYPE_START:
            # off enable
            status_element.SetSwitchTime()
            status_element.SetEnable(False)
            group = status_element.GetFieldBy(AlarmElement.FIELD_GROUP)

            # search group next
            next_status_element = \
                self.SearchStatusBy(group, AlarmElement.ELEMENT_TYPE_END)
            if next_status_element is not None:
                next_status_element.SetEnable(True)

            # write log
            self.writeWorkStartLog(status_element)

        elif opt_command == AlarmStatusElement.COMMAND_TYPE_CHANGE:
            # change delta time
            delta_time = opt[AlarmStatusElement.OPT_APPEND_TIME]
            status_element.AppendDeltaTime(delta_time, current_base)

        elif opt_command == AlarmStatusElement.COMMAND_TYPE_SNOOZE:
            # change delta time
            delta_time = opt[AlarmStatusElement.OPT_APPEND_TIME]
            status_element.AppendDeltaTime(delta_time, current_base)

        elif opt_command == AlarmStatusElement.COMMAND_TYPE_CANCEL:
            # off enable
            status_element.SetEnable(False)

        elif opt_command == AlarmStatusElement.COMMAND_TYPE_EXIT:
            # off enable
            status_element.SetSwitchTime()
            status_element.SetEnable(False)
            work_log = True

        elif opt_command == AlarmStatusElement.COMMAND_TYPE_STOP:
            # off enable
            status_element.SetEnable(False)

        # create work log
        if work_log:
            group = status_element.GetFieldBy(AlarmElement.FIELD_GROUP)
            start_status = self.SearchStatusBy(group, AlarmElement.ELEMENT_TYPE_START)
            exit_status = status_element
            self.writeWorkTermLog(start_status, exit_status)

        # write log
        self.writeAlarmLog(status_element, base_element, opt)

    def writeWorkStartLog(self, start_status):
        # write log
        mode = WxAlarmApp.LOG_APP_WORK
        start_comment = start_status.GetComment()

        log_work = {
            'date': datetime.datetime.now().strftime("%m/%d"),
            'work-name': start_status.GetStatusText(),
            'plan-start': start_status.GetBaseTime().strftime('%H:%M'),
            'real-start': start_status.GetSwitchTime().strftime('%H:%M'),
            'work-start-comment': start_comment,
        }
        # write log
        logger = self.data_store.GetLogger()
        logger.writeLog(mode, log_work)

    def writeWorkTermLog(self, start_status, exit_status):
        # write log
        mode = WxAlarmApp.LOG_APP_WORK
        plan_time = exit_status.GetBaseTime() - start_status.GetBaseTime()
        real_time = exit_status.GetSwitchTime() - start_status.GetSwitchTime()
        start_comment = start_status.GetComment()
        exit_comment = exit_status.GetComment()

        log_work = {
            'date': datetime.datetime.now().strftime("%m/%d"),
            'work-name': start_status.GetStatusText(),
            'plan-start': start_status.GetBaseTime().strftime('%H:%M'),
            'plan-exit': exit_status.GetBaseTime().strftime('%H:%M'),
            'plan-work-time': change_delta(plan_time),
            'real-start': start_status.GetSwitchTime().strftime('%H:%M'),
            'real-exit': exit_status.GetSwitchTime().strftime('%H:%M'),
            'real-work-time': change_delta(real_time),
            'work-start-comment': start_comment,
            'work-exit-comment': exit_comment,
        }
        # write log
        logger = self.data_store.GetLogger()
        logger.writeLog(mode, log_work)

    def writeAlarmLog(self, status_element, base_element, opt):
        # write log
        mode = WxAlarmApp.LOG_APP_ALARM
        total_delta = status_element.GetTotalDeltaTime()
        log_infor = {
            'model': base_element.GetTitle(),
            'status': status_element.GetStatusText(),
            'select': opt[AlarmStatusElement.OPT_TITLE],
            'current_time' : datetime.datetime.now().strftime("%Y/%m/%d %H:%M"),
            'base_time': status_element.GetBaseTime().strftime('%H:%M'),
            'delta_time': change_delta(total_delta)
        }
        # write log
        logger = self.data_store.GetLogger()
        logger.writeLog(mode, log_infor)

