from tkinter import *
import os
import time

app = Tk()

xx = -1
yy = -1

def x_y(x1,y1):
	global xx
	global yy
	xx = x1
	yy = y1
	print('=',xx,yy)

#通过event形参来获取对应事件描述
def callback(event): 
	x_y(event.x,event.y)
	print("当前位置：",event.x,event.y)

#创建框架，窗口尺寸
frame = Frame(app, width = 400, height = 600)
#frame.bind("<Motion>",callback)
frame.bind("<Button-1>",callback)
frame.bind("<Button-2>",callback)
frame.bind("<Button-3>",callback)
frame.pack()
#<Button-1>Button：表示鼠标的点击事件 “—”左边是事件本身，右边是事件描述
#1：表示左键 2：中间键的滚轮点击 3：右键

s0 = 'adb shell \"sendevent /dev/input/event1 1 330 1;'
s1 = 'sendevent /dev/input/event1 3 53 '
s2 = 'sendevent /dev/input/event1 3 54 '
s3 = 'sendevent /dev/input/event1 0 0 0;'
s4 = 'sendevent /dev/input/event1 1 330 0;\"'

ox = 0
oy = 0

while True:
	global xx
	global yy
	sx = s1 + str(xx) + ';'
	sy = s2 + str(yy) + ';'

	#print(sx,ox)
	#print(sy,oy)
	ss = s0 + sx + sy + s3 + s4 +s3
	#print('========',ss)
	if ox != xx or oy != yy :
		os.system(ss)
		time.sleep(0.05)
		ox = xx
		oy = yy
	#print()
	#print()


	#os.system('adb shell sendevent /dev/input/event0 3 0 40')
	#os.system('adb shell sendevent /dev/input/event0 3 1 210')
	#os.system('adb shell sendevent /dev/input/event0 1 330 1')
	#os.system('adb shell sendevent /dev/input/event0 0 0 0')
	#os.system('adb shell sendevent /dev/input/event0 1 330 0')
	#os.system('adb shell sendevent /dev/input/event0 0 0 0')
	time.sleep(0.05)
	app.update()

mainloop()





#adb shell sendevent /dev/input/event0 3 35 40
#adb shell sendevent /dev/input/event0 3 36 210
#adb shell sendevent /dev/input/event0 1 330 1 //touch
#adb shell sendevent /dev/input/event0 0 0 0 //it must have
#adb shell sendevent /dev/input/event0 1 330 0 //untouch
#adb shell sendevent /dev/input/event0 0 0 0 //it must have
