# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 15:48:37 2017

@author: lenovo2
"""


from Tkinter import *
import os
top = Tk()
#import time
import MySQLdb
import mysql.connector
import ttk
from PIL import Image
#import Tix
import datetime
import sys
import pyautogui
import socket
import random
import threading
import shutil
from tkFileDialog import *
import tkMessageBox
import tkFont
python_green = "#476042"
def getipaddress():
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname)   
    #print("Your Computer Name is:"+hostname)   
    #print("Your Computer IP Address is:"+IPAddr)
    return IPAddr


global timegap
timegap=600


#top.geometry("1500x860")
top.wm_title("PySnap")
top.config(bg="white")
top.resizable(0,0)
w = Canvas(top, 
           width=1400, 
           height=900,bg="white")
w.pack()
points = [0,0,1500,420, 0, 950]
w.create_polygon(points, outline=python_green, 
            fill='black', width=3)
def getdatetime():
            now=datetime.datetime.now()
            both=str(now)
            bdif=both.split(" ")
            return bdif

try:    
# Open database connection
    db = MySQLdb.connect("127.0.0.1","root","","TESTDB" )
        
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    db.autocommit(True)
except:
    print "Please check your internet connection."
    tkMessageBox.showwarning("Connectivity Error","Please check your internet connection.")
    top.destroy()
    sys.exit()

    
username="Null"
global nowi,bothi,bdifi,datei
nowi=datetime.datetime.now()
bothi=str(nowi)
bdifi=bothi.split(" ")
datei=bdifi[0]

global userid            
userid=0
try:
    cursor.execute('''SELECT user FROM pruser''')
    row=cursor.fetchone()
    if row is not None:
            if len(row)>0:
                username=str(row[0])
                print username,""
                cursor.execute("DELETE FROM pruser where 1=1")
    #            file1=open("username.txt","r")
    #            username=file1.read()
    #            file1.close()
                sqli="SELECT * FROM EMPLOYEE WHERE USERNAME='%s'"% username
                cursor.execute(sqli)
                irow=cursor.fetchone()
                global userid
                userid=irow[0]
                bdif=getdatetime()
                date=bdif[0]
                timee=bdif[1]
                ipaddress=getipaddress()
                try:
                    sqli3="INSERT INTO gst(uid,date,markin,inip) VALUES ('%d','%s','%s','%s')" %(userid,date,timee,str(ipaddress))
                    cursor.execute(sqli3)
                except:
                    tkMessageBox.showerror("Login Problem","You can't markin twice in a same day")
                    top.destroy()
                    sys.exit()
                #cursor.execute("DELETE FROM firsttable WHERE date < (NOW()-(0000-00-07)) AND uid='%d'"%userid)
    #            cursor.execute("DELETE FROM firsttable WHERE date < (DATE_SUB(NOW(), INTERVAL 1 MONTH)) AND uid='%d'"%userid)            
    #            db.commit()
            else:
                print "No user name"
                tkMessageBox.showwarning("Warning","UserName Not Found")
    else:
        print "No match found"
        tkMessageBox.showwarning("Warning","No Match Found")
except:
    tkMessageBox.showerror("Connectivity Error","Please contact your HR over this issue")
    top.destroy()
    sys.exit()
#file1=open("username.txt","r")
#username=file1.read()
#file1.close()
#sqli="SELECT * FROM EMPLOYEE WHERE USERNAME='%s'"% username
#cursor.execute(sqli)
#irow=cursor.fetchone()
#userid=irow[0]

global workid
workid=0


try:
    sqli="SELECT * from imgtimegap LIMIT 1"
    cursor.execute(sqli)
    row=cursor.fetchone()
    global timegap
    timegap=row[0]
    print timegap
except Exception as e:
    print "Error in Database connection is ",e




L2 = Label(w, text=username,bg="#13CEF5",fg="white")
L2.grid(row=0, column=3,padx=(0,0),pady=(0,20))      #---------------------TIMER-------------------
L2.config(font=("Courier", 40))

#txt="TaskNo.  ClientName  Worktype  Timespent"
#L5 = Label(top, text="")
#L5.grid(row=0, column=5,padx=20,pady=0)
#L5.config(font=("Courier", 20))
global task
task="Task.No\n"+"\n----------------------"
LE0= Label(w, text=task,bg="#13CEF5",fg="black",borderwidth=2, relief="groove",bd=12)
LE0.grid(row=3,column=1,padx=(60,0),pady=(30,30))   #-----------------------    TASK NO.-------
LE0.config(font=("Courier", 15))

global clientname,worktype,timespent
clientname="ClientName\n"+"\n----------------------"
worktype="WorkType\n"+"\n----------------------"
timespent="TimeSpent\n"+"\n----------------------"
LE1= Label(w, text=clientname, borderwidth=2, relief="groove")
LE1.grid(row=3,column=2,padx=(0,0),pady=(30,30))
LE1.config(font=("Courier", 15))

LE2= Label(w, text=worktype, borderwidth=2, relief="groove",bg="white")
LE2.grid(row=3, column=3,padx=(0,0),pady=(30,30))
LE2.config(font=("Courier", 15))

LE3= Label(w, text=timespent, borderwidth=2, relief="groove")
LE3.grid(row=3, column=4,padx=(0,0),pady=(30,30))
LE3.config(font=("Courier", 15))


    
my_dict = {}
sql1="SELECT * FROM client"
cursor.execute(sql1)
clients=cursor.fetchall()
for client in clients:
    my_dict[client[1]]=client[0]
combobox_values = my_dict.keys()
organism = ttk.Combobox(w, values=combobox_values,state="readonly") 
organism.grid(row=2, column=2, sticky="w", padx=2, pady=2)
organism.current(0)


my_dict1 = {}
sql2="SELECT * FROM work"
cursor.execute(sql2)
works=cursor.fetchall()
for work in works:
    my_dict1[work[1]]=work[0]
combobox_values = my_dict1.keys()
organism1 = ttk.Combobox(w, values=combobox_values,state="readonly") 
organism1.grid(row=2, column=3, sticky="w", padx=2, pady=2)
organism1.current(0)

global hh,mm,ss;
hh=00;
mm=00;
ss=00;
global flag
flag=0
global i
i=0


def timeset():
    global ss,mm,hh
    if(ss==59):
        if(mm==59):
            hh=hh+1
            mm=0
        else:    
            mm=mm+1
            ss=0
    else:
        ss=ss+1
    return str(hh)+":"+str(mm)+":"+str(ss) 

def presenttime():
    return str(hh)+":"+str(mm)+":"+str(ss)

def screenshots():
    try:    
        ptime=presenttime()
        global i
        li=getdatetime()
        timefull=li[1].split(".")
        scrname=timefull[0]
        scrname=scrname.replace(":","-")
        foldrname=li[0]
    #    foldrname=foldrname.replace("-",",")
        i=i+1
        scrl=pyautogui.screenshot()
        if not os.path.exists("screenshots\\"+username+"\\"+foldrname):
            os.makedirs("screenshots\\"+username+"\\"+foldrname)    
        pathname=str("screenshots\\"+username+"\\"+foldrname+"\\"+str(scrname)+".jpg")
        print pathname
    #    scrl.pixel(500,500)
        scrl.save(pathname+"")
        img = Image.open(pathname)
        new_width  = 500
        new_height = 500
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save(pathname)
        img.close()        
        blobvalue=open(pathname,'rb').read()
        print "Screenshot Taken"
        db1 = mysql.connector.connect(user='root', password='',
                                  host='localhost',
                                  database='testdb')
        # Prepare SQL query to INSERT a record into the database.
        sql = """INSERT INTO firsttable(date,screenshots,scrtime,uid)
             VALUES (%s,%s,%s,%s)""" 
        args = (datei,blobvalue,ptime,userid,)
        cursor1=db1.cursor()
        try:
            # Execute the SQL command
            cursor1.execute(sql,args)
            # Commit your changes in the database
            db1.commit()
            db1.close()
            print "Printed"
        except Exception as e:
            print e
            print "Rolling back"
            # Rollback in case there is any error
            db1.rollback()
            db1.close()
    #        # disconnect from server
    #        db.close()
    except:
        tkMessageBox.showwarning("Screenshots Error","Permit access to take photos")
       
    
def scrstart():        
    t2=threading.Timer(timegap,scrstart)
    t2.setDaemon(True)
    if(flag==0):
        try:
            t2.stop()
        except:
            "Just Chill"
    else:
        screenshots()
        t2.start()
        
def start():
    #now=time.strftime("%H:%M:%S")
    now=presenttime()
    L2.configure(text=now) 
    global t1
    t1 = threading.Timer(1,start)
    t1.setDaemon(True)
    #t2=threading.Timer(5,screenshots)
    if(flag==0):
        #print "paused"," ",flag
        try:
            t1.stop()
   ##         t2.stop() 
        except:
            "Just Chill"
    else:   
        t1.start()
        now1=timeset()
  ##      t2.start()
#        print "flag value is ",flag

global workflag
workflag=0

def updateclock():
    if flag==-1:
        print "Don't Click again"
        tkMessageBox.showwarning("Warning","Timer already started,don't click again")
        return
    if workflag==0:
        print "Select worktype"
        tkMessageBox.showwarning("Warning","WorkType is not selected!Please Select it")
        return
    global flag
    flag=-1
    start()
    scrstart()
#    global client,work
#    client=organism.get()
#    work=organism1.get()
#    li=getdatetime()
#    sqli="INSERT INTO worktype(usrid,client,work,date,time) VALUES ('%d','%s','%s','%s','%s')" %(userid,client,work,datei,li[1])
#    cursor.execute(sqli)

global workstart
workstart="00:00:00"    
def addtask():
    if workflag==0:
        global client,work
        client=organism.get()
        work=organism1.get()
        li=getdatetime()
        global workstart
        workstart=li[1]
        global workflag
        workflag=1
        sqli="INSERT INTO worktype(usrid,client,work,date,time) VALUES ('%d','%s','%s','%s','%s')" %(userid,client,work,datei,li[1])
        cursor.execute(sqli)
        li=getdatetime()
        sql3="SELECT client,work,hours from worktype where usrid='%d' and date='%s'"%(userid,li[0])
        cursor.execute(sql3)
        rowsets=cursor.fetchall()
        eachrows = [rowsets[x:x+10] for x in xrange(0, len(rowsets), 10)]
        print "Length of rows is "+str(len(rowsets))
        if len(rowsets)%10==0 and len(rowsets)>=10:
            global rownos
            rownos=(len(rowsets)/10)-1
            count=(rownos*10)+1
            print "No of rows is "+str(rownos)
        else:
            global rownos
            rownos=(len(rowsets)/10)
            count=(rownos*10)+1
        #print eachrows    
        global currentrow               #currentrow is used for displaying the rows
        currentrow=rownos
        print "Row No. is "+str(rownos)
        print eachrows
        rows=eachrows[rownos]
        for row in rows:
            global clientname                    
            clientname=clientname+"\n"+row[0]+"\n----------------------"
            global worktype
            worktype=worktype+"\n"+row[1]+"\n----------------------"
            global timespent
            timespent=timespent+"\n"+str(row[2])+"\n----------------------"
            global task
            task=task+"\n"+str(count)+"."+"\n----------------------"
            count=count+1
        LE0.configure(text=task)    
        LE1.configure(text=clientname)
        LE2.configure(text=worktype)
        LE3.configure(text=timespent)
        clientname="ClientName\n"+"\n----------------------"
        worktype="WorkType\n"+"\n----------------------"
        timespent="TimeSpent\n"+"\n----------------------"
        task="Task.No\n"+"\n----------------------"
        sqli2="SELECT id from worktype where usrid='%d' order by id DESC LIMIT 1"%userid
        cursor.execute(sqli2)
        row=cursor.fetchone()
        global workid
        workid=row[0]
    #    sqli3="DELETE FROM worktype where id='%d'"%workid
    #    cursor.execute(sqli3)
    else:
        if tkMessageBox.askyesno("Warning","Seems that your previous task isn't completed.Do you want to start another task?"):
            global workflag
            workflag=0
        else:
            global workflag
            workflag=1
            
    

def pauseclock():
    global flag
    flag=0
    start()
    scrstart()
    
    
    
def clrtime():
    hours=presenttime()
#    try:
#        print workid
#        sqli2="UPDATE worktype SET hours='00:10:00' where usrid='%d'"%(workid)
#        cursor.execute(sqli2)
#        print "Executed"
#    except:
#        print "Error in SQL command"
    global workflag
    if workflag==1:
        global client,work
        client=organism.get()
        work=organism1.get()
        #sqli="INSERT INTO worktype(usrid,client,work,date,time,hours) VALUES ('%d','%s','%s','%s','%s','%s')" %(userid,client,work,datei,workstart,hours)
        sqli="UPDATE worktype SET hours='%s' WHERE usrid='%d' and id='%d'"%(hours,userid,workid)
        cursor.execute(sqli)
        global workflag
        workflag=0
        li=getdatetime()
        sql3="SELECT client,work,hours from worktype where usrid='%d' and date='%s'"%(userid,li[0])
        cursor.execute(sql3)
        rowsets=cursor.fetchall()
        eachrows = [rowsets[x:x+10] for x in xrange(0, len(rowsets), 10)]
        if len(rowsets)%10==0 and len(rowsets)>=10:
            global rownos
            rownos=(len(rowsets)/10)-1
            count=(rownos*10)+1
            print "Number of rows is "+str(rownos)
        else:
            global rownos
            rownos=(len(rowsets)/10)
            count=(rownos*10)+1    
        global currentrow               #currentrow is used for displaying the rows
        currentrow=rownos
        print "Row no is "+str(rownos)
        rows=eachrows[rownos]
        for row in rows:
            global clientname                    
            clientname=clientname+"\n"+row[0]+"\n----------------------"
            global worktype
            worktype=worktype+"\n"+row[1]+"\n----------------------"
            global timespent
            timespent=timespent+"\n"+str(row[2])+"\n----------------------"
            global task
            task=task+"\n"+str(count)+"."+"\n----------------------"
            count=count+1
        LE0.configure(text=task)    
        LE1.configure(text=clientname)
        LE2.configure(text=worktype)
        LE3.configure(text=timespent)
        clientname="ClientName\n"+"\n----------------------"
        worktype="WorkType\n"+"\n----------------------"
        timespent="TimeSpent\n"+"\n----------------------"
        task="Task.No\n"+"\n----------------------"        
    else:
        print "Select Worktype"
        tkMessageBox.showwarning("Warning","WorkType is not selected,please select one")
    global hh,mm,ss
    hh=0
    mm=0
    ss=-1
    now=timeset()
    L2.configure(text=now)
    global flag
    flag=0
     
        
def uploadfiles():
    uploadedfilenames = askopenfilenames(multiple=True)
    if uploadedfilenames == '':
        tkMessageBox.showinfo(message="File Upload has been cancelled program will stop")
        return
#        if len(uploadedfiles)!=2:
#           tkMessageBox.showinfo(message="2 files have not been selected!")
    else:
        try:
            uploadedfiles = top.splitlist(uploadedfilenames)
            targetdirectory=askdirectory()
            for fil in uploadedfiles:
                shutil.copy(fil,targetdirectory)
            tkMessageBox.showinfo("Info","Files are uploaded")    
            return uploadedfiles
        except:
            tkMessageBox.showerror("Error","There is a problem in uploading your files,please try later.")

def nextshow():
    if currentrow<rownos:
        li=getdatetime()
        sql3="SELECT client,work,hours from worktype where usrid='%d' and date='%s'"%(userid,li[0])
        cursor.execute(sql3)
        rowsets=cursor.fetchall()
        eachrows = [rowsets[x:x+10] for x in xrange(0, len(rowsets), 10)]
        rows=eachrows[currentrow+1]
        count=((currentrow+1)*10)+1
        for row in rows:
            global clientname                    
            clientname=clientname+"\n"+row[0]+"\n----------------------"
            global worktype
            worktype=worktype+"\n"+row[1]+"\n----------------------"
            global timespent
            timespent=timespent+"\n"+str(row[2])+"\n----------------------"
            global task
            task=task+"\n"+str(count)+"."+"\n----------------------"
            count=count+1
        LE0.configure(text=task)    
        LE1.configure(text=clientname)
        LE2.configure(text=worktype)
        LE3.configure(text=timespent)
        clientname="ClientName\n"+"\n----------------------"
        worktype="WorkType\n"+"\n----------------------"
        timespent="TimeSpent\n"+"\n----------------------"
        task="Task.No\n"+"\n----------------------"
        global currentrow
        currentrow=currentrow+1
    else:
        print "Error"        
def prevshow():
    if currentrow>0:
        li=getdatetime()
        sql3="SELECT client,work,hours from worktype where usrid='%d' and date='%s'"%(userid,li[0])
        cursor.execute(sql3)
        rowsets=cursor.fetchall()
        eachrows = [rowsets[x:x+10] for x in xrange(0, len(rowsets), 10)]
        rows=eachrows[currentrow-1]
        count=((currentrow-1)*10) + 1
        global currentrow
        currentrow=currentrow-1
        for row in rows:
            global clientname                    
            clientname=clientname+"\n"+row[0]+"\n----------------------"
            global worktype
            worktype=worktype+"\n"+row[1]+"\n----------------------"
            global timespent
            timespent=timespent+"\n"+str(row[2])+"\n----------------------"
            global task
            task=task+"\n"+str(count)+"."+"\n----------------------"
            count=count+1
        LE0.configure(text=task)    
        LE1.configure(text=clientname)
        LE2.configure(text=worktype)
        LE3.configure(text=timespent)
        clientname="ClientName\n"+"\n----------------------"
        worktype="WorkType\n"+"\n----------------------"
        timespent="TimeSpent\n"+"\n----------------------"
        task="Task.No\n"+"\n----------------------" 
    else:
        print "Add a warning"        
helv36 = tkFont.Font(family='Courier', size=15, weight=tkFont.BOLD)


MyButton1 = Button(w, text="Start",font=helv36, width=10, command=updateclock,bd=7,bg="#13CEF5",fg="white")
MyButton1.grid(row=1, column=2,padx=(0,0),pady=(0,20))
MyButton2 = Button(w, text="Pause",font=helv36, width=10, command=pauseclock,bd=7,bg="#13CEF5",fg="white")
MyButton2.grid(row=1, column=3,padx=(0,0),pady=(0,20))
MyButton3 = Button(w, text="Stop", width=10,font=helv36, command=clrtime,bd=7,bg="#13CEF5",fg="white")
MyButton3.grid(row=1, column=4,padx=(0,0),pady=(0,20))
MyButton4 = Button(w, text="Add task", width=10,font=helv36, command=addtask,bd=7,bg="#13CEF5",fg="white")
MyButton4.grid(row=2, column=4,padx=20,pady=2)
MyButton5 = Button(w, text="Upload Files", width=12,font=helv36, command=uploadfiles,bd=7,bg="#13CEF5",fg="white")
MyButton5.grid(row=2, column=5,padx=20,pady=2)
MyButton6 = Button(w, text="Next", width=10,font=helv36,command=nextshow,bd=7,bg="#13CEF5",fg="white")
MyButton6.grid(row=7, column=5,padx=20,pady=2)
MyButton7 = Button(w, text="Previous", width=10,font=helv36,command=prevshow,bd=7,bg="#13CEF5",fg="white")
MyButton7.grid(row=7, column=6,padx=20,pady=2)
#scrollbar = Scrollbar(top)
#scrollbar.pack(side=RIGHT, fill=Y)
#scr_h1 = Scrollbar(top,orient=VERTICAL)
#scr_h1.pack(side=RIGHT,fill=Y)
#scr_h1.config(command=w1.xview)

def on_closing():
    global flag
    flag=0
    if workflag==1:
        if tkMessageBox.askyesno("Warning","You have current taks running,do you want to stop them before leaving?"):
            clrtime()
    if tkMessageBox.askyesno("Quit","You will be logged out,if you close.Do you want to close?"):        
        sqli="SELECT id from gst where uid='%d' order by id DESC LIMIT 1"%userid
        cursor.execute(sqli)
        row=cursor.fetchone()
        ids=row[0]
        li=getdatetime()
        markout=li[1]
        ipaddress=getipaddress()
        sqli2="UPDATE gst SET markout='%s',outip='%s' WHERE id='%d'"%(markout,str(ipaddress),ids)
        cursor.execute(sqli2)
        top.destroy()
            
top.protocol("WM_DELETE_WINDOW", on_closing)
top.mainloop()
# disconnect from server
db.close()
sys.exit()
#Murali manohar Chowdary