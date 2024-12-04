from PyQt5 import QtCore, QtGui, QtWidgets
from toggle_switch import SwitchControl  # Import your custom widget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Add SwitchControl
        self.switchControl = SwitchControl(self.centralwidget)
        self.switchControl.setGeometry(QtCore.QRect(100, 100, 70, 30))
        self.switchControl.setObjectName("switchControl")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def toggleDarkMode(self, checked):
        if checked:
            print("Dark mode enabled")
        else:
            print("Dark mode disabled")
