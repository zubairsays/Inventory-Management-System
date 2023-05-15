from posixpath import expanduser
from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3


class SupplierClass:
    def __init__(self,root):
        self.root=root
        root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()            #Focus on the child window
        self.root.resizable(0,0)
        #Turn off window resizeable, now user cannot resize the window
        #self.root.grabset()                 


        #=============variables============
        
        self.var_invoice=StringVar()
        self.var_invoice1=StringVar()
        self.var_supplier_name=StringVar()
        self.var_contact=StringVar()
       
        title=Label(self.root,text="Manage Supplier Details",font=("goudy old style",20),bg="#0f4d7d",fg="white").place(x=50,y=20,width=1000)

        lbl_invoice_number=Label(self.root,text="Invoice No.",font=("goudy old style",15),bg="white",).place(x=700,y=80)
        txt_search=Entry(self.root,bg="lightyellow",textvariable=self.var_invoice1,font=("goudy old style",15),background="lightyellow").place(x=800,y=80,width=140)
        search_btn=Button(self.root,text="Search",bg="#2196f3",fg="black",font=("goudy old style",15),cursor="hand2",activebackground="#2196f3",command=self.search).place(x=950,y=80,w=100,height=28)
        

        #===============Content================
        #===Row1=====
        lbl_invoice_numberr=Label(self.root,text="Invoice No.",font=("goudy old style",15),bg="white",).place(x=50,y=80)
        txt_invoice_number=Entry(self.root,textvariable=self.var_invoice,font=("goudy old style",15),bg="lightyellow").place(x=200,y=80,width=180 )
      
        #====Row2===
        lbl_name=Label(self.root,text="Supplier Name",font=("goudy old style",15),bg="white",).place(x=50,y=120)
       
        txt_name=Entry(self.root,textvariable=self.var_supplier_name,font=("goudy old style",15),bg="lightyellow",).place(x=200,y=120,width=180 )
       
        #====Row3======
        lbl_contant=Label(self.root,text="Contact",font=("goudy old style",15),bg="white",).place(x=50,y=160)
        txt_contant=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow",).place(x=200,y=160,width=180 )
       
        #===Row4===
        lbl_description=Label(self.root,text="Address",font=("goudy old style",15),bg="white",).place(x=50,y=200)
        self.txt_description=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_description.place(x=200,y=200,width=470,height=150 )
       
        #====Buttons=====
        save_btn=Button(self.root,text="Save",command=self.add,bg="#2196f3",fg="black",font=("goudy old style",15),cursor="hand2",activebackground="#2196f3").place(x=200,y=400,w=110,height=30)
        update_btn=Button(self.root,text="Update",command=self.update,bg="#4caf50",fg="black",font=("goudy old style",15),cursor="hand2",activebackground="#4caf50").place(x=320,y=400,w=110,height=30)
        delete_btn=Button(self.root,text="Delete",command=self.delete,bg="#f44336",fg="black",font=("goudy old style",15),cursor="hand2",activebackground="#f44336").place(x=440,y=400,w=110,height=30)
        clear_btn=Button(self.root,text="Clear",command=self.clear,bg="#607d8b",fg="black",font=("goudy old style",15),cursor="hand2",activebackground="#607d8b").place(x=560,y=400,w=110,height=30)
        
        #================================================== Supplier Details ========================================================
        supframe=Frame(self.root,bd=3,relief=RIDGE)
        supframe.place(x=700,y=120,height=330,width=380)

        #========scroll Bar============
        scrolly=Scrollbar(supframe,orient=VERTICAL)
        scrollx=Scrollbar(supframe,orient=HORIZONTAL)

        #Tree view help to show the data in our software in a readalbe format . or table view
        self.supliertable=ttk.Treeview(supframe,columns=("sup_id","invoice_no","name","contact","address"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.supliertable.yview)
        scrollx.config(command=self.supliertable.xview)


        #Creating the heading , these heading shold be same as in our database
        self.supliertable.heading("sup_id",text="Sup ID")
        self.supliertable.heading("invoice_no",text="Invoice No.")
        self.supliertable.heading("name",text="Name")
        self.supliertable.heading("contact",text="Contact")
        self.supliertable.heading("address",text="Address")
      

        self.supliertable["show"]="headings"           #When we make any heading it will now show any heading untill or unless we run this command


        # To set the width of each colunm we do this 

        self.supliertable.column("sup_id",width=50)
        self.supliertable.column("invoice_no",width=70)
        self.supliertable.column("name",width=100)
        self.supliertable.column("contact",width=100)
        self.supliertable.column("address",width=100)

        self.supliertable.pack(expand=1,fill=BOTH)
        self.supliertable.bind("<ButtonRelease-1>",self.get_data)              #When some one click on a perticular data this getdata fuction will call , this is bind methon which help for event handing in a position

        self.show()

         

    #=============================================================================================================

    def add(self):
        if self.var_invoice.get()=="" or self.var_supplier_name.get()=="":
            messagebox.showerror("Error","Invoice Number and Name Must required!",parent=self.root)
        
        else:
            try:
                con=sqlite3.connect(database=r"ims.db")
                cur=con.cursor()
                cur.execute("select * from supplier where invoice_no=?",(self.var_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Supplier ID Already assigned to the employee, Try different one ",parent=self.root)
                else:
                    cur.execute("insert into supplier (invoice_no,name,contact,address) values(?,?,?,?)",(self.var_invoice.get(),self.var_supplier_name.get(),self.var_contact.get(),self.txt_address.get(1.0,END)))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Added Successfully.",parent=self.root)
                    self.show()


            except Exception as e:
                messagebox.showerror("Error","Error due to "+str(e),parent=self.root)

    def update(self):
        if self.var_invoice.get()=="" or self.var_supplier_name.get()=="":
            messagebox.showerror("Error","Invoice Number and Name Must required!",parent=self.root)
        else:
            con=sqlite3.connect(database=r"ims.db")
            cur=con.cursor()
            try:
                cur.execute("select * from supplier where invoice_no=?",(self.var_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice ID",parent=self.root)
                else:
                    cur.execute("update supplier set name=?,contact=?,description=? where invoice_no=?",
                    (
                        self.var_supplier_name.get(),
                        self.var_contact.get(),
                        self.txt_address.get(1.0,END),
                        self.var_invoice.get()
                        
                        
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Updated Successfully",parent=self.root)
                    self.show()
            except Exception as e:
                messagebox.showerror("Error","Error due to "+str(e),parent=self.root)
                

    def delete(self):           #delete a particular record from the database
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()

        try:
            if self.var_invoice.get()=="":
                messagebox.showerror("Error",f"Supplier ID must be required",parent=self.root)
            else:
                cur.execute("select * from supplier where invoice_no=?",(self.var_invoice.get(),))
                row=cur.fetchone()
                if row==None:               #To delete a data there should be a valid supplier, thats why we are putting the validation here
                    messagebox.showerror("Error","Invalid Supplier ID",parent=self.root)
                confirm=messagebox.askyesno("Confirm","Are You Sure ,You want to remove the record ?",parent=self.root)
                if confirm==True:
                     
                    cur.execute("delete from supplier where invoice_no=?",(self.var_invoice.get(),))
                    con.commit()
                    self.show()
                    self.clear()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)


        

    def clear(self):
        self.var_invoice.set("")
        self.var_invoice1.set("")
        self.var_supplier_name.set("")
        self.var_contact.set("")
        self.txt_address.delete(1.0,END)
        self.show()

    def get_data(self,ev):              #When someone is click on the data on tree view , this function will put data selected data in the textfield
        f=self.supliertable.focus()    
        contant=(self.supliertable.item(f))        #contant variable contain the data of that column as a dictnary
        # print(contant)
        row=contant["values"]  #row have all the data in a list 
        # print(row)
        self.var_invoice.set(row[1])
        self.var_supplier_name.set(row[2])
        self.var_contact.set(row[3])
        self.txt_address.delete(1.0,END)
        self.txt_address.insert(END,row[4])


    def show(self):     #This function help to show the data in the tree view
        
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()

        try:
            cur.execute("select * from supplier")           #select * the data from the table
            row=cur.fetchall()              #fetch all the data in the row variable 
            self.supliertable.delete(*self.supliertable.get_children())           #delete previous data from the treeview
            for row in row:
                self.supliertable.insert('',END,values=row)            #insert new data from the tree view, We only pass the tuples as a value 
        except Exception as e:
            messagebox.showerror("Error","Error Due To "+str(e),parent=self.root)

    def search(self):
        if(self.var_invoice1.get()==""):
            messagebox.showerror("Error","Searc Field can not be empty")
        else:
            try:
                con=sqlite3.connect(database=r"ims.db")
                cur=con.cursor()
                cur.execute("select * from supplier where invoice_no=?",(self.var_invoice1.get(),))
                data=cur.fetchone()
                if(data!=None):
                    print(data)
                    self.supliertable.delete(*self.supliertable.get_children())     

                    self.supliertable.insert('',END,values=data)
                    
                else:
                    messagebox.showerror("No record","No record Found")
                
            except Exception as e:
                messagebox.showerror("Error",f"Error due to {str(e)}")

       

   


if __name__=="__main__":
    root=Tk()
    obj=SupplierClass(root)
    root.mainloop()
