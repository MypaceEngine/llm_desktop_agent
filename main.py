import os
import sys
import threading
import time
import tkinter as tk
from tkinter import *

import customtkinter
import flet
from PIL import Image, ImageTk
from pystray import Icon, Menu, MenuItem
from screeninfo import get_monitors
from tkinterdnd2 import *
from win11toast import toast

import subwindow

Title = "LLM Agent"
Width = 128
Height = 128


def createsTaskIcon():
    image = Image.open('./default.ico')
    menu = Menu(MenuItem('Quit', quit_app))
    return Icon(name=Title, icon=image, title=Title, menu=menu)


def showTaskTrayIcon():
    taskTrayIcon.run()


destroy_flag = False


def quit_app():
    global destroy_flag
    global rootDesktop
    destroy_flag = True
    # try:
    taskTrayIcon.stop()
    subWin.destroy()
    rootDesktop.quit()
    rootDesktop.destroy()
    
    # finally:
    # sys.exit()


def createDesktopWindow():

    # Modes: system (default), light, dark
    customtkinter.set_appearance_mode("dark")
    # Themes: blue (default), dark-blue, green
    customtkinter.set_default_color_theme("blue")
    # ディスプレイの情報取得
    for m in get_monitors():
        if m.is_primary:
            screenName = m.name
            dispWidth = m.width
            dispHeight = m.height

    # create CTk window like you do with the Tk window
    app = customtkinterPlus(dispWidth, dispHeight, screenName=screenName)

    return app


class customtkinterPlus(customtkinter.CTk, TkinterDnD.DnDWrapper):
    dispWidth = 0
    dispHeight = 0
    lastMove = 0

    def enter_bg(self, event):
        global rootDesktop
        rootDesktop.attributes("-alpha", 1)
        # マウスの座標を覚えておく
        mouse_x = event.x
        mouse_y = event.y

        if self.mouseLedtPushed:

            current = time.time()
            if (self.lastMove == 0):
                self.lastMove = current
            if (current-self.lastMove > 0.5):
                rootDesktop.geometry(str(Width)+"x"+str(Height)+"+" +
                                     str(int(rootDesktop.winfo_rootx()+mouse_x-(rootDesktop.winfo_width()/2)))+"+"+str(int(rootDesktop.winfo_rooty()+mouse_y-rootDesktop.winfo_width()/2)))
                rootDesktop.update()
        else:
            self.lastMove = 0

    def leave_bg(self, event):
        rootDesktop.attributes("-alpha", 0.35)

    def closeExec(self):
        rootDesktop.destroy()

    mouseLedtPushed = False
    mouseX_pushed = 0
    mouseY_pushed = 0

    def pushStartMouseLest(self, event):
        self.mouseX_pushed, self.mouseY_pushed = event.x, event.y

        self.mouseLedtPushed = True

    def pushEndMouseLest(self, event):
        if abs(self.mouseX_pushed-event.x) < 10 and abs(self.mouseY_pushed-event.y) < 10:
            self.closeExec()

        self.mouseLedtPushed = False

    def __init__(self, dispWidth, dispHeight, * args, **kwargs, ):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

        self.iconbitmap(default='./default.ico')

        self.title(Title)
        self.geometry(str(Width)+"x"+str(Height)+"+" +
                      str(dispWidth-Width)+"+"+str(dispHeight-Height-60))
        # Windowのバーを消す
        self.wm_overrideredirect(True)

        # 最前面にもっていく
        self.lift()
        self.attributes("-topmost", True)

        # 透明率設定
        self.attributes("-alpha", 0.5)

        self.bind('<Enter>', self.enter_bg)
        self.bind("<Motion>", self.enter_bg)
        self.bind("<Leave>", self.leave_bg)

        self.bind("<Button-1>", self.pushStartMouseLest)  # 左ボタンを押したとき
        self.bind("<ButtonRelease-1>", self.pushEndMouseLest)  # 左ボタンを離したとき

        # 画像読み込み
        img = Image.open("./hatsune.png")
        # 大きさ変更
        img = img.resize((128, 128))
        logo_image = ImageTk.PhotoImage(img, master=self,)

        button = customtkinter.CTkButton(self,
                                         text="",
                                         width=128,
                                         height=128,
                                         border_width=0,
                                         corner_radius=0,
                                         border_spacing=0,
                                         image=logo_image,
                                         # command=button_function
                                         )
        button.pack()

        def dropAny(event):
            if event.type == "CF_HDROP":
                print(event.data)
            else:
                print(event.data)

        entryWidget = customtkinter.CTkEntry(self)
        button.drop_target_register(DND_ALL)
        button.dnd_bind('<<Drop>>', dropAny)


taskTrayIcon: Icon = createsTaskIcon()
subWin = subwindow.SubWindow(Title)
rootDesktop = None
if __name__ == "__main__":
    thread1 = threading.Thread(target=showTaskTrayIcon, daemon=True)
    thread1.start()

    while True:
        if (destroy_flag):
            break
        rootDesktop = createDesktopWindow()
        rootDesktop.mainloop()
        if (destroy_flag):
            break
        flet.app(target=subWin.main, name=Title)
