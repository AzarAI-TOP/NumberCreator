# -*- coding : utf-8 -*-

from cmath import sin
import sys, os, time
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import *

def get_GroupPoints(x0, y0, rec_range, r, n) -> list:
    point_group = []
    # 随机获取给定半径大小的随机点数
    rng = np.random.RandomState()
    r0 = rng.randint(0, r+1, n, dtype=int)
    thete0 = rng.randint(0, int(2*np.pi), n, dtype=int)

    for i in range(n):
        x = x0 + r0[i] * np.cos(thete0[i])
        y = y0 + r0[i] * np.sin(thete0[i])

        point_group.append((int(x), int(y)))

    return point_group


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QtWidgets.QWidget, self).__init__(parent)
        uic.loadUi("./ui.ui", self)

        # 设置部分UI
        self.setWindowTitle("NumberCreater")
        self.isLeftClicked = False
        self.isRightClicked = False

        # 设置点坐标的列表以及半径(以及数目)
        self.pointRadius = 10
        self.pointNumber = 10
        self.pointList = []

        # 设置控件事件
        self.painter = QtGui.QPainter(self)
        self.pen = QtGui.QPen(QtGui.QColorConstants.Blue, 2)

        self.controllable_range = (1000, 750)
        self.btn_finish.clicked.connect(self.Finish)
        self.btn_clear.clicked.connect(self.Clear)

        self.setMouseTracking(True)

    def on_radius_changed(self, f: float):
        self.pointRadius = f
        print("Radius Changed")

    def on_number_changed(self, n: int):
        self.pointNumber = n
        print("Number Changed")

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == 1:
            # 若为左键将坐标加入行列并绘图
            self.isLeftClicked = True
            self.pointList.append((event.x(), event.y()))
        elif event.button() == 2:
            # 若为右键将坐标加入行列并绘图
            self.isRightClicked = True
            self.pointList.extend(get_GroupPoints(event.x(), event.y(), self.controllable_range, self.pointRadius, self.pointNumber))

        self.update()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
            if self.isLeftClicked == True:
                # 若为左键将坐标加入行列并绘图
                self.pointList.append((a0.x(), a0.y()))
            elif self.isRightClicked == True:
                # 若为右键将坐标加入行列并绘图
                self.isRightClicked = True
                self.pointList.extend(get_GroupPoints(a0.x(), a0.y(), self.controllable_range, self.pointRadius, self.pointNumber))

            self.update()
            super().mouseMoveEvent(a0)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if a0.button() == 1:
            # 若为左键释放
            self.isLeftClicked = False
        elif a0.button() == 2:
            # 若为右键释放
            self.isRightClicked = False


        super().mouseReleaseEvent(a0)

    def paintEvent(self, a0: QtGui.QPaintEvent):
        # 绘点
        self.painter.begin(self)
        self.painter.setPen(self.pen)
        for x, y in self.pointList:
            self.painter.drawPoint(x, y)
        self.painter.end()

        super().paintEvent(a0)

    def Finish(self):
        # 依次录入数据
        with open("Points_List.txt", "w", encoding='utf-8') as file:
            for x, y in self.pointList:
                file.write(str(x) + " " + str(y) + "\n")

        # 删除最后一个换行符
        with open("Points_List.txt", "rb+") as file:
            # 判断是否为空
            if len(self.pointList) != 0:
                file.seek(-2, os.SEEK_END) # 因为是utf-8编码所以\n占2字节
                file.truncate()

        # 关闭应用
        app = QCoreApplication.instance()
        app.quit()

    def Clear(self):
        self.pointList = []
        self.update()


if __name__  == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    myWidget = MainWindow()
    myWidget.show()

    sys.exit(app.exec_())
