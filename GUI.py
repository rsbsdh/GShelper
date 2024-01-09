from PIL import Image, ImageTk
import subprocess
import os
import ctypes
import sys


if getattr(sys, 'frozen', False):
    # 在可执行文件中
    script_path = sys.executable
else:
    # 在脚本中
    script_path = os.path.abspath(__file__)

path = os.path.dirname(script_path)


def start_program():
    try:
        subprocess.Popen(path + "/Borderless.exe")
        print("程序已启动！")
    except FileNotFoundError:
        print("找不到可执行文件！")




def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


import subprocess
import win32gui
import win32con

def start_main():
    if is_admin():
        try:
            # 将主程序设置为后台运行
            hWnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hWnd, win32con.SW_HIDE)

            # 启动外部程序
            subprocess.call([path + "/taskclick.exe"])
            print("程序已以管理员权限启动！")

            # 恢复主程序窗口
            win32gui.ShowWindow(hWnd, win32con.SW_SHOW)
        except FileNotFoundError:
            print("找不到可执行文件！")
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        print("程序正在请求以管理员权限运行，请允许。")



def start_map():
    try:
        subprocess.Popen(path + "/map.exe")
        print("程序已启动！")
    except FileNotFoundError:
        print("找不到可执行文件！")




import tkinter as tk
from tkinter import ttk

# 创建主窗口
window = tk.Tk()
window.geometry("960x600")
window.title("GUI正在施工中")

# 设置窗口样式
style = ttk.Style()
style.configure("My.TFrame", background="#e1e1e1")
window.configure(background="#e1e1e1")

# 创建一个文本框作为公告栏
text_box = tk.Text(window, height=15, width=80)
text_box.insert("1.0", """更新日志：\n
2023.12.29:增加鼠标初始检测功能,增加模拟鼠标点击,增加SSIM结构图形对比,增加圆形扫描区域完成,增加自动登录\n
2024.01.03:程序打包完成,增加屏幕分辨率,窗口分辨率检测,增加窗口活动化检测,增加全屏检测,适配2k分辨率,暂停自动登录\n
2024.01.07:修复了游戏按键滞后问题,编写GUI(未完成),新增无边框全屏程序(独立程序,预计日后并入GUI内),增加地图窗口缩放调整按键\n
2024.01.08:修改对话逻辑\n
2024.01.09::GUI功能初步完成,分离各功能模块以满足多样化需求,成功将功能并入GUI\n""")

text_box.configure(state="disabled")
text_box.place(x=180, y=0)

# 设置按钮样式
style.configure("My.TButton", background="#4caf50", foreground="black", font=("微软雅黑", 10))

button_Borderless = ttk.Button(window, text="无边框修改", style="My.TButton", command=start_program)
button_Borderless.place(x=400, y=300)
button_autoclick = ttk.Button(window, text="对话模式", style="My.TButton", command=start_main)
button_autoclick.place(x=400, y=400)
button_map = ttk.Button(window, text="悬浮窗地图", style="My.TButton", command=start_map)
button_map.place(x=400, y=500)

# 进入主循环
window.mainloop()




