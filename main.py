from tkinter import *
from tkinter import messagebox


def login():
    if usernameentry.get() == '' or passwordentry.get() == '':
        messagebox.showerror('Error!', 'Fields cannot be Empty!')
    elif usernameentry.get() == 'srit' and passwordentry.get() == 'srit@123':
        messagebox.showinfo('Login Successful', 'Welcome SRIT')
        window.destroy()
        import sms
    else:
        messagebox.showwarning('Error!', 'Incorrect Credentials Check Again!')


window = Tk()
window.geometry('1500x750+0+0')
window.title('Login to Student Management System')

bg = PhotoImage(file='srit.png')
bglabel = Label(window, image=bg)
bglabel.place(x=600, y=0)

detailsframe = Frame(window)
detailsframe.place(x=520, y=350)

username = Label(detailsframe, text='Username : ', font=('times new roman', 20, 'bold'))
username.grid(row=1, column=0, pady=10)

usernameentry = Entry(detailsframe, font=('times new roman', 16, 'bold'), width=25, bd=5)
usernameentry.grid(row=1, column=1, pady=10)

password = Label(detailsframe, text='Password : ', font=('times new roman', 20, 'bold'))
password.grid(row=2, column=0, pady=10)

passwordentry = Entry(detailsframe, font=('times new roman', 16, 'bold'), width=25, bd=5)
passwordentry.grid(row=2, column=1, pady=10)

login = Button(detailsframe, text='Login', font=('times new roman', 20, 'bold'), width=10, bd=5, cursor='hand2',
               command=login)
login.grid(row=3, column=1, pady=20)
window.mainloop()
