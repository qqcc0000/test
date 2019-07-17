#coding:utf-8 
from Tkinter import *  
from ScrolledText import ScrolledText
import threading  
import time  
from PIL import ImageTk,Image  
  
  
  
def count(i):  
     for k in range(1, 100+1):  
        text.insert(END,'第'+str(i)+'线程count:  '+str(k)+'\n')  
        time.sleep(0.001)  
            
  
def fun():  
    for i in range(1, 5+1):  
        th=threading.Thread(target=count,args=(i,))  
        th.setDaemon(True)#守护线程  
        th.start()  
    var.set('MDZZ')  
  
  
  
root=Tk()  
root.title('九日王朝')  #窗口标题  
root.geometry('+600+100')#窗口呈现位置  
text=ScrolledText(root,font=('微软雅黑',10),fg='blue')  
text.grid()  
button=Button(root,text='屠龙宝刀 点击就送',font=('微软雅黑',10),command=fun)  
button.grid()  
var=StringVar()#设置变量  
label=Label(root,font=('微软雅黑',10),fg='red',textvariable=var)  
label.grid()  
var.set('我不断的洗澡，油腻的师姐在哪里')  
image2 =Image.open(r'/home/q/1.png')  
background_image = ImageTk.PhotoImage(image2)  
textlabel=Label(root,image=background_image)  
textlabel.grid()  

root.mainloop()  

