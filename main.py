import sys
import time
import threading
import os
import keyboard
script_path = os.path.abspath(__file__)
path = os.path.dirname(script_path)

#map
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("提瓦特大地图")
        self.setGeometry(0, 700, 800, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba(255, 255, 255, 0.8), stop: 1 rgba(255, 255, 255, 1)); border: none;")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # 创建一个工具栏
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.toolbar.setStyleSheet("background-color:rgba(255,255,255,0.8);")
        
        zoom_in_action = QAction(self)
        zoom_out_action = QAction(self)
        zoom_in_icon = QIcon(QPixmap(path + "\\image\\ico\\zoom_in.png"))
        zoom_in_action.setIcon(zoom_in_icon)
        zoom_out_icon = QIcon(QPixmap(path + "\\image\\ico\\zoom_out.png"))
        zoom_out_action.setIcon(zoom_out_icon)
        
        self.toolbar.addAction(zoom_in_action)
        self.toolbar.addAction(zoom_out_action)

       
        zoom_in_action.triggered.connect(self.zoom_in)
        zoom_out_action.triggered.connect(self.zoom_out)

        layout = QVBoxLayout()
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.isVisible = True

    def load_url(self, url):
        self.browser.load(QUrl(url))

    def toggle_visibility(self):
        if self.isVisible:
            self.hide()
        else:
            self.show()
        self.isVisible = not self.isVisible

    def zoom_in(self):
        
        current_zoom = self.browser.zoomFactor()
        self.browser.setZoomFactor(current_zoom + 0.1)

    def zoom_out(self):
        
        current_zoom = self.browser.zoomFactor()
        self.browser.setZoomFactor(current_zoom - 0.1)
    
        
    






#window_to_front
import win32gui

def is_window_foreground(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    foreground_hwnd = win32gui.GetForegroundWindow()

    if hwnd == foreground_hwnd:
        print("窗口已前置")
    else:
        print("警告：窗口未启动或前置化，即将终止程序运行")
        time.sleep(2)
        sys.exit()



#window_check
import pygetwindow as gw
def get_window_size(window_title):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        width = window.width
        height = window.height
        print(f"检测到游戏窗口，分辨率为{width}x{height}")
        return(width,height)
    except:
        print("当前无游戏窗口，请手动打开游戏/启动器")
        



#windows_check
from PIL import ImageGrab

def get_screen_resolution():
    screen = ImageGrab.grab()
    width, height = screen.size
    print(f"当前屏幕分辨率：{width}x{height}")
    return width, height




#window_correction
import win32gui
import win32con

def set_window_position(window_title, x, y):
    hwnd = win32gui.FindWindow(None, window_title)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, 0, 0, win32con.SWP_NOSIZE)

x = 0
y = 0




#screenshot
import pyautogui
from PIL import Image, ImageDraw


def capture_and_save_screenshot(data):
    if data == "1080p":
        screen = (13, 32, 120, 50)  # 设置截图区域的左上角和右下角坐标
    elif data == "2k":
        screen = (55,39,88,68)
    else:
        print("暂未适配当前分辨率，正在退出")
        sys.exit()
    screenshot = pyautogui.screenshot(region=screen)  # 截图指定区域
    
    # 创建一个圆形的遮罩图像
    mask = Image.new("L", screenshot.size, 0)
    draw = ImageDraw.Draw(mask)
    center_x = screenshot.width // 2.1
    center_y = screenshot.height // 2.8
    radius = min(center_x, center_y)
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)
    
    # 将截图和遮罩图像合并，只保留圆形区域
    result = Image.new("RGBA", screenshot.size)
    result.paste(screenshot, (0, 0), mask=mask)
    
    result.save(path + "/image/screenshot.png")  # 保存截图

data = "1080p"
capture_and_save_screenshot(data)

#similarity
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as compare_ssim
from skimage.metrics import peak_signal_noise_ratio as compare_psnr


def compare_images_pixel(img1_path, img2_path):
    # 读取两张图片
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)

    # 确保两张图片具有相同的尺寸
    img1 = img1.resize((img2.size[0], img2.size[1]))

    # 将图片转换成灰度图像
    img1_gray = img1.convert('L')
    img2_gray = img2.convert('L')

    # 将图像转换为NumPy数组
    img1_arr = np.array(img1_gray)
    img2_arr = np.array(img2_gray)

    # 计算结构相似性（SSIM）指标
    ssim_score = compare_ssim(img1_arr, img2_arr)

    # 计算均方误差（MSE）
    mse = np.mean((img1_arr - img2_arr) ** 2)

    # 如果两张图片完全相同，直接返回一个较大的PSNR值
    if mse == 0:
        psnr_score = 100
    else:
        # 计算峰值信噪比（PSNR）指标
        psnr_score = compare_psnr(img1_arr, img2_arr)

    # 综合考虑SSIM指标和PSNR指标，得到最终的相似度评分
    similarity = ssim_score * psnr_score
    return similarity

