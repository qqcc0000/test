#!/bin/bash
# 当Ctrl+c 清空屏幕再退出，见引用3
#trap "clear;exit" 2
# 翻一个新屏幕
clear
# 每秒刷新输出屏幕的端口统计结果
while [ true ]
do
    # 需要执行的功能命令，各写各的业务
    r1='+'
    r2='++'
    r3='+++'
    r4='++'
    r5='+'
    # echo输出特殊处理，见引用2
    echo -e $r1
    echo -e $r2
    echo -e $r3
    echo -e $r4
    echo -e $r5
    # 使用ASCI码控制光标定位回到第一行第一列，见引用1
    echo -ne "\033[1;1H"
    # 进程睡眠1秒
    sleep 1
    clear
done

