# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import QWidget,QLineEdit,QFileDialog,QGraphicsView,QGraphicsScene,QTabWidget, QToolTip, QPushButton,QLabel, QApplication, QMessageBox,QDesktopWidget,QPushButton
from PyQt5.QtGui import QFont
from PyQt5 import  QtGui
from PyQt5.QtCore import QCoreApplication, QPoint,Qt
from PyQt5.QtGui import QPalette, QPixmap,QPainter,QColor

from data_collection import DataSerialization
import re
import os

class Tab2UI(QWidget):
    def __init__(self,parent):
        super(Tab2UI,self).__init__()
        self.setParent(parent)
        self.outerParent = parent
        self.initUI()

    def initUI(self):
        self.setGeometry(0,0,self.parent().width(),self.parent().height())
        header = QLabel("手语识别系统",self)

        header.setGeometry(50,50,400,40)

        header.setAlignment(Qt.AlignCenter)
        pe = QPalette()
        pe.setColor(QPalette.WindowText, QColor("#4180f4"))  
        header.setPalette(pe)

        header.setFont(QFont("Roman times", 36, QFont.Bold))
        #self.setGeometry(50,50,300,200)

        self.signLanLabel = QLabel("",self)
        self.signLanLabel.setGeometry(100,100,300,50)

        self.center(header)
        #self.show()

        directoryLabel = QLabel("存储路径：",self)
        directoryLabel.setGeometry(90,100,80,36)
        #directoryLabel.setAlignment(Qt.AlignCenter)
        directoryLabel.setFont(QFont("Roman times", 18))

        self.directoryLine = QLineEdit(self)
        self.directoryLine.setGeometry(180,100,self.width()-320,36)

        browseButton = QPushButton('浏览', self)
        browseButton.setCheckable(True)
        browseButton.setGeometry(self.width() - 130, 100, 40 ,36)

        browseButton.clicked[bool].connect(self.browseButtonPressed)

        fileLabel = QLabel("文件名：",self)
        fileLabel.setGeometry(90,150,80,36)
        #directoryLabel.setAlignment(Qt.AlignCenter)
        fileLabel.setFont(QFont("Roman times", 18))

        self.fileLine = QLineEdit(self)
        self.fileLine.setGeometry(180,150,self.width()-320,36)

        prevButton = QPushButton("Prev",self)
        #prevButton.setCheckable(True)
        prevButton.setGeometry(self.width()/2 -165, 250, 60,30)
        prevButton.clicked[bool].connect(self.prevButtonPressed)

        nextButton = QPushButton("Next",self)
        #nextButton.setCheckable(True)
        nextButton.setGeometry(self.width()/2 -75, 250, 60,30)
        nextButton.clicked[bool].connect(self.nextButtonPressed)

        stopButton = QPushButton("开始",self)
        stopButton.setCheckable(True)
        stopButton.setGeometry(self.width()/2 + 15, 250, 60,30)
        stopButton.clicked[bool].connect(self.stopButtonPressed)

        deleteButton = QPushButton("删除",self)
        #deleteButton.setCheckable(True)
        deleteButton.setGeometry(self.width()/2 + 105, 250, 60,30)
        deleteButton.clicked[bool].connect(self.deleteButtonPressed)

        self.canCollectingData = False

    def browseButtonPressed(self,pressed):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(file)
        if file != None and file != "":
            self.directoryLine.setText(file)

    def prevButtonPressed(self,pressed):
        if not self.checkDirectory():
            return

        newFileName = self.getNewFileName(self.fileLine.text(),True)
        if newFileName != None:
            self.fileLine.setText(newFileName)
    def nextButtonPressed(self,pressed):
        if not self.checkDirectory():
            return        
        newFileName = self.getNewFileName(self.fileLine.text(),False)
        if newFileName != None:
            self.fileLine.setText(newFileName)

    def stopButtonPressed(self,pressed):
        source = self.sender()

        if pressed:
            # start
            if self.checkDirectory() and self.checkFilePath():
                self.outerParent.isPredictingDynamic = False
                source.setText("停止")
                self.canCollectingData = True


        else:
            self.outerParent.isPredictingDynamic = True
            source.setText("开始")
            self.canCollectingData = False
    
    def getFilePath(self):
        return self.directoryLine.text() + "/" + self.fileLine.text()

    def checkDirectory(self):
        if self.directoryLine.text() == None or self.directoryLine.text() == "" or not os.path.isdir(self.directoryLine.text()):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("File directory Error!")
            msg.setInformativeText("请指定一个文件夹用于存储文件")
            msg.setWindowTitle("File directory Error!")
            #msg.setDetailedText("The details are as follows:")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
            return False
        else:
            return True
    def deleteButtonPressed(self, pressed):
        delteFilePath = self.getFilePath()
        if os.path.isdir(delteFilePath):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("File delete Error!")
            msg.setInformativeText("不支持删除该文件夹")
            msg.setWindowTitle("File delete Error!")
            #msg.setDetailedText("The details are as follows:")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
        elif not os.path.exists(delteFilePath):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("File delete Error!")
            msg.setInformativeText("该文件不存在")
            msg.setWindowTitle("File delete Error!")
            #msg.setDetailedText("The details are as follows:")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
        else:
            os.remove(delteFilePath)

    def getNewFileName(self, fileName,prev):
        filerange = re.finditer("\d+", fileName)
        try:
            filerange = filerange.next()
            start = filerange.start(0)
            end = filerange.end(0)
            number = int(fileName[start:end]) + (-1 if prev else 1)
            if number < 0:
                raise Exception()
            newFileName = "%s%s%s"%(fileName[:start],number,fileName[end:])
            return newFileName
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("File Name Error!")
            msg.setInformativeText("文件名中必须有一个正整数编号")
            msg.setWindowTitle("File Name Error!")
            #msg.setDetailedText("The details are as follows:")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
            return None
        
        

    def center(self,btn):
        qr = btn.frameGeometry()
        cp = QPoint(self.width()/2,50)
        qr.moveCenter(cp)
        btn.move(qr.topLeft())

    def persisitData(self,frames):
        if self.canCollectingData:
            if self.checkDirectory():
                filePath = self.getFilePath()
                if not self.checkFilePath():
                    return

                if not os.path.isdir(filePath):
                    serialize_stream = open(filePath,'wb')
                    dataSe = DataSerialization(frames,serialize_stream)

                    serialize_stream.close()
                    self.nextButtonPressed(True)
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)

                    msg.setText("File Name Error!")
                    msg.setInformativeText("请提供正确的文件名")
                    msg.setWindowTitle("File Name Error!")
                    #msg.setDetailedText("The details are as follows:")
                    msg.setStandardButtons(QMessageBox.Ok)
                    retval = msg.exec_()

    def checkFilePath(self):
        fileName = self.fileLine.text()
        filerange = re.finditer("\d+", fileName)
        try:
            print(filerange)
            filerange = filerange.next()
            start = filerange.start(0)
            end = filerange.end(0)
            number = int(fileName[start:end])
            if number < 0:
                raise Exception()
            return True
        except Exception as e:
            print(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("File Name Error!")
            msg.setInformativeText("文件名中必须有一个正整数编号")
            msg.setWindowTitle("File Name Error!")
            #msg.setDetailedText("The details are as follows:")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
            return False


    def closeEvent(self, event):
        pass

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        else:
            #self.signLanLabel.setText(chr(e.key()))
            #file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            #print(file)
            pass