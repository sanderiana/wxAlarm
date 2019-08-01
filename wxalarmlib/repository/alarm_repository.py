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

from wxalarmlib.utils import *
from wxalarmlib.repository import BaseRepository, BaseElement, BaseStatus, BaseStatusElement


class AlarmStatusElement(BaseStatusElement):
    TIME_TYPE_BEFORE = 'before'
    TIME_TYPE_JUST = 'just'
    TIME_TYPE_SNOOZE = 'snooze'
    OPT_APPEND_TIME = 'append_time'
    OPT_TITLE = 'title'
    OPT_INDEX = 'index'
    OPT_COMMAND = 'command'
    COMMAND_TYPE_START = 'start'
    COMMAND_TYPE_CHANGE = 'change'
    COMMAND_TYPE_CANCEL = 'cancel'
    COMMAND_TYPE_SNOOZE = 'snooze'
    COMMAND_TYPE_STOP = 'stop'
    COMMAND_TYPE_EXIT = 'exit'

    def __init__(self, fields, base_element):
        super(AlarmStatusElement, self).__init__(fields, base_element)

        # pp(self.GetFieldBy(base_element.FIELD_TIME))
        base_time = change_time(self.GetFieldBy(base_element.FIELD_TIME))
        self.time_info = base_time
        self.base_time = base_time
        self.link_name = self.GetFieldBy(base_element.FIELD_LINK)
        self.is_enable = False
        self.pass_just = False
        self.switch_time = None
        self.comment = ""
        self.delta_time = datetime.timedelta(minutes=0)

    def SetComment(self, comment):
        self.comment = comment

    def GetComment(self):
        return self.comment

    def SetSwitchTime(self):
        self.switch_time = datetime.datetime.now()

    def GetSwitchTime(self):
        return self.switch_time

    def GetBaseTime(self):
        return self.base_time

    def GetAlarmTime(self):
        return self.time_info

    def GetTotalDeltaTime(self):
        return self.delta_time

    def AppendDeltaTime(self, minutues, current_base):
        delta_time = datetime.timedelta(minutes=minutues)
        if current_base:
            now = datetime.datetime.now()
            base_diff = now - self.time_info
            delta_time = base_diff + delta_time

        self.delta_time += delta_time
        self.time_info += delta_time

    def IsOverTime(self, date_time):
        return self.time_info <= date_time

    def SetEnable(self, enable):
        self.is_enable = enable

    def IsEnable(self):
        return self.is_enable

    def GetSelectionElement(self):
        return self.GetBaseElement().GetLinkByName(self.link_name)

    def GetStatusText(self):
        return self.GetFieldBy(AlarmElement.FIELD_TITLE)

    def JudgeForChange(self):
        # 一回でもジャスト状態を迎えたものは、スヌーズ
        if self.pass_just:
            return self.TIME_TYPE_SNOOZE

        # それ以外は、ビフォア
        return self.TIME_TYPE_BEFORE

    def JudgeTime(self, current_time=None):
        # current time
        current_time = current_time if current_time is not None else datetime.datetime.now()

        # 一回でもジャスト状態を迎えたものは、スヌーズ
        if self.pass_just:
            return self.TIME_TYPE_SNOOZE

        # 基準時間を超えて、ジャスト状態を迎えてないものは、ジャスト
        elif current_time > self.time_info:
            self.pass_just = True
            return self.TIME_TYPE_JUST

        # それ以外は、ビフォア
        return self.TIME_TYPE_BEFORE


class AlarmStatus(BaseStatus):
    def __init__(self, alarm_element):
        self.wake_up = False
        super(AlarmStatus, self).__init__(alarm_element)

    def StartEnable(self):
        # grouping [group][time]
        group_dict = {}
        for index, status_element in self.GetElementDict().items():
            group = status_element.GetFieldBy(AlarmElement.FIELD_GROUP)
            if not group in group_dict:
                group_dict[group] = {}

            time = status_element.GetFieldBy(AlarmElement.FIELD_TIME)
            element_type = status_element.GetFieldBy(AlarmElement.FIELD_ELEMENT_TYPE)
            if element_type == AlarmElement.ELEMENT_TYPE_START:
                group_dict[group][time] = status_element

        # set enable
        for group, group_time in group_dict.items():
            for time, element in group_time.items():
                element.SetEnable(True)
                break


