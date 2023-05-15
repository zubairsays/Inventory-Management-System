from tkinter import *
from tkinter import font
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3


class CategoryClass:
    def __init__(self,root):
        self.root=root
        root.geometry("1100x500+220+130")
        self.root.title("Inventry Management System")
        self.root.config(bg="white")
        self.root.focus_force()             #Focus on the child window
        self.root.resizable(0,0)   #Tuen off window resizeable , now user cannot resize the window
        # self.root.bind('<Return>', self.add_ev)              #bind the Enter key event


        #===========vaiable============
        self.cat_id=StringVar()
        self.var_name=StringVar()
        #==========Title===========
        lbl_title=Label(self.root,text="Manage Category Product",font=("Goudy old style",30,),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20) 
        lbl_title=Label(self.root,text="Enter Category Name",font=("Goudy old style",30,),bg="white").place(x=50,y=100)
        txt_field=Entry(self.root,textvariable=self.var_name,font=("Goudy old style",18,),bg="lightyellow")
        txt_field.bind('<Return>',self.add_ev)
        txt_field.place(x=50,y=170,width=300)


        #==============Button=================

        btn_add=Button(self.root,text="Add",command=self.add,font=("Goudy old style",15,),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=170,width=150,height=30)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("Goudy old style",15,),bg="red",fg="white",cursor="hand2").place(x=520,y=170,width=150,height=30)


        #================================================== CAtegory Details TreeView ========================================================
        catframe=Frame(self.root,bd=3,relief=RIDGE)
        catframe.place(x=700,y=100,w=380,height=100)

        #========scroll Bar============
        scrolly=Scrollbar(catframe,orient=VERTICAL)
        scrollx=Scrollbar(catframe,orient=HORIZONTAL)

        #Tree view help to show the data in our software in a readalbe format . or table view
        self.categorytable=ttk.Treeview(catframe,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.categorytable.yview)
        scrollx.config(command=self.categorytable.xview)


        #Creating the heading , these heading shold be same as in our database
        self.categorytable.heading("cid",text="C ID")
        self.categorytable.heading("name",text="Name")
     

        self.categorytable["show"]="headings"           #When we make any heading it will now show any heading untill or unless we run this command


        # To set the width of each colunm we do this 
        self.categorytable.column("cid",width=90)
        self.categorytable.column("name",width=100)

        self.categorytable.pack(expand=1,fill=BOTH)
       
        self.categorytable.bind("<ButtonRelease-1>",self.get_data)              #When some one click on a perticular data this getdata fuction will call , this is bind methon which help for event handing in a position


        #====================Image resizeable====================
        self.img1=Image.open("images/cat.jpg")
        self.img1=self.img1.resize((500,250),Image.ANTIALIAS)
        self.img1=ImageTk.PhotoImage(self.img1)
        self.lbl_img1=Label(self.root,image=self.img1,bd=2,relief=RAISED)
        self.lbl_img1.place(x=50,y=220)

        self.img2=Image.open("images/category.jpg")
        self.img2=self.img2.resize((500,250),Image.ANTIALIAS)
        self.img2=ImageTk.PhotoImage(self.img2)
        self.lbl_img2=Label(self.root,image=self.img2,bd=2,relief=RAISED)
        self.lbl_img2.place(x=580,y=220)

        self.show()


    #================Add=====================
    #This function is for Enter event
    def add_ev(self,ev):
        self.add()



    def add(self):
        con=sqlite3.connect(database=r"ims.db")             #Making the connection with the database
        cur=con.cursor()                        #To execute the command we make the cirsor

        try:
            if  self.var_name.get()=="":
                messagebox.showerror("Error",f"Please Enter the category name",parent=self.root)
            else:
                cur.execute("select * from category where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Category already exists, Enter other catogory ",parent=self.root)
                else:
                    cur.execute("insert into category (name) values(?)",
                    (
                       
                        self.var_name.get(),
                        

                    ))
                    con.commit()
                    messagebox.showinfo("Success","Category Added Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            cur.execute("select * from category")
            row=cur.fetchall()
            self.categorytable.delete(*self.categorytable.get_children())
            for item in row:
                self.categorytable.insert('',END,values=item)

        except Exception as e:
            messagebox.showerror("Eoor","Error Due to "+str(e),parent=self.root)
            

        
    def get_data(self,ev):
        f=self.categorytable.focus()    
        content=(self.categorytable.item(f))        #content variable contain the data of that column as a dictnary
        row=content["values"]  #row have all the data in a list
        # print(row)
        self.var_name.set(row[1])

    def delete(self):
        if self.var_name.get() == "":
            messagebox.showerror("Error","Category name must required",parent=self.root)
        else:
            con=sqlite3.connect(database=r"ims.db")      
            cur=con.cursor()

            try:
                confirm=messagebox.askyesno("Confirm","You Want to Delete this record",parent=self.root)
                if confirm==True: 
                    cur.execute("delete from category where name=?",(self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Deleted","Deleted succesfully",parent=self.root)
                    self.var_name.set("")
                    self.show()
            except Exception as e:
                messagebox.showerror("Error Due to "+str(e),parent=self.root)

                






if __name__=="__main__":
    root=Tk()
    obj=CategoryClass(root)
    root.mainloop()
