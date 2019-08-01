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

import wx
from wxalarmlib.repository import AlarmElement, AlarmStatusElement


class AlarmChangeView(wx.Dialog):
    WINDOW_WIDTH = 370
    WINDOW_HEIGHT = 370

    def __init__(self, parent, status_element, close_event):
        # self.element = element
        self.status_element = status_element
        self.close_event = close_event

        self.title = None
        self.listctrl = None
        self.listItem = {}
        self.selectOpt = None

        self.InitializeComponents(parent)
        self.SetWindowValue()

    def GetSelectOpt(self):
        return self.selectOpt

    def ShowModal(self):
        super(AlarmChangeView, self).ShowModal()

    def InitializeComponents(self, parent):
        # ------------------------------------------------------------------
        # Layout

        # dialog
        title = "アラーム変更"
        style = (wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT)\
                & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        size = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        wx.Dialog.__init__(self, parent=parent, title=title, size=size, style=style)
        self.CenterOnScreen()

        # base layout
        body_panel = wx.Panel(self, wx.ID_ANY)
        contents_vbox = wx.BoxSizer(wx.VERTICAL)
        body_panel.SetSizer(contents_vbox)

        # 1段目
        div1_hbox = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(body_panel, wx.ID_ANY, style=wx.ALIGN_CENTER)
        div1_hbox.Add(title, -1, wx.EXPAND)
        contents_vbox.Add(div1_hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, 15)
        self.title = title

        # 2段目
        div2_box = wx.BoxSizer(wx.HORIZONTAL)
        listctrl = wx.ListCtrl(body_panel, wx.ID_ANY, style=wx.LC_REPORT)
        div2_box.Add(listctrl, -1, wx.EXPAND)
        contents_vbox.Add(div2_box, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        self.listctrl = listctrl

        # 3段目
        div3_box = wx.BoxSizer(wx.HORIZONTAL)
        button_run = wx.Button(body_panel,  wx.ID_ANY, "実行", size=(0, 50))
        div3_box.Add(button_run, -1, wx.EXPAND)
        contents_vbox.Add(div3_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        # ------------------------------------------------------------------
        # ListCtrl
        listctrl.InsertColumn(0, "変更内容", wx.LIST_FORMAT_LEFT, 350)

        # ------------------------------------------------------------------
        # Event
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        button_run.Bind(wx.EVT_BUTTON, self.OnClickOption)

    def GetWindowSize(self):
        min_w = 200 * 4
        min_h = 200 * 3
        return min_w, min_h

    def OnClickOption(self, event):
        select_index = self.listctrl.GetFirstSelected()
        if select_index == -1:
            style = wx.OK | wx.ICON_EXCLAMATION
            title = '変更選択'
            message = "変更内容を選択してください"
            dialog = wx.MessageDialog(None, message, title, style=style)
            dialog.ShowModal()
            dialog.Destroy()
            return

        # selected item
        opt = self.listItem[select_index]

        # message box
        title = '選択'
        opt_title = AlarmStatusElement.OPT_TITLE
        opt_command = AlarmStatusElement.OPT_COMMAND
        message = "「%s」に作業を変更しますか？" % opt[opt_title].strip()

        if opt[opt_command] == 'start' or opt[opt_command] == 'exit':
            dialog = wx.TextEntryDialog(None, message, title)

        else:
            style = wx.YES_NO
            dialog = wx.MessageDialog(None, message, title, style=style)

        # after message
        res = dialog.ShowModal()
        if res == wx.ID_YES or res == wx.ID_OK:
            if isinstance(dialog, wx.TextEntryDialog):
                self.status_element.SetComment(dialog.GetValue())

            self.selectOpt = opt
            self.Unbind(wx.EVT_CLOSE)
            self.Close()
        dialog.Destroy()

    def SetWindowValue(self):
        # const
        append_time = AlarmStatusElement.OPT_APPEND_TIME
        index = AlarmStatusElement.OPT_INDEX
        opt_title = AlarmStatusElement.OPT_TITLE

        # entity
        status_element = self.status_element

        # title
        title = status_element.GetStatusText()
        base_time = status_element.GetFieldBy(AlarmElement.FIELD_TIME)
        time = base_time
        text = "「" + title + " (" + time + ")」の変更です。"
        self.title.SetLabelText(text)

        # link to section
        link = status_element.GetFieldBy(AlarmElement.FIELD_LINK)
        element = status_element.GetBaseElement()
        section = element.GetLinkByName(link)

        # judge time
        judge_time = status_element.JudgeForChange()
        options = section.GetElementsBy(judge_time)

        # sort
        options.sort(key=lambda x: x.get(index, x.get(append_time, 0)))

        # create option
        idx = 0
        for opt in options:
            # set window
            line = opt[opt_title].strip()
            self.listctrl.InsertItem(idx, line)
            self.listItem[idx] = opt
            idx += 1

    def OnCloseWindow(self, event):
        # after message
        self.Unbind(wx.EVT_CLOSE)
        self.Close()