class AlarmElement(BaseElement):
    INI_TYPE_TIME_TABLE = 'time_table'
    INI_TYPE_TIME_START = 'start'
    INI_TYPE_TIME_EXIT = 'exit'
    FIELD_INDEX = 'index'
    FIELD_TITLE = 'title'
    FIELD_GROUP = 'group'
    FIELD_TIME = 'time'
    FIELD_LINK = 'link'
    FIELD_ELEMENT_TYPE = 'element_type'
    ELEMENT_TYPE_END = 'end'
    ELEMENT_TYPE_START = 'start'

    def __init__(self, name, dicts):
        super(AlarmElement, self).__init__(name, dicts)
        section_type = self.GetSectionType()

        try:
            if section_type == self.INI_TYPE_TIME_TABLE:
                self.SetAsTimeTable(dicts)

            elif section_type == self.INI_TYPE_TIME_START:
                self.SetAsStart(dicts)

            elif section_type == self.INI_TYPE_TIME_EXIT:
                self.SetAsExit(dicts)

            else:
                raise Exception(None)
        except Exception, e:
            error = {
                'name': name,
                'type': section_type,
                'detail': e.message,
            }
            message = 'Type "{type}" of section "{name}" is not accept '
            message += 'because of {detail}.'
            raise Exception(message.format(**error))

    # ---------------------------------------------------------
    # create status list

    def CreateStatus(self):
        # check type: time table only
        element_type = self.GetSectionType()
        if element_type != self.INI_TYPE_TIME_TABLE:
            err = {'type': element_type}
            message = "{type} is not support as status." % err
            raise Exception(message)

        ret = AlarmStatus(self)
        for one in self.GetElementsBy(self.FIELD_TIME):
            index = one[self.FIELD_INDEX]
            status = AlarmStatusElement(one, self)
            ret.AppendElement(index, status)

        return ret

    # ---------------------------------------------------------
    # create choice

    def SetAsTimeTable(self, dicts):
        ignore = ['title', 'type', 'index']

        for key_text, val_text in dicts.items():
            if key_text in ignore:
                continue

            key_list = key_text.split(self.INI_KEY_SPLIT)
            val_list = val_text.split(self.INI_VALUE_SPLIT)

            one = {
                self.FIELD_INDEX: int(key_list[1]),
                self.FIELD_TIME: val_list[0].strip(),
                self.FIELD_ELEMENT_TYPE: val_list[1].strip(),
                self.FIELD_GROUP: int(val_list[2]),
                self.FIELD_TITLE: val_list[3].strip(),
                self.FIELD_LINK: val_list[4].strip()
            }
            self.SetNeedList(val_list[4])
            self.AppendElementType(self.FIELD_TIME, one)

    def SetAsStart(self, dicts):
        # map_infor = {
        #     'before': ['change', 'start',  'cancel'],
        #     'just':   ['start',  'snooze', 'cancel'],
        #     'snooze': ['start',  'snooze', 'cancel']}
        ignore = ['title', 'type']
        for key_text, val_text in dicts.items():
            if key_text in ignore:
                continue

            key_list = key_text.split(self.INI_KEY_SPLIT)
            val_list = val_text.split(self.INI_VALUE_SPLIT)
            judge = key_list[0].strip()
            one = {
                'time_flag': judge,
                'command': key_list[1].strip(),
                self.FIELD_INDEX: int(key_list[2]) if (2 < len(key_list)) else 1,
                self.FIELD_TITLE: val_list[0],
                'append_time': int(val_list[1]) if (1 < len(val_list)) else 0
            }
            self.AppendElementType(judge, one)

    def SetAsExit(self, dicts):
        # map_infor = {
        #     'before':  ['stop', 'change'],
        #     'just':    ['stop', 'snooze'],
        #     'snooze':  ['stop', 'snooze']}
        ignore = ['title', 'type']
        for key_text, val_text in dicts.items():
            if key_text in ignore:
                continue

            key_list = key_text.split(self.INI_KEY_SPLIT)
            val_list = val_text.split(self.INI_VALUE_SPLIT)
            judge = key_list[0].strip()
            one = {
                'time_flag': key_list[0].strip(),
                'command': key_list[1].strip(),
                self.FIELD_INDEX: key_list[2] if (2 < len(key_list)) else 1,
                self.FIELD_TITLE: val_list[0],
                'append_time': int(val_list[1]) if (1 < len(val_list)) else 0
            }
            self.AppendElementType(judge, one)


class AlarmRepository(BaseRepository):
    def __init__(self, filepath):
        super(AlarmRepository, self).__init__(filepath)

    def ConvertElement(self, name, dicts):
        return AlarmElement(name, dicts)
