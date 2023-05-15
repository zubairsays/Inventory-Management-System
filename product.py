#Update Button is pending 
from tkinter import *
from tkinter import font
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3


class ProductClass:
    def __init__(self,root):
        self.root=root
        root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()             # Focus on the child window
        self.root.resizable(0,0)   # Tune off window resizeable , now user cannot resize the window
        


        #===================variable=================
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_category=[]
        self.var_supplier=[]

        self.var_categoryy=StringVar()
        self.var_supplierr=StringVar()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()

        self.var_category.append("Select")
        self.var_supplier.append("Select")

        self.fetch_category_supplier() 

    #================Frame prodects details==================

        product_details=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        product_details.place(x=10,y=10,width=500,height=480)

        #=====Title============
        lbl_title=Label(product_details,text="Manage Product Details",fg="white",bg="#1f5c70",font=("goudy old style",20)).pack(side=TOP,fill=X)

        #=======Entry Field and Lebal============

        lbl_category=Label(product_details,text="Category",font=("goudy old style",20,),bg="white").place(x=20,y=60)
        lbl_supplier=Label(product_details,text="Supplier",font=("goudy old style",20,),bg="white").place(x=20,y=120)
        lbl_name=Label(product_details,text="Name",font=("goudy old style",20,),bg="white").place(x=20,y=180)
        lbl_price=Label(product_details,text="Price",font=("goudy old style",20,),bg="white").place(x=20,y=240)
        lblqty=Label(product_details,text="QTY",font=("goudy old style",20,),bg="white").place(x=20,y=300)
        lbl_status=Label(product_details,text="Status",font=("goudy old style",20,),bg="white").place(x=20,y=360)


        cmbcategory=ttk.Combobox(product_details,values=self.var_category,textvariable=self.var_categoryy,state="readonly",justify=CENTER,font=("goudy old style",20))
        cmbcategory.place(x=160,y=60,width=200 )
        cmbcategory.current(0) 


        cmbsupplier=ttk.Combobox(product_details,values=self.var_supplier,textvariable=self.var_supplierr,state="readonly",justify=CENTER,font=("goudy old style",20))
        cmbsupplier.place(x=160,y=120,width=200 )
        cmbsupplier.current(0) 

        txt_name=Entry(product_details,bg="lightyellow",bd=2,relief=RIDGE,textvariable=self.var_name,font=("goudy old style",20),background="white").place(x=160,y=180,width=200)
        txt_price=Entry(product_details,bg="lightyellow",bd=2,relief=RIDGE,textvariable=self.var_price,font=("goudy old style",20),background="white").place(x=160,y=240,width=200)
        txt_qty=Entry(product_details,bg="lightyellow",bd=2,relief=RIDGE,textvariable=self.var_qty,font=("goudy old style",20),background="white").place(x=160,y=300,width=200)

        
        cmbstatus=ttk.Combobox(product_details,values=("Active","Inactive"),textvariable=self.var_status,state="readonly",justify=CENTER,font=("goudy old style",20))
        cmbstatus.place(x=160,y=360,width=200 )
        cmbstatus.current(0) 

        #========================Buttton==========================
        save_btn=Button(product_details,text="Save",command=self.save,bg="#2196f3",fg="black",font=("goudy old style",15),cursor="hand2",activebackground="#2196f3").place(x=20,y=425,w=110,height=30)
        update_btn=Button(product_details,text="Update",command=self.update,bg="#4caf50",fg="black",font=("goudy old style",15),cursor="hand2",activebackground="#4caf50").place(x=140,y=425,w=110,height=30)
        delete_btn=Button(product_details,text="Delete",command=self.delete,bg="#f44336",fg="black",font=("goudy old style",15),cursor="hand2",activebackground="#f44336").place(x=260,y=425,w=110,height=30)
        clear_btn=Button(product_details,text="Clear",command=self.clear,bg="#607d8b",fg="black",font=("goudy old style",15),cursor="hand2",activebackground="#607d8b").place(x=380,y=425,w=100,height=30)
        


        #=========SearchFrame================
        searchFrame=LabelFrame(self.root,text="Search Products",bg="white",font=("goudy old style",12,"bold"))          #Label Frame is same as label , but this give a border shape 
        searchFrame.place(x=520,y=10,width=570,height=70)

        cmbserch=ttk.Combobox(searchFrame,values=("Search By","pid","category","supplier","name"),textvariable=self.var_searchby,state="readonly",justify=CENTER,font=("goudy old style",15))
        cmbserch.place(x=10,y=5,width=180 )
        cmbserch.current(0)                     #This help for bydefault select option ,in tuple we have search by option which we want to select by defalu so the index of search by is 0 .

        txt_search=Entry(searchFrame,bg="lightyellow",textvariable=self.var_searchtxt,font=("goudy old style",15)).place(x=200,y=5)

        txt_search_btn=Button(searchFrame,text="Search",command=self.search,bg="#5bd9c2",fg="black",font=("goudy old style",15),cursor="hand2",activebackground="#5bd9c2").place(x=415,y=5,w=120,height=27)

        #======================Product Tree view================================

        productframe=Frame(self.root,bd=3,relief=RIDGE)
        productframe.place(x=520,y=90,height=400,width=570)

        #========scroll Bar============
        scrolly=Scrollbar(productframe,orient=VERTICAL)
        scrollx=Scrollbar(productframe,orient=HORIZONTAL)

        #Tree view help to show the data in our software in a readalbe format . or table view
        self.producttable=ttk.Treeview(productframe,columns=("pid","category","supplier","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.producttable.yview)
        scrollx.config(command=self.producttable.xview)


        #Creating the heading , these heading shold be same as in our database
        self.producttable.heading("pid",text="P ID")
        self.producttable.heading("category",text="Category")
        self.producttable.heading("supplier",text="Supplier")
        self.producttable.heading("name",text="Name")
        self.producttable.heading("price",text="Price")
        self.producttable.heading("qty",text="QTY")
        self.producttable.heading("status",text="Status")
    

        self.producttable["show"]="headings"           #When we make any heading it will now show any heading untill or unless we run this command

        self.producttable.column("pid",width=90)
        self.producttable.column("category",width=100)
        self.producttable.column("supplier",width=100)
        self.producttable.column("name",width=100)
        self.producttable.column("price",width=100)
        self.producttable.column("qty",width=90)
        self.producttable.column("status",width=100)

        # To set the width of each colunm we do this 
        
        self.producttable.pack(expand=1,fill=BOTH)
        self.producttable.bind("<ButtonRelease-1>",self.get_data)              #When some one click on a perticular data this getdata fuction will call , this is bind methon which help for event handing in a position

        self.show() 
               



    def save(self):
        if self.var_name.get()=="" or self.var_qty.get()=="" or self.var_price.get()=="" or self.var_categoryy.get()=="Select" or self.var_supplierr.get()=="Select":
            messagebox.showerror("Error","Fill all the fiels",parent=self.root)
        else:
            try:
                con=sqlite3.connect(database=r"ims.db")
                cur=con.cursor()
                cur.execute("select * from product where category=? and supplier=? and name=?",
                (
                    self.var_categoryy.get(),
                    self.var_supplierr.get(),
                    self.var_name.get(),
                    
                ))
             
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Product Already Exist",parent=self.root)
                else:
                   
                    cur.execute("insert into product (category,supplier,name,price,qty,status) values(?,?,?,?,?,?)",
                    (
                        self.var_categoryy.get(),
                        self.var_supplierr.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get()

                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product Added Successfully",parent=self.root)
                    self.show()
            except Exception as e:
                messagebox.showerror("Error","Error due to "+str(e),parent=self.root)
  

    #woring here 
    def update(self):
        if self.var_name.get()=="" or self.var_qty.get()=="" or self.var_price.get()=="" or self.var_categoryy.get()=="Select" or self.var_supplierr.get()=="Select":
            messagebox.showerror("Error","All Field Are required!",parent=self.root)
        else:
            try:
                con=sqlite3.connect(database=r"ims.db")
                cur=con.cursor()
                cur.execute("select * from product where category=? and supplier=? and name=?",
                (
                    self.var_categoryy.get(),
                    self.var_supplierr.get(),
                    self.var_name.get(),
                    
                ))
                row=cur.fetchone()
                if(row!=None):
                    cur.execute("update product set price=?,qty=?,status=? where category=? and supplier=? and name=?",
                    (
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                        self.var_categoryy.get(),
                        self.var_supplierr.get(),
                        self.var_name.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product updated Successfully",parent=self.root)
                    self.show()
                    
                else:
                    messagebox.showerror("Error","No record found to Update",parent=self.root)
                


            except Exception as e:
                messagebox.showerror("Erroe",f"Error due to {str(e)}",parent=self.root)


    def delete(self):
        if self.var_name.get()=="" or self.var_qty.get()=="" or self.var_price.get()=="" or self.var_categoryy.get()=="Select" or self.var_supplierr.get()=="Select":
            messagebox.showerror("Error","Fill all the fiels",parent=self.root)

        else:
            try:
                con=sqlite3.connect(database=r"ims.db")
                cur=con.cursor()
                cur.execute("select * from product where category=? and supplier=? and name=? and price=? and qty=? and status=?",
                (
                    self.var_categoryy.get(),
                    self.var_supplierr.get(),
                    self.var_name.get(),
                    self.var_price.get(),
                    self.var_qty.get(),
                    self.var_status.get()
                    
                ))
                result=cur.fetchone()
                # print(result)
                if result!=None:
                    confirm=messagebox.askyesno("Confirm","Do You Really Want To Delete ?",parent=self.root)
                    if confirm==True:
                        cur.execute("delete from product where category=? and supplier=? and name=? and price=? and qty=? and status=?",
                        (
                            self.var_categoryy.get(),
                            self.var_supplierr.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get()
                            
                        ))
                        con.commit()
                        messagebox.showinfo("Deleted","Deleted Successfully",parent=self.root)
                        self.show()
                  

                else:
                    messagebox.showerror("Error","This record does't exist in database",parent=self.root)

            except Exception as e:
                messagebox.showerror("Error","Error due to "+str(e),parent=self.root)
                
        

    def clear(self):
        self.var_categoryy.set("Select")
        self.var_supplierr.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")

        self.var_searchby.set("Search By")
        self.var_searchtxt.set("")

        self.show()
    
    def search(self):     
        
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()

        try:
            if self.var_searchtxt.get()=="" or self.var_searchby.get()=="Search By":
                messagebox.showerror("Error","Select any option and Type keyword in serch box",parent=self.root)
            else:
           
                cur.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                row=cur.fetchall()
              
                if len(row)!=0:
                    self.producttable.delete(*self.producttable.get_children())
                    for row in row:
                        self.producttable.insert('',END,values=row)
                else:
                    pass
                    #print("No record filtered")

        except Exception as e:
            messagebox.showerror("Error","Error due to "+str(e),parent=self.root)

 
    def show(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            result=cur.fetchall()
            # print(result)
            self.producttable.delete(*self.producttable.get_children())
            for i in result:
                self.producttable.insert('',END,values=i)

        except Exception as e:
            messagebox.showerror("Error","Error due to "+str(e),parent=self.root)


    def get_data(self,ev):
        f=self.producttable.focus()    
        contant=(self.producttable.item(f))        #contant variable contain the data of that column as a dictnary
        row=contant["values"]  #row have all the data in a list 
        
        self.var_categoryy.set(row[1])
        self.var_supplierr.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])


        

    def fetch_category_supplier(self):               #   It will fetch all the record and show in the combo box
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            #This potion is for category 
            cur.execute("select name from category")
            result=cur.fetchall()
            for i in result:
                self.var_category.append(i[0])
        

            #This potion is for supplier
            cur.execute("select name from supplier")
            result=cur.fetchall()
            for i in result:
                self.var_supplier.append(i[0])

        except Exception as e:
            messagebox.showerror("Error","Error due to "+str(e),parent=self.root)

        
if __name__=="__main__":
    root=Tk()
    obj=ProductClass(root)
    root.mainloop()