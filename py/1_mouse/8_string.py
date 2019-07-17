str_1 = "aaa"
str_2 = "bbbb"

#1
print(str_1 + str_2)
#aaabbbb


#2
print(str_1,str_2)
#aaa bbbb

print('aa','bb')
#aa bb

#3
print('aa''bb')
#aabb


#4
print('%s-%s' % (str_1,str_2))
#aaa-bbbb
print('%s-%s' % ('aa','bb'))
#aa-bb

#5
data = ['wbz','ctt','Python']
str_0 = '@@@'
str_3 = '111'
print(str_0)
print(data)
print(str_0.join(data))
print(str_3.join('00000'))
#@@@
#['wbz', 'ctt', 'Python']
#wbz@@@ctt@@@Python
#01110111011101110


#6
str_0 = 'Python'
print(str_0 * 2)
#PythonPython

#7
n4 = 100
str_4 = 'adb shell sendevent /dev/input/event0 3 0 '
sn4 = 'adb shell sendevent /dev/input/event0 3 0 ' + str(n4)
print(sn4)


