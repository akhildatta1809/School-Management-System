from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
import mysql.connector as con
from datetime import date
import datetime
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors

ui, _ = loadUiType('school.ui')

class Mainapp(QMainWindow,ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)


        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.menuBar().setVisible(False)
        self.b01.clicked.connect(self.login)
        self.b12.clicked.connect(self.save_student_details)
        self.menu11.triggered.connect(self.add_new_student_tab)
        self.menu12.triggered.connect(self.edit_or_delete_student_tab)
        self.menu21.triggered.connect(self.add_update_delete_marks_tab)
        self.menu31.triggered.connect(self.add_update_delete_attendence_tab)
        self.menu41.triggered.connect(self.add_edit_delete_fee_tab)
        self.b31.clicked.connect(self.fill_details_in_form_of_selected_registration_number)
        self.b32.clicked.connect(self.update_student_details)
        self.b33.clicked.connect(self.delete_student_details)
        self.b34.clicked.connect(self.reset)
        self.b41.clicked.connect(self.insert_marks_of_student)
        self.b42.clicked.connect(self.get_marks)
        self.b43.clicked.connect(self.update_marks_of_student)
        self.b44.clicked.connect(self.delete_marks_of_student)
        self.b45.clicked.connect(self.reset_marks)
        self.b51.clicked.connect(self.insert_attendence)
        self.txt55.currentIndexChanged.connect(self.get_dates)
        self.b52.clicked.connect(self.get_attendence)
        self.b53.clicked.connect(self.update_attendence)
        self.b54.clicked.connect(self.delete_attendence)
        self.b61.clicked.connect(self.add_fee_details)
        self.b62.clicked.connect(self.get_fee_details)
        self.b63.clicked.connect(self.update_fee_details)
        self.b63.clicked.connect(self.update_fee_details)
        self.b64.clicked.connect(self.delete_fee_details)
        self.b65.clicked.connect(self.reset_fee)
        self.menu51.triggered.connect(self.show_reports)
        self.menu52.triggered.connect(self.show_reports)
        self.menu53.triggered.connect(self.show_reports)
        self.menu54.triggered.connect(self.show_reports)
        self.b91.clicked.connect(self.print_pdf)
        self.b92.clicked.connect(self.cancel_print)
        self.menu61.triggered.connect(self.logout)
######### Login Method ################  
    def login(self):
        username = self.tb01.text()
        password = self.tb02.text()
        if(username =="admin" and password =="admin"):
            self.menuBar().setVisible(True)
            self.tabWidget.setCurrentIndex(1)
        else:
            QMessageBox.information(self,"School Management System","Invalid Credentials,Try again !")
            self.l01.setText("Invalid Credentials,Try again !")
############### Login ####################    
############### Student Insert #######    
    def add_new_student_tab(self):
        self.tabWidget.setCurrentIndex(2)
        self.fill_next_registration_number()
        
    def fill_next_registration_number(self):
        try:
            rn = 0
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()
            cursor.execute("select * from student")
            result = cursor.fetchall()
            
            if result:
                for stud in result:
                    rn = stud[0]
            self.tb11.setText(str(rn+1))
        except con.Error as e:
            print("Connction error"+f"{e}")
    def save_student_details(self):
        
        try:
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()
            registration_number = self.tb11.text()
            full_name = self.tb12.text()
            gender = self.cb11.currentText()
            date_of_birth = self.tb13.text()
            age = self.tb14.text()
            address = self.txb11.toPlainText()
            phone = self.tb15.text()
            email = self.tb16.text()
            standard = self.cb12.currentText()
            if registration_number == "":
                QMessageBox.information(self,"School Management System","registration number must not be Empty")
            elif full_name == "":
                QMessageBox.information(self,"School Management System","full_name must not be Empty")
            elif date_of_birth == "":
                QMessageBox.information(self,"School Management System","date of birth must not be Empty")
            elif age == "":
                QMessageBox.information(self,"School Management System"," age must not be Empty")
            elif address == "":
                QMessageBox.information(self,"School Management System"," address must not be Empty")
            elif phone == "":
                QMessageBox.information(self,"School Management System","phone must not be Empty")
            elif email == "":
                QMessageBox.information(self,"School Management System","email must not be Empty")
            
            else:
                qry = "insert into student (registration_number,full_name,gender,date_of_birth,age,address,phone,email,standard) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                values=(registration_number,full_name,gender,date_of_birth,age, address,phone,email,standard)
                cursor.execute(qry,values)
                mydb.commit()
                self.l11.setText("Student Inserted Successfully")
                QMessageBox.information(self,"School Management System","Student Inserted Successfully")
                self.fill_next_registration_number()
                full_name = self.tb12.setText("")
                gender = self.cb11.setCurrentIndex(0)
                date_of_birth = self.tb13.setText("")
                age = self.tb14.setText("")
                address = self.txb11.setText("")              
                phone = self.tb15.setText("")
                email = self.tb16.setText("")
                standard = self.cb12.setCurrentIndex(0)

        except con.Error:
            self.l11.setText("Student Not Inserted Successfully")
            QMessageBox.information(self,"School Management System","Student not Inserted")





