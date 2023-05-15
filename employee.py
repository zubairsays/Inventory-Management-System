from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3


class EmployeeClass:
    def __init__(self,root):
        self.root=root
        root.geometry("1100x500+220+130")
        self.root.title("Inventry Management System")
        self.root.config(bg="white")
        self.root.focus_force()             #Focus on the child window
        self.root.resizable(0,0)                    #Tuen off window resizeable , now user cannot resize the window

        #=============variables============
        self.var_searchtxt=StringVar()
        self.var_searchby=StringVar()
        self.var_empid=StringVar()
        self.var_gender=StringVar()
        self.var_contack=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        self.var_salary=StringVar()

        #=========SearchFrame================
        searchFrame=LabelFrame(self.root,text="Search Employee",bg="white",font=("goudy old style",12,"bold"))          #Label Frame is same as label , but this give a border shape 
        searchFrame.place(x=250,y=20,width=600,height=70)
        #====Combo Box=====
        cmbserch=ttk.Combobox(searchFrame,values=("Search By","Email","Name","Contact"),textvariable=self.var_searchby,state="readonly",justify=CENTER,font=("goudy old style",15))
        cmbserch.place(x=10,y=10,width=180 )
        cmbserch.current(0)                     #This help for bydefault select option ,in tuple we have search by option which we want to select by defalu so the index of search by is 0 .

        txt_search=Entry(searchFrame,bg="lightyellow",textvariable=self.var_searchtxt,font=("goudy old style",15)).place(x=200,y=10)

        txt_search_btn=Button(searchFrame,text="Search",command=self.search,bg="#4caf50",fg="black",font=("goudy old style",15),cursor="hand2",activebackground="#4acf50").place(x=415,y=9,w=150,height=30)


        title=Label(self.root,text="Employee Details",font=("goudy old style",15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1000)

        #===============Contant================
        #===Row1=====
        lbl_empid=Label(self.root,text="Emp Id",font=("goudy old style",15),bg="white",).place(x=50,y=150)
        lbl_gender=Label(self.root,text="Gender",font=("goudy old style",15),bg="white",).place(x=350,y=150)
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white",).place(x=750,y=150)

        txt_empid=Entry(self.root,textvariable=self.var_empid,font=("goudy old style",15),bg="lightyellow").place(x=150,y=150,width=180 )
        cmbgender=ttk.Combobox(self.root,values=("Select","Male","Female","Other"),textvariable=self.var_gender,state="readonly",justify=CENTER,font=("goudy old style",15))
        cmbgender.place(x=500,y=150,width=180 )
        cmbgender.current(0)  
        txt_contact=Entry(self.root,textvariable=self.var_contack,font=("goudy old style",15),bg="lightyellow",).place(x=850,y=150,width=180 )

        #====Row2===
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="white",).place(x=50,y=190)
        lbl_dob=Label(self.root,text="D.O.B",font=("goudy old style",15),bg="white",).place(x=350,y=190)
        lbl_doj=Label(self.root,text="D.O.J",font=("goudy old style",15),bg="white",).place(x=750,y=190)

        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow",).place(x=150,y=190,width=180 )
        txt_dob=Entry(self.root,textvariable=self.var_dob,font=("goudy old style",15),bg="lightyellow",).place(x=500,y=190,width=180 )
        txt_doj=Entry(self.root,textvariable=self.var_doj,font=("goudy old style",15),bg="lightyellow",).place(x=850,y=190,width=180 )

        #====Row3======
        lbl_email=Label(self.root,text="Email",font=("goudy old style",15),bg="white",).place(x=50,y=230)
        lbl_pass=Label(self.root,text="Password",font=("goudy old style",15),bg="white",).place(x=350,y=230)
        lbl_utype=Label(self.root,text="User Type",font=("goudy old style",15),bg="white",).place(x=750,y=230)

        txt_email=Entry(self.root,textvariable=self.var_email,font=("goudy old style",15),bg="lightyellow",).place(x=150,y=230,width=180 )
        txt_pass=Entry(self.root,textvariable=self.var_pass,font=("goudy old style",15),bg="lightyellow",).place(x=500,y=230,width=180 )
        cmbutype=ttk.Combobox(self.root,values=("Admin","Employee"),textvariable=self.var_utype,state="readonly",justify=CENTER,font=("goudy old style",15))
        cmbutype.place(x=850,y=230,width=180 )
        cmbutype.current(0)  
        

        #===Row4===
        lbl_address=Label(self.root,text="Address",font=("goudy old style",15),bg="white",).place(x=50,y=270)
        lbl_salary=Label(self.root,text="Salary",font=("goudy old style",15),bg="white",).place(x=500,y=270)

        self.txt_address=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_address.place(x=150,y=270,width=300,height=60 )
        txt_salary=Entry(self.root,textvariable=self.var_salary,font=("goudy old style",15),bg="lightyellow",).place(x=600,y=270,width=180 )

        #====Buttons=====
        save_btn=Button(self.root,text="Save",command=self.add,bg="#2196f3",fg="black",font=("goudy old style",15),cursor="hand2",activebackground="#2196f3").place(x=500,y=310,w=110,height=30)
        update_btn=Button(self.root,text="Update",command=self.update,bg="#4caf50",fg="black",font=("goudy old style",15),cursor="hand2",activebackground="#4caf50").place(x=620,y=310,w=110,height=30)
        delete_btn=Button(self.root,text="Delete",command=self.delete,bg="#f44336",fg="black",font=("goudy old style",15),cursor="hand2",activebackground="#f44336").place(x=740,y=310,w=110,height=30)
        clear_btn=Button(self.root,text="Clear",command=self.clear,bg="#607d8b",fg="black",font=("goudy old style",15),cursor="hand2",activebackground="#607d8b").place(x=860,y=310,w=110,height=30)
        
        #================================================== Employee Details ========================================================
        empframe=Frame(self.root,bd=3,relief=RIDGE)
        empframe.place(x=0,y=350,relwidth=1,height=150)

        #========scroll Bar============
        scrolly=Scrollbar(empframe,orient=VERTICAL)
        scrollx=Scrollbar(empframe,orient=HORIZONTAL)

        #Tree view help to show the data in our software in a readalbe format . or table view
        self.employeetable=ttk.Treeview(empframe,columns=("eid","name","email","gender","contact","dob","doj","pass","utype","address","salary"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.employeetable.yview)
        scrollx.config(command=self.employeetable.xview)


        #Creating the heading , these heading shold be same as in our database
        self.employeetable.heading("eid",text="EMP ID")
        self.employeetable.heading("name",text="Name")
        self.employeetable.heading("email",text="Email")
        self.employeetable.heading("gender",text="Gender")
        self.employeetable.heading("contact",text="Contact")
        self.employeetable.heading("dob",text="D.O.B")
        self.employeetable.heading("doj",text="D.O.J")
        self.employeetable.heading("pass",text="Password")
        self.employeetable.heading("utype",text="UserType")
        self.employeetable.heading("address",text="Address")
        self.employeetable.heading("salary",text="Salary")

        self.employeetable["show"]="headings"           #When we make any heading it will now show any heading untill or unless we run this command


        # To set the width of each colunm we do this 
        self.employeetable.column("eid",width=10)
        self.employeetable.column("name",width=50)
        self.employeetable.column("email",width=50)
        self.employeetable.column("gender",width=10)
        self.employeetable.column("contact",width=10)
        self.employeetable.column("dob",width=10)
        self.employeetable.column("doj",width=10)
        self.employeetable.column("pass",width=20)
        self.employeetable.column("utype",width=10)
        self.employeetable.column("address",width=100)
        self.employeetable.column("salary",width=10)
        self.employeetable.pack(expand=1,fill=BOTH)
        self.employeetable.bind("<ButtonRelease-1>",self.get_data)              #When some one click on a perticular data this getdata fuction will call , this is bind methon which help for event handing in a position

        self.show()         #This is the fucntion , to understand what this function do just go throug that 

    #=============================================================================================================

    def add(self):
        con=sqlite3.connect(database=r"ims.db")             #Making the connection with the database
        cur=con.cursor()                        #To execute the command we make the cirsor

        try:
            if self.var_empid.get()=="" or self.var_name.get()=="":
                messagebox.showerror("Error",f"Employee ID and Name must be required",parent=self.root)
            else:
                cur.execute("select * from employee where eid=?",(self.var_empid.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Employee ID Already assigned to the employee, Try different one ",parent=self.root)
                else:
                    cur.execute("insert into employee (eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        self.var_empid.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contack.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get(1.0,END),
                        self.var_salary.get()

                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Added Successfully",parent=self.root)
                    self.show()
                    
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)


    def show(self):     #This function help to show the data in the tree view
        
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()

        try:
            cur.execute("select * from employee")           #select * the data from the table
            row=cur.fetchall()              #fetch all the data in the row variable 
            self.employeetable.delete(*self.employeetable.get_children())           #delete previous data from the treeview
            for row in row:
                self.employeetable.insert('',END,values=row)            #insert new data from the tree view, We only pass the tuples as a value 
     
        
        except Exception as e:
            print(e)
    
    def get_data(self,ev):              #When someone is click on the data on tree view , this function will put data selected data in the textfield
        f=self.employeetable.focus()    
        contant=(self.employeetable.item(f))        #contant variable contain the data of that column as a dictnary
        row=contant["values"]  #row have all the data in a list 
        # print(row)
        self.var_empid.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contack.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete(1.0,END)
        self.txt_address.insert(END,row[9])
        self.var_salary.set(row[10])
        
    def update(self):   #To Update the data 
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()

        try:
            if self.var_empid.get()=="" or self.var_name.get()=="":
                messagebox.showerror("Error",f"Employee ID and Name must be required",parent=self.root)
            else:
                cur.execute("select * from employee where eid=?",(self.var_empid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    cur.execute("update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",
                    (
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contack.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get(1.0,END),
                        self.var_salary.get(),
                        self.var_empid.get()

                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Updated Successfully",parent=self.root)
                    self.show()
                    

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)

    def delete(self):           #delete a particular record from the database
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()

        try:
            if self.var_empid.get()=="":
                messagebox.showerror("Error",f"Employee ID must be required",parent=self.root)
            else:
                cur.execute("select * from employee where eid=?",(self.var_empid.get(),))
                row=cur.fetchone()
                if row==None:               #To delete a data there should be a valid emp id , thats why we are putting the validation here
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
            
                confirm=messagebox.askyesno("Confirm","Are You Sure , You Really Want to Delete the Record",parent=self.root)   #asking For conferfation
                if confirm==True:
                    cur.execute("delete from employee where eid=?",(self.var_empid.get(),))
                    con.commit()
                    self.show()
                    self.clear()
                    

        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)

    def clear(self):                #cleraing all the field 
        self.var_searchtxt.set("")
        self.var_searchby.set("Search By")
        self.var_empid.set("")
        self.var_gender.set("Select")
        self.var_contack.set("")
        self.var_name.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_email.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.var_salary.set("")
        self.txt_address.delete(1.0,END)
        self.show()


    def search(self):     
        
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()

        try:
            if self.var_searchtxt.get()=="" or self.var_searchby.get()=="Search By":
                messagebox.showerror("Error","Select any option and Type keyword in serch box",parent=self.root)
            else:
                cur.execute("select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                row=cur.fetchall()
                # print(len(row))
                if len(row)!=0:
                    self.employeetable.delete(*self.employeetable.get_children())
                    for row in row:
                        self.employeetable.insert('',END,values=row)

        except Exception as e:
            print(e)
     



if __name__=="__main__":
    root=Tk()
    obj=EmployeeClass(root)
    root.mainloop()
