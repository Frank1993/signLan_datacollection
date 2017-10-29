# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import QWidget,QGraphicsView,QGraphicsScene,QTabWidget, QToolTip, QPushButton,QLabel, QApplication, QMessageBox,QDesktopWidget,QPushButton
from PyQt5.QtGui import QFont
from PyQt5 import  QtGui
from PyQt5.QtCore import QCoreApplication, QPoint,Qt
from PyQt5.QtGui import QPalette, QPixmap,QPainter,QColor
from baidu_tts import BaiduRest
class Tab1UI(QWidget):
    def __init__(self,parent):
        super(Tab1UI,self).__init__(parent)
        self.setParent(parent)
        self.outerParent = parent
        self.initUI()


    def initUI(self):
        header = QLabel("手语识别系统",self)

        header.setGeometry(50,50,400,40)

        header.setAlignment(Qt.AlignCenter)

        self.baiduTTS = BaiduRest()
        """
        backgroundPE = QPalette()
        backgroundPE.setColor(QPalette.Window,Qt.white)
        backgroundPE.setColor(self.backgroundRole(),Qt.white)
        self.setAutoFillBackground(True) 
        self.setPalette(backgroundPE)
        """

        pe = QPalette()
        pe.setColor(QPalette.WindowText, QColor("#4180f4"))  # 设置字体颜色
        #header.setAutoFillBackground(True)  # 设置背景充满，为设置背景颜色的必要条件
        #pe.setColor(QPalette.Window, Qt.blue)  # 设置背景颜色

        # pe.setColor(QPalette.Background,Qt.blue)<span style="font-family: Arial, Helvetica, sans-serif;">#设置背景颜色，和上面一行的效果一样
        header.setPalette(pe)

        header.setFont(QFont("Roman times", 36, QFont.Bold))

        self.setGeometry(0,0,self.parent().width(),self.parent().height())

        #self.signLanLabel = QLabel("Predict:",self)
        #self.signLanLabel.setGeometry(self.width()-350,120,300,50)
        #self.signLanLabel.setFont(QFont("Roman times",36,QFont.Bold))
        self.center(header)
        #self.show()

        """
        # set up the scene
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 800, 600)

        # add a view of that scene
        self.view = QGraphicsView()
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setFixedSize(800, 600)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        """
        self.imageLable = QLabel(self)
        self.imageLable.setGeometry(50,60,300,300)

        self.PredictLabel = QLabel("你",self)
        self.PredictLabel.setGeometry(self.width() - 360, 130, 300, 100)
        self.PredictLabel.setFont(QFont("Roman times",70,QFont.Bold))
        self.PredictLabel.setAlignment(Qt.AlignCenter)

        dynamicButton = QPushButton('动态', self)
        dynamicButton.setCheckable(True)
        dynamicButton.setGeometry(self.width() - 280, self.height() - 100, 60,30)
        #dynamicButton.setFont(QFont("Roman times",18))
        # 将按钮点击信号与自定义方法关联。We use the 'clicked'
        # signal that operates with Boolean value.
        # （备注：不太清楚该如何翻译。）
        dynamicButton.clicked[bool].connect(self.dynamicButtonPressed)

        audioButton = QPushButton("语音", self)
        audioButton.setCheckable(True)
        audioButton.setGeometry(self.width() - 200, self.height() - 100, 60,30)
        #audioButton.setFont(QFont("Roman times",18))
    def dynamicButtonPressed(self,pressed):
        source = self.sender()

        if pressed:
            # static
            self.outerParent.isPredictingDynamic = False
            source.setText("静态")
        else:
            self.outerParent.isPredictingDynamic = True
            source.setText("动态")

    def centerHeader(self,header):
        qr = header.frameGeometry()
        cp = QPoint(self.parent().width()/2,100)
        qr.moveCenter(cp)
        header.move(qr.topLeft())

    def centerTab(self):
        qr = self.frameGeometry()
        cp = QPoint()
    def center(self,btn):
        qr = btn.frameGeometry()
        cp = QPoint(self.width()/2,50)
        qr.moveCenter(cp)
        btn.move(qr.topLeft())

    def closeEvent(self, event):
        pass

    def setPredictedLabel(self, label):
        #self.PredictLabel.setText(label)
        self.PredictLabel.setText(label)
        audioFile = "./audio/%s.mp3"%label
        self.baiduTTS.playVoice(label,audioFile)

    def setNewImage(self, image):
        """
        qPixMap = QPixmap.fromImage(image)
        self.imageLable.setPixmap(qPixMap)
        #QApplication.processEvents()
        """
        pass
    def displayImage(self,i):

        qPixMap = QPixmap("/Users/frank/Desktop/images/%s.png"%(i + 1))
        self.imageLable.setPixmap(qPixMap)
        QApplication.processEvents()
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        #else:
            #self.signLanLabel.setText(chr(e.key()))