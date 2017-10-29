# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import QWidget,QTabWidget, QToolTip, QPushButton,QLabel, QApplication, QMessageBox,QDesktopWidget
from PyQt5.QtGui import QFont
from PyQt5 import  QtGui
from PyQt5.QtCore import QCoreApplication, QPoint,Qt

from tab1UI import Tab1UI
from tab2UI import Tab2UI

class MainWindow(QTabWidget):
    def __init__(self):
        super(MainWindow,self).__init__()

        self.setGeometry(50,50,800,400)
        #tab = QTabWidget(self)

        self.tab1 = Tab1UI(self)
        self.tab2 = Tab2UI(self)

        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")

        self.setTabText(0, "手势识别")
        self.setTabText(1, "数据收集")
        self.isPredictingDynamic = True
        self.isCollectingData = False

        self.currentChanged.connect(self.onChange)

    def keyPressEvent(self, e):
        self.currentWidget().keyPressEvent(e)
        print(e)

    def setPredictedLabel(self,label):
        self.tab1.setPredictedLabel(label)

    def setNewImage(self,image):
        self.tab1.setNewImage(image)

    def onChange(self,currentTab):
        if currentTab == 0:
            self.isCollectingData = False
        else:
            self.isCollectingData = True

    def persisitData(self, frames):
        self.tab2.persisitData(frames)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())