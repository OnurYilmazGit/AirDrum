from PyQt5 import QtCore, QtGui, QtWidgets
import os


class Ui_Dialog(object):
    def button_1(self):
        os.system("python3 main2.py")

    def button_3(self):
        os.system("python3 ScreenRecorder.py & python3 main2.py")

    def button_2(self):
        os.system("python3 playerMain.py & python3 main2.py")
    
    def button_4(self):
        os.system("exit")
        sys.exit(app.exec_())


    def button_5(self):
        os.system("evince AirDrum.pdf")    

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(955, 635)
        self.btnRun = QtWidgets.QPushButton(Dialog)
        self.btnRun.setGeometry(QtCore.QRect(80, 80, 180, 40))
        self.btnRun.setObjectName("btnRun")
        self.btnRun.clicked.connect(self.button_1)
        
        self.btnRun2 = QtWidgets.QPushButton(Dialog)
        self.btnRun2.setGeometry(QtCore.QRect(80, 140, 180, 40))
        self.btnRun2.setObjectName("btnRun2")
        self.btnRun2.clicked.connect(self.button_2)

        self.btnRun3 = QtWidgets.QPushButton(Dialog)
        self.btnRun3.setGeometry(QtCore.QRect(720, 80, 180, 40))
        self.btnRun3.setObjectName("btnRun3")
        self.btnRun3.clicked.connect(self.button_3) 
        
        self.btnRun4 = QtWidgets.QPushButton(Dialog)
        self.btnRun4.setGeometry(QtCore.QRect(720, 140, 180, 40))
        self.btnRun4.setObjectName("btnRun4")
        self.btnRun4.clicked.connect(self.button_4)


        self.btnRun5 = QtWidgets.QPushButton(Dialog)
        self.btnRun5.setGeometry(QtCore.QRect(840, 590, 100, 40))
        self.btnRun5.setObjectName("btnRun5")
        self.btnRun5.clicked.connect(self.button_5) 
       


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "AirDrum Game"))
        self.btnRun.setText(_translate("Dialog", "SOLO PLAYING"))
        self.btnRun2.setText(_translate("Dialog", "PLAY WITH YOUR MUSICS"))
        self.btnRun3.setText(_translate("Dialog", "RECORD YOURSELF"))
        self.btnRun4.setText(_translate("Dialog", "	QUIT"))
        self.btnRun5.setText(_translate("Dialog", " USER MANUAL"))
        self.btnRun.setStyleSheet('QPushButton {background-color: #A3C1DA; color: white;}')
        self.btnRun2.setStyleSheet('QPushButton {background-color: #A3C1DA; color: white;}')
        self.btnRun3.setStyleSheet('QPushButton {background-color: #A3C1DA; color: white;}')
        self.btnRun4.setStyleSheet('QPushButton {background-color: #A3C1DA; color: white;}')
        self.btnRun5.setStyleSheet('QPushButton {background-color: #A3C1DA; color: white;}')


stylesheet = """
    MainWindow {
        background-image: url('1.png'); 
        background-repeat: no-repeat; 
        background-position: center;
    }
"""


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    Dialog.setStyleSheet("background-image:url(1.jpg); background-position: center; background-repeat: no-repeat; " )
    ui = Ui_Dialog()
    ui.setupUi(Dialog)	
    Dialog.show()
    sys.exit(app.exec_())