import os
# 创建GUI窗口打开图像 并显示在窗口中
import time
import threading
from PIL import Image, ImageTk # 导入图像处理函数库
import tkinter as tk           # 导入GUI界面函数库

# 创建窗口 设定大小并命名
window = tk.Tk()
window.title('图像显示界面')
window.geometry('600x500')
global img_png           # 定义全局变量 图像的
global Img


var = tk.StringVar()    # 这时文字变量储存器


# 创建打开图像和显示图像函数
def Open_Img():
    global img_png
    var.set('已打开')
    Img = Image.open('/home/q/图片/1.png')
    img_png = ImageTk.PhotoImage(Img)



def _Show_Img():
    global img_png
    global Img
    while True:
        #lock.acquire()
        os.system('adb shell screencap -p /sdcard/1.png')
        os.system('adb pull /sdcard/1.png ~/')
        print('已打开')
        time.sleep(0.1)

        Img = Image.open('/home/q/1.png')
        img_png = ImageTk.PhotoImage(Img)
        label_Img = tk.Label(window, image=img_png)
        label_Img.pack()
        tk.update()
        print('tk.update')
        #lock.release()
        time.sleep(5)

        os.system('adb shell screencap -p /sdcard/1.png')
        os.system('adb pull /sdcard/1.png ~/')
        
        time.sleep(0.1)

        Img = Image.open('/home/q/1.png')
        img_png = ImageTk.PhotoImage(Img)
        label_Img = tk.Label(window, image=img_png)
        label_Img.pack()
        tk.update()


# 创建文本窗口，显示当前操作状态
Label_Show = tk.Label(window,
    textvariable=var,   # 使用 textvariable 替换 text, 因为这个可以变化
    bg='blue', font=('Arial', 12), width=15, height=2)
Label_Show.pack()
# 创建打开图像按钮
btn_Open = tk.Button(window,
    text='打开图像',      # 显示在按钮上的文字
    width=15, height=2,
    command=Open_Img)     # 点击按钮式执行的命令
btn_Open.pack()    # 按钮位置
# 创建显示图像按钮
btn_Show = tk.Button(window,
    text='显示图像',      # 显示在按钮上的文字
    width=15, height=2,
    command=_Show_Img)     # 点击按钮式执行的命令
btn_Show.pack()    # 按钮位置

# 创建锁
lock = threading.Lock()


try:
# 创建线程
#   t1 = threading.Thread( target=Open_Img )#, args=(lock, ) )
#   t2 = threading.Thread( target=Show_Img )#, args=(lock, ) )
#   t1.start()
#   t2.start()
#   print ("creat threading.Thread")
#   # 等待子进程执行完
#   t1.join()
#   t2.join()
   print("exit threading")
except:
   print ("Error: 无法启动线程")

while True:
        #lock.acquire()
        os.system('adb shell screencap -p /sdcard/1.png')
        os.system('adb pull /sdcard/1.png ~/')
        print('已打开')
        time.sleep(0.1)

        Img = Image.open('/home/q/1.png')
        img_png = ImageTk.PhotoImage(Img)
        label_Img = tk.Label(window, image=img_png)
        label_Img.pack()
        #tk.update_idletasks()
        tk.update()
        print('tk.update')
        #lock.release()
        time.sleep(5)

# 运行整体窗口
#window.mainloop()
print ("exit")
