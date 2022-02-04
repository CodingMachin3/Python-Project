import datetime
import math
import time
import tkinter
# root = tkinter.Tk()
# root.withdraw()
import PyPDF2
from tkinter import filedialog
import sqlite3
import os
import csv

# To password protect a file
global filename
class Project:


# The driver function
    def protect(filename, password):


        fn= filename + ".pdf"

        x = datetime.datetime.now()
# Exception handling for if the file is not present
        try:
            pdf_in_file= open(fn,'rb')
        except:
            print("File "+filename+ " is not present")
            return
        inputpdf = PyPDF2.PdfFileReader(pdf_in_file)
        pages_no = inputpdf.numPages
        output= PyPDF2.PdfFileWriter()

# To copy and password protect the contents of the pdf

        for i in range(pages_no):
            inputpdf= PyPDF2.PdfFileReader(pdf_in_file)
            output.addPage(inputpdf.getPage(i))
            output.encrypt(password)

 # new file naming plus the date time stamp
        t = time.localtime()
        ctime= time.strftime("%H;%M", t)
        dt = ""
        dt = dt + str(x.day) + "-" + str(x.month) + "-" + str(x.year)+"_"+str(ctime)

        fn = filename+"-password-protected-"+dt + ".pdf"

        with open(fn,'wb') as outputStream:
            output.write(outputStream)

        pdf_in_file.close()
        print("SUCCESSFULLY CREATED PROTECTED PDF")
        sqlDB.Database(filename)




#------------------------------------------------------------#


# Creating information regarding the file
# class database
# Creating database to store data about the files
class sqlDB:

    def CreateDB():
        conn =sqlite3.connect("Database.db")
        query = """create table details ("Filename" text, "Filesize in KB" integer, "Time" text, "Password" text)"""
        execution = conn.execute(query)
        conn.commit()
        conn.close()
        print("SUCCESSFULLY CREATED DATABASE")
    def my_db(query, db,data):
            conn=sqlite3.connect(db)
            execution=conn.execute(query,data)
            db_data=execution.fetchall()
            print(db_data)
            conn.commit()
            conn.close()
            print("SUCCESSFULLY UPDATED DATABASE")

#   Create and update database automatically
    def Database(filename):
        file_size = os.path.getsize(filename+".pdf")/1024
        file_size=math.trunc(file_size)
# conditional statements so if database is already present only append to it not create new
        if os.path.isfile("Database.db") is True :
            data = (filename, file_size, ctime, password)
            db = "Database.db"
            query = """insert into details values (?,?,?,?);"""
            sqlDB.my_db(query, db, data)
            CSVdatabase.MaintainCSV(filename, file_size)
        else:
            sqlDB.CreateDB()
            data = (filename, file_size, ctime, password)
            db="Database.db"
            query = """insert into details values (?,?,?,?);"""
            sqlDB.my_db(query,db,data)
            CSVdatabase.MaintainCSV(filename,file_size)

#--------------------------------------------------------------------------
# creating csv file
class CSVdatabase:
    def MaintainCSV(filename, file_size):
#conditional statement to check if csv is already present or not if yes then append to it
            if os.path.isfile("database.csv") is False :
                with open("database.csv", "a", newline="") as file_obj:
                    obj = csv.writer(file_obj)
                    obj.writerow(["FileName", "FileSize", "Time of encryption", "Password", "Email id"])
                    email = input("Enter your email ID: ")
                    obj.writerow([filename, file_size, ctime, password, email])
            else:
                with open("database.csv", "a", newline="") as file_obj:
                    obj = csv.writer(file_obj)
                    email = input("Enter your email ID: ")
                    obj.writerow([filename, file_size, ctime, password, email])

            # email= input("Enter your email ID: ")
            # obj.writerow([filename,file_size,ctime, password,email])
            print("CSV file updated successfully")

# -------------------------------------------------------
#Driver class
# which will call all the remaining classes
class main:
    def Input_Values(filename):
        global ch
        ch=1
        global password
        password = input("Create password of your choice: ")
        global ctime
        ctime=""
        if filename=="" or password=="":
            print ("ERROR Input a valid filename or password")
            ch=0
        if ch==1:
            Project.protect(filename, password)


    def Select_file():

        file_name=filedialog.askopenfilename()
        base_file_name=os.path.basename(file_name)
        filename=os.path.splitext(base_file_name)[0]
        main.Input_Values(filename)


# ----------------------------------------------------
#choose method of choosing a file
# Execution begins here
# global filename
choice= input("Enter 1 if you want to select file from computer \nEnter 2 if you want to input the directory name\n")
if choice =="1" :
    main.Select_file()
if choice == "2":
    file_name = input("Enter the pdf name (without extension): ")
    base_file_name = os.path.basename(file_name)
    filename = os.path.splitext(base_file_name)[0]
    main.Input_Values(filename)




