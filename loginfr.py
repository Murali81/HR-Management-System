# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 18:10:28 2017
@author: lenovo2
"""

from Tkinter import *
import tkMessageBox
#import time
import base64
from subprocess import Popen
import os
import tkFont
#import urllib2
from multiprocessing.dummy import Pool as ThreadPool
import MySQLdb
python_green = "#476042"
try:
    hostname="127.0.0.1"
    username="root"
    password=""
    dbname="TESTDB"
# Open database connection
    db = MySQLdb.connect(hostname,username,password,dbname)
# prepare a cursor object using cursor() method
    cursor = db.cursor() 
except:
    print "Connection error!"
    
top = Tk()
top.geometry("605x370")
top.wm_title("PySnap")
top.config(bg="black")
top.resizable(0,0)
w = Canvas(top, 
           width=670, 
           height=370,bg="white")
w.pack()
points = [0,39,650,160,0, 375]
w.create_polygon(points, outline=python_green, 
            fill='black', width=3)
#top.configure(background="Red")
#filename=PhotoImage(file="images.jpeg")
#background_label = Label(top, image=filename)
#background_label.place(x=0, y=0, relwidth=1, relheight=1)
helv36 = tkFont.Font(family='Courier', size=14)
L7 = Label(w, text="H! geek",fg="#13CEF5",bg="white",bd=12)
L7.grid(row=0, column=1,padx=40,pady=2)
L7.config(font=("Courier", 39))
L2 = Label(w, text="Username",bg="black",fg="#13CEF5",bd=12)
L2.grid(row=1, column=0,padx=20,pady=(30,0))
L2.config(font=("Courier", 18))
E3 = Entry(w, bd = 10,width=40,bg="#13CEF5")
E3.grid(row=1, column=1,padx=20,pady=(30,0))
DE1=Entry(w, bd = 10,show="*",width=40,bg="#13CEF5")
DE1.grid(row=2, column=1,padx=20,pady=20)
DL1=Label(w,text="Password",bg="black",fg="#13CEF5",bd=12)
DL1.grid(row=2, column=0,padx=20,pady=0)
DL1.config(font=("Courier", 18))
check=IntVar()
ckbox= Checkbutton(w, text="Remember me",font=helv36,variable=check,bg="black",fg="#13CEF5",bd=12)
ckbox.grid(row=3,column=0,padx=(20,10),pady=10)
#textPad = ScrolledText(top, width=50, height=40)
# textPad.pack()

def login():
    usr=str(E3.get())
    psw=str(DE1.get())
    print usr
    try:
        # Open database connection
        db = MySQLdb.connect("127.0.0.1","root","","TESTDB" )
# prepare a cursor object using cursor() method
        cursor = db.cursor() 
    except:
        print "Connection error"
    sql="SELECT * FROM EMPLOYEE WHERE USERNAME='%s'"% usr
    cursor.execute(sql)
    row=cursor.fetchone()
    print row
    if row is not None:
        if len(row)>0:
            username=str(row[1])
            password=str(row[2])
            if username==usr and password==psw:
                print "Login Matched"
                sql3="INSERT INTO pruser (user) VALUES ('%s');"%username
                cursor.execute(sql3)
                db.commit()
                print "Query executed"
#                file1=open("username.txt","w+") 
#                file1.write(username)
#                file1.close()
                db.close()
                if not os.path.exists("screenshots"):
                    os.makedirs("screenshots")
                workdir = "screenshots/"+username
                if not os.path.exists(workdir):
                    os.makedirs(workdir)    
                if check.get():
                    print "Remembered"
                    try:
                        fhand=open("rmbr.txt","a")
                        fhand.write(username+","+base64.encodestring(password))
                        fhand.close()
                    except:
                        fhand=open("rmbr.txt","a+")
                        fhand.write(username+","+base64.encodestring(password))                    
                        fhand.close()
                top.destroy()
                import delasap
                #os.system("python mainpart.py")
                #Popen('python delasap.py')   # shell = true makes cmd invisible
                #top.destroy()
                #os.startfile('delasap.exe')
            else:
                print "No match Found"
                tkMessageBox.showwarning("Warning","No match found")
        else:
            print "No match found"
            tkMessageBox.showwarning("Warning","Username not found")
    else:
            print "No match found"
            tkMessageBox.showwarning("Warning","Username not found")

def checkin(event):
    substring=E3.get()
    data=open("rmbr.txt").read()
    lines=data.split("\n")
    print "calling"
    #print lines
    for line in range(len(lines)):
        if not len(lines[line])>0:continue
        print lines[line]
        if lines[line].startswith(str(substring)):
            print lines[line]
            li=lines[line].split(",")
            print line
            E3.delete(0,"end")
            DE1.delete(0,"end")            
            E3.insert(END,li[0])
            DE1.insert(END,base64.decodestring(li[1]))
            print "MATCHED with REMEMBER ME"
            break
E3.bind("<Return>",checkin)          
    
DB1=Button(w, text="Login", width=10,command=login,bd=8,bg="#13CEF5")
DB1.grid(row=3, column=1,padx=20,pady=0)

L4 = Label(w, text="Forgot Password?",bg="white",fg="black")
L4.grid(row=4, column=1,pady=0)
L4.config(font=("Courier", 14))
def press(event):
    tkMessageBox.showinfo("Info","Contact your HR over this issue")
L4.bind("<Button-1>",press)
top.mainloop()

#Developed by Murali,Premith,Vamsi(Interns @ Geek Online Ventures,Bengaluru)
#Make this into an exe using the command --pyinstaller --noconsole --onefile loginfr.py and then
# then in the code call other exe file whatever it is mainpart or delasap using os.startfile("asfa.exe")
#That's it,Thank you for coming this far.