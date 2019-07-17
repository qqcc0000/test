from tkinter import *
import time
import os

master = Tk()

canvas = Canvas(master, width=800, height=600,bg='pink')

canvas.pack()

img = PhotoImage(file="/home/q/图片/1.png")
canvas.create_image(5,5,anchor=NW,image=img)

while True:
	print("d")
	master.update()

	os.system('adb shell screencap -p /sdcard/1.png')
	os.system('adb pull /sdcard/1.png ~/')

	time.sleep(0.05)

	img = PhotoImage(file="/home/q/1.png")
	canvas.create_image(5,5,anchor=NW,image=img)

mainloop()
