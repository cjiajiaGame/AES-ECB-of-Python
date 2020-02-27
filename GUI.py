#-*- coding: utf-8 -*-

import wx
import sys, os
import AES

APP_TITLE = u'AES进制转换器'
APP_ICON = 'Key.ico' # 请更换成你的icon

class mainFrame(wx.Frame):
    '''程序主窗口类，继承自wx.Frame'''
    
    def __init__(self):
        '''构造函数'''
        
        wx.Frame.__init__(self, None, -1, APP_TITLE, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        # 默认style是下列项的组合：wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN 
        self.panel = wx.Panel(self)
        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize((800, 600))
        self.ico = wx.Icon('key.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.ico)
        self.Center()
        
        # 以下可以添加各类控件
        self.data = wx.TextCtrl(self.panel,wx.ID_ANY, style=wx.TE_MULTILINE)
        self.locked_data = wx.TextCtrl(self.panel,wx.ID_ANY, style=wx.TE_MULTILINE)
        self.lock_button = wx.Button(self.panel, label=u"AES加密")
        self.lock_button.Bind(wx.EVT_BUTTON,self.lock_fun)
        self.unlock_button = wx.Button(self.panel, label=u"AES解密")
        self.unlock_button.Bind(wx.EVT_BUTTON, self.unlock_fun)
        self.KEY = wx.StaticText(self.panel, wx.ID_ANY, label="请输入密钥：")
        self.KEYS = wx.TextCtrl(self.panel, wx.ID_ANY)
        self.box = wx.BoxSizer()
        self.box.Add(self.lock_button, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        self.box.Add(self.KEY, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        self.box.Add(self.KEYS, proportion=3, flag=wx.EXPAND | wx.ALL, border=5)
        self.box.Add(self.unlock_button, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.data, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.box, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.locked_data, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        self.SetSizer(self.vbox)
    def lock_fun(self, event):
        try:
            data = self.data.GetValue()
            KEYS = self.KEYS.GetValue()
            if len(KEYS)%16 != 0:
                self.locked_data.SetValue("密钥长度应是16的倍数！")
                return
            if not KEYS.isalpha():
                self.locked_data.SetValue("密钥只能是纯英文字符！")
                return
            locking = AES.PrpCrypt(self.KEYS.GetValue())
            self.locked_data.SetValue(locking.encrypt(self.data.GetValue()))
        except BaseException as f:
            self.locked_data.SetValue(str(f))
    def unlock_fun(self, event):
        try:
            locked_data = self.data.GetValue()
            KEYS = self.KEYS.GetValue()
            if len(KEYS)%16 != 0:
                self.locked_data.SetValue("密钥长度应是16的倍数！")
                return
            if not KEYS.isalpha():
                self.locked_data.SetValue("密钥只能是纯英文字符！")
                return
            locking = AES.PrpCrypt(self.KEYS.GetValue())
            self.locked_data.SetValue(locking.decrypt(self.data.GetValue()))
        except ValueError as f:
            self.locked_data.SetValue("加密以后的字符串不带英文的！\n" + str(f))
        except BaseException as f:
            self.locked_data.SetValue(str(f))
class mainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = mainFrame()
        self.Frame.Show()
        return True


app = mainApp(redirect=False)
app.MainLoop()
