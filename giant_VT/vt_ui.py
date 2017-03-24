# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vt.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(190, 10, 421, 251))
        self.frame.setMinimumSize(QtCore.QSize(421, 251))
        self.frame.setMaximumSize(QtCore.QSize(421, 251))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.widget = QtGui.QWidget(self.frame)
        self.widget.setGeometry(QtCore.QRect(70, 0, 278, 219))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(271, 29))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.pushButton = QtGui.QPushButton(self.widget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(self.widget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_4 = QtGui.QPushButton(self.widget)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.verticalLayout.addWidget(self.pushButton_4)
        self.pushButton_3 = QtGui.QPushButton(self.widget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.verticalLayout.addWidget(self.pushButton_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 35))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuVirus_Total_Upload_Tool = QtGui.QMenu(self.menubar)
        self.menuVirus_Total_Upload_Tool.setObjectName(_fromUtf8("menuVirus_Total_Upload_Tool"))
        MainWindow.setMenuBar(self.menubar)
        self.actionUpload_a_File = QtGui.QAction(MainWindow)
        self.actionUpload_a_File.setObjectName(_fromUtf8("actionUpload_a_File"))
        self.actionTarget_a_URL = QtGui.QAction(MainWindow)
        self.actionTarget_a_URL.setObjectName(_fromUtf8("actionTarget_a_URL"))
        self.actionCheck_on_Queued_Reports = QtGui.QAction(MainWindow)
        self.actionCheck_on_Queued_Reports.setObjectName(_fromUtf8("actionCheck_on_Queued_Reports"))
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuVirus_Total_Upload_Tool.addAction(self.actionUpload_a_File)
        self.menuVirus_Total_Upload_Tool.addAction(self.actionTarget_a_URL)
        self.menuVirus_Total_Upload_Tool.addAction(self.actionCheck_on_Queued_Reports)
        self.menuVirus_Total_Upload_Tool.addAction(self.actionSettings)
        self.menuVirus_Total_Upload_Tool.addSeparator()
        self.menuVirus_Total_Upload_Tool.addAction(self.actionExit)
        self.menubar.addAction(self.menuVirus_Total_Upload_Tool.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Virus Total Upload Tool", None))
        self.pushButton.setText(_translate("MainWindow", "Select File", None))
        self.pushButton_2.setText(_translate("MainWindow", "Select URL", None))
        self.pushButton_4.setText(_translate("MainWindow", "Generate Reports", None))
        self.pushButton_3.setText(_translate("MainWindow", "Exit", None))
        self.menuVirus_Total_Upload_Tool.setTitle(_translate("MainWindow", "Virus Total Upload Tool", None))
        self.actionUpload_a_File.setText(_translate("MainWindow", "Upload a File", None))
        self.actionUpload_a_File.setShortcut(_translate("MainWindow", "Ctrl+F", None))
        self.actionTarget_a_URL.setText(_translate("MainWindow", "Target a URL", None))
        self.actionTarget_a_URL.setShortcut(_translate("MainWindow", "Ctrl+U", None))
        self.actionCheck_on_Queued_Reports.setText(_translate("MainWindow", "Check on Queued Reports", None))
        self.actionCheck_on_Queued_Reports.setShortcut(_translate("MainWindow", "Ctrl+R", None))
        self.actionSettings.setText(_translate("MainWindow", "Settings", None))
        self.actionSettings.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+E", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