#task_click
import pygetwindow as gw

def click_at_position(x, y, x1, y1, click_interval):
    # 指定游戏窗口标题
    window_title = "原神"

    # 获取游戏窗口对象
    game_window = pyautogui.getWindowsWithTitle(window_title)[0]

    # 设置游戏窗口为活动窗口
    game_window.activate()

    prev_position = (x,y)  # 获取初始鼠标位置

    pyautogui.click(x, y)

    i = 0

    while True:
        current_position = pyautogui.position()  # 获取当前鼠标位置
        if current_position != (x,y):  # 如果鼠标位置发生变化
            break  # 停止循环
        elif pyautogui.onScreen(x, y):
            pyautogui.click(x1,y1)
            time.sleep(0.2)
            pyautogui.click(x, y)  # 点击指定的坐标
            i = i + 1
            print("自动点击已执行：",i,"次")
            time.sleep(click_interval)







action = False





def func1():
    while True:
        global action
        capture_and_save_screenshot(data)
        img1_path = path + '\\image\\screenshot.png'
        if data == "1080p":
            img2_path = path + '\\image\\zd.png'
        elif data == "2k":
            img2_path = path + "\\image\\zd_2k.png"
        #剧情模式
        if compare_images_pixel(img1_path,img2_path) >=50:
            action = True


        if action == True:
            print("已检测到目标满足，3秒后进入任务模式")
            time.sleep(3)
            print("当前正在任务模式，请勿移动鼠标或执行其他操作")
            if data == "1080p":
                x = 1462  # 指定x坐标
                y = 820  # 指定y坐标

                x1 = 1377
                y1 = 719
            elif data == "2k":
                x =1280
                y = 810

                x1 = 1280
                y1 = 709

            else:
                print("抱歉，程序暂不支持该分辨率")
                print("正在退出程序")
                sys.exit()
            click_interval = 2
            click_at_position(x,y,x1,y1,click_interval)
            action = False
            print("当前任务模式已结束")
            continue
        


def func2():
    is_window_closed = False

    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.load_url("https://webstatic.mihoyo.com/ys/app/interactive-map/index.html?lang=zh-cn#/map/2?shown_types=&center=2008.50,-1084.00&zoom=-3.00")
    window.show()

    while not is_window_closed:
        if keyboard.is_pressed("shift+alt"):
            window.toggle_visibility()
            time.sleep(0.2)

        app.processEvents()



say = True
def func3():
    while say == True:
        print("显示/隐藏悬浮窗:shift+alt组合键")
        time.sleep(10)
        print("更多功能持续更新中")
        time.sleep(3)
        






print("程序作者bilibili@人生bsdh,点个关注谢谢,群号:482386706")
print()
print("本程序意图在于辅助玩家轻松快乐地游玩游戏，不提供任何作弊内容，以前包括未来都不会更新有关作弊的内容")
print()
print("===============更新日志===============")
print()
print("2023.12.29:增加鼠标初始检测功能,增加模拟鼠标点击,增加SSIM结构图形对比,增加圆形扫描区域完成,增加自动登录")
print()
print("2024.01.03:程序打包完成,增加屏幕分辨率,窗口分辨率检测,增加窗口活动化检测,增加全屏检测,尝试适配2k分辨率,暂停自动登录")
print()
print("2024.01.04:修复了全屏导致的y轴偏移,移除自动登录功能(删除有关源码),新增功能:悬浮窗地图")
print()
print("2024.01.07:修复了游戏按键滞后问题,编写GUI(未完成),新增无边框全屏程序(独立程序,预计日后并入GUI内),增加地图窗口缩放调整按键")
print()
print("2024.01.08:修改对话逻辑,优先点击最顶部对话框")
print()
print("==========以下为程序运行提示==========")
time.sleep(3)














print("程序正在自检")
time.sleep(3)
window_title = "原神"

print("重要的事情说三遍")
print("请在5秒内回到游戏窗口")
print("请在5秒内回到游戏窗口")
print("请在5秒内回到游戏窗口")
time.sleep(5)
is_window_foreground(window_title)



set_window_position(window_title, x, y)
checkwidth,checkheight = get_screen_resolution()
checkwidth_,checkheight_ = get_window_size(window_title)


if checkheight == 1080:
    data = "1080p"
    print(data)
if checkheight == 1440:
    data = "2k"
    print(data)



while True:
    

    if checkwidth != checkwidth_ or checkheight != checkheight_:
        print("当前窗口未全屏，请手动全屏")
        print("程序将在5秒后重新运行")



    else:
        print("自检已通过")
        break

    time.sleep(5)
    checkwidth,checkheight = get_screen_resolution()
    checkwidth_,checkheight_ = get_window_size(window_title)


print("扫描程序已启动，当前模式：无")





t1 = threading.Thread(target=func1)
t2 = threading.Thread(target=func2)
t3 = threading.Thread(target=func3)


t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

    
    



