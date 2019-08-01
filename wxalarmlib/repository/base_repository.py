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


class BaseStatusElement(object):
    def __init__(self, fields, base_element):
        self.base_element = base_element
        self.fields = fields

    def GetFieldBy(self, field_name):
        return self.fields[field_name]

    def GetBaseElement(self):
        return self.base_element

    def GetStatusText(self):
        raise Exception("not implementation")


class BaseStatus(object):
    def __init__(self, base_element):
        self.element_dict = {}
        self.base_element = base_element

    def AppendElement(self, index, status_element):
        self.element_dict[index] = status_element

    def GetElementDict(self):
        return self.element_dict

    def GetBaseElement(self):
        return self.base_element

    def GetTitle(self):
        return self.base_element.GetTitle()

    def CheckAllStatus(self, param):
        pass


class BaseElement(object):
    INI_KEY_SPLIT = '-'
    INI_VALUE_SPLIT = ','
    INI_TITLE = 'title'
    INI_TYPE = 'type'
    INI_INDEX = 'index'

    def __init__(self, section_name, dicts):
        self.section_name = section_name
        self.section_type = dicts[self.INI_TYPE]
        self.title = dicts[self.INI_TITLE]
        self.dicts = dicts
        self.need_link = {}
        self.type_dict = {}

    # ---------------------------------------------------------
    # base property

    def GetTitle(self):
        return self.title

    def GetName(self):
        return self.section_name

    def GetSectionType(self):
        return self.section_type

    def GetByField(self, field_name):
        return self.dicts[field_name]

    # ---------------------------------------------------------
    # type infor

    def GetElementsBy(self, element_type):
        # pp(self.type_dict)
        # exit()
        return self.type_dict[element_type]

    def AppendElementType(self, element_type, table):
        if not element_type in self.type_dict:
            lists = []
            self.type_dict[element_type] = lists
        else:
            lists = self.type_dict[element_type]
        lists.append(table)

    # ---------------------------------------------------------
    # link

    def SetNeedList(self, name):
        self.need_link[name] = None

    def GetNeedLinkList(self):
        ret = []
        for key, value in self.need_link.items():
            if value is None:
                ret.append(key)
        return ret

    def SetLinkElement(self, section_name, element):
        self.need_link[section_name] = element

    def GetLinkByName(self, section_name):
        return self.need_link[section_name]


class BaseRepository(object):
    def __init__(self, filepath):
        self.inifile = ConfigParser.SafeConfigParser()
        self.filepath = filepath
        self.inifile.read(self.filepath)
        self.element_dict = self.CreateElementDicts()
        self.status_idx = 0
        self.status_dict = {}
        self.ConvertAll()

    # ---------------------------------------------------------
    # convert to object
    def ConvertAll(self):
        # convert to object
        for section in self.inifile.sections():
            dicts = {}
            options = self.inifile.options(section)
            for key in options:
                dicts[key] = self.inifile.get(section, key)

            element = self.ConvertElement(section, dicts)
            self.AppendElementTo(section, element)

        # repair link
        err_message = "link %{link_name} in section %{section} is not found"
        for key, element in self.element_dict.items():
            need_links = element.GetNeedLinkList()
            for section_name in need_links:
                target = self.GetElementByName(section_name)
                if target is None:
                    error = {'link_name': section_name, 'section': key}
                    raise Exception(err_message % error)
                element.SetLinkElement(section_name, target)

        return self.element_dict

    def CreateElementDicts(self):
        return {}

    def ConvertElement(self, section, dicts):
        return BaseElement(section, dicts)

    def AppendElementTo(self, section, element):
        self.element_dict[section] = element

    # ---------------------------------------------------------
    # for gui

    def GetListByType(self, section_type):
        ret = {}
        for section, element in self.element_dict.items():
            if element.GetSectionType() == section_type:
                ret[section] = element
        return ret

    def GetElementByName(self, section_name):
        return self.element_dict[section_name]
