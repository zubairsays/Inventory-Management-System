from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
import os


class EmployeeClass:
    def __init__(self,root):
        self.root=root
        root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()             # Focus on the child window
        self.root.resizable(0,0)            # Turn off window resizeable, now user cannot resize the window

        # =============Variables============
        self.var_searchtxt = StringVar()
        self.var_searchby = StringVar()
        self.var_empid = StringVar()
        self.var_gender = StringVar()
        self.var_contack = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()



        title=  Label(self.root,text="Admin Details",font=("goudy old style",30),bg="#0f4d7d",fg="white").place(x=50,y=50,width=1000)

        # =============== Content ================
        # === Row1 =====
        lbl_empid = Label(self.root,text="Emp Id",font=("goudy old style",15),bg="white",).place(x=50,y=150)
        lbl_gender = Label(self.root,text="Gender",font=("goudy old style",15),bg="white",).place(x=350,y=150)
        lbl_contact = Label(self.root,text="Contact",font=("goudy old style",15),bg="white",).place(x=750,y=150)

        txt_empid = Entry(self.root,textvariable=self.var_empid,font=("goudy old style",15),bg="lightyellow").place(x=150,y=150,width=180 )
        cmbgender = ttk.Combobox(self.root,values = ("Select","Male","Female","Other"),textvariable=self.var_gender, state="readonly",justify=CENTER,font=("goudy old style",15))
        cmbgender.place(x=500,y=150,width=180 )
        cmbgender.current(0)  
        txt_contact = Entry(self.root,textvariable=self.var_contack,font=("goudy old style",15),bg="lightyellow",).place(x=850,y=150,width=180 )

        # ==== Row2 ===
        lbl_name = Label(self.root,text ="Name",font=("goudy old style",15),bg="white",).place(x=50,y=190)
        lbl_dob = Label(self.root,text="D.O.B",font=("goudy old style",15),bg="white",).place(x=350,y=190)
        lbl_doj = Label(self.root,text="D.O.J",font=("goudy old style",15),bg="white",).place(x=750,y=190)

        txt_name = Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow",).place(x=150,y=190,width=180 )
        txt_dob = Entry(self.root,textvariable=self.var_dob,font=("goudy old style",15),bg="lightyellow",).place(x=500,y=190,width=180 )
        txt_doj = Entry(self.root,textvariable=self.var_doj,font=("goudy old style",15),bg="lightyellow",).place(x=850,y=190,width=180 )

        # ==== Row3 ======
        lbl_email = Label(self.root,text="Email",font=("goudy old style",15),bg="white",).place(x=50,y=230)
        lbl_pass = Label(self.root,text="Password",font=("goudy old style",15),bg="white",).place(x=350,y=230)
        lbl_utype = Label(self.root,text="User Type",font=("goudy old style",15),bg="white",).place(x=750,y=230)

        txt_email = Entry(self.root,textvariable=self.var_email,font=("goudy old style",15),bg="lightyellow",).place(x=150,y=230,width=180 )
        txt_pass = Entry(self.root,textvariable=self.var_pass,font=("goudy old style",15),bg="lightyellow",).place(x=500,y=230,width=180 )
        cmbutype = ttk.Combobox(self.root,values=("Admin",),textvariable=self.var_utype,state="readonly",justify=CENTER,font=("goudy old style",15))
        cmbutype.place(x=850,y=230,width=180 )
        cmbutype.current(0)  
        

        # === Row4 ===
        lbl_address = Label(self.root,text="Address",font=("goudy old style",15),bg="white",).place(x=50,y=270)
 
        self.txt_address = Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_address.place(x=150,y=270,width=300,height=60 )
     
        # ==== Buttons =====
        save_btn = Button(self.root,text="Save",command=self.add,bg="#2196f3",fg="black",font=("goudy old style",15),cursor="hand2",activebackground="#2196f3").place(x=500,y=310,w=110,height=30)
        clear_btn = Button(self.root,text="Clear",command=self.clear,bg="#607d8b",fg="black",font=("goudy old style",15),cursor="hand2",activebackground="#607d8b").place(x=860,y=310,w=110,height=30)
        


    # =============================================================================================================

    def add(self):
        con = sqlite3.connect(database=r"ims.db")             # Making the connection with the database
        cur = con.cursor()                                    # To execute the command we make the cirsor

        try:
            if self.var_empid.get() == "" or self.var_name.get() == "":
                messagebox.showerror("Error",f"Employee ID and Name must be required",parent=self.root)
            else:
                cur.execute("select * from employee where eid=?",(self.var_empid.get(),))
                row = cur.fetchone()
                if row != None:
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
                    messagebox.showinfo("Success","Details Saved Successfully , Now login into the Dashboard",parent=self.root)
                    self.root.destroy()
                    os.system("login.py")

                   
                    
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)



    def clear(self):                # Clearing all the field
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


if __name__ == "__main__":
    root = Tk()
    obj = EmployeeClass(root)
    root.mainloop()
