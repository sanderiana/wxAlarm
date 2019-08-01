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
from wxalarmlib import repository
from operator import itemgetter


class AlarmDetailView(wx.Dialog):
    WINDOW_WIDTH = 370
    WINDOW_HEIGHT = 370

    def __init__(self, parent, element, close_event):
        self.title = None
        self.listctrl = None
        self.close_event = close_event
        self.element = element  # type: repository.AlarmElement
        self.InitializeComponents(parent)

    def ShowModal(self):
        self.SetWindowValue()
        super(AlarmDetailView, self).ShowModal()

    def InitializeComponents(self, parent):
        # ------------------------------------------------------------------
        # Layout

        # dialog
        title = "アラーム詳細"
        style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        size = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        wx.Dialog.__init__(self, parent=parent, title=title, size=size, style=style)

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
        button_exit = wx.Button(body_panel,  wx.ID_ANY, "戻る", size=(0, 50))
        div3_box.Add(button_exit, -1, wx.EXPAND)
        contents_vbox.Add(div3_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        # ------------------------------------------------------------------
        # ListCtrl

        listctrl.InsertColumn(0, "内容", format=wx.LIST_FORMAT_LEFT, width=270)
        listctrl.InsertColumn(1, "時刻", format=wx.LIST_FORMAT_CENTER)

        # ------------------------------------------------------------------
        # Event
        button_exit.Bind(wx.EVT_BUTTON, self.OnCloseWindow)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def SetWindowValue(self):
        element = self.element
        alert_title = element.GetTitle()
        self.title.SetLabelText(alert_title)

        table = element.GetElementsBy(element.FIELD_TIME)  # type: list
        sorted_table = sorted(table, key=itemgetter(element.FIELD_INDEX))

        for item in sorted_table:
            title = item[element.FIELD_TITLE]
            time = item[element.FIELD_TIME]
            index = item[element.FIELD_INDEX] - 1
            self.listctrl.InsertItem(index, title)
            self.listctrl.SetItem(index, 1, time)

    def OnCloseWindow(self, event):
        self.Unbind(wx.EVT_CLOSE)
        self.close_event(self)

