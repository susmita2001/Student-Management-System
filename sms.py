from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox,filedialog #apply themes to buttons
import pymysql
import pandas

#functionality part

def clock():
    date=time.strftime("%d/%m/%Y")
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'  Date:{date}\n Time:{currenttime}')
    datetimeLabel.after(1000,clock)# to update the time

count=0    
text=''
def slider():
        global text,count
        if count==len(s):
              count=0
              text=''
        text=text+s[count]
        sliderLabel.config(text=text)#32min
        count+=1
        sliderLabel.after(300,slider)



def connect_database():
      def connect():
        global mycursor,con
        try:
           
            con=pymysql.connect(host='localhost',user='root',password='susmita')
            mycursor=con.cursor()#execute commands del,entry,update,search
            messagebox.showinfo("Success","Database connection is successful",parent=connectWindow)
        except:
             messagebox.showerror("error","Invalid details",parent=connectWindow)#we are writing the parent to show to error
                                                                                #or success message on the connectWindow not on main window (lec-3)
             return



        try:
            query="create database student_management_system"
            mycursor.execute(query)
            #create table inside database
            query='use student_management_system'
            mycursor.execute(query)
            query='create table student(id int not null primary key,name varchar(30),mobile varchar(10),email varchar(100),'\
                'address varchar(100),gender varchar(20),dob varchar(78),date varchar(67),time varchar(43))'
            mycursor.execute(query)
        except:
            query='use student_management_system'
            mycursor.execute(query)               #lec3 (40:00)
        
        connectWindow.destroy()
        addStudentButton.config(state=NORMAL)
        searchStudentButton.config(state=NORMAL)
        updateStudentButton.config(state=NORMAL)
        deleteStudentButton.config(state=NORMAL)
        showStudentButton.config(state=NORMAL)
        ExportStudentButton.config(state=NORMAL)

      connectWindow=Toplevel()
      connectWindow.grab_set()#If we don't close the connectwindow we can't close other windows
      connectWindow.geometry("470x230+730+230")
      connectWindow.title("Database Connection")
      connectWindow.resizable(False,False)

    #after clicking connect to database button
      hostnameLabel=Label(connectWindow,text='Host Name',font=("Arial",16,'bold'))
      hostnameLabel.grid(row=0,column=0,padx=20,pady=10)

      hostEntry=Entry(connectWindow,font=("roman",14,'bold'),bd=2)
      hostEntry.grid(row=0,column=1,padx=30)
    
      usernameLabel=Label(connectWindow,text='User Name',font=("Arial",16,'bold'))
      usernameLabel.grid(row=1,column=0,padx=20,pady=10)

      userEntry=Entry(connectWindow,font=("roman",14,'bold'),bd=2)
      userEntry.grid(row=1,column=1,padx=30)

      passwordLabel=Label(connectWindow,text='Password',font=("Arial",16,'bold'))
      passwordLabel.grid(row=2,column=0,padx=20,pady=10)

      passwordEntry=Entry(connectWindow,font=("roman",14,'bold'),bd=2)
      passwordEntry.grid(row=2,column=1,padx=30)

      connectButton=ttk.Button(connectWindow,text="CONNECT",command=connect)
      connectButton.grid(row=3,columnspan=2,pady=20)


def export_data():
    url =filedialog.asksaveasfile(defaultextension='.csv')# whole table is saved as csv
    #print(url)-->gives the url of the file
    indexing=studentTable.get_children()
    newlist=[]
    for index in indexing:
        content=studentTable.item(index)
        datalist=content['values']
        #print(datalist)--> print all the datas in table in lists
        newlist.append(datalist)

    table=pandas.DataFrame(newlist,columns=['Id',"Name",'Mobile no',"Address","Gender","D.O.B",'Added Date','Added Time'])
    #print(table)
    table.to_csv(url,index=False) #save the data in table and convert it to excel and save it to url
    messagebox.showinfo("success","Data is saved successfully")

def delete_student():
    indexing=studentTable.focus()#the row we want to delete
    #print(indexing)
    content=studentTable.item(indexing)
    #print(content)  --> gives the values in dictionary
    content_id=content['values'][0]
    query='delete from student where id=%s'
    mycursor.execute(query,content_id)
    con.commit()
    messagebox.showinfo("Deleted",f'ID {content_id} is deleted successfully')
    query='select * from student'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('',END,values=data)





def show_student():
        query="select * from student"
        mycursor.execute(query)
        fetched_data=mycursor.fetchall() 
            #print(fetched_data)  -->print all the inserted data in the table in tuple form in terminal
        studentTable.delete(*studentTable.get_children())#new data will be inserted and previous data will be deleted
        for data in fetched_data:
            datalist= list(data)  #convert the tuple in list
            studentTable.insert('',END,values=datalist)

