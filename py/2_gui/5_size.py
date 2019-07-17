# coding: utf8
# 获取指定图片的长和宽
from PIL import Image
img = Image.open("/home/q/图片/1.png")
print (img.size)
