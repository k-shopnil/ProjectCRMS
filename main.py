import os
import sqlite3
import sys
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QShortcut, QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from ui import Ui_MainWindow
from about import Ui_Dialog as Ui_AboutDialog
from database_handler import store_reservation, get_all_reservations
from toggle_switch import SwitchControl
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QFile, QUrl
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QKeySequence, QDesktopServices
from PyQt5.QtGui import QIcon, QPainter, QPdfWriter
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QPushButton, QWidget, QHBoxLayout, QGraphicsBlurEffect


class AboutWindow(QDialog):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)

        # Connect the GitHub button to open the repository link
        self.ui.pushButton.clicked.connect(self.open_github_repo)

    def open_github_repo(self):
        # Replace the URL below with your GitHub repository link
        QDesktopServices.openUrl(QUrl("https://github.com/k-shopnil/ProjectCRMS"))
class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pages.tabBar().setVisible(False)
        self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.lineEdit_2.setPlaceholderText("Enter Password")
        self.ui.label_3.setText("CRMS V1.3 Beta | Developed By Group 5")
        self.add_combos()
        
        self.ui.actionAbout.triggered.connect(self.show_about)
        self.ui.actionForce_Exit.triggered.connect(self.force_exit)
        self.ui.actionRefresh.triggered.connect(self.refresh_app)
        
        self.ui.radioButton.setChecked(True)
        self.ui.radioButton_6.setChecked(True)
        self.ui.pushButton_4.clicked.connect(self.passwordVisibility)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second
        
        
        for index in range(1, self.ui.pages.count()):
            self.ui.pages.setTabVisible(index, False)

        # Connect login button to login function
        self.ui.pushButton.clicked.connect(self.login)
        self.ui.admin_logout.clicked.connect(self.logout)
        self.ui.admin_logout_4.clicked.connect(self.logout)
        self.ui.homeButton.clicked.connect(lambda: self.ui.pages.setCurrentIndex(1))
        self.ui.homeButton_2.clicked.connect(lambda: self.ui.pages.setCurrentIndex(5))
        self.ui.logsButton.clicked.connect(lambda: self.ui.pages.setCurrentIndex(3))
        self.ui.pendingreqButton.clicked.connect(lambda: self.ui.pages.setCurrentIndex(2))
        self.ui.noticeButton.clicked.connect(lambda: self.ui.pages.setCurrentIndex(4))
        self.ui.reservation_BTH.clicked.connect(lambda: self.ui.pages.setCurrentIndex(1))
        self.ui.reservation_BTH_2.clicked.connect(lambda: self.ui.pages.setCurrentIndex(1))
        self.ui.reservation_BTH_3.clicked.connect(lambda: self.ui.pages.setCurrentIndex(1))
        self.ui.reservation_BTH_4.clicked.connect(lambda: self.ui.pages.setCurrentIndex(5))
        self.ui.reservation_BTH_5.clicked.connect(lambda: self.ui.pages.setCurrentIndex(5))
        self.ui.reservation_BTH_6.clicked.connect(lambda: self.ui.pages.setCurrentIndex(5))
        self.ui.pushButton_8.clicked.connect(lambda: self.ui.pages.setCurrentIndex(7))
        self.ui.pushButton_7.clicked.connect(lambda: self.ui.pages.setCurrentIndex(8))
        self.ui.admin_logout_3.clicked.connect(lambda: self.ui.pages.setCurrentIndex(6))
        self.ui.pushButton_3.clicked.connect(self.submit_reservation)
        #self.ui.menubar
        self.enter_shortcut = QShortcut(QKeySequence(Qt.Key_Return), self)
        self.enter_shortcut.activated.connect(self.handle_enter_key)

        # Locate the toggle switch widget
        self.toggle_switch = self.findChild(SwitchControl, "checkBox_2")
        self.toggle_switch.setChecked(False)
        # Connect signals and slots
        self.toggle_switch.stateChanged.connect(self.on_toggle_state_changed)
        #self.ui.homeButton_2.setStyleSheet("background-color: #0b4fa7; border:none;")
        #self.ui.homeButton.setStyleSheet("background-color: #0b4fa7; border:none;")
    
    def passwordVisibility(self):
        if self.ui.lineEdit_2.echoMode() == QtWidgets.QLineEdit.Password:
            self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.ui.pushButton_4.setIcon(QtGui.QIcon("Asset\eye-svgrepo-com.svg"))
        else:
            self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
            self.ui.pushButton_4.setIcon(QtGui.QIcon("Asset/eye-slash-svgrepo-com.svg"))
      
    def force_exit(self):
        QApplication.quit()
    
    def refresh_app(self):
        
        #self.load_latest_data()

        self.refresh_popup = QDialog(self)
        self.refresh_popup.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog) 
        self.refresh_popup.setFixedSize(300, 100)
        layout = QVBoxLayout(self.refresh_popup)
        label = QLabel("Refreshing System... Please wait!", self.refresh_popup)
        label.setAlignment(Qt.AlignCenter) 
        layout.addWidget(label)
        self.refresh_popup.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: black;
                alignment: center;
            }
            QDialog {
                border: 1px solid gray;
                border-radius: 15px;
            }
        """)
        self.refresh_popup.setModal(False)  # Non-blocking
        self.refresh_popup.show()

        # Automatically close the dialog after 1 second
        QTimer.singleShot(1000, self.refresh_popup.close)
    
    def show_about(self):
        self.about_window = AboutWindow()
        self.about_window.exec_()
        
    def handle_enter_key(self):
        # Ensure the Enter key triggers the login only on the login page
        if self.ui.pages.currentIndex() == 0:  # Assuming login is tab 0
            self.ui.pushButton.click()
    
    def update_time(self):
        # Get the current date and time
        current_datetime = QDateTime.currentDateTime()
        current_date = current_datetime.toString("dddd, MMMM dd, yyyy")
        current_time = current_datetime.toString("hh:mm:ss AP")
        current_time_global = current_datetime.toString("HH:mm:ss")
        if(current_time_global>="00:00:00" and current_time_global<="12:00:00"):
            self.ui.greet.setText("Good Morning!")
        elif(current_time_global>="12:00:00" and current_time_global<="17:00:00"):
            self.ui.greet.setText("Good Afternoon!")
        else:
            self.ui.greet.setText("Good Evening!")

        # Update the labels with the new time and date
        self.ui.date.setText(current_date)
        self.ui.time.setText(current_time)
        self.ui.date_2.setText(current_date)
        self.ui.time_2.setText(current_time)
            
    def add_combos(self):
        # Add items to the resource combo box
        self.ui.comboBox.addItem("Classroom")

        # Add items to the time slot combo box
        self.ui.comboBox_2.addItem("B2-705")
        self.ui.comboBox_2.addItem("B2-910")
        
    def login(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        if self.ui.radioButton_2.isChecked():
            role = "Student"
        elif self.ui.radioButton_3.isChecked():
            role = "Teacher"
        else:
            role = "Admin"
        conn = sqlite3.connect('data/crms_central.db')
        #print(f"Database path: {'listview.db')}")
        cur = conn.cursor()
        query = "SELECT * FROM user WHERE user_id=? AND password=? AND roles=?"
        cur.execute(query, (username, password, role))
        result = cur.fetchone()
        print(role)
        conn.close()
        
        if result and role == "Admin":
            self.ui.pages.setCurrentIndex(1)
            QMessageBox.information(self, "Success", "Login Successful!")
        elif result and role == "Student":
            self.ui.pages.setCurrentIndex(5)
            QMessageBox.information(self, "Success", "Login Successful!")
        elif result and role == "Teacher":
            self.ui.pages.setCurrentIndex(5)
            QMessageBox.information(self, "Success", "Login Successful!")
        else:
            QMessageBox.warning(self, "Error", "Incorrect credentials! Try again with correct details.")
    


    def closeEvent(self, event):
    
        reply = QMessageBox.question(
            self,
            "Exit Confirmation",
            "Are you sure you want to exit?\nAll unsaved changes will be saved automatically.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            try:
                self.save_all_data()

                self.database.close()

                event.accept()
                print("Application closed successfully.")

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"An error occurred while safe exiting the application:\n{str(e)}, \n try Force Exit",
                )
                # Ignore the close event
                event.ignore()
        else:
            # Ignore the close event
            event.ignore()
    
    def logout(self):
        # Navigate back to the login page (tab index 0)
        
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to log out?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.ui.pages.setCurrentIndex(0)
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
            QMessageBox.information(self, "Logout", "You have successfully logged out.")
        else:
            pass
        
    def submit_reservation(self):
        # Get the selected values from the combo boxes and the text field
        resource = self.ui.comboBox.currentText()
        space = self.ui.comboBox_2.currentText()
        date_time = self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm")  # Format the DateTime
        notes = self.ui.plainTextEdit.toPlainText()

        # Validate the input fields
        if not resource or not space or not date_time:
            QMessageBox.warning(self, "Input Error", "Please fill out all fields.")
            return

        # Store the reservation details in the database
        if store_reservation(resource, space, date_time, notes):
            QMessageBox.information(self, "Success", "Your reservation request has been submitted successfully.")

    
    def on_toggle_state_changed(self, checked):
        # Handle the toggle switch state change
        if checked:
            self.setStyleSheet(stylesheetDark)
            self.ui.admin_hero_2.setStyleSheet("border: 2px solid #ffffff;border-radius: 20px;")
            self.ui.admin_hero.setStyleSheet("border: 2px solid #ffffff;border-radius: 20px;")
            self.ui.frame_20.setStyleSheet("background-color: #272727; border:none; border-radius: 20px;")
        else:
            self.setStyleSheet(stylesheetLight)
            self.ui.admin_hero_2.setStyleSheet("border: 2px solid rgb(4, 29, 45);border-radius: 20px;")
            self.ui.admin_hero.setStyleSheet("border: 2px solid rgb(4, 29, 45);border-radius: 20px;")
            self.ui.frame_20.setStyleSheet("background-color: rgb(227, 227, 227); border:none; border-radius: 20px;")
            
            print(f"debug State: {'Dark mode ON' if checked else 'Dark mode OFF'}")    


        
def load_stylesheet(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
def dayFromdate(date):
    date="2024,12,19"
    date = date.split(",")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    date_object = datetime.date(year, month, day)
    day_name = date_object.strftime("%A")
    return day_name

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    stylesheetDark = load_stylesheet('dark.qss')
    stylesheetLight = load_stylesheet('light.qss')
    main_window = MainApp()
    main_window.show()
    print(dayFromdate("2024,12,19"))
    sys.exit(app.exec_())
