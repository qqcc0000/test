import os

s1 = 'adb shell sendevent /dev/input/event1 3 53 395'
s2 = 'adb shell sendevent /dev/input/event1 3 54 657'
os.system(s1)
os.system(s2)
os.system('adb shell sendevent /dev/input/event1 1 330 1')
os.system('adb shell "sendevent /dev/input/event1 0 0 0;\
	sendevent /dev/input/event1 1 330 0;\
	sendevent /dev/input/event1 0 0 0"')

#os.system('adb shell sendevent /dev/input/event1 0 0 0;adb shell sendevent /dev/input/event1 1 330 0;adb shell sendevent /dev/input/event1 0 0 0')

#os.system('adb shell sendevent /dev/input/event1 1 330 0')
#os.system('adb shell sendevent /dev/input/event1 0 0 0')



#os.system('adb shell sendevent /dev/input/event1 1 330 1')
#os.system('adb shell sendevent /dev/input/event1 3 57 1')
#os.system('adb shell sendevent /dev/input/event1 3 53 395')
#os.system('adb shell sendevent /dev/input/event1 3 54 657')
#os.system('adb shell sendevent /dev/input/event1 3 58 32')
#os.system('adb shell sendevent /dev/input/event1 3 48 32')
#os.system('adb shell sendevent /dev/input/event1 0 0 0')
#
#os.system('adb shell sendevent /dev/input/event1 1 330 0')
#os.system('adb shell sendevent /dev/input/event1 3 57 0xffffffff')
#os.system('adb shell sendevent /dev/input/event1 0 0 0')
