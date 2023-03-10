# -*- coding:utf-8 -*-
import subprocess
import time
import tkinter.messagebox
from tkinter import messagebox
import os
import re
import win32api
import win32con


f = open("file_path.txt",encoding = "utf-8")
path = f.read()  # 要添加的exe路径
f.close()

print('file_path:'+ path)
# "注册到启动项"
try:
    runpath = "Software\Microsoft\Windows\CurrentVersion\Run"
    hKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, runpath, 0, win32con.KEY_SET_VALUE)
    # run = True
    # if run:
    #     win32api.RegSetValueEx(hKey, "MyTool", 0, win32con.REG_SZ, path)
    # else:
    #     win32api.RegDeleteValue(hKey, "MyTool")
    win32api.RegSetValueEx(hKey, "Select_Net", 0, win32con.REG_SZ, path)
    win32api.RegCloseKey(hKey)
except Exception as e:
    print('开机自启动变量加入注册表错误')
    print(e.args)


p = subprocess.run('ipconfig', stdout=subprocess.PIPE, universal_newlines=True)
print(p.stdout)
q =r'以太网适配器 (.*?):'
slotList1 = re.findall(q, p.stdout)
print(slotList1)
l =r'无线局域网适配器 (.*?):'
slotList2 = re.findall(l, p.stdout)
print(slotList2)
len1=len(slotList1)
netcard1={}
for i in range(len1):
    print(slotList1[i])
    netcard1[i] = slotList1[i]
    print(netcard1)

len2=len(slotList2)
netcard2={}
for i in range (len2):
    print(slotList2[i])
    netcard2[i] = slotList2[i]
    print(netcard2)

x_result_dict = {'x':""}

def send1():
    x = ""
    for j in cheakboxs:
        # 如果被勾选的话传回来的值为True
        # 如果没有被勾选的话传回来的值为False
        if cheakboxs[j].get():
            x = x + netcard1[j] + "\n"
    print('x:::::'+x)
    x_result_dict['x'] = x
    root.destroy()
    return x


# 创建主窗口
root = tkinter.Tk()
label = tkinter.Label(root, text="请选择使用的有线网卡", bg="lightyellow", fg="red", width=50)
label.grid(row=0)

cheakboxs = {}
for i in range(len(netcard1)):
    cheakboxs[i] = tkinter.BooleanVar()
    tkinter.Checkbutton(root,text=netcard1[i], variable=cheakboxs[i]).grid(row=i + 1, sticky=tkinter.W)

buttonOne = tkinter.Button(root, text="提交", width=10, command=send1)
buttonOne.grid(row=len(netcard1) + 1)
root.mainloop()

y_result_dict = {'y':""}
def send2():
    y = ""
    for j in cheakboxs:
        # 如果被勾选的话传回来的值为True
        # 如果没有被勾选的话传回来的值为False
        if cheakboxs[j].get():
            y = y + netcard2[j] + "\n"
    print('y::::'+y)
    y_result_dict['y'] = y
    root.destroy()
    return y

# 创建主窗口
root = tkinter.Tk()
label = tkinter.Label(root, text="请选择使用的无线网卡", bg="lightyellow", fg="red", width=50)
label.grid(row=0)

cheakboxs = {}
for i in range(len(netcard2)):
    cheakboxs[i] = tkinter.BooleanVar()
    # 只有被勾选才变为True
    tkinter.Checkbutton(root,text=netcard2[i], variable=cheakboxs[i]).grid(row=i + 1, sticky=tkinter.W)

buttonOne = tkinter.Button(root, text="提交", width=10, command=send2)
buttonOne.grid(row=len(netcard2) + 1)
root.mainloop()

def send3():
    #开始循环运行
    while True:
        x = x_result_dict['x']
        y = y_result_dict['y']
        cmd1 = 'netsh interface show interface {}'.format(x)
        print('cmd1:'+cmd1)
        a = subprocess.check_output(cmd1, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        ss=str(a)
        time.sleep(1)
        print("未连接有线网络")
        if (ss.find(u"已连接"))>0:
            print("已连接有线网络")
            cmd2 = 'netsh interface show interface {}'.format(y)
            print('cmd2:' + cmd2)
            a = subprocess.check_output(cmd2, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            ss1=str(a)
            if(ss1.find(u"已连接")) >0:
                print("已连接无线网络")
                messagebox.showinfo("警告", "发生双跨，即将禁用无线网卡")

                os.popen('netsh interface set interface {} admin=DISABLE'.format(y))  # 禁用无线网卡
        time.sleep(15)

# 创建主窗口
root = tkinter.Tk()
label = tkinter.Label(root, text="开始循环运行查询,轮询间隔15s", bg="lightyellow", fg="red", width=50)
label.grid(row=0)

buttonOne = tkinter.Button(root, text="提交", width=10, command=send3)
buttonOne.grid(row=50)
root.mainloop()