def search_student():
    def search_data():
        query="select * from student where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s"
        mycursor.execute(query,(idEntry.get(),nameEntry.get(),emailEntry.get(),phoneEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get()))
        studentTable.delete(*studentTable.get_children())
        fetched_data=mycursor.fetchall()
        for data in fetched_data:
            studentTable.insert('',END,values=data)



     
    search_window=Toplevel()
    search_window.title("Search student")
    search_window.grab_set()
    search_window.resizable(False,False)
    idLabel=Label(search_window,text='ID',font=("times new roman",15,'bold'))
    idLabel.grid(padx=20,pady=15)
    idEntry=Entry(search_window,font=('roman',11,'bold'),bd=2)
    idEntry.grid(row=0,column=1,padx=9)

    nameLabel=Label(search_window,text='NAME',font=('times new roman',15,'bold'))
    nameLabel.grid(row=1,column=0,padx=20,pady=15)
    nameEntry=Entry(search_window,font=("roman",11,'bold'),bd=2)
    nameEntry.grid(row=1,column=1,padx=9)

    phoneLabel=Label(search_window,text='PHONE',font=('times new roman',15,'bold'))
    phoneLabel.grid(row=2,column=0,padx=20,pady=15)
    phoneEntry=Entry(search_window,font=("roman",11,'bold'),bd=2)
    phoneEntry.grid(row=2,column=1,padx=9)

    emailLabel=Label(search_window,text='EMAIL',font=('times new roman',15,'bold'))
    emailLabel.grid(row=3,column=0,padx=20,pady=15)
    emailEntry=Entry(search_window,font=("roman",11,'bold'),bd=2)
    emailEntry.grid(row=3,column=1,padx=9)

    addressLabel=Label(search_window,text='ADDRESS',font=('times new roman',15,'bold'))
    addressLabel.grid(row=4,column=0,padx=20,pady=15)
    addressEntry=Entry(search_window,font=("roman",11,'bold'),bd=2)
    addressEntry.grid(row=4,column=1,padx=9)

    genderLabel=Label(search_window,text='GENDER',font=('times new roman',15,'bold'))
    genderLabel.grid(row=5,column=0,padx=20,pady=15)
    genderEntry=Entry(search_window,font=("roman",11,'bold'),bd=2)
    genderEntry.grid(row=5,column=1,padx=9)

    dobLabel=Label(search_window,text='D.O.B',font=('times new roman',15,'bold'))
    dobLabel.grid(row=6,column=0,padx=20,pady=15)
    dobEntry=Entry(search_window,font=("roman",11,'bold'),bd=2)
    dobEntry.grid(row=6,column=1,padx=9)

    search_student_Button=ttk.Button(search_window,text='SEARCH',width=15,command=search_data)
    search_student_Button.grid(row=7,columnspan=2,padx=20,pady=12)


def update_student():
    def update_data():
        currentdate=time.strftime("%d/%m/%Y")
        currenttime=time.strftime('%H:%M:%S')
        query='update student set name=%s,mobile=%s,email=%s,address=%s,gender=%s,dob=%s,date=%s,time=%s where id=%s'
        mycursor.execute(query,(nameEntry.get(),phoneEntry.get(),addressEntry.get(),emailEntry.get(),genderEntry.get(),dobEntry.get(),currentdate,currenttime,idEntry.get()))
        con.commit()
        messagebox.showinfo('Success',f'{idEntry.get()}is modified successfully',parent=update_window)
        update_window.destory()
        show_student()


    update_window=Toplevel()
    update_window.title("Search student")
    update_window.grab_set()
    update_window.resizable(False,False)
    idLabel=Label(update_window,text='ID',font=("times new roman",15,'bold'))
    idLabel.grid(padx=20,pady=15)
    idEntry=Entry(update_window,font=('roman',11,'bold'),bd=2)
    idEntry.grid(row=0,column=1,padx=9)

    nameLabel=Label(update_window,text='NAME',font=('times new roman',15,'bold'))
    nameLabel.grid(row=1,column=0,padx=20,pady=15)
    nameEntry=Entry(update_window,font=("roman",11,'bold'),bd=2)
    nameEntry.grid(row=1,column=1,padx=9)

    phoneLabel=Label(update_window,text='PHONE',font=('times new roman',15,'bold'))
    phoneLabel.grid(row=2,column=0,padx=20,pady=15)
    phoneEntry=Entry(update_window,font=("roman",11,'bold'),bd=2)
    phoneEntry.grid(row=2,column=1,padx=9)

    emailLabel=Label(update_window,text='EMAIL',font=('times new roman',15,'bold'))
    emailLabel.grid(row=3,column=0,padx=20,pady=15)
    emailEntry=Entry(update_window,font=("roman",11,'bold'),bd=2)
    emailEntry.grid(row=3,column=1,padx=9)

    addressLabel=Label(update_window,text='ADDRESS',font=('times new roman',15,'bold'))
    addressLabel.grid(row=4,column=0,padx=20,pady=15)
    addressEntry=Entry(update_window,font=("roman",11,'bold'),bd=2)
    addressEntry.grid(row=4,column=1,padx=9)

    genderLabel=Label(update_window,text='GENDER',font=('times new roman',15,'bold'))
    genderLabel.grid(row=5,column=0,padx=20,pady=15)
    genderEntry=Entry(update_window,font=("roman",11,'bold'),bd=2)
    genderEntry.grid(row=5,column=1,padx=9)

    dobLabel=Label(update_window,text='D.O.B',font=('times new roman',15,'bold'))
    dobLabel.grid(row=6,column=0,padx=20,pady=15)
    dobEntry=Entry(update_window,font=("roman",11,'bold'),bd=2)
    dobEntry.grid(row=6,column=1,padx=9)

    update_student_Button=ttk.Button(update_window,text='UPDATE',width=15,command=update_data)
    update_student_Button.grid(row=7,columnspan=2,padx=20,pady=12)

    indexing=studentTable.focus()
    #print(indexing)
    content=studentTable.item(indexing)
    listdata=content['values']
    idEntry.insert(0,listdata[0])
    nameEntry.insert(0,listdata[1])
    phoneEntry.insert(0,listdata[2])
    addressEntry.insert(0,listdata[4])
    emailEntry.insert(0,listdata[3])
    genderEntry.insert(0,listdata[5])
    dobEntry.insert(0,listdata[6])

