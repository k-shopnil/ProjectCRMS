import os
import re
import sqlite3
import sys
import hashlib
import datetime
from datetime import date, datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QShortcut, QDialog, QVBoxLayout, QLabel, QInputDialog, QTableWidgetItem
from PyQt5.QtCore import Qt
from ui import Ui_MainWindow
from about import Ui_Dialog as Ui_AboutDialog
from database_handler import *
from toggle_switch import SwitchControl
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QFile, QUrl
from PyQt5.QtCore import QTimer, QDateTime, QByteArray
from PyQt5.QtGui import QKeySequence, QDesktopServices, QPixmap, QMovie
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QPushButton, QWidget, QHBoxLayout, QGraphicsBlurEffect

class LoginSession:
    def __init__(self):
        self.user_id = None
        self.role = None
        self.name = None
        self.flag = None

    def clear(self):
        self.user_id = None
        self.role = None
        self.name = None
        self.flag = None

# Initialize session globally

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
        self.current_session = LoginSession()
        self.ui.pages.tabBar().setVisible(False)
        self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.lineEdit_2.setPlaceholderText("Enter Password")
        self.ui.label_3.setText("CRMS V1.3 Beta | Developed By Group 5")
        
        
        self.update_greeting()
        self.load_notices(self.current_session.role)
        #self.add_combos()
        
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
        self.ui.pushButton_2.clicked.connect(self.post_notice)
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
        self.ui.reservation_BTH_7.clicked.connect(lambda: self.ui.pages.setCurrentIndex(5))
        self.ui.pushButton_6.clicked.connect(lambda: self.ui.pages.setCurrentIndex(9))
        self.ui.pushButton_8.clicked.connect(lambda: self.ui.pages.setCurrentIndex(7))
        self.ui.pushButton_8.clicked.connect(lambda: self.load_profile(self.current_session.user_id))
        print(f"Current user_id: {self.current_session.user_id}")
        self.ui.pushButton_7.clicked.connect(lambda: self.ui.pages.setCurrentIndex(8))
        self.ui.admin_logout_3.clicked.connect(lambda: self.ui.pages.setCurrentIndex(6))
        self.ui.admin_logout_3.clicked.connect(self.load_notifications)
        self.ui.pushButton_3.clicked.connect(self.apply_reservation)
        self.ui.pushButton_5.clicked.connect(self.resource_release)
        self.ui.pendingreqButton.clicked.connect(self.load_reservation_requests)
        self.ui.logsButton.clicked.connect(self.load_application_logs)
        #self.ui.menubar
        self.enter_shortcut = QShortcut(QKeySequence(Qt.Key_Return), self)
        self.enter_shortcut.activated.connect(self.handle_enter_key)

        # Locate the toggle switch widget
        self.toggle_switch = self.findChild(SwitchControl, "checkBox_2")
        self.toggle_switch.setChecked(False)
        # Connect signals and slots
        self.toggle_switch.stateChanged.connect(self.on_toggle_state_changed)
        self.ui.timeEdit.setEnabled(False)
        self.ui.timeEdit_2.setEnabled(False)
        self.ui.timeEdit_3.setEnabled(False)
        self.ui.timeEdit_4.setEnabled(False)
        self.ui.comboBox.currentIndexChanged.connect(self.update_widget_states)
        self.ui.comboBox_4.currentIndexChanged.connect(self.update_widget_states_c)
        #self.ui.homeButton_2.setStyleSheet("background-color: #0b4fa7; border:none;")
        #self.ui.homeButton.setStyleSheet("background-color: #0b4fa7; border:none;")
    def update_greeting(self):
        """Updates the greeting label based on the current session"""
        if self.current_session.name:
            self.current_session.user_id = self.current_session.user_id
            self.current_session.role = self.current_session.role
            first_name = self.current_session.name.split()[0]
            self.ui.greet_2.setText(f"Welcome, {first_name}!")
        else:
            self.ui.greet_2.setText("Welcome!")
            
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
        self.refresh_popup.setFixedSize(80, 80)
        layout = QVBoxLayout(self.refresh_popup)
        label = QLabel(self.refresh_popup)
        pixmap = QMovie("Asset/speech-bubble.gif")
        label.setMovie(pixmap)
        pixmap.start()
        label.setScaledContents(True)
        
        
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
        if self.current_session.role=="Admin":
            self.load_notices(self.current_session.role)
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
            
    # def add_combos(self):
    #     # Add items to the resource combo box
    #     self.ui.comboBox.addItem("Classroom")

    #     # Add items to the time slot combo box
    #     self.ui.comboBox_2.addItem("B2-705")
    #     self.ui.comboBox_2.addItem("B2-910")
        

        
    def login(self):
        userid = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        password=hashlib.sha256(password.encode()).hexdigest()
        if self.ui.radioButton_2.isChecked():
            role = "Student"
        elif self.ui.radioButton_3.isChecked():
            role = "Teacher"
        else:
            role = "Admin"
        print(userid,password,role)
        conn = sqlite3.connect('data/crms_central.db')
        #print(f"Database path: {'listview.db')}")
        cur = conn.cursor()
        query = "SELECT user_id,full_name,roles,account_flag FROM user WHERE user_id=? AND password=? AND roles=?"
        cur.execute(query, (userid, password, role))
        result = cur.fetchone()
        print(result)
        conn.close()
        if result:
            user_id,name,role,flag = result
            #print(user_id,name,role,flag)
            self.current_session.user_id = user_id
            self.current_session.role = role
            self.current_session.flag = flag
            self.current_session.name = name
            name = name.split()[0]
            self.update_greeting()
            self.load_notices(role)
            QMessageBox.information(self, "Success", "Login Successful! \n Welcome "+name+"!")
            if role == "Admin":
                self.ui.pages.setCurrentIndex(1)
            elif result and role == "Teacher" or role == "Student":
                self.ui.pages.setCurrentIndex(5)
                if role == "Teacher":
                    self.ui.pushButton_6.setVisible(True)
                else:
                    self.ui.pushButton_6.setVisible(False)
        else:
            QMessageBox.warning(self, "Error", "Incorrect credentials! Try again with correct details.")
        
    def load_profile(self,user_id):
        
        """Retrieve the user's profile details from the users table."""
        print(f"User ID: {user_id}")
        conn,cur = connect_to_db()
        query = "SELECT Picture,full_name,roles,dept,account_flag FROM user WHERE user_id = ?"
        cur.execute(query, (user_id,))
        result = cur.fetchone()
        #print(result)
        picture, name, role, dept, flag = result
        self.ui.resevation_heading_6.setText(name)
        self.ui.resevation_heading_10.setText(role)
        self.ui.resevation_heading_11.setText(dept)
        self.ui.resevation_heading_13.setText(str(user_id))
        #print(picture)
        image_data = QByteArray(picture)  # Convert binary data
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        self.ui.label_6.setPixmap(pixmap)
        self.ui.label_6.setScaledContents(True)
        if flag == 1:
            self.ui.resevation_heading_12.setText("Account Restricted for system abuse")
        else:
            self.ui.resevation_heading_12.setText("No restrictions")

        conn.close()
    
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
            self.current_session.clear()
            self.ui.pages.setCurrentIndex(0)
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
            QMessageBox.information(self, "Logout", "You have successfully logged out.")
        else:
            pass
        
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
                self.logout()
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

    def post_notice(self):
        audience = ""
        if self.ui.radioButton_6.isChecked():
            audience = "Everyone"
        elif self.ui.radioButton_4.isChecked():
            audience = "Teacher"
        elif self.ui.radioButton_5.isChecked():
            audience = "Student"
        
        message = self.ui.textEdit.toPlainText().strip()

        if not message:
            QMessageBox.warning(self, "Warning", "Message cannot be empty.")
            return

        add_notice(audience, message)
        QMessageBox.information(self, "Success", "Notice posted successfully.")
        self.ui.textEdit.clear()
        
    def load_notices(self,role):
        print(f"Role: {role}")
        notices = fetch_notices(role)
        self.ui.tableWidget_3.setRowCount(0)  # Clear the table
        self.ui.tableWidget_3.setColumnWidth(1,400)
        for row_idx, (notice_date, message) in enumerate(notices):
            self.ui.tableWidget_3.insertRow(row_idx)
            self.ui.tableWidget_3.setItem(row_idx, 0, QTableWidgetItem(notice_date))
            self.ui.tableWidget_3.setItem(row_idx, 1, QTableWidgetItem(message))
            
    def apply_reservation(self):
        conn,cur=connect_to_db()
        if self.current_session.flag == 1:
            QMessageBox.warning(self, "Error", "Your account has been restricted for system abuse. Please contact the admin.")
            self.ui.plainTextEdit.clear()
            self.ui.dateEdit.clear()
            self.ui.timeEdit.clear()
            self.ui.timeEdit_2.clear()
            self.ui.comboBox.setCurrentIndex(0)
            self.ui.comboBox_2.setCurrentIndex(0)
            self.ui.comboBox_3.setCurrentIndex(0)
            return
        else:
            try:
                # Step 3: Extract user_id from the current session
                user_id = self.current_session.user_id

                # Step 4: Extract notes and date
                notes = self.ui.plainTextEdit.toPlainText()
                date = self.ui.dateEdit.date().toString("yyyy-MM-dd")
                if date < datetime.today().strftime("%Y-%m-%d"):
                    QMessageBox.warning(self, "Error", "You cannot apply for a reservation in the past.")
                    return

                # Step 5: Record application_time
                application_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Step 6: Handle resource_id and time
                resource = self.ui.comboBox.currentText()
                resource_id = None
                time = None
                is_available = True

                if resource == "Classroom":
                    # Extract resource_id from Space combo box
                    space = self.ui.comboBox_2.currentText()  # Example: "B2-203"
                    resource_id = int(re.sub(r'[^0-9]', '', space))# Convert "B2-203" to 2203

                    # Extract time from the timeslot combo box
                    time = self.ui.comboBox_3.currentText()

                    # Check availability in resource_classroom
                    check_query = """
                    SELECT available FROM resource_log
                    WHERE resource_id = ? AND date = ? AND time = ?
                    """
                    cur.execute(check_query, (resource_id, date, time))
                    result = cur.fetchone()

                else:
                    # Query resources table for the selected resource type
                    resource_type = self.ui.comboBox.currentText()
                    cur.execute("SELECT resource_id FROM resources WHERE resource_type = ?", (resource_type,))
                    resource_row = cur.fetchone()
                    if resource_row:
                        resource_id = resource_row[0]
                    else:
                        raise ValueError(f"No resource found for type: {resource_type}")

                    # Combine start and end times
                    start_time = self.ui.timeEdit.time().toString("h:mm AP")
                    end_time = self.ui.timeEdit_2.time().toString("h:mm AP")
                    time = f"{start_time}-{end_time}"

                    # Check availability in resource_htp
                    check_query = """
                    SELECT available FROM resource_log 
                    WHERE resource_id = ? AND date = ? AND 
                        time = ?
                    """
                    cur.execute(check_query, (resource_id, date, time,))
                    result = cur.fetchone()
                # if resource == "Classroom":
                #     if result!=None:
                #     # Check the value in the `available` column
                #         if result[0] == 0:
                #             is_available = False
                #         else:
                #             is_available = True
                #     else:
                #         is_available = False
                        
                # else:
                #     if result!=None:
                #     # Check the value in the `available` column
                #         if result[0] == 0:
                #             is_available = False
                #         else:
                #             is_available = True
                #     else:
                #         is_available = True
                
                if result is not None:
                    if result[0] == 0:
                        is_available = False
                    else:
                        is_available = True
                else:
                    is_available = True

                if not is_available:
                    QMessageBox.warning(self, "Error", "The selected resource is not available for the chosen date and time.")
                    return  # Exit the function if the resource is not available
                #check if the same entry(same date,time,user_id,resource_id) is already in the database
                cur.execute("SELECT * FROM bookings WHERE user_id = ? AND date = ? AND time = ? AND resource_id = ?", (user_id, date, time, resource_id))
                existing_entry = cur.fetchone()
                cur.execute("SELECT COUNT(*) FROM bookings")
                count = cur.fetchone()[0]
                if not existing_entry:
                    if count == 0:
                        cur.execute('''
                        INSERT INTO bookings (booking_id, user_id, notes, date, application_time, time, resource_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (1, user_id, notes, date, application_time, time, resource_id))
                    else:
                        cur.execute('''
                        INSERT INTO bookings (user_id, notes, date, application_time, time, resource_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                        ''', (user_id, notes, date, application_time, time, resource_id))
                else:
                    QMessageBox.warning(self, "Error", "You have already applied for this reservation.")
                    return

                conn.commit()

                # Success message
                QMessageBox.information(self, "Success", "Reservation applied successfully!")
                self.ui.plainTextEdit.clear()
                self.ui.dateEdit.clear()
                self.ui.timeEdit.clear()
                self.ui.timeEdit_2.clear()
                self.ui.comboBox.setCurrentIndex(0)
                self.ui.comboBox_2.setCurrentIndex(0)
                self.ui.comboBox_3.setCurrentIndex(0)
            except Exception as e:
                conn.rollback()
                QMessageBox.warning(self, "Error", f"Failed to apply reservation: {e}")
            finally:
                conn.close()
                
    def load_reservation_requests(self):
        conn, cur = connect_to_db()
        try:
            # Clear existing rows in the table
            self.ui.tableWidget.setRowCount(0)

            # Query to fetch reservation requests
            query = """
                SELECT b.application_time, b.user_id, b.resource_id, b.date, b.time, b.notes, u.full_name, u.roles, b.booking_id
                FROM bookings b
                INNER JOIN user u ON b.user_id = u.user_id
            """
            cur.execute(query)
            rows = cur.fetchall()

            # Populate the table widget
            for row_number, row_data in enumerate(rows):
                application_time, user_id, resource_id, date, time, notes, full_name, role, booking_id = row_data

                # Reverse format resource_id (e.g., 2203 → B2-203)
                if len(str(resource_id)) == 4:
                    building = f"B{str(resource_id)[0]}"
                    room = str(resource_id)[1:]
                    resource_name = f"{building}-{room}"
                else:
                    result_type = cur.execute("SELECT resource_type FROM resources WHERE resource_id = ?", (resource_id,))
                    resource_name = result_type.fetchone()[0]

                # Add a new row to the table
                self.ui.tableWidget.insertRow(row_number)

                # Populate columns
                self.ui.tableWidget.setItem(row_number, 0, QTableWidgetItem(application_time))
                self.ui.tableWidget.setItem(row_number, 1, QTableWidgetItem(full_name))
                self.ui.tableWidget.setItem(row_number, 2, QTableWidgetItem(role))
                self.ui.tableWidget.setItem(row_number, 3, QTableWidgetItem(resource_name))
                self.ui.tableWidget.setItem(row_number, 4, QTableWidgetItem(date))
                self.ui.tableWidget.setItem(row_number, 5, QTableWidgetItem(time))
                self.ui.tableWidget.setItem(row_number, 7, QTableWidgetItem(notes))

                # Add buttons for Approval column
                approve_button = QPushButton("Approve")
                decline_button = QPushButton("Decline")
                flag_button = QPushButton("Flag")

                # #Assign button IDs or data if needed (e.g., booking_id)
                # approve_button.setProperty("booking_id", row_data[0])
                # decline_button.setProperty("booking_id", row_data[0])
                # flag_button.setProperty("booking_id", row_data[0])

                ## Connect buttons to their respective functions (to be defined)
                # approve_button.clicked.connect(lambda: self.approve_request(approve_button.property("booking_id")))
                # decline_button.clicked.connect(lambda: self.decline_request(decline_button.property("booking_id")))
                # flag_button.clicked.connect(lambda: self.flag_request(flag_button.property("booking_id")))
                approve_button.clicked.connect(lambda _, bid=booking_id: self.handle_approve_button(bid))
                decline_button.clicked.connect(lambda _, bid=booking_id: self.handle_declined_button(bid))
                flag_button.clicked.connect(lambda _, uid=user_id: self.handle_flagged_button(uid))

                # Create a container widget for buttons
                button_widget = QWidget()
                button_layout = QHBoxLayout(button_widget)
                button_layout.addWidget(approve_button)
                button_layout.addWidget(decline_button)
                button_layout.addWidget(flag_button)
                button_layout.setContentsMargins(0, 0, 0, 0)
                button_layout.setSpacing(5)

                # Add the button widget to the table
                self.ui.tableWidget.setCellWidget(row_number, 6, button_widget)
                self.ui.tableWidget.setColumnWidth(6, 200)

            # Commit and close the connection
            conn.commit()

        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Failed to load reservation requests: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
                
    def handle_declined_button(self, booking_id):
        # Retrieve user_id and resource_id for the given booking_id
        conn, cur = connect_to_db()
        
        # Fetch user_id and resource_id from bookings
        cur.execute("SELECT user_id, resource_id, date, time FROM bookings WHERE booking_id = ?", (booking_id,))
        result = cur.fetchone()
        if not result:
            QMessageBox.warning(self, "Error", f"No booking found for booking_id {booking_id}.")
            return
        
        user_id, resource_id, date, time = result
        
        # Get current timestamp for reviewed_on
        reviewed_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insert data into booking_report
        try:
            cur.execute(
                "INSERT INTO booking_report (booking_id, user_id, status, reviewed_on, date, time) VALUES (?, ?, ?, ?, ?, ?)",
                (booking_id, user_id, "Declined", reviewed_on, date, time)
            )
            
            # Show a Text Edit box for feedback message
            feedback_message, ok = QInputDialog.getText(
                self, "Feedback Message", "Type your feedback for the applicant:"
            )
            
            if ok and feedback_message.strip():  # If the user provides a message
                # Insert data into notifications table
                cur.execute(
                    "INSERT INTO notifications (user_id, resource_id, booking_id, message) VALUES (?, ?, ?, ?)",
                    (user_id, resource_id, booking_id, feedback_message.strip())
                )
                conn.commit()
                cur.execute("DELETE FROM bookings WHERE booking_id = ?", (booking_id,))
                conn.commit()
            
            # Remove the row from the table widget
                table = self.ui.tableWidget
                for row in range(table.rowCount()):
                    cell_widget = table.cellWidget(row, 6)  # Assuming column 6 is where the button is
                    if cell_widget:
                        button = cell_widget.findChild(QPushButton)
                        if button and button.text() == "Approve" and button.clicked:  # Match the clicked button
                            table.removeRow(row)
                            break
                QMessageBox.information(self, "Success", f"Booking declined with feedback.")
            else:
                QMessageBox.warning(self, "Warning", "Please provide feedback for the applicant.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to decline booking: {str(e)}")
        finally:
            conn.close()
            
    def handle_approve_button(self, booking_id):
        # Retrieve user_id and resource_id for the given booking_id
        conn, cur = connect_to_db()
        
        # Fetch user_id and resource_id from bookings
        cur.execute("SELECT user_id, resource_id, date, time FROM bookings WHERE booking_id = ?", (booking_id,))
        result = cur.fetchone()
        if not result:
            QMessageBox.warning(self, "Error", f"No booking found for booking_id {booking_id}.")
            return
        
        user_id, resource_id, date, time = result
        
        # Get current timestamp for reviewed_on
        reviewed_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insert data into booking_report
        try:
            cur.execute(
                "INSERT INTO booking_report (booking_id, user_id, status, reviewed_on, date, time) VALUES (?, ?, ?, ?, ?, ?)",
                (booking_id, user_id, "Approved", reviewed_on, date, time)
            )
            
            # Show a Text Edit box for feedback message
            feedback_message, ok = QInputDialog.getText(
                self, "Feedback Message", "Type your feedback for the applicant:"
            )
            
            if ok and feedback_message.strip():  # If the user provides a message
                # Insert data into notifications table
                cur.execute(
                    "INSERT INTO notifications (user_id, resource_id, booking_id, message) VALUES (?, ?, ?, ?)",
                    (user_id, resource_id, booking_id, feedback_message.strip())
                )
                conn.commit()
                cur.execute("INSERT INTO resource_log (resource_id, date, time, available) VALUES (?, ?, ?, ?)", (resource_id, date, time, 0))
                conn.commit()
                cur.execute("DELETE FROM bookings WHERE booking_id = ?", (booking_id,))
                conn.commit()
            
            # Remove the row from the table widget
                table = self.ui.tableWidget
                for row in range(table.rowCount()):
                    cell_widget = table.cellWidget(row, 6)  # Assuming column 6 is where the button is
                    if cell_widget:
                        button = cell_widget.findChild(QPushButton)
                        if button and button.text() == "Approve" and button.clicked:  # Match the clicked button
                            table.removeRow(row)
                            break
                
                QMessageBox.information(self, "Success", f"Booking approved with feedback.")
            else:
                QMessageBox.warning(self, "Warning", "Please provide feedback for the applicant.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to approve booking: {str(e)}")
        finally:
            conn.close()
            
    def handle_flagged_button(self, user_id):
        conn, cur = connect_to_db()
        try:
            cur.execute("UPDATE user SET account_flag = 1 WHERE user_id = ?", (user_id,))
            conn.commit()
            QMessageBox.information(self, "Success", "User account has been flagged for system abuse.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Operation failed: {str(e)}")
            
    def resource_release(self):
        self.ui.plainTextEdit_2.clear()
        self.ui.dateEdit_2.clear()
        self.ui.timeEdit_3.clear()
        self.ui.timeEdit_4.clear()
        self.ui.comboBox_4.setCurrentIndex(0)
        self.ui.comboBox_5.setCurrentIndex(0)
        self.ui.comboBox_6.setCurrentIndex(0)
        conn, cur = connect_to_db()
        notes = self.ui.plainTextEdit_2.toPlainText()
        date = self.ui.dateEdit_2.date().toString("yyyy-MM-dd")
        if date < datetime.today().strftime("%Y-%m-%d"):
                QMessageBox.warning(self, "Error", "You are past this date. Please choose a valid date.")
                return

        # Step 6: Handle resource_id and time
        resource = self.ui.comboBox_4.currentText()
        resource_id = None
        time = None

        if resource == "Classroom":
                    # Extract resource_id from Space combo box
            space = self.ui.comboBox_5.currentText()  # Example: "B2-203"
            resource_id = int(re.sub(r'[^0-9]', '', space))# Convert "B2-203" to 2203

                    # Extract time from the timeslot combo box
            time = self.ui.comboBox_6.currentText()
        else:
            cur.execute("SELECT resource_id FROM resources WHERE resource_type = ?", (resource,))
            resource_row = cur.fetchone()
            if resource_row:
                resource_id = resource_row[0]
            else:
                raise ValueError(f"No resource found for type: {resource}")

                    # Combine start and end times
            start_time = self.ui.timeEdit_3.time().toString("h:mm AP")
            end_time = self.ui.timeEdit_4.time().toString("h:mm AP")
            time = f"{start_time}-{end_time}"
        try:
            cur.execute("SELECT * FROM resource_log WHERE resource_id = ? AND date = ? AND time = ?", (resource_id, date, time))
            existing_entry = cur.fetchone()
            if not existing_entry:
                cur.execute("INSERT INTO resource_log (resource_id, date, time, available) VALUES (?, ?, ?, ?)", (resource_id, date, time, 1))
            else:
                cur.execute("UPDATE resource_log SET available = 1 WHERE resource_id = ? AND date = ? AND time = ?", (resource_id, date, time))
            conn.commit()
            add_notice("Student", notes)
            QMessageBox.information(self, "Success", "Resource released and announced successfully!")
        except Exception as e:
            conn.rollback()
            QMessageBox.warning(self, "Error", f"Failed to release resource: {e}")
        finally:
            conn.close()
    
    def load_application_logs(self):
        try:
            conn, cur = connect_to_db()

            # Fetch the data from bookings and related tables
            query = """
            SELECT booking_report.booking_id, 
                user.full_name, 
                user.roles, 
                notifications.resource_id, 
                booking_report.date, 
                booking_report.time,
                notifications.message,
                booking_report.status
                
            FROM booking_report
            INNER JOIN user ON booking_report.user_id = user.user_id
            INNER JOIN notifications ON booking_report.booking_id = notifications.booking_id
            """
            cur.execute(query)
            results = cur.fetchall()

            # Clear the table first
            self.ui.tableWidget_2.setRowCount(0)

            for row_number, row_data in enumerate(results):
                # Insert a new row
                self.ui.tableWidget_2.insertRow(row_number)

                # Fill data for Applicant, Role, Resource, Date, Time, Notes columns
                booking_id = row_data[0]
                full_name = row_data[1]
                role = row_data[2]
                resource_id = row_data[3]
                date = row_data[4]
                time = row_data[5]
                #notes = row_data[6]
                status = row_data[7]

                # Reverse format Resource ID (e.g., 2203 to B2-203)
                if len(str(resource_id)) == 4:
                    building = f"B{str(resource_id)[0]}"
                    room = str(resource_id)[1:]
                    resource_name = f"{building}-{room}"
                else:
                    result_type = cur.execute("SELECT resource_type FROM resources WHERE resource_id = ?", (resource_id,))
                    resource_name = result_type.fetchone()[0]

                self.ui.tableWidget_2.setItem(row_number, 1, QTableWidgetItem(full_name))
                self.ui.tableWidget_2.setItem(row_number, 2, QTableWidgetItem(role))
                self.ui.tableWidget_2.setItem(row_number, 3, QTableWidgetItem(resource_name))
                self.ui.tableWidget_2.setItem(row_number, 4, QTableWidgetItem(date))
                self.ui.tableWidget_2.setItem(row_number, 5, QTableWidgetItem(time))
                # self.ui.tableWidget_2.setItem(row_number, 6, QTableWidgetItem(notes))

                # Add the Override Status column content
                if status.lower() == "approved":
                    btn_revoke = QPushButton("Revoke")
                    btn_revoke.clicked.connect(lambda _, : self.revoke_booking(resource_id, date, time, booking_id))
                    self.ui.tableWidget_2.setCellWidget(row_number, 0, btn_revoke)
                elif status.lower() == "declined":
                    declined_item = QTableWidgetItem("Declined")
                    declined_item.setTextAlignment(Qt.AlignCenter)  # Center the text
                    self.ui.tableWidget_2.setItem(row_number, 0, declined_item)
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load application logs: {e}")
    
    def revoke_booking(self, resource, date, time, booking_id):
        conn, cur = connect_to_db()
        try:
            cur.execute("UPDATE resource_log SET available = 1 WHERE resource_id = ? AND date = ? AND time = ?", (resource, date, time))
            conn.commit()
            cur.execute("UPDATE booking_report SET status = 'Declined' WHERE booking_id = ?", (booking_id,))
            conn.commit()
            QMessageBox.information(self, "Success", "Booking revoked successfully.")
            self.load_application_logs()
        except Exception as e:
            conn.rollback()
            QMessageBox.warning(self, "Error", f"Failed to revoke booking: {e}")
        finally:
            conn.close()
            
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
            
    def update_widget_states(self):
        # Get selected resource
        selected_resource = self.ui.comboBox.currentText()
        if selected_resource == "Classroom":
            # Disable start_time and end_time
            self.ui.timeEdit.setEnabled(False)
            self.ui.timeEdit_2.setEnabled(False)

            # Enable other widgets
            self.ui.comboBox_2.setEnabled(True)
            self.ui.comboBox_3.setEnabled(True)
            self.ui.dateEdit.setEnabled(True)
        else:
            # Enable start_time and end_time
            self.ui.timeEdit.setEnabled(True)
            self.ui.timeEdit_2.setEnabled(True)
            self.ui.dateEdit.setEnabled(True)
            # Disable other widgets
            self.ui.comboBox_2.setEnabled(False)
            self.ui.comboBox_3.setEnabled(False)  
            
    def update_widget_states_c(self):
        selected_resource = self.ui.comboBox_4.currentText()
        if selected_resource == "Classroom":
            # Disable start_time and end_time
            self.ui.timeEdit_3.setEnabled(False)
            self.ui.timeEdit_4.setEnabled(False)

            # Enable other widgets
            self.ui.comboBox_5.setEnabled(True)
            self.ui.comboBox_6.setEnabled(True)
            self.ui.dateEdit_2.setEnabled(True)
        else:
            # Enable start_time and end_time
            self.ui.timeEdit_3.setEnabled(True)
            self.ui.timeEdit_4.setEnabled(True)
            self.ui.dateEdit_2.setEnabled(True)
            # Disable other widgets
            self.ui.comboBox_5.setEnabled(False)
            self.ui.comboBox_6.setEnabled(False)  
   
    def load_notifications(self):
        try:
            user_id = self.current_session.user_id # Retrieve the logged-in user's ID
            if not user_id:
                raise ValueError("User not logged in.")

            conn, cur = connect_to_db()

            # Query to fetch all notifications related to the logged-in user
            query = """
            SELECT
                n.booking_id,
                n.message,
                br.reviewed_on,
                br.date,
                br.time,
                br.status,
                r.resource_id
            FROM notifications n
            JOIN booking_report br ON n.booking_id = br.booking_id
            JOIN resources r ON r.resource_id = n.resource_id
            WHERE n.user_id = ?
            """
            cur.execute(query, (user_id,))
            notifications = cur.fetchall()
            print(f"Notifications: {notifications}, User ID: {user_id}")
            # Clear the table widget before loading new data
            self.ui.tableWidget_6.setRowCount(0)

            # Populate the table widget
            for row_number, row_data in enumerate(notifications):
                booking_id, message, reviewed_on, date, time, status, resource_id = row_data

                # Reverse format resource_id (e.g., "2203" -> "B2-203")
                if len(str(resource_id)) == 4:
                    building = f"B{str(resource_id)[0]}"
                    room = str(resource_id)[1:]
                    resource_name = f"{building}-{room}"
                else:
                    result_type = cur.execute("SELECT resource_type FROM resources WHERE resource_id = ?", (resource_id,))
                    resource_name = result_type.fetchone()[0]

                # Add rows to the table widget
                self.ui.tableWidget_6.insertRow(row_number)

                # Set columns in order: Reviewed On, Resource, Date, Time, Status, Feedback
                self.ui.tableWidget_6.setItem(row_number, 0, QTableWidgetItem(reviewed_on))
                self.ui.tableWidget_6.setItem(row_number, 1, QTableWidgetItem(resource_name))
                self.ui.tableWidget_6.setItem(row_number, 2, QTableWidgetItem(date))
                self.ui.tableWidget_6.setItem(row_number, 3, QTableWidgetItem(time))
                self.ui.tableWidget_6.setItem(row_number, 4, QTableWidgetItem(status))
                self.ui.tableWidget_6.setItem(row_number, 5, QTableWidgetItem(message))

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load notifications: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()


        
def load_stylesheet(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
def dayFromdate(date):
    date="2024,12,19"
    date = date.split(",")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    date_object = datetime(year, month, day).date()
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
