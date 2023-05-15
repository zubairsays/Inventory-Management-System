import sqlite3
from tkinter import *
import time
from tkinter import messagebox
from PIL import Image, ImageTk
from employee import EmployeeClass
from supplier import SupplierClass
from category import CategoryClass
from product import ProductClass
from sales import SalesClass
import os


class IMS:
    def __init__(self, root):
        self.root = root
        root.geometry("1350x750+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")

        # =============Title=========
        self.icon_title = PhotoImage(file="images/logo1.png")  # icon image

        title = Label(self.root, text="Inventory Management System", image=self.icon_title, compound=LEFT,
                      font=("times new roman", 40, 'bold'), bg='#010c48', fg="white", anchor="w", padx=20).place(x=0,y=0,relwidth=1,height=70)

        # ============btn_log_out=========
        btn_logout = Button(self.root, text="Logout", font=("times new roman", 15, "bold"), bg="yellow", cursor="hand2",
                            command=self.logOut).place(x=1100, y=15, height=40, width=160)

        # ==========clock============
        self.lbl_clock = Label(self.root,
                               text="Welcome to Inventry Management\t\t Date: DD//mm//YYYY \t\t Time: HH//MM//SS",
                               font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # ===========Left menu===========
        leftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        leftMenu.place(x=0, y=120, width=200, height=565)

        # To resize the png image.
        self.menu_logo = Image.open("images/menu_im.png")
        self.menu_logo = self.menu_logo.resize((200, 200), Image.ANTIALIAS)
        self.menu_logo = ImageTk.PhotoImage(self.menu_logo)

        lbl_menu_logo = Label(leftMenu, image=self.menu_logo)
        lbl_menu_logo.pack(fill=X, side=TOP)

        # =========left menu btn============
        lbl_menu = Label(leftMenu, text="Menu", font=("times new roman", 20), bg="#009688")
        lbl_menu.pack(side=TOP, fill=X)

        self.icon_side = PhotoImage(file="images/side.png")

        btn_employee = Button(leftMenu, text="Employee", image=self.icon_side, compound=LEFT, padx=10,
                              font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2", anchor="w",
                              command=self.employee).pack(side=TOP, fill=X)

        btn_supplier = Button(leftMenu, text="Supplier", command=self.supplier, image=self.icon_side, compound=LEFT,
                              padx=10, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2",
                              anchor="w").pack(side=TOP, fill=X)

        btn_category = Button(leftMenu, text="Category", command=self.category, image=self.icon_side, compound=LEFT,
                              padx=10, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2",
                              anchor="w").pack(side=TOP, fill=X)

        btn_product = Button(leftMenu, text="Product", command=self.product, image=self.icon_side, compound=LEFT,
                             padx=10, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2",
                             anchor="w").pack(side=TOP, fill=X)

        btn_sales = Button(leftMenu, text="Sales", command=self.sales, image=self.icon_side, compound=LEFT, padx=10,
                           font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2", anchor="w").pack(
            side=TOP, fill=X)

        btn_exit = Button(leftMenu, text="Exit", image=self.icon_side, compound=LEFT, padx=10,
                          font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2", anchor="w").pack(
            side=TOP, fill=X)

        # ===========Contant=================
        self.lbl_emplee = Label(self.root, text="Total Employee\n[0]", bg="#33bbf9",
                                font=("goudy old style", 20, "bold"), bd=5, relief=RIDGE)
        self.lbl_emplee.place(x=300, y=120, height=150, width=300)

        self.lbl_supplier = Label(self.root, text="Total Supplier\n[0]", bg="#ff5722",
                                  font=("goudy old style", 20, "bold"), bd=5, relief=RIDGE)
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)

        self.lbl_category = Label(self.root, text="Total Category\n[0]", bg="#009688",
                                  font=("goudy old style", 20, "bold"), bd=5, relief=RIDGE)
        self.lbl_category.place(x=1000, y=120, height=150, width=300)

        self.lbl_product = Label(self.root, text="Total Product\n[0]", bg="#ffc107",
                                 font=("goudy old style", 20, "bold"), bd=5, relief=RIDGE)
        self.lbl_product.place(x=300, y=300, height=150, width=300)

        self.lbl_sales = Label(self.root, text="Total Sales\n[0]", bg="#33bbf9", font=("goudy old style", 20, "bold"),
                               bd=5, relief=RIDGE)
        self.lbl_sales.place(x=650, y=300, height=150, width=300)

        self.update_details()

    # ========================================================================================================================

    def employee(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = EmployeeClass(self.new_window)

    def supplier(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = SupplierClass(self.new_window)

    def category(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = CategoryClass(self.new_window)

    def product(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = ProductClass(self.new_window)

    def sales(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = SalesClass(self.new_window)

    def update_details(self):
        con = sqlite3.connect(database=r"ims.db")  # Making the connection with the database
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            product = cur.fetchall()
            self.lbl_product.config(text=f"Total Product\n[{str(len(product))}]")

            cur.execute("select * from employee")
            emp = cur.fetchall()
            self.lbl_emplee.config(text=f"Total Employee\n[{str(len(emp))}]")

            cur.execute("select * from category")
            category = cur.fetchall()
            self.lbl_category.config(text=f"Total Category\n[{str(len(category))}]")

            cur.execute("select * from supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f"Total Supplier\n[{str(len(supplier))}]")
            self.lbl_sales.config(text=f"Total sales\n[{str(len(os.listdir('bill')))}]")

            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory Management\t\t Date: {date_} \t\t Time: {time_}",
                                  font=("times new roman", 15), bg="#4d636d", fg="white")

            self.lbl_clock.after(200, self.update_details)
        except Exception as e:
            messagebox.showerror("Error", "Error due to " + str(e))

    def logOut(self):
        self.root.destroy()
        os.system("login.py")


if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()



