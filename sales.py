from time import strftime, time_ns
from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os


class SalesClass:
    def __init__(self, root):
        self.root = root
        root.geometry("1100x500+220+130")
        self.root.title("Inventry Management System")
        self.root.config(bg="white")
        self.root.focus_force()  # Focus on the child window
        self.root.resizable(0, 0)  # Tuen off window resizeable , now user cannot resize the window

        self.var_invoice = StringVar()
        self.bill_list = []

        # =========Title================
        lbl_title = Label(self.root, text="View Coustumer Bills", font=("Goudy old style", 30,), bg="#184a45",
                          fg="white", bd=3, relief=RIDGE).pack(side=TOP, fill=X, padx=10, pady=20)

        lbl_invoice = Label(self.root, text="Invoice No", font=("times new roman", 15), bg="white").place(x=50, y=100)

        self.txt_invoice = Entry(self.root, text="Invoice No", textvariable=self.var_invoice, bg="lightyellow",
                                 font=("times new roman", 15))
        self.txt_invoice.place(x=160, y=100, w=180, h=28)
        self.txt_invoice.bind('<Return>', self.search2)

        btn_search = Button(self.root, text="Search", command=self.search, font=("times new roman", 15, "bold"),
                            bg="#2196f3", fg="white", cursor="hand2").place(x=360, y=100, width=120, height=28)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("times new roman", 15, "bold"),
                           bg="lightgrey", fg="black", cursor="hand2").place(x=490, y=100, width=120, height=28)

        # =========sales frame======================
        sales_frame = Frame(self.root, bd=2, relief=RIDGE)  # 8057713022
        sales_frame.place(x=50, y=140, width=200, height=330)

        # ================List Box==============
        scrolly = Scrollbar(sales_frame, orient=VERTICAL)

        self.sales_list = Listbox(sales_frame, font=("goudy old style", 15), bg="white", yscrollcommand=scrolly)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.sales_list.yview)
        self.sales_list.pack(fill=BOTH, expand=1)
        self.sales_list.bind("<ButtonRelease-1>", self.getdata)

        # =========Bill frame======================
        bill_frame = Frame(self.root, bd=2, relief=RIDGE)
        bill_frame.place(x=280, y=140, width=500, height=330)

        lbl_title2 = Label(bill_frame, text="Coustumer Bills Area", font=("Goudy old style", 20,), bg="orange").pack(
            side=TOP, fill=X)
        scrolly2 = Scrollbar(bill_frame, relief=RIDGE)
        self.bill_txt = Text(bill_frame, font=("goudy old style", 15), bg="lightyellow", yscrollcommand=scrolly2)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_txt.yview)
        self.bill_txt.pack(fill=BOTH, expand=1)

        # =============Image================
        self.bill_logo = Image.open("images/cat2.jpg")
        self.bill_logo = self.bill_logo.resize((350, 200), Image.ANTIALIAS)
        self.bill_logo = ImageTk.PhotoImage(self.bill_logo)

        lbl_img = Label(self.root, image=self.bill_logo, bd=0)
        lbl_img.place(x=780, y=160)

        self.show()

    # =======================================================================================================
    def show(self):

        self.sales_list.delete(0, END)
        for i in os.listdir('bill'):
            if i.split('.')[-1] == 'txt':
                self.sales_list.insert(END, i)
                self.bill_list.append(i.split('.')[0])

    def getdata(self, ev):
        index_ = self.sales_list.curselection()
        filename = self.sales_list.get(index_)
        # print(filename)
        self.bill_txt.delete(1.0, END)
        fp = open(f"bill/{filename}", 'r')
        for i in fp:
            self.bill_txt.insert(END, i)
        fp.close()

    def search2(self, ev):
        self.search()

    def search(self):

        if self.txt_invoice.get() == "":
            messagebox.showerror("Error", "Enter the Invoice No", parent=self.root)
        else:
            if self.txt_invoice.get() in self.bill_list:
                self.bill_txt.delete(1.0, END)
                fp = open(f"bill/{self.txt_invoice.get()}.txt", 'r')
                for i in fp:
                    self.bill_txt.insert(END, i)
                fp.close()
            else:
                messagebox.showerror("Error", "Not in List", parent=self.root)

    def clear(self):
        self.show()

        self.bill_txt.delete(1.0, END)


if __name__ == "__main__":
    root = Tk()
    obj = SalesClass(root)
    root.mainloop()
