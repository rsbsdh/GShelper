import keyboard
import sys
import time
import threading
import os

script_path = os.path.abspath(__file__)
path = os.path.dirname(script_path)
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
print("==========以下为程序运行提示==========")

t2 = threading.Thread(target=func2)
t3 = threading.Thread(target=func3)


t2.start()
t3.start()

t2.join()
t3.join()