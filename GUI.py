import tkinter as tk
from PIL import Image, ImageTk
import subprocess

import subprocess

def start_program():
    try:
        subprocess.Popen("Borderless.exe")
        print("程序已启动！")
    except FileNotFoundError:
        print("找不到可执行文件！")






# 创建主窗口
window = tk.Tk()
window.geometry("960x600")
window.title("测试窗口")

# # 加载图像
# image = Image.open("image.jpg")
# image = image.resize((300, 200), Image.ANTIALIAS)  # 调整图像大小
# photo = ImageTk.PhotoImage(image)

# # 创建一个标签，并显示图像
# image_label = tk.Label(window, image=photo)
# image_label.place(x=100, y=100)

# 创建一个文本框作为公告栏
text_box = tk.Text(window, height=10, width=80)
text_box.insert("1.0", """更新日志：\n
2023.12.29:增加鼠标初始检测功能,增加模拟鼠标点击,增加SSIM结构图形对比,增加圆形扫描区域完成,增加自动登录\n
2024.01.03:程序打包完成,增加屏幕分辨率,窗口分辨率检测,增加窗口活动化检测,增加全屏检测,适配2k分辨率,暂停自动登录\n
2024.01.07:修复了游戏按键滞后问题,尝试写一个简单的GUI\n""")

text_box.configure(state="disabled")
text_box.place(x=180, y=0)


button = tk.Button(window, text="无边框修改", command=start_program)
button.place(x=200,y=200)






# 进入主循环
window.mainloop()





