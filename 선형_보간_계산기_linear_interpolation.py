#-*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5 import uic

#Import UI file
main = uic.loadUiType("mainwindow.ui")[0]
second = uic.loadUiType("secondwindow.ui")[0]

# MainWindow (start page) 
class MainWindow(QMainWindow, main) :
  def __init__(self) :
    super().__init__()
    self.setupUi(self)
    self.Start_but.clicked.connect(self.Start)
    self.End_but.clicked.connect(self.End)
  
  def closeEvent(self, event):
    quit_msg = "정말로 종료하시겠습니까?"
    reply = QMessageBox.question(self, 'ME7', quit_msg, QMessageBox.Yes, QMessageBox.No)

    if reply == QMessageBox.Yes:
      event.accept()
    else:
      event.ignore()
    
  def Start(self) :
    self.hide()
    self.second = SecondWindow()
    self.second.exec()
    self.show()
    
  def End(self) :
    self.close()

# Second window (Calculator)
class SecondWindow(QDialog,QWidget,second):
  def __init__(self):
    super(SecondWindow,self).__init__()
    self.initUi()
    self.show()
    
    # Define x & y variable
    self.x,self.x1,self.x2,self.y,self.y1,self.y2 = 0,0,0,0,0,0
    self.error = False
    
    # Define various button
    self.Home_but.clicked.connect(self.Home)
    self.Cal_but.clicked.connect(self.Calculate)
    self.Erase_but.clicked.connect(self.Eraseall)
    self.Graph_but.clicked.connect(self.Graph)
    
    # Define x & y button
    self.x_LE.textChanged.connect(self.set)
    self.x_but.clicked.connect(self.erase)
    self.x1_LE.textChanged.connect(self.set)
    self.x1_but.clicked.connect(self.erase)
    self.x2_LE.textChanged.connect(self.set)
    self.x2_but.clicked.connect(self.erase)
    self.y1_LE.textChanged.connect(self.set)
    self.y1_but.clicked.connect(self.erase)
    self.y2_LE.textChanged.connect(self.set)
    self.y2_but.clicked.connect(self.erase)
    
  def initUi(self):
    self.setupUi(self)
  
  def set_only_double(self):
    self.onlydouble = QDoubleValidator()
    self.x_LE.setValidator(self.onlydouble)
    
  def Home(self):
    self.close()
  
  # Receive variable's value from user
  def set(self):
    if self.sender() == self.x_LE:
      self.x = self.x_LE.text()
      self.x_label.setText("X = {}".format(self.x))
    elif self.sender() == self.x1_LE:
      self.x1 = self.x1_LE.text()
      self.x1_label.setText("X1 = {}".format(self.x1))
    elif self.sender() == self.x2_LE:
      self.x2 = self.x2_LE.text()
      self.x2_label.setText("X2 = {}".format(self.x2))
    elif self.sender() == self.y1_LE:
      self.y1 = self.y1_LE.text()
      self.y1_label.setText("Y1 = {}".format(self.y1))
    else:
      self.y2 = self.y2_LE.text()
      self.y2_label.setText("Y2 = {}".format(self.y2))
    
  # Eraser button
  def erase(self):
    if self.sender() == self.x_but:
      self.x_LE.setText("")
      self.x = 0
      self.x_label.setText("X = {}".format(self.x))
    elif self.sender() == self.x1_but:
      self.x1_LE.setText("")
      self.x1 = 0
      self.x1_label.setText("X1 = {}".format(self.x1))
    elif self.sender() == self.x2_but:
      self.x2_LE.setText("")
      self.x2 = 0
      self.x2_label.setText("X2 = {}".format(self.x2))
    elif self.sender() == self.y1_but:
      self.y1_LE.setText("")
      self.y1 = 0
      self.y1_label.setText("Y1 = {}".format(self.y1))
    else:
      self.y2_LE.setText("")
      self.y2 = 0
      self.y2_label.setText("Y2 = {}".format(self.y2))
  
  # Reset button
  def Eraseall(self):
    self.x_but.click()
    self.x1_but.click()
    self.x2_but.click()
    self.y1_but.click()
    self.y2_but.click()
    self.y = 0
    self.y_TB.setHtml("<html><head/><body><p>결과<span style=\" font-weight:600;\">: </span><span style=\" color:#ff0000;\">Y = None</span></p></body></html>")
  
  # Do Linear Interpolation  
  def Calculate(self):
    try:
      x = float(self.x)
      x1 = float(self.x1)
      x2 = float(self.x2)
      y1 = float(self.y1)
      y2 = float(self.y2)
      self.y = y1 + (y1-y2) * ((x-x1)/(x1-x2))
      self.y_TB.setHtml("<body style=\" font-family:'연세소제목체'; font-size:18pt; font-weight:400; font-style:normal;\"><p>결과<span style=\" font-weight:600;\">:</span><span style=\" color:#ff0000;\"> Y = {:.4f}</span></p></body>".format(self.y))
      self.error = False
      
    except ZeroDivisionError:
      error_msg = QMessageBox.warning(self, 'error', "0으로 나눌 수 없습니다. 입력된 값을 확인해 주세요!")
      self.error = True
    except ValueError:
      error_msg = QMessageBox.warning(self, 'error', "잘못된 형식입니다. 입력된 값을 확인해 주세요! (정수 or 실수)")
      self.error = True
  
  # Plot the graph (Only no error condition)    
  def Graph(self):
    self.Cal_but.click()
    if self.error == False:
      x = list(map(float,[self.x1,self.x,self.x2]))
      y = list(map(float,[self.y1,self.y,self.y2]))
      
      plt.plot(x,y,'bo--')
      plt.xlabel('x',fontsize=15)
      plt.ylabel('y',fontsize=15)
      plt.xticks(x)
      plt.yticks(y)
      plt.text(x[0],y[0],"(x1,y1)",va='top')
      plt.text(x[1],y[1],"(x,y)",va='top')
      plt.text(x[2],y[2],"(x2,y2)",va='baseline')
      plt.show()

# Execute        
if __name__ == "__main__" :
  app = QApplication(sys.argv) 
  myWindow = MainWindow()
  myWindow.show()
  app.exec_()