def Exit():
    res=messagebox.askyesno("Confirm","Do you want to exit?")
    if res:
        root.destroy()
    else:
        pass

     

def add_student():
     def add_data():

        if idEntry.get()=='' or phoneEntry.get()=='' or nameEntry.get()==''or emailEntry.get()=='' or addressEntry.get()==''\
        or genderEntry.get()==''or dobEntry.get()=='':
               messagebox.showerror("error","All fields are required",parent=add_window)
        else:
            currentdate=time.strftime("%d/%m/%Y")
            currenttime=time.strftime('%H:%M:%S')
            try:
                query='insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'#%s are for id,phone,name.....,dob,date,time
                mycursor.execute(query,(idEntry.get(),nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get(),currentdate,currenttime))
                con.commit()#commit changes
                result=messagebox.askyesno('Data added successfully do you want to clear the form',parent=add_window)#after inserting the value in add_window it shows a message
                if result:     #it result true
                    idEntry.delete(0,END)
                    nameEntry.delete(0,END)
                    phoneEntry.delete(0,END)
                    emailEntry.delete(0,END)
                    addressEntry.delete(0,END)
                    genderEntry.delete(0,END)
                    dobEntry.delete(0,END)
                else:
                    pass
            except:
                messagebox.showerror("error","Id canot be repeted",parent=add_window)
                return
        


            query="select * from student"
            mycursor.execute(query)
            fetched_data=mycursor.fetchall() 
            #print(fetched_data)  -->print all the inserted data in the table in tuple form in terminal
            studentTable.delete(*studentTable.get_children())#new data will be inserted and previous data will be deleted
            for data in fetched_data:
                datalist= list(data)  #convert the tuple in list
                studentTable.insert('',END,values=datalist) # all the datas will be shown on main page by treeview
                                                            #if we insert new data the whole table will be shown again

     add_window=Toplevel()
     add_window.grab_set()
     add_window.resizable(False,False)
     idLabel=Label(add_window,text='ID',font=("times new roman",15,'bold'))
     idLabel.grid(padx=20,pady=15)
     idEntry=Entry(add_window,font=('roman',11,'bold'),bd=2)
     idEntry.grid(row=0,column=1,padx=9)

     nameLabel=Label(add_window,text='NAME',font=('times new roman',15,'bold'))
     nameLabel.grid(row=1,column=0,padx=20,pady=15)
     nameEntry=Entry(add_window,font=("roman",11,'bold'),bd=2)
     nameEntry.grid(row=1,column=1,padx=9)

     phoneLabel=Label(add_window,text='PHONE',font=('times new roman',15,'bold'))
     phoneLabel.grid(row=2,column=0,padx=20,pady=15)
     phoneEntry=Entry(add_window,font=("roman",11,'bold'),bd=2)
     phoneEntry.grid(row=2,column=1,padx=9)

     emailLabel=Label(add_window,text='EMAIL',font=('times new roman',15,'bold'))
     emailLabel.grid(row=3,column=0,padx=20,pady=15)
     emailEntry=Entry(add_window,font=("roman",11,'bold'),bd=2)
     emailEntry.grid(row=3,column=1,padx=9)

     addressLabel=Label(add_window,text='ADDRESS',font=('times new roman',15,'bold'))
     addressLabel.grid(row=4,column=0,padx=20,pady=15)
     addressEntry=Entry(add_window,font=("roman",11,'bold'),bd=2)
     addressEntry.grid(row=4,column=1,padx=9)

     genderLabel=Label(add_window,text='GENDER',font=('times new roman',15,'bold'))
     genderLabel.grid(row=5,column=0,padx=20,pady=15)
     genderEntry=Entry(add_window,font=("roman",11,'bold'),bd=2)
     genderEntry.grid(row=5,column=1,padx=9)

     dobLabel=Label(add_window,text='D.O.B',font=('times new roman',15,'bold'))
     dobLabel.grid(row=6,column=0,padx=20,pady=15)
     dobEntry=Entry(add_window,font=("roman",11,'bold'),bd=2)
     dobEntry.grid(row=6,column=1,padx=9)

     add_student_Button=ttk.Button(add_window,text='SUBMIT',width=15,command=add_data)
     add_student_Button.grid(row=7,columnspan=2,padx=20,pady=12)

