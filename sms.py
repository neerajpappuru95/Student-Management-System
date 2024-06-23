from tkinter import *
import time
from tkinter import ttk, messagebox, filedialog
import pymysql
import ttkthemes
from ttkthemes import ThemedTk
import pandas

root = ttkthemes.ThemedTk()
themes = root.get_themes()
root.set_theme('radiance')
root.geometry('1500x750+0+0')
root.title('Student Registration System')

def winexit():
    result = messagebox.askyesno('Confirm!','Do you want to Exit?')
    if result:
        root.destroy()
    else:
        pass
def exportdata():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = studtable.get_children()
    newlist = []
    for index in indexing:
        content = studtable.item(index)
        datalist = content['values']
        newlist.append(datalist)
    table = pandas.DataFrame(newlist, columns=['Id', 'Name', 'Gender', 'Email', 'Mobile No', 'D.O.B', 'Added Date',
                                               'Added Time'])
    table.to_csv(url, index=False)
    messagebox.showinfo('Success', 'Data Saved Successfully')


def showstudentdata():
    query = 'select *from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studtable.delete(*studtable.get_children())
    for data in fetched_data:
        datalist = list(data)
        studtable.insert('', END, values=datalist)


def updatestudentdata():
    def updatedata():
        try:
            date = time.strftime('%d/%m/%Y')
            curtime = time.strftime('%H:%M:%S')
            query = 'update student set name=%s, gender=%s, email=%s, mobile=%s, dob=%s, date=%s, time=%s WHERE id=%s'
            values = (nameentry.get(), genderentry.get(), emailentry.get(), mobileentry.get(), dobentry.get(),
                      date, curtime, identry.get())
            mycursor.execute(query, values)
            con.commit()
            messagebox.showinfo('Updated!', f'Id {identry.get()} is Updated')
            updatewindow.destroy()
            showstudentdata()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to update data: {str(e)}')

    updatewindow = Toplevel()
    updatewindow.resizable(False, False)
    updatewindow.grab_set()
    updatewindow.title('Update Student Data')
    updatewindow.geometry('550x500')

    updateframe = Frame(updatewindow)
    updateframe.place(x=0, y=10, height=500, width=540)
    idlabel = Label(updateframe, text='Id : ', font=('times new roman', 20, 'bold'), fg='red')
    idlabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    identry = Entry(updateframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    identry.grid(row=1, column=1, pady=10)
    namelabel = Label(updateframe, text='Name : ', font=('times new roman', 20, 'bold'), fg='red')
    namelabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    nameentry = Entry(updateframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    nameentry.grid(row=2, column=1, pady=10)
    genderlabel = Label(updateframe, text='Gender : ', font=('times new roman', 20, 'bold'), fg='red')
    genderlabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    genderentry = Entry(updateframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    genderentry.grid(row=3, column=1, pady=10)
    emaillabel = Label(updateframe, text='Email : ', font=('times new roman', 20, 'bold'), fg='red')
    emaillabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    emailentry = Entry(updateframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    emailentry.grid(row=4, column=1, pady=10)
    mobilelabel = Label(updateframe, text='Mobile NO : ', font=('times new roman', 20, 'bold'), fg='red')
    mobilelabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    mobileentry = Entry(updateframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    mobileentry.grid(row=5, column=1, pady=10)
    doblabel = Label(updateframe, text='D.O.B : ', font=('times new roman', 20, 'bold'), fg='red')
    doblabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobentry = Entry(updateframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    dobentry.grid(row=6, column=1, pady=10)
    updatebutton = ttk.Button(updateframe, text='Update Student', width=20, command=updatedata)
    updatebutton.grid(row=7, columnspan=2, pady=5)

    index = studtable.focus()
    content = studtable.item(index)
    datalist = content['values']
    identry.insert(0, datalist[0])
    nameentry.insert(0, datalist[1])
    genderentry.insert(0, datalist[2])
    emailentry.insert(0, datalist[3])
    mobileentry.insert(0, datalist[4])
    dobentry.insert(0, datalist[5])


def deletestudentdata():
    index = studtable.focus()
    content = studtable.item(index)
    id = content['values'][0]
    query = 'delete from student where id=%s'
    mycursor.execute(query, id)
    con.commit()
    messagebox.showinfo('Student Deleted', f'Id {id} is Deleted!')
    query = 'select *from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studtable.delete(*studtable.get_children())
    for data in fetched_data:
        datalist = list(data)
        studtable.insert('', END, values=datalist)


def searchstudentdata():
    def searchdata():
        query = 'select *from student where id=%s or name=%s or gender=%s or email=%s or mobile=%s or dob=%s'
        mycursor.execute(query, (
            identry.get(), nameentry.get(), genderentry.get(), emailentry.get(), mobileentry.get(), dobentry.get()))
        fetched_data = mycursor.fetchall()
        studtable.delete(*studtable.get_children())
        for data in fetched_data:
            datalist = list(data)
            studtable.insert('', END, values=datalist)

    searchwindow = Toplevel()
    searchwindow.resizable(False, False)
    searchwindow.grab_set()
    searchwindow.title('Search Student data')
    searchwindow.geometry('550x500')
    searchframe = Frame(searchwindow)
    searchframe.place(x=0, y=10, height=500, width=540)
    idlabel = Label(searchframe, text='Id : ', font=('times new roman', 20, 'bold'), fg='red')
    idlabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    identry = Entry(searchframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    identry.grid(row=1, column=1, pady=10)
    namelabel = Label(searchframe, text='Name : ', font=('times new roman', 20, 'bold'), fg='red')
    namelabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    nameentry = Entry(searchframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    nameentry.grid(row=2, column=1, pady=10)
    genderlabel = Label(searchframe, text='Gender : ', font=('times new roman', 20, 'bold'), fg='red')
    genderlabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    genderentry = Entry(searchframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    genderentry.grid(row=3, column=1, pady=10)
    emaillabel = Label(searchframe, text='Email : ', font=('times new roman', 20, 'bold'), fg='red')
    emaillabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    emailentry = Entry(searchframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    emailentry.grid(row=4, column=1, pady=10)
    mobilelabel = Label(searchframe, text='Mobile NO : ', font=('times new roman', 20, 'bold'), fg='red')
    mobilelabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    mobileentry = Entry(searchframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    mobileentry.grid(row=5, column=1, pady=10)
    doblabel = Label(searchframe, text='D.O.B : ', font=('times new roman', 20, 'bold'), fg='red')
    doblabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobentry = Entry(searchframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    dobentry.grid(row=6, column=1, pady=10)
    searchbutton = ttk.Button(searchframe, text='Search Student', width=20, command=searchdata)
    searchbutton.grid(row=7, columnspan=2, pady=5)


def addstudentdata():
    def adddata():
        global currentdate, currenttime
        if identry.get() == '' or nameentry.get() == '' or genderentry.get() == '' or emailentry.get() == '' or mobileentry.get() == '' or dobentry.get() == '':
            messagebox.showerror('Error!', 'All Fields are Required!', parent=addwindow)
        else:
            try:
                currentdate = time.strftime('%d/%m/%Y')
                currenttime = time.strftime('%H:%M:%S')
                query = 'insert into student values(%s,%s,%s,%s,%s,%s,%s,%s)'
                mycursor.execute(query, (
                    identry.get(), nameentry.get(), genderentry.get(), emailentry.get(), mobileentry.get(),
                    dobentry.get(),
                    currentdate, currenttime))
                con.commit()
                result = messagebox.askyesno('Confirm!', 'Data Added Successfully. Do you want to clean the form?',
                                             parent=addwindow)
                if result:
                    identry.delete(0, END)
                    nameentry.delete(0, END)
                    genderentry.delete(0, END)
                    emailentry.delete(0, END)
                    mobileentry.delete(0, END)
                    dobentry.delete(0, END)
                else:
                    pass
            except:
                messagebox.showerror('Error!', 'Duplicate Id is found', parent=addwindow)
                return
            query = 'select *from student'
            mycursor.execute(query)
            fetched_data = mycursor.fetchall()
            studtable.delete(*studtable.get_children())
            for data in fetched_data:
                datalist = list(data)
                studtable.insert('', END, values=datalist)

    addwindow = Toplevel()
    addwindow.resizable(False, False)
    addwindow.grab_set()
    addwindow.title('Add Student data')
    addwindow.geometry('550x500')
    addframe = Frame(addwindow)
    addframe.place(x=0, y=10, height=500, width=540)
    idlabel = Label(addframe, text='Id : ', font=('times new roman', 20, 'bold'), fg='red')
    idlabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    identry = Entry(addframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    identry.grid(row=1, column=1, pady=10)
    namelabel = Label(addframe, text='Name : ', font=('times new roman', 20, 'bold'), fg='red')
    namelabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    nameentry = Entry(addframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    nameentry.grid(row=2, column=1, pady=10)
    genderlabel = Label(addframe, text='Gender : ', font=('times new roman', 20, 'bold'), fg='red')
    genderlabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    genderentry = Entry(addframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    genderentry.grid(row=3, column=1, pady=10)
    emaillabel = Label(addframe, text='Email : ', font=('times new roman', 20, 'bold'), fg='red')
    emaillabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    emailentry = Entry(addframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    emailentry.grid(row=4, column=1, pady=10)
    mobilelabel = Label(addframe, text='Mobile NO : ', font=('times new roman', 20, 'bold'), fg='red')
    mobilelabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    mobileentry = Entry(addframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    mobileentry.grid(row=5, column=1, pady=10)
    doblabel = Label(addframe, text='D.O.B : ', font=('times new roman', 20, 'bold'), fg='red')
    doblabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobentry = Entry(addframe, bd=5, width=20, font=('times new roman', 20, 'bold'))
    dobentry.grid(row=6, column=1, pady=10)
    submitbutton = ttk.Button(addframe, text='Submit', width=10, command=adddata)
    submitbutton.grid(row=7, columnspan=2, pady=5)


def connectdatabase():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(host='localhost', user='root', password='1234')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error!', 'Invalid Details Entered!', parent=connectwin)
            return
        try:
            query = 'create database studentmanagementsystem'
            mycursor.execute(query)
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
            query = (
                'create table student(id int not null primary key, name varchar(30), gender varchar(15), '
                'email varchar(30), mobile varchar(10), dob varchar(30), date varchar(50), time varchar(50))')
            mycursor.execute(query)
        except:
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
        messagebox.showinfo('Success!', 'Database Connection is Successful!', parent=connectwin)
        connectwin.destroy()
        addstudent.config(state=NORMAL)
        searchstudent.config(state=NORMAL)
        deletestudent.config(state=NORMAL)
        updatestudent.config(state=NORMAL)
        showstudent.config(state=NORMAL)
        exportdata.config(state=NORMAL)

    connectwin = Toplevel()
    connectwin.resizable(False, False)
    connectwin.grab_set()
    connectwin.title('Database Connection')
    connectwin.geometry('450x300+1000+100')
    winframe = Frame(connectwin)
    winframe.place(x=20, y=10, height=280, width=440)
    hostnamelabel = Label(winframe, text='Hostname : ', font=('times new roman', 20, 'bold'), fg='red')
    hostnamelabel.grid(row=1, column=0, pady=10)
    hostnameentry = Entry(winframe, bd=5, width=18, font=('times new roman', 20, 'bold'))
    hostnameentry.grid(row=1, column=1, pady=10)
    usernamelabel = Label(winframe, text='Username : ', font=('times new roman', 20, 'bold'), fg='red')
    usernamelabel.grid(row=2, column=0, pady=10)
    usernameentry = Entry(winframe, bd=5, width=18, font=('times new roman', 20, 'bold'))
    usernameentry.grid(row=2, column=1, pady=10)
    passwordlabel = Label(winframe, text='Password : ', font=('times new roman', 20, 'bold'), fg='red')
    passwordlabel.grid(row=3, column=0, pady=10)
    passwordentry = Entry(winframe, bd=5, width=18, font=('times new roman', 20, 'bold'))
    passwordentry.grid(row=3, column=1, pady=10)
    connectbutton = Button(winframe, text='Connect', font=('times new roman', 20, 'bold'), fg='red',
                           activeforeground='red', bd=5, command=connect)
    connectbutton.grid(row=4, columnspan=2, pady=10)


def clock():
    global date, curtime
    date = time.strftime('%d/%m/%Y')
    curtime = time.strftime('%H:%M:%S')
    datetimelabel.config(text=f'   Date: {date}\nTime: {curtime}')
    datetimelabel.after(1000, clock)


datetimelabel = Label(root, font=('times new roman', 16, 'bold'))
datetimelabel.place(x=5, y=5)
clock()

textlabel = Label(root, text='Student Management System', font=('Aerial', 30, 'bold'), fg='dark orange')
textlabel.place(x=520, y=10)

connectdatabasebutton = ttk.Button(root, text='Connect to Database', command=connectdatabase)
connectdatabasebutton.place(x=1300, y=20)

leftframe = Frame(root)
leftframe.place(x=30, y=90, width=400, height=650)

addstudent = ttk.Button(leftframe, text='Add Student', width=25, state=DISABLED, command=addstudentdata)
addstudent.grid(row=1, column=0, padx=70, pady=25)

searchstudent = ttk.Button(leftframe, text='Search Student', width=25, state=DISABLED, command=searchstudentdata)
searchstudent.grid(row=2, column=0, padx=30, pady=25)

deletestudent = ttk.Button(leftframe, text='Delete Student', width=25, state=DISABLED, command=deletestudentdata)
deletestudent.grid(row=3, column=0, padx=30, pady=25)

updatestudent = ttk.Button(leftframe, text='Update Student', width=25, state=DISABLED, command=updatestudentdata)
updatestudent.grid(row=4, column=0, padx=30, pady=25)

showstudent = ttk.Button(leftframe, text='Show Student', width=25, state=DISABLED, command=showstudentdata)
showstudent.grid(row=5, column=0, padx=30, pady=25)

exportdata = ttk.Button(leftframe, text='Export Data', width=25, state=DISABLED, command=exportdata)
exportdata.grid(row=6, column=0, padx=30, pady=25)

exitbutton = ttk.Button(leftframe, text='Exit', width=25, command=winexit)
exitbutton.grid(row=7, column=0, padx=30, pady=25)

rightframe = Frame(root)
rightframe.place(x=400, y=90, width=1080, height=650)

scrollbarx = Scrollbar(rightframe, orient=HORIZONTAL)
scrollbary = Scrollbar(rightframe, orient=VERTICAL)
studtable = ttk.Treeview(rightframe,
                         columns=('Id', 'Name', 'Gender', 'Email', 'Mobile No', 'D.O.B', 'Added Date', 'Added Time'),
                         xscrollcommand=scrollbarx.set, yscrollcommand=scrollbary.set)
scrollbarx.config(command=studtable.xview)
scrollbary.config(command=studtable.yview)

scrollbarx.pack(side=BOTTOM, fill=X)
scrollbary.pack(side=RIGHT, fill=Y)

studtable.pack(fill=BOTH, expand=1)

studtable.heading('Id', text='Id')
studtable.heading('Name', text='Name')
studtable.heading('Gender', text='Gender')
studtable.heading('Email', text='Email')
studtable.heading('Mobile No', text='Mobile No')
studtable.heading('D.O.B', text='D.O.B')
studtable.heading('Added Date', text='Added Date')
studtable.heading('Added Time', text='Added Time')

studtable.column('Id', width=70, anchor=CENTER)
studtable.column('Name', width=200, anchor=CENTER)
studtable.column('Gender', width=100, anchor=CENTER)
studtable.column('Email', width=250, anchor=CENTER)
studtable.column('Mobile No', width=150, anchor=CENTER)
studtable.column('D.O.B', width=150, anchor=CENTER)
studtable.column('Added Date', width=150, anchor=CENTER)
studtable.column('Added Time', width=150, anchor=CENTER)

style = ttk.Style()
style.configure('Treeview', rowheight=30, font='aerial,18,bold', background='yellow')
style.configure('Treeview.Heading', font='aerial,18,bold', foreground='red')
studtable.config(show='headings')
root.mainloop()
