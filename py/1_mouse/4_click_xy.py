from tkinter import *

app = Tk()

#通过event形参来获取对应事件描述
def callback(event): 
    print("当前位置：",event.x,event.y)

#创建框架，窗口尺寸
frame = Frame(app, width = 200, height = 200)
#frame.bind("<Motion>",callback)
frame.bind("<Button-1>",callback)
frame.bind("<Button-2>",callback)
frame.bind("<Button-3>",callback)
frame.pack()
#<Button-1>Button：表示鼠标的点击事件 “—”左边是事件本身，右边是事件描述
#1：表示左键 2：中间键的滚轮点击 3：右键

mainloop()

