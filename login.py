from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

def login():
    if usernameEntry.get()=="" or passwordEntry.get()=="":
        messagebox.showerror("error","Fields can't be empty")

    elif usernameEntry.get()=="Susmita" and passwordEntry.get()=="1234":
        messagebox.showinfo("success","Welcome")
        window.destroy()#previous window is closed new window imported(the login window)
        import sms
    else:
        messagebox.showerror("error","Please enter correct details")

window=Tk()


window.geometry("1240x827+0+0")
window.title("Student Management login System")

window.resizable(False,False) #to disable maximize button

#background image
image=Image.open("student management system/student1.jpg")
photo=ImageTk.PhotoImage(image)

label_img = Label(window, image=photo).pack()

#frame is for logo
loginFrame=Frame(window,bg='white')
loginFrame.place(x=500,y=200)

#logo image
logoImage=PhotoImage(file="student management system/logo.png")

logoLabel=Label(loginFrame,image=logoImage,pady=10)
logoLabel.grid(row=0,column=0,columnspan=2)#columnspan forthe upperlogo taking 2 columns


userImage=PhotoImage(file="student management system/user.png")
usernameLabel=Label(loginFrame,image=userImage,text='Username',compound=LEFT,font=("times new roman",14,'bold'))
usernameLabel.grid(row=1,column=0,pady=10,padx=20)

usernameEntry=Entry(loginFrame,font=("times new roman",14,'bold'),bd=5,fg='royalblue')
usernameEntry.grid(row=1,column=1,pady=10,padx=20)


passwordImage=PhotoImage(file="student management system/padlock.png")
passwordLabel=Label(loginFrame,image=passwordImage,text='password',compound=LEFT,font=("times new roman",14,'bold'))
passwordLabel.grid(row=2,column=0,pady=10,padx=20)

passwordEntry=Entry(loginFrame,font=("times new roman",14,'bold'),bd=5,fg='royalblue')
passwordEntry.grid(row=2,column=1,pady=10,padx=20)

loginButton=Button(loginFrame,text="login",font=("times new roman",14,'bold'),width=15,
                   fg='white',bg='gray',cursor='hand2',command=login)#use activebackground and active forground while clicking the button the color would be same as button
loginButton.grid(row=3,column=1,padx=10)

window.mainloop() #to see the window we need to put the method in a loop 