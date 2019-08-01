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

import ConfigParser
import wx


class Config:

    RESOURCE_DIR = "/resource/"
    CONFIG_DIR = "config/"
    INIT_INI = "init.ini"
    LOGGER_SECTION = "logger"
    LOGGER_DIR_KEY = "folder"
    INI_KEY = "ini"
    ALARM_SECTION = "alarm"

    def __init__(self, root_dir, process_id):
        self.root_dir = root_dir
        inifile = ConfigParser.SafeConfigParser()
        inifile.read(root_dir + self.CONFIG_DIR + self.INIT_INI)
        self.ini_file = inifile
        self.process_id = process_id

    def ReadAppIcon(self):
        icon = wx.Icon()
        icon_file = self.GetIconPath()
        icon_source = wx.Image(icon_file, wx.BITMAP_TYPE_PNG)
        icon.CopyFromBitmap(icon_source.ConvertToBitmap())
        return icon

    def GetProcessId(self):
        return self.process_id

    def GetRootDir(self):
        return self.root_dir

    def GetConfigDir(self):
        return self.root_dir + self.CONFIG_DIR

    def GetAlarmIni(self):
        config_dir = self.GetConfigDir()
        return config_dir + self.ReadIniData(self.ALARM_SECTION, self.INI_KEY)

    def GetIconPath(self):
        return self.root_dir + self.RESOURCE_DIR + 'wxalarm.png'

    def GetLogFolder(self):
        return self.ReadIniData(self.LOGGER_SECTION, self.LOGGER_DIR_KEY)

    def ReadIniData(self, section, key):
        try:
            return self.ini_file.get(section, key)
        except Exception, e:
            item = (section, key)
            print "logger section:%s, key:%s is not found at " \
                  + self.CONFIG_DIR + self.INIT_INI % item
            exit(-1)
