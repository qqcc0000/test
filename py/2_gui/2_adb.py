import os
import re


os.system('adb version')
os.system('adb devices') #os.system是不支持读取操作的
out = os.popen('adb shell "dumpsys activity | grep "mFocusedActivity""').read() #os.popen支持读取操作
print(out)

#下面的代码是获取当前窗口的component参数
def getFocusedPackageAndActivity():

        pattern = re.compile(r"[a-zA-Z0-9\.]+/[a-zA-Z0-9\.]+") #这里使用了正则表达式，对输出的内容做了限制，只会显示类似"com.mediatek.factorymode/com.mediatek.factorymode.FactoryMode"的字符串
        out = os.popen("adb shell dumpsys window windows ").read() #window下使用findstr
        list = pattern.findall(out)
        component = list[0] #输出列表中的第一条字符串

        return component
print(getFocusedPackageAndActivity())