############### Student Insert #######    
############### Edit or Delete student#########
    def edit_or_delete_student_tab(self):
        self.tabWidget.setCurrentIndex(3)
        self.fill_registration_numbers()
    def fill_details_in_form_of_selected_registration_number(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()
            cursor.execute("select * from student where id="+str(self.txt31.currentText()))
            result = cursor.fetchall()
            if result:
                for stud in result:
                    self.txt32.setText(f"{stud[2]}")
                    self.txt33.setText(f"{stud[3]}")
                    self.txt34.setText(f"{stud[4]}")
                    self.txt35.setText(f"{stud[5]}")
                    self.mtxt31.setText(f"{stud[6]}")
                    self.txt36.setText(f"{stud[7]}")
                    self.txt37.setText(f"{stud[8]}")
                    if stud[9] == "First Standard":
                        self.cmb32.setCurrentIndex(0)
                    elif stud[9] == "Second Standard":
                        self.cmb32.setCurrentIndex(1)
                    elif stud[9] == "Third Standard":
                        self.cmb32.setCurrentIndex(2)
                    elif stud[9] == "Fourth Standard":
                        self.cmb32.setCurrentIndex(3)
                    elif stud[9] == "Fifth Standard":
                        self.cmb32.setCurrentIndex(4)
                    elif stud[9] == "Sixth Standard":
                        self.cmb32.setCurrentIndex(5)
                    elif stud[9] == "Seventh Standard":
                        self.cmb32.setCurrentIndex(6)
                    elif stud[9] == "Eighth Standard":
                        self.cmb32.setCurrentIndex(7)
                    elif stud[9] == "Ninth Standard":
                        self.cmb32.setCurrentIndex(8)
                    elif stud[9] == "Tenth Standard":
                        self.cmb32.setCurrentIndex(9)
                    elif stud[9] == "11th Standard":
                        self.cmb32.setCurrentIndex(10)
                    else: 
                        self.cmb32.setCurrentIndex(11)
                    
        except con.Error as e:
            QMessageBox.information(self,"School Management System","Valid Registration Number")
    def reset(self):
        self.txt31.setCurrentIndex(0)
        self.txt32.setText("")
        self.txt33.setText("")
        self.txt34.setText("")
        self.txt35.setText("")
        self.mtxt31.setText("")
        self.txt36.setText("")
        self.txt37.setText("")
        self.cmb32.setCurrentIndex(0)
    def fill_registration_numbers(self):
        mydb = con.connect(host="localhost",user="root",password="",db="school")
        cursor = mydb.cursor()
        cursor.execute("select * from student")
        result = cursor.fetchall()
        self.txt31.clear()
        self.txt41.clear()
        self.txt49.clear()
        self.txt51.clear()
        self.txt55.clear()
        self.txt62.clear()
        if result:
            for stud in result:
                self.txt31.addItem(stud[1])
                self.txt41.addItem(stud[1])
                self.txt49.addItem(stud[1])
                self.txt51.addItem(stud[1])
                self.txt55.addItem(stud[1])
                self.txt62.addItem(stud[1])
    def update_student_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()
            registration_number = str(self.txt31.currentText())
            full_name = self.txt32.text()
            gender = self.txt33.text()
            date_of_birth = self.txt34.text()
            age = self.txt35.text()
            address = self.mtxt31.toPlainText()
            phone = self.txt36.text()
            email = self.txt37.text()
            standard = self.cmb32.currentText()
            if registration_number == "":
                QMessageBox.information(self,"School Management System","registration number must not be Empty")
            elif full_name == "":
                QMessageBox.information(self,"School Management System","full_name must not be Empty")
            elif date_of_birth == "":
                QMessageBox.information(self,"School Management System","date of birth must not be Empty")
            elif age == "":
                QMessageBox.information(self,"School Management System"," age must not be Empty")
            elif address == "":
                QMessageBox.information(self,"School Management System"," address must not be Empty")
            elif phone == "":
                QMessageBox.information(self,"School Management System","phone must not be Empty")
            elif email == "":
                QMessageBox.information(self,"School Management System","email must not be Empty")

            else:
                
                qry = f"UPDATE student SET full_name='{full_name}',gender='{gender}',date_of_birth='{date_of_birth}',age='{age}',address='{address}',phone='{phone}',email='{email}',standard='{standard}' WHERE registration_number='{registration_number}'"
                cursor.execute(qry)
                mydb.commit()
                self.l31.setText("Student Updated Successfully")
                QMessageBox.information(self,"School Management System","Student Updated Successfully")
                self.reset()

        except con.Error as e:
            self.l31.setText("Student Not Updated Successfully")
            QMessageBox.information(self,"School Management System",f"{e}")
            print(e)

    def delete_student_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()
            registration_number = str(self.txt31.currentText())
            qry = f"DELETE FROM student WHERE registration_number='{registration_number}'"
            cursor.execute(qry)
            mydb.commit()
            self.l31.setText("Student Deleted Successfully")
            QMessageBox.information(self,"School Management System","Student Deleted Successfully")
            self.reset()
        except con.Error as e:
            self.l31.setText("Student Not Deleted Successfully")
            QMessageBox.information(self,"School Management System",f"{e}")
# ======================================Edit or Delete Student============================
# ==========================================Marks CRUD===========================
    def add_update_delete_marks_tab(self):
        self.tabWidget.setCurrentIndex(4)
        self.fill_registration_numbers()
    def insert_marks_of_student(self):
        registration_number = self.txt41.currentText()
        exam_name = self.txt42.currentText()
        language = self.txt43.text()
        hindi = self.txt44.text()
        english = self.txt45.text()
        maths= self.txt46.text()
        science =self.txt47.text()
        social =self.txt48.text()
        if language == "" or hindi =="" or english == "" or maths == "" or science == "" or social == "":
            QMessageBox.information(self,"School Management System","All Fields Are Required !")
        else:
            try:
                exist = False
                mydb = con.connect(host="localhost",user="root",password="",db="school")
                cursor = mydb.cursor()
                qry1 = f"SELECT exam_name FROM mark WHERE registration_number='{registration_number}'"
                cursor.execute(qry1)
                result = cursor.fetchall()
                if result:
                    for mark in result:
                        if mark[0] == exam_name:
                            exist = True
                            break
                if exist:
                    QMessageBox.information(self,"School Management System",f"Registration Number:{registration_number} marks of {exam_name} already Exist")
                else:           
                    qry = f"INSERT INTO mark(registration_number, exam_name, language, hindi, english, maths, science, social) VALUES ('{registration_number}','{exam_name}','{language}','{hindi}','{english}','{maths}','{science}','{social}')"
                    cursor.execute(qry)
                    mydb.commit()
                    self.l41.setText("Marks inserted Successfully")
                    QMessageBox.information(self,"School Management System","Marks Inserted Successfully")
                    self.txt41.setCurrentIndex(0)
                    self.txt42.setCurrentIndex(0)
                    self.txt43.setText("")
                    self.txt44.setText("")
                    self.txt45.setText("")
                    self.txt46.setText("")
                    self.txt47.setText("")
                    self.txt48.setText("")
            except con.Error as e:
                self.l41.setText("Marks not inserted")
                QMessageBox.information(self,"School Management System",f"{e}")
    def update_marks_of_student(self):
        registration_number = self.txt49.currentText()
        exam_name = self.txt410.currentText()
        language = self.txt411.text()
        hindi = self.txt412.text()
        english = self.txt413.text()
        maths= self.txt414.text()
        science =self.txt415.text()
        social =self.txt416.text()
        if language == "" or hindi =="" or english == "" or maths == "" or science == "" or social == "":
            QMessageBox.information(self,"School Management System","All Fields Are Required !")
        else:
            try:
                mydb = con.connect(host="localhost",user="root",password="",db="school")
                cursor = mydb.cursor()

                qry = f"UPDATE mark SET  language='{language}', hindi='{hindi}', english='{english}', maths='{maths}', science='{science}', social='{social}' WHERE registration_number ='{registration_number}' AND exam_name = '{exam_name}'"
                cursor.execute(qry)
                mydb.commit()
                self.l42.setText("Marks updated Successfully")
                QMessageBox.information(self,"School Management System","Marks updated Successfully")
                self.txt49.setCurrentIndex(0)
                self.txt410.setCurrentIndex(0)
                self.txt411.setText("")
                self.txt412.setText("")
                self.txt413.setText("")
                self.txt414.setText("")
                self.txt415.setText("")
                self.txt416.setText("")
            except con.Error as e:
                self.l42.setText("Marks not inserted")
                QMessageBox.information(self,"School Management System",f"{e}")
    def delete_marks_of_student(self):
        registration_number = self.txt49.currentText()
        exam_name = self.txt410.currentText()

        try:
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()

            qry = f"DELETE FROM mark WHERE registration_number='{registration_number}' AND exam_name='{exam_name}'"
            cursor.execute(qry)
            mydb.commit()
            self.l42.setText("Marks Deleted Successfully")
            QMessageBox.information(self,"School Management System","Marks Deleted Successfully")
            self.txt49.setCurrentIndex(0)
            self.txt410.setCurrentIndex(0)
            self.txt411.setText("")
            self.txt412.setText("")
            self.txt413.setText("")
            self.txt414.setText("")
            self.txt415.setText("")
            self.txt416.setText("")
        except con.Error as e:
            self.l42.setText("Marks not inserted")
            QMessageBox.information(self,"School Management System",f"{e}")
    def get_marks(self):
        registration_number = self.txt49.currentText()
        exam_name = self.txt410.currentText()
        try:
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()

            qry = f"SELECT * FROM mark WHERE registration_number='{registration_number}' AND exam_name='{exam_name}'"
            cursor.execute(qry)
            result = cursor.fetchall()
            if result:
                for stud in result:
                    self.txt411.setText(str(stud[3]))
                    self.txt412.setText(str(stud[4]))
                    self.txt413.setText(str(stud[5]))
                    self.txt414.setText(str(stud[6]))
                    self.txt415.setText(str(stud[7]))
                    self.txt416.setText(str(stud[8]))
        except con.Error as e:
            self.l42.setText("Marks not Updated")
            QMessageBox.information(self,"School Management System",f"{e}")
    def reset_marks(self):
        self.txt49.setCurrentIndex(0)
        self.txt410.setCurrentIndex(0)
        self.txt411.setText("")
        self.txt412.setText("")
        self.txt413.setText("")
        self.txt414.setText("")
        self.txt415.setText("")
        self.txt416.setText("")
# ============================Marks CRUD=========================
# ============================Attendence CRUD====================
    def add_update_delete_attendence_tab(self):
        self.tabWidget.setCurrentIndex(5)
        self.fill_registration_numbers()
        self.add_date_to_attendence()
    def add_date_to_attendence(self):
        today = date.today()
        TodayDate= today.strftime("%b-%d-%Y")
        self.txt52.setText(f"{TodayDate}")
    def insert_attendence(self):
        registration_number = self.txt51.currentText()
        date = self.txt52.text()
        morning=self.txt53.currentText()
        afternoon=self.txt54.currentText()
        try:
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()

            qry = f"INSERT INTO attendence (registration_number,date,morning,afternoon) VALUES ('{registration_number}','{date}','{morning}','{afternoon}')"
            cursor.execute(qry)
            mydb.commit()
            self.l51.setText("Attendence Inserted Successfully")
            QMessageBox.information(self,"School Management System","Attendence Inserted Successfully")
            self.txt51.setCurrentIndex(0)
            self.add_date_to_attendence()
            self.txt53.setCurrentIndex(0)
            self.txt54.setCurrentIndex(0)
            self.get_dates()

        except con.Error as e:
            self.l42.setText("Marks not inserted")
            QMessageBox.information(self,"School Management System",f"{e}")
    def update_attendence(self):
        registration_number = self.txt55.currentText()
        date = self.txt56.currentText()
        morning=self.txt57.currentText()
        afternoon=self.txt58.currentText()
        try:
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()

            qry = f"UPDATE attendence SET morning='{morning}',afternoon='{afternoon}' WHERE registration_number='{registration_number}' AND date='{date}'"
            cursor.execute(qry)
            mydb.commit()
            self.l52.setText("Attendence Updated Successfully")
            QMessageBox.information(self,"School Management System","Attendence Updated Successfully")
            self.txt55.setCurrentIndex(0)
            self.txt56.setCurrentIndex(0)
            self.txt57.setCurrentIndex(0)

        except con.Error as e:
            self.l42.setText("Marks not Updated")
            QMessageBox.information(self,"School Management System",f"{e}")
    def delete_attendence(self):
        registration_number = self.txt55.currentText()
        try:
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()

            qry = f"DELETE FROM attendence WHERE registration_number='{registration_number}'"
            cursor.execute(qry)
            mydb.commit()
            self.l52.setText("Attendence Updated Successfully")
            QMessageBox.information(self,"School Management System","Attendence Updated Successfully")
            self.txt55.setCurrentIndex(0)
            self.txt56.setCurrentIndex(0)
            self.txt57.setCurrentIndex(0)

        except con.Error as e:
            self.l42.setText("Marks not Updated")
            QMessageBox.information(self,"School Management System",f"{e}")
    def get_dates(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()
            registration_number = self.txt55.currentText()

            qry = f"SELECT date from  attendence WHERE registration_number='{registration_number}'"
            cursor.execute(qry)
            result = cursor.fetchall()
            self.txt56.clear()
            if result:
                for date in result:
                    self.txt56.addItem(str(date[0])) 
            mydb.commit()

        except con.Error as e:
            QMessageBox.information(self,"Student Management System",f"{e}")
    def get_attendence(self):
        try:  
             
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()
            registration_number = self.txt55.currentText()
            date = self.txt56.currentText()
            qry=f"SELECT morning,afternoon from attendence WHERE registration_number='{registration_number}' AND date='{date}'"
            cursor.execute(qry)
            result=cursor.fetchall()
            if result:
                for attendence in result:
                    if attendence[0] == "Present":
                        self.txt57.setCurrentIndex(0)
                    else:
                        self.txt57.setCurrentIndex(1)
                    if attendence[1] == "Present":
                        self.txt58.setCurrentIndex(0)
                    else:
                        self.txt58.setCurrentIndex(1)
            mydb.commit()
            mydb.close()
        except con.Error as e:
            QMessageBox.information(self,"School Management System",f"{e}")
# ============================Attendence CRUD==================== 
# ===========================Fee CRUD ===========================
    def add_edit_delete_fee_tab(self):
        self.tabWidget.setCurrentIndex(6)
        self.fill_registration_numbers()
        self.add_reciept_number()
        
    def add_reciept_number(self):
        x = datetime.datetime.now()
        reciept_number=x.strftime("%Y"+"%m"+"%d"+"%H"+"%M"+"%S")
        date=x.strftime("%d"+"%m"+"%Y")
        self.txt61.setText("REF"+str(reciept_number))
        self.txt61.setReadOnly(True)
        self.txt65.setText(str(date))
        self.txt65.setReadOnly(True)
    def add_fee_details(self):
        try:  
            exist = False  
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()
            reciept_number = self.txt61.text()
            registration_number = self.txt62.currentText()
            reason = self.txt63.currentText()
            ammount = self.txt64.text()
            date = self.txt65.text()
            qry1 = f"SELECT fee_payment_reason,reciept_number FROM fee WHERE registration_number = '{registration_number}'"
            cursor.execute(qry1)
            result = cursor.fetchall()
            if reason == "Exam Fee" or reason == "School Fee":
                if result:
                    for fee in result:
                        if fee[0] == reason:
                            searched_reciept_number = fee[1]
                            exist = True
                            break
            if exist:
                QMessageBox.information(self,"School Management System",f"Registration Number: {registration_number} already paid fee Reciept number:{searched_reciept_number}")
                self.l61.setText(f"Reciept:{searched_reciept_number}")
            else:           
                qry = f"INSERT INTO fee (reciept_number ,registration_number,fee_payment_reason,amount,date) VALUES ('{reciept_number}','{registration_number}','{reason}','{ammount}','{date}')"
                cursor.execute(qry)
                
                mydb.commit()
                self.add_reciept_number()
                self.txt62.setCurrentIndex(0)
                self.txt63.setCurrentIndex(0)
                self.txt64.setText("")
                QMessageBox.information(self,"School Management System","Inserted Successfully")
                self.l81.setText(str(reciept_number))
                self.l82.setText(str(date))
                self.l86.setText(str(date))
                self.l85.setText(str(reason))
                self.l84.setText(str(ammount))
                qry1=f"SELECT full_name FROM student where registration_number = '{registration_number}'"
                cursor.execute(qry1)
                result = cursor.fetchone()
                self.l83.setText(str(result[0]))
                self.tabWidget.setCurrentIndex(8)
        except con.Error as e:
            QMessageBox.information(self,"School Management System",f"{e}")
    def get_fee_details(self):
        self.txt66.setReadOnly(True)
        try:    
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()
            reciept_number = self.txt66.text()
            qry = f"SELECT * from fee WHERE reciept_number = '{reciept_number}'"
            cursor.execute(qry)
            result = cursor.fetchall()
            if result:
                for res in result:
                   self.txt67.setText(res[1])
                   self.txt68.setText(res[3]) 
                   self.txt69.setText(res[4])
                   self.txt70.setText(res[5]) 
        except con.Error as e:
            QMessageBox.information(self,"School Management System",f"{e}")
    def update_fee_details(self):
        try:    
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()
            reciept_number = self.txt66.text()
            registration_number = self.txt67.text()
            reason = self.txt68.text()
            ammount = self.txt69.text()
            date = self.txt70.text()
            qry = f"UPDATE fee SET registration_number='{registration_number}',fee_payment_reason = '{reason}',amount='{ammount}',date = '{date}'  WHERE reciept_number='{reciept_number}'"
            cursor.execute(qry)
            mydb.commit()
            mydb.close()
            QMessageBox.information(self,"School Management System","Updated Successfully.")
            self.txt66.setText("")
            self.txt67.setText("")
            self.txt68.setText("")
            self.txt69.setText("")
            self.txt70.setText("")
            self.txt66.setReadOnly(False)
        except con.Error as e:
            QMessageBox.information(self,"School Management System",f"{e}")
    def reset_fee(self):
        self.txt66.setText("")
        self.txt67.setText("")
        self.txt68.setText("")
        self.txt69.setText("")
        self.txt70.setText("")
        self.txt66.setReadOnly(False)
    def delete_fee_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()
            reciept_number = self.txt66.text()
            qry = f"DELETE FROM fee WHERE reciept_number='{reciept_number}'"
            cursor.execute(qry)
            mydb.commit()
            mydb.close()
            QMessageBox.information(self,"School Management System","Deleted Successfully")
            self.txt66.setText("")
            self.txt67.setText("")
            self.txt68.setText("")
            self.txt69.setText("")
            self.txt70.setText("")
            self.txt66.setReadOnly(False)
        except con.Error as e:
            QMessageBox.information(self,"School Management System",f"{e}")
    
    
    
    
    def print_pdf(self):
        RecieptNumber = self.l81.text()
        Date = self.l82.text()
        Name = self.l83.text()
        Reason = self.l85.text()
        Amount = self.l84.text()
        data = [
        ["School Management System"],
        ["Reciept Number:", f"{RecieptNumber}"],
        ["Name:" ,f"{Name}"],
        ["Reason:" ,f"{Reason}"],
        ["Amount:",f"{Amount}"],
        ["Date",f"{Date}"]]
        fileName = f"Reports/{RecieptNumber}.pdf"
        pdf = SimpleDocTemplate(
                fileName,
                pagesize=letter)
        table = Table(data)
        style = TableStyle([
                ('BACKGROUND', (0,0), (3,0), colors.green),
                ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),

                ('ALIGN',(0,0),(-1,-1),'CENTER'),

                ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 14),

                ('BOTTOMPADDING', (0,0), (-1,0), 12),

                ('BACKGROUND',(0,1),(-1,-1),colors.beige)])
        table.setStyle(style)
        rowNumb = len(data)
        for i in range(1, rowNumb):
            if i % 2 == 0:
                bc = colors.burlywood
            else:
                bc = colors.beige
            
            ts = TableStyle(
                [('BACKGROUND', (0,i),(-1,i), bc)]
            )
            table.setStyle(ts)
        ts = TableStyle(
            [('BOX',(0,0),(-1,-1),2,colors.black),
            ('LINEBEFORE',(2,1),(2,-1),2,colors.red),
            ('LINEABOVE',(0,2),(-1,2),2,colors.green),
            ('GRID',(0,1),(-1,-1),2,colors.black),])
        table.setStyle(ts)

        elems = []
        elems.append(table)

        pdf.build(elems)

        QMessageBox.information(self,"School Management System","Pdf Generated")
    
    def cancel_print(self):
        self.tabWidget.setCurrentIndex(1)
