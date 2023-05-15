import time
from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter import ttk
import os
import tempfile


class BillClass:
    def __init__(self,root):
        self.root=root
        root.geometry("1350x750+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.cart_list = []
        self.chk_print = 0

        # =============Title=========
        self.icon_title=PhotoImage(file="images/logo1.png")     # icon image

        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,'bold'),bg='#010c48',fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        # ============btn_log_out=========
        btn_logout=Button(self.root,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2",command=self.logOut).place(x=1100,y=15,height=40,width=160)

        # ==========clock============
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management\t\t Date: dd//mm//YYYY \t\t Time: HH//MM//SS", font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # =================================================Product frame====================================================================
        self.var_search=StringVar()

        ProductFrame = Frame(self.root,relief=RIDGE,bg="white",bd=4)
        ProductFrame.place(x=6,y=110,width=410,height=550)

        pTitle = Label(ProductFrame,text="All Products",font=("goudy old style",20,"bold"),fg="white",bg="#262626").pack(side=TOP,fill=X)

        ProductFrame2 = Frame(ProductFrame,relief=RIDGE,bg="white",bd=2)
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        labl_search=Label(ProductFrame2,text="Search Product | By Name",font=("times new roman",15,"bold"),fg="green",background="white").place(x=2,y=5)
        lbl_name=Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),background="white").place(x=5,y=45)
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15,),background="lightyellow").place(x=132,y=47,width=150,h=22)
        btn_search=Button(ProductFrame2,text="Search",font=("goudy old style",15),fg="black",bg="#93f071",cursor="hand2",command=self.search).place(x=286,y=45,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text="Show All",font=("goudy old style",15),fg="white",bg="#163450",cursor="hand2",command=self.show).place(x=286,y=10,width=100,height=25)

         #======================ProductDetails=====================================

        ProductFrame3=Frame(ProductFrame,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,height=380,width=398)

        #========scroll Bar============
        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)

        #Tree view help to show the data in our software in a readalbe format . or table view
        self.product_details=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.product_details.yview)
        scrollx.config(command=self.product_details.xview)


        #Creating the heading, these heading shold be same as in our database
        self.product_details.heading("pid",text="P_ID")
        self.product_details.heading("name",text="Name")
        self.product_details.heading("price",text="Price")
        self.product_details.heading("qty",text="QTY")
        self.product_details.heading("status",text="Status")
      

        self.product_details["show"] = "headings"           #When we make any heading it will now show any heading untill or unless we run this command


        # To set the width of each column we do this

        self.product_details.column("pid",width=50)
        self.product_details.column("name",width=70)
        self.product_details.column("price",width=100)
        self.product_details.column("qty",width=100)
        self.product_details.column("status",width=100)
        self.product_details.pack(expand=1,fill=BOTH)
        self.product_details.bind("<ButtonRelease-1>",self.getdata)              #When some one click on a perticular data this getdata fuction will call , this is bind methon which help for event handing in a position

        lbl_note=Label(ProductFrame,text="Enter 0 Quantity to Remove the Product from the cart",font=("goudy old style",10),anchor="w",bg="white",fg="red").pack(side=BOTTOM,fill=X)


        #======================customerFrame================================
        self.var_cname=StringVar()
        self.var_contact=StringVar()

        CustomerFrame=Frame(self.root,relief=RIDGE,bg="white",bd=4)
        CustomerFrame.place(x=420,y=110,width=530,height=70)

        cTitle=Label(CustomerFrame,text="Customer Details",font=("goudy old style",15),bg="lightgrey").pack(side=TOP,fill=X)

        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15),background="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13,),background="lightyellow")
        txt_name.bind('<Return>',lambda ev:self.genrate_bill())
        txt_name.place(x=80,y=35,width=180)

        lbl_contact=Label(CustomerFrame,text="Contact No.",font=("times new roman",15),background="white").place(x=270,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13,),background="lightyellow")
        txt_contact.bind('<Return>',lambda ev:self.genrate_bill())
        txt_contact.place(x=380,y=35,width=140)

        #============cal cart frame======
        Cal_Cart_Frame=Frame(self.root,relief=RIDGE,bg="white",bd=4)
        Cal_Cart_Frame.place(x=420,y=190,width=530,height=360)

        Cal_Frame=Frame(Cal_Cart_Frame,relief=RIDGE,bg="white",bd=4)
        Cal_Frame.place(x=5,y=10,width=268,height=340)

        self.var_cal_input=StringVar()

        self.txt_cal_input=Entry(Cal_Frame,bg="lightyellow",justify=RIGHT,state=DISABLED,bd=5,relief=GROOVE,font=("arial",15,"bold"),width=22,textvariable=self.var_cal_input)
        self.txt_cal_input.grid(row=0,columnspan=4)

        btn7=Button(Cal_Frame,text='7',font=("arial",15,"bold"),bd=5,width=3,pady=10,cursor="hand2",command=lambda:self.cal_input(7)).grid(row=1,column=0)
        btn8=Button(Cal_Frame,text='8',font=("arial",15,"bold"),bd=5,width=4,pady=10,cursor="hand2",command=lambda:self.cal_input(8)).grid(row=1,column=1)
        btn9=Button(Cal_Frame,text='9',font=("arial",15,"bold"),bd=5,width=4,pady=10,cursor="hand2",command=lambda:self.cal_input(9)).grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text="+",font=("arial",15,"bold"),bd=5,width=4,pady=10,cursor="hand2",command=lambda:self.cal_input('+')).grid(row=1,column=3)

        btn4=Button(Cal_Frame,text='4',font=("arial",15,"bold"),bd=5,width=3,pady=10,cursor="hand2",command=lambda:self.cal_input(4)).grid(row=2,column=0)
        btn5=Button(Cal_Frame,text='5',font=("arial",15,"bold"),bd=5,width=4,pady=10,cursor="hand2",command=lambda:self.cal_input(5)).grid(row=2,column=1)
        btn6=Button(Cal_Frame,text='6',font=("arial",15,"bold"),bd=5,width=4,pady=10,cursor="hand2",command=lambda:self.cal_input(6)).grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text="-",font=("arial",15,"bold"),bd=5,width=4,pady=10,cursor="hand2",command=lambda:self.cal_input('-')).grid(row=2,column=3)

        btn1=Button(Cal_Frame,text='1',font=("arial",15,"bold"),bd=5,width=3,pady=10,cursor="hand2",command=lambda:self.cal_input(1)).grid(row=3,column=0)
        btn2=Button(Cal_Frame,text='2',font=("arial",15,"bold"),bd=5,width=4,pady=10,cursor="hand2",command=lambda:self.cal_input(2)).grid(row=3,column=1)
        btn3=Button(Cal_Frame,text='3',font=("arial",15,"bold"),bd=5,width=4,pady=10,cursor="hand2",command=lambda:self.cal_input(3)).grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text="*",font=("arial",15,"bold"),bd=5,width=4,pady=10,cursor="hand2",command=lambda:self.cal_input('*')).grid(row=3,column=3)

        btn0=Button(Cal_Frame,text='0',font=("arial",15,"bold"),bd=5,width=3,pady=20,cursor="hand2",command=lambda:self.cal_input(0)).grid(row=4,column=0)
        btnc=Button(Cal_Frame,text='C',font=("arial",15,"bold"),bd=5,width=4,pady=20,cursor="hand2",command=lambda:self.clear_cal()).grid(row=4,column=1)
        btneq=Button(Cal_Frame,text='=',font=("arial",15,"bold"),bd=5,width=4,pady=20,cursor="hand2",command=lambda:self.cal_eq()).grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text="/",font=("arial",15,"bold"),bd=5,width=4,pady=20,cursor="hand2",command=lambda:self.cal_input("/")).grid(row=4,column=3)


        Cart_Frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        Cart_Frame.place(x=280,y=8,height=342,width=245)

        self.cartTitle=Label(Cart_Frame,text="Cart\tTotal Product: [0]",font=("goudy old style",15),bg="lightgrey")
        self.cartTitle.pack(side=TOP,fill=X)

        #========scroll Bar============
        scrolly=Scrollbar(Cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(Cart_Frame,orient=HORIZONTAL)

        #Tree view help to show the data in our software in a readalbe format . or table view
        self.cart_details=ttk.Treeview(Cart_Frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.cart_details.yview)
        scrollx.config(command=self.cart_details.xview)


        #Creating the heading, these heading shold be same as in our database
        self.cart_details.heading("pid",text="P_ID")
        self.cart_details.heading("name",text="Name")
        self.cart_details.heading("price",text="Price")
        self.cart_details.heading("qty",text="QTY")
        
      

        self.cart_details["show"] = "headings"           #When we make any heading it will now show any heading untill or unless we run this command


        # To set the width of each column we do this

        self.cart_details.column("pid",width=50)
        self.cart_details.column("name",width=70)
        self.cart_details.column("price",width=90)
        self.cart_details.column("qty",width=30)
      
        self.cart_details.pack(expand=1,fill=BOTH)
        self.cart_details.bind("<ButtonRelease-1>",self.get_data)            


        #=====================Add Cart Widget Frame ===================

        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_inStock=StringVar()

        Add_CartWidget_Frame=Frame(self.root,relief=RIDGE,bg="white",bd=4)
        Add_CartWidget_Frame.place(x=420,y=550,width=530,height=110) 

        lbl_p_name=Label(Add_CartWidget_Frame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidget_Frame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state="readonly").place(x=5,y=35,width=190,height=22)

        lbl_p_price=Label(Add_CartWidget_Frame,text="Price Per Qty",font=("times new roman",15),bg="white").place(x=230,y=5)
        txt_p_price=Entry(Add_CartWidget_Frame,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow",state="readonly").place(x=230,y=35,width=150,height=22)

        lbl_p_Qty=Label(Add_CartWidget_Frame,text="Quantity",font=("times new roman",15),bg="white").place(x=390,y=5)
        txt_p_Qty=Entry(Add_CartWidget_Frame,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow")
        txt_p_Qty.bind('<Return>',lambda ev:self.add_update())
        txt_p_Qty.place(x=390,y=35,width=120,height=22)

        self.lbl_instock=Label(Add_CartWidget_Frame,text="Stock [0]",font=("times new roman",15),bg="white")
        self.lbl_instock.place(x=5,y=70)

        btn_clear_cart=Button(Add_CartWidget_Frame,text="Clear",command=self.clearCart,font=("times new roman",15,"bold"),bg="lightgrey",cursor="hand2").place(x=180,y=70,width=150,height=30)
        btn_add_update=Button(Add_CartWidget_Frame,text="Add| Update",font=("times new roman",15,"bold"),command=self.add_update,bg="#0cf5f1",cursor="hand2").place(x=340,y=70,width=180,height=30)


        #=======================================Bill Frame============================

        BillFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        BillFrame.place(x=953,y=110,width=400,height=410)

        bTitle=Label(BillFrame,text="Coustumers Bill",font=("goudy old style",20,"bold"),fg="white",bg="#66b3ff").pack(side=TOP,fill=X)

        scrolly=Scrollbar(BillFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(BillFrame,state=DISABLED,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)

        scrolly.config(command=self.txt_bill_area.yview)

        #===============Bill Menu Frame===================


        BillMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        BillMenuFrame.place(x=953,y=520,width=400,height=140)

        self.lbl_amount=Label(BillMenuFrame,text="Bill Amount\n[0]",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amount.place(x=2,y=5,width=120,height=70)
        self.lbl_discount=Label(BillMenuFrame,text="Discount\n[5%]",font=("goudy old style",15,"bold"),bg="#2f9674",fg="white")
        self.lbl_discount.place(x=124,y=5,width=120,height=70)
        self.lbl_netpay=Label(BillMenuFrame,text="Net Pay\n[0]",font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_netpay.place(x=246,y=5,width=140,height=70)

        btn_print=Button(BillMenuFrame,text="Print",command=self.print_bill,font=("goudy old style",15,"bold"),cursor="hand2",bg="grey",fg="white")
        btn_print.place(x=2,y=80,width=120,height=50)
        btn_clear=Button(BillMenuFrame,text="Clear All",command=self.clearAll,font=("goudy old style",15,"bold"),cursor="hand2",bg="#bf5f54",fg="black")
        btn_clear.place(x=124,y=80,width=120,height=50)
        btn_genrate=Button(BillMenuFrame,text="Generate Bill",command=self.genrate_bill,font=("goudy old style",15,"bold"),cursor="hand2",bg="#009688",fg="white")
        btn_genrate.place(x=246,y=80,width=140,height=50)

    #===============================================================================================================================


    def cal_input(self,num):
        self.var_cal_input.set(self.var_cal_input.get()+str(num))
    def clear_cal(self):
        self.var_cal_input.set("")
    def cal_eq(self):
        try:
            ans=eval(str(self.var_cal_input.get()))
            self.var_cal_input.set(ans)
        except Exception as e:
            messagebox.showerror("Error ",f"Wrong Equation")

    def show(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            #   self.product_details=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
            cur.execute("select pid,name,price,qty,status from product")
            result=cur.fetchall()
            # print(result)
            self.product_details.delete(*self.product_details.get_children())
            for i in result:
                
                self.product_details.insert('',END,values=i)

        except Exception as e:
            messagebox.showerror("Error","Error due to "+str(e),parent=self.root)
            
    def getdata(self,ev):           #Taking the data form product to entry field
        f=self.product_details.focus()    
        content = (self.product_details.item(f))        #content variable contain the data of that column as a dictnary
        row = content["values"]  #row have all the data in a list

        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"Stock [{row[3]}]")
        self.stock = row[3]
        self.var_qty.set("1")

    def get_data(self,ev):              # taking the data from product cart to entry field
        f=self.cart_details.focus()    
        content=(self.cart_details.item(f))        #content variable contains the data of that column as a dictionary
        row=content["values"]
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"Stock [{row[4]}]")

   
        # cur.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
        
    def search(self):
        if(self.var_search.get()==""):
            messagebox.showerror("Error","Search Field can not be empty")
        else:
            try:
                con=sqlite3.connect(database=r"ims.db")
                cur=con.cursor()
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%'")
                data=cur.fetchone()
                if(data!=None):
                    print(data)
                    self.product_details.delete(*self.product_details.get_children())     

                    self.product_details.insert('',END,values=data)
                    
                else:
                    messagebox.showerror("No record","No record Found",parent=self.root)
                
            except Exception as e:
                messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)

    def add_update(self):
        if(self.var_qty.get()==""):
            messagebox.showerror("Error","Quantity must Required",parent=self.root)
        elif(self.var_pname.get()==""):
            messagebox.showerror("Error","Select the Products ",parent=self.root)
        elif(int(self.var_qty.get())>self.stock):
            messagebox.showerror("Error","Invalid Quantity",parent=self.root)

        else:
            
            cart_data=[self.var_pid.get(),self.var_pname.get(),self.var_price.get(),self.var_qty.get(),self.stock]

            present='no'
            index=0

            for row in self.cart_list:
                if(self.var_pid.get()==row[0]):
                    present='yes'
                    break

                index+=1
            if(present=='yes'):
                ask=messagebox.askyesno("Confirm ","Product already in cart,Do you want to update/Remove?",parent=self.root)
                if(ask==True):
                    if(self.var_qty.get()=='0'):
                        self.cart_list.pop(index)
                    else:
                        self.cart_list[index][3]=self.var_qty.get()

            else:
                self.cart_list.append(cart_data)


            self.show_cart()
            self.total_item()
            self.bill_Amount()

    def bill_Amount(self):
        self.amount=0
        self.netpay=0
        for i in self.cart_list:
            self.amount+=(float(i[2])*int(i[3]))
        # print(f"Total price is {amount}")
        self.dis=(self.amount*5)/100
        self.netpay=self.amount-self.dis
        self.lbl_amount.config(text=f"Bill Amount\n[{self.amount}]")
        self.lbl_netpay.config(text=f"Ney Pay\n[{self.netpay}]")

    def genrate_bill(self):

        if self.var_cname.get()=="" or self.var_contact.get()=="":
            messagebox.showerror("Error ","Fill the Customer details.",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error ","Add the product in the cart",parent=self.root)

        else:
            self.txt_bill_area.config(state=NORMAL)
            #==Top===
            self.bill_top()
            #===Middle===
            self.bill_middle()
            #===Buttom===
            self.bill_bottom()

            fp=open(f'bill/{self.invoice}.txt','w')
            fp.write(self.txt_bill_area.get(1.0,END))
            fp = open(f"bill/{self.invoice}.txt", 'r')
            bill_data = fp.read()
            fp.close()

            self.txt_bill_area.config(state=DISABLED)
            # self.store_sales_data(self.invoice, bill_data)

            conn = sqlite3.connect('ims.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS sales
                                     (invoice_no TEXT, bill_data TEXT)''')
            c.execute("INSERT INTO sales VALUES (?, ?)", (self.invoice, bill_data))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success ","Bill generated and saved successfully",parent=self.root)

            self.chk_print=1


    def total_item(self):
        self.cartTitle.config(text=f"Cart\tTotal Product: [{str(len(self.cart_list))}]")

    def show_cart(self):
        self.cart_details.delete(*self.cart_details.get_children())
        for i in self.cart_list:
            self.cart_details.insert('',END,values=i)


    def bill_top(self):
        self.invoice = int(int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y")))
        bill_top_temp = f'''
\t\tXYZ-Inventory
\t Phone No. 7017463867, Delhi-125001
{str("="*45)}
 Customer Name: {self.var_cname.get()}
 Ph no. :{self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*45)}
 Product Name\t\t\tQTY\tPrice
{str("="*45)}
        '''
        self.txt_bill_area.delete(1.0,END)
        self.txt_bill_area.insert(1.0,bill_top_temp)


    def bill_middle(self):

        for row in self.cart_list:
        # pid,name,price,qty,stock
            name=row[1]
            qty=row[3]
            price=float(row[2])*int(row[3])
            price=str(price)
            self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+qty+"\tRs."+price)


    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*45)}
 Bill Amount\t\t\t\tRs.{self.amount}
 Discount\t\t\t\tRs.{self.dis}
 Net Pay\t\t\t\tRs.{self.netpay}
{str("="*45)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)

    def print_bill(self):
        if(self.chk_print==1):
            messagebox.showinfo("success ","bill generating")
            new_file=tempfile.mkdtemp(".txt")
            open(new_file,'w').write(self.txt_bill_area.get(1.0,END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror("Error","First Generate the bill!")
        

    def clearCart(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.lbl_instock.config(text=f"Stock [0]")
        self.stock=0
        self.var_qty.set("")

    def clearAll(self):
        del self.cart_list[:]
        self.var_cname.set("")
        self.var_contact.set("")
        self.var_search.set("")
        self.txt_bill_area.config(state=NORMAL)
        self.txt_bill_area.delete(1.0,END)
        self.txt_bill_area.config(state=DISABLED)
        self.clearCart()
        self.show()
        self.show_cart()
        self.total_item()
        self.chk_print=0
    
    def update_date_time(self):
        time_ = str(time.strftime("%H:%M:%S"))
        date_ = str(time.strftime("%d/%m/%Y"))

        self.lbl_clock.config(text=f"Welcome to Inventory Management\t\t Date: {date_} \t\t Time: {time_}",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.after(200,self.update_date_time())

    def logOut(self):
        self.root.destroy()
        os.system("login.py")

    # def store_sales_data(self, invoice_no, bill_data):
    # pass

if __name__=="__main__":
    root=Tk()
    obj=BillClass(root)
    root.mainloop()