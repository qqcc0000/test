#!/usr/bin/python3
# -*- coding: UTF-8 -*-  

import time
import pyautogui as pag  
import tkinter


def get():
    po.delete(0,tkinter.END)  
    time.sleep(1) #几秒后返回位置
    x , y = pag.position()
    po.insert(0,str(x)+','+str(y))

root = tkinter.Tk()
tip = tkinter.Label(root,text="返回点击获取1s后的光标位置")
tip.grid(row=0)
po = tkinter.Entry(root)
po.grid(row=1)
do = tkinter.Button(root,text="获取",command=get)
#点击获取位置
do.grid(row=2)


root.mainloop()