# ==================================================Fee CRUD==========================================
# ==================================================REPORTS===========================================
    def show_reports(self):
        table_name = self.sender()
        self.tabWidget.setCurrentIndex(7)
        self.l71.setText(str(table_name.text()))
        try:
            self.ReportsTable.setRowCount(0)
        # ===============================Student Reports==========================
            if table_name.text() == "Student Reports":
                mydb = con.connect(host="localhost",user="root",password="",db="school")
                cursor = mydb.cursor()
                qry = "SELECT registration_number,full_name,gender,date_of_birth,age,address,phone,email,standard FROM student"
                cursor.execute(qry)
                result = cursor.fetchall()
                r = 0
                c = 0
                for row_number,row_data in enumerate(result):
                    r+=1
                    c=0
                    for row_number,data in enumerate(row_data):
                        c+=1
                self.ReportsTable.clear()
                self.ReportsTable.setColumnCount(c)
                for row_number,row_data in enumerate(result):
                    self.ReportsTable.insertRow(row_number)
                    for column_number,data in enumerate(row_data):
                        self.ReportsTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))
                
                self.ReportsTable.setHorizontalHeaderLabels(['Register Number','Full Name','Gender','Date Of Birth','Age','Address','Phone','Email','Standard'])
        # ================================================Attendence Report================================
            if table_name.text() == "Attendence Report":
                mydb = con.connect(host="localhost",user="root",password="",db="school")
                cursor = mydb.cursor()
                qry = "SELECT registration_number,date,morning,afternoon FROM attendence"
                cursor.execute(qry)
                result = cursor.fetchall()
                r = 0
                c = 0
                for row_number,row_data in enumerate(result):
                    r+=1
                    c=0
                    for row_number,data in enumerate(row_data):
                        c+=1
                self.ReportsTable.clear()
                self.ReportsTable.setColumnCount(c)
                for row_number,row_data in enumerate(result):
                    self.ReportsTable.insertRow(row_number)
                    for column_number,data in enumerate(row_data):
                        self.ReportsTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))
                self.ReportsTable.setHorizontalHeaderLabels(['Register Number','Date','Morning','Afternoon'])
        # =============================Marks=============================================
            if table_name.text() == "Marks Report":
                mydb = con.connect(host="localhost",user="root",password="",db="school")
                cursor = mydb.cursor()
                qry = "SELECT registration_number,exam_name,language,hindi,english,maths,science,social FROM mark"
                cursor.execute(qry)
                result = cursor.fetchall()
                r = 0
                c = 0
                for row_number,row_data in enumerate(result):
                    r+=1
                    c=0
                    for row_number,data in enumerate(row_data):
                        c+=1
                self.ReportsTable.clear()
                self.ReportsTable.setColumnCount(c)
                for row_number,row_data in enumerate(result):
                    self.ReportsTable.insertRow(row_number)
                    for column_number,data in enumerate(row_data):
                        self.ReportsTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))
                self.ReportsTable.setHorizontalHeaderLabels(['Register Number','Exam Name','Language','Hindi','English','Maths','Science','Social'])
            # =================================Fees Report===================
            if table_name.text() == "Fees Report":
                mydb = con.connect(host="localhost",user="root",password="",db="school")
                cursor = mydb.cursor()
                qry = "SELECT registration_number,reciept_number,fee_payment_reason,amount,date FROM fee"
                cursor.execute(qry)
                result = cursor.fetchall()
                r = 0
                c = 0
                for row_number,row_data in enumerate(result):
                    r+=1
                    c=0
                    for row_number,data in enumerate(row_data):
                        c+=1
                self.ReportsTable.clear()
                self.ReportsTable.setColumnCount(c)
                for row_number,row_data in enumerate(result):
                    self.ReportsTable.insertRow(row_number)
                    for column_number,data in enumerate(row_data):
                        self.ReportsTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))
                self.ReportsTable.setHorizontalHeaderLabels(['Register Number','Reciept Number','Fee Payment Reason','Amount','Date'])
        except con.Error as e:
            QMessageBox.information(self,"School Management System",f"{e}")
    def logout(self):
            self.menuBar().setVisible(False)
            self.tabWidget.setCurrentIndex(0)
            self.tb01.setText("")
            self.tb02.setText("")

# ==================================================REPORTS===========================================
def main():
    app = QApplication(sys.argv)
    window = Mainapp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()