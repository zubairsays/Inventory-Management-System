import os
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import sqlite3
import smtplib
import email_pass
import random


class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1500x750+0+0")
        self.root.title("Login System")
        self.root.config(bg="#fafafa")
        self.otp = ''

        # ==================Images=================
        self.phone_image = ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_phone_image = Label(self.root, image=self.phone_image, bd=0).place(x=200, y=90)

        # ======LOgin Frame==========

        self.var_employeeId = StringVar()
        self.var_password = StringVar()

        login_frame = Frame(self.root, bd=2, bg="white", relief=RIDGE)
        login_frame.place(x=700, y=110, width=350, height=460)

        lbl_title = Label(login_frame, text="Login System", font=("Elephant", 30, "bold"), bg="white")
        lbl_title.place(x=0, y=0, relwidth=1)

        lbl_employeId = Label(login_frame, text="Employe Id", font=("anadlus", 15), bg="white", fg="#767171").place(
            x=50, y=100)
        txt_employeId = Entry(login_frame, font=("times new roman", 15), textvariable=self.var_employeeId,
                              bg="#ECECEC").place(x=50, y=140, width=250)

        lbl_pass = Label(login_frame, text="Password", font=("anadlus", 15), bg="white", fg="#767171").place(x=50,
                                                                                                             y=200)
        txt_password = Entry(login_frame, font=("times new roman", 15), bg="#ECECEC", textvariable=self.var_password,
                             show="*").place(x=50, y=240, width=250)

        btn_login = Button(login_frame, text="Log In", font=("Arial Ronded MT Bold", 15), activeforeground="white",
                           cursor="hand2", bg="#00B0F0", fg="white", activebackground="#00B0F0",
                           command=self.login).place(x=50, y=300, width=250, height=35)

        hr = Label(login_frame, bg="lightgrey").place(x=50, y=370, width=250, height=2)
        or_ = Label(login_frame, text="Or", font=("times new roman", 15, "bold"), bg="white", fg="lightgrey").place(
            x=150, y=355)

        btn_forget = Button(login_frame, text="Forget Password", font=("times new roman", 13), bd=0, bg="white",
                            fg="#00759E", activeforeground="white", activebackground="white", cursor="hand2",
                            command=self.forgetPassword).place(x=100, y=390)

        # ============Frame2================
        registerFrame = Frame(self.root, bd=2, bg="white", relief=RIDGE)
        registerFrame.place(x=700, y=590, width=350, height=60)

        lbl_reg = Label(registerFrame, text="Dont have an account ?", font=("times new roman", 13), bg="white").place(
            x=40, y=20)
        btn_signup = Button(registerFrame, text="Sign Up", font=("times new roman", 13, "bold"), bd=0, bg="white",
                            fg="#00759E", activeforeground="white", activebackground="white", cursor="hand2").place(
            x=200, y=20)

        # =================Image Annimation ==========================
        self.im1 = ImageTk.PhotoImage(file="images/im1.png")
        self.im2 = ImageTk.PhotoImage(file="images/im2.png")
        self.im3 = ImageTk.PhotoImage(file="images/im3.png")
        self.lbl_change_image = Label(self.root, bg="white")
        self.lbl_change_image.place(x=367, y=192, width=240, height=428)
        self.animate()

    # =====================================Funtion========================================================

    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000, self.animate)

    def login(self):
        if (self.var_password.get() == "" or self.var_employeeId.get() == ""):
            messagebox.showerror("Error", "Both Fields Are Require", parent=self.root)
        else:
            con = sqlite3.connect(database=r"ims.db")  # Making the connection with the database
            cur = con.cursor()
            try:
                cur.execute("select utype from employee where eid=? and pass=?",
                            (self.var_employeeId.get(), self.var_password.get()))
                user = cur.fetchone()
                if user == None:
                    messagebox.showerror("Error", "Invalid Employee Id or Password", parent=self.root)
                else:
                    if (user[0] == "Admin"):
                        self.root.destroy()
                        os.system("dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("billing.py")


            except Exception as e:
                messagebox.showerror("Error", f"Error due to {str(e)}")

    def forgetPassword(self):
        if (self.var_employeeId == ""):
            messagebox.showerror("Error", "Enter The Employee Id", parent=self.root)
        else:
            con = sqlite3.connect(database=r"ims.db")
            cur = con.cursor()
            try:
                cur.execute("select email from employee where eid=?", (self.var_employeeId.get(),))
                email = cur.fetchone()
                if (email == None):
                    messagebox.showerror("Error", "Invalid Employee Id", parent=self.root)
                else:
                    self.var_otp = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_conf_pass = StringVar()
                    # gmail otp send function will run.
                    chk = self.send_email(email[0])
                    if (chk == 'f'):
                        messagebox.showerror("Error", "Connection Error, Try Again", parent=self.root)
                    else:

                        self.forget_win = Toplevel(self.root)
                        self.forget_win.title("RESET PASSWORD")
                        self.forget_win.geometry("400x350+500+100")
                        self.forget_win.focus_force()
                        self.forget_win.resizable(False, False)

                        title = Label(self.forget_win, text="Reset Password", font=("goudy old style", 15, "bold"),
                                      bg="#3f51b5", fg="white").pack(side=TOP, fill=X)

                        lbl_reset = Label(self.forget_win, text="Enter OTP Sent on Register Email",
                                          font=("times new roman", 15)).place(x=20, y=60)
                        txt_reset = Entry(self.forget_win, textvariable=self.var_otp, font=("times new roman", 15),
                                          bg="lightyellow").place(x=20, y=100, width=250, height=30)

                        self.btn_reset = Button(self.forget_win, text="submit", font=("times new roman", 15),
                                                bg="lightblue", cursor="hand2", activebackground="lightblue",
                                                command=self.sub_otp)
                        self.btn_reset.place(x=280, y=100, width=100, height=30)

                        new_pass = Label(self.forget_win, text="New Password", font=("times new roman", 15)).place(x=20,
                                                                                                                   y=160)
                        txt_pass = Entry(self.forget_win, textvariable=self.var_new_pass, font=("times new roman", 15),
                                         bg="lightyellow").place(x=20, y=190, width=250, height=30)

                        conf_pass = Label(self.forget_win, text="Confirm Password", font=("times new roman", 15)).place(
                            x=20, y=225)
                        txt_conf_pass = Entry(self.forget_win, textvariable=self.var_conf_pass,
                                              font=("times new roman", 15), bg="lightyellow").place(x=20, y=255,
                                                                                                    width=250,
                                                                                                    height=30)

                        self.btn_update = Button(self.forget_win, text="Update", font=("times new roman", 15),
                                                 bg="lightblue", cursor="hand2", activebackground="lightblue",
                                                 state=DISABLED, command=self.update_pas)
                        self.btn_update.place(x=150, y=300, width=100, height=30)

            except Exception as e:
                messagebox.showerror("Error", f"Error due to {str(e)}")

    def send_email(self, to_):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        email_ = email_pass.email_
        pass_ = email_pass.pass_

        s.login(email_, pass_)
        # self.otp='12345';
        self.otp = random.randrange(121365, 987451)

        subj = 'IMS-Reset Password OTP'
        msg = f"Dear Sir/Madam,\n\nYour Reset OTP is {self.otp}.\n\nWith Regards,\nIMS Team"
        msg = "Subject:{}\n\n{}".format(subj, msg)
        s.sendmail(email_, to_, msg)

        chk = s.ehlo()
        if (chk[0] == 250):
            return 's';
        else:
            return 'f';

    def sub_otp(self):
        if (self.var_otp == ""):
            messagebox.showerror("Error", "Type Youe OTP ", parent=self.forget_win)
        else:
            if (self.var_otp.get() == str(self.otp)):
                self.btn_update.config(state=NORMAL)
                self.btn_reset.config(state=DISABLED)
            else:
                messagebox.showerror("Error", "Invalid OTP ", parent=self.forget_win)

    def update_pas(self):
        if (self.var_new_pass.get() == "" or self.var_conf_pass.get() == ""):
            messagebox.showerror("Error", "Type Your password", parent=self.forget_win)
        else:
            if (self.var_new_pass.get() != self.var_conf_pass.get()):
                messagebox.showerror("Error", "New Password and Confirm pass should be Same", parent=self.forget_win)
            else:
                con = sqlite3.connect(database=r"ims.db")
                cur = con.cursor()

                try:
                    cur.execute("update employee set pass=? where eid=?",
                                (

                                    self.var_conf_pass.get(),
                                    self.var_employeeId.get()

                                ))
                    con.commit()
                    messagebox.showerror("Success", "New Password Set Successfully.", parent=self.forget_win)
                    self.forget_win.destroy()

                except Exception as e:
                    messagebox.showerror("Error", f"Error due to {str(e)}", parent=self.forget_win)


root = Tk()
obj = Login_System(root)

root.mainloop()