#GUI part
#root =Tk() class
root=ttkthemes.ThemedTk()#same as Tk() we use this class to add themes to buttons

root.get_themes()

root.set_theme("radiance")

root.geometry("1240x827+0+0")
root.resizable(False,False)

root.title("Student Management System")

datetimeLabel=Label(root,font=("times new roman",18,'bold'))
datetimeLabel.pack(side=LEFT,anchor='nw')
clock()
s="Student Management System"
sliderLabel=Label(root,text=s,font=('arial',28,'italic bold'),width=30)
sliderLabel.pack()
slider()

connectButton=ttk.Button(root,text="Connect To Database",width=30,command=connect_database)
connectButton.place(x=980,y=0)

#left frame
leftFrame=Frame(root)#bg="white")
leftFrame.place(x=50,y=80,width=300,height=600)

logo_image=PhotoImage(file='student management system/graduates.png')
logo_label=Label(leftFrame,image=logo_image)
logo_label.grid(row=0,columnspan=2) 

addStudentButton=ttk.Button(leftFrame,text='Add Student',width=20,state=DISABLED,command=add_student)
addStudentButton.grid(row=1,column=1,pady=20)

searchStudentButton=ttk.Button(leftFrame,text='Search Student',width=20,state=DISABLED,command=search_student)
searchStudentButton.grid(row=2,column=1,pady=20)

deleteStudentButton=ttk.Button(leftFrame,text='Delete Student',width=20,state=DISABLED,command=delete_student)
deleteStudentButton.grid(row=3,column=1,pady=20)

updateStudentButton=ttk.Button(leftFrame,text='Update Student',width=20,state=DISABLED,command=update_student)
updateStudentButton.grid(row=4,column=1,pady=20)

showStudentButton=ttk.Button(leftFrame,text='Show Student',width=20,state=DISABLED,command=show_student)
showStudentButton.grid(row=5,column=1,pady=20)

ExportStudentButton=ttk.Button(leftFrame,text='Export Student',width=20,state=DISABLED,command=export_data)
ExportStudentButton.grid(row=6,column=1,pady=20)

exitButton=ttk.Button(leftFrame,text='Exit',width=20,command=Exit)
exitButton.grid(row=7,column=1,pady=20)

#right frame
rightFrame=Frame(root)
rightFrame.place(x=350,y=80,width=820,height=600)

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)

studentTable=ttk.Treeview(rightFrame,columns=("Id","Name","Mobile no","Email","Address","Gender",
                                 "D.O.B","Added Date","Added Time"),
                                 xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

studentTable.pack(fill=BOTH,expand=1)

#add column
studentTable.heading("Id",text='ID')
studentTable.heading("Name",text='NAME')
studentTable.heading("Mobile no",text='MOBILE NO')
studentTable.heading("Email",text='EMAIL')
studentTable.heading("Address",text='ADDRESS')
studentTable.heading("Gender",text='GENDER')
studentTable.heading("D.O.B",text='DOB')
studentTable.heading("Added Date",text='ADDED DATE')
studentTable.heading("Added Time",text='ADDED TIME')

studentTable.column("Id",width=50,anchor=CENTER)#--> shows the column elements in the middle
studentTable.column("Name",width=200,anchor=CENTER)


style=ttk.Style()
style.configure('Treeview',rowheight=40,font=('Arial','12'),fieldbackground='sky blue')#,background="sky blue")#-->rowheight= gapping between the rows


studentTable.config(show='headings')

root.mainloop()