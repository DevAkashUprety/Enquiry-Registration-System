import tkinter as tk
from PIL import Image, ImageTk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import math
import random
import pymysql
from tkinter import PhotoImage, Label, Entry, Button, Canvas, messagebox
from HomePage import *

        
class SignInApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1520x760+0+0")
        self.root.iconbitmap('ErsIcon.ico')
        self.root.resizable(False, False)
        self.frame = tk.Frame(self.root, bg="white")
        self.frame.place(x=350, y=170, width=800, height=380)
    
        img = Image.open('Ers.png')
        img = ImageTk.PhotoImage(img)
        
        label = tk.Label(self.frame, image=img,bg="white")
        label.image = img
        label.place(x=50, y=40)  
        
        self.create_widgets()
        
    def send_otp_email(self,to_email):
        digits = "0123456789"
        OTP = ""
        for i in range(6):
            OTP += digits[math.floor(random.random() * 10)]
        
        from_address = "akshuprety1025@gmail.com"
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Enquiry Registraction System"
        msg['From'] = from_address
        msg['To'] = to_email
        
        otp_message = " Hii," + OTP +" is the OTP for completing your transaction on Enquiry Registraction System - ERS"
        msg_text = MIMEText(otp_message)
        msg.attach(msg_text)
        
        username = 'akashuprety1025@gmail.com'
        password = 'precxfifxngccphq'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(from_address, to_email, msg.as_string())
        server.quit()
        return OTP
    
    def updatedata(self):
         try:
            db = pymysql.connect(host='localhost', user='root', password='root', database='ersdb')
            cur = db.cursor()
            a = self.usern.get()
            c = self.passnn_En.get()
            
            print("Username:", a)
            print("New Password:", c)
            
            sql = "UPDATE login SET password=%s WHERE user=%s"
            cur.execute(sql, (c, a))
            db.commit()
            print("Password updated successfully")
            messagebox.showinfo('Forgot Password', 'Password updated successfully')
         except pymysql.Error as e:
            print(f"Error: {e}")
            messagebox.showerror('Error', 'Failed to update password')
         finally:
            db.close()

   
    def create_pass(self):
        self.can = tk.Frame(self.canvas2, bg="white")
        self.can.place(x=2, y=170, width=345, height=128)

        self.passnn_En = tk.Entry(self.can, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 13))
        self.passnn_En.place(x=30, y=5)
        self.passnn_En.insert(0, 'Password')
        self.passnn_En.bind('<FocusIn>', self.pass_on_enter)
        self.passnn_En.bind('<FocusOut>', self.pass_on_leave)
        tk.Canvas(self.can, width=295, height=2, bg='black').place(x=25, y=30)
   
        # Buttons
        self.button = tk.Button(self.can, width=40, pady=7, text='Save', bg='green', fg='white', border=0,command=self.updatedata)
        self.button.place(x=33, y=50)
        self.label = tk.Label(self.can, text="Back to login page.", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
        self.label.place(x=90, y=95)
        self.back_up = tk.Button(self.can, width=6, text='Back', border=0, bg='white', cursor='hand2', fg='green',command=self.create_widgets)
        self.back_up.place(x=200, y=95)

    def pass_on_enter(self, e):
        self.passnn_En.delete(0, tk.END)

    def pass_on_leave(self, e):
        name = self.passnn_En.get()
        if name == '':
            self.passnn_En.insert(0, 'Password')


    def verify_otp(self, generated_otp, user_input):
        if user_input == generated_otp:
            print("Verified OTP")
            messagebox.showinfo('Success', 'OTP Verify')
            self.create_pass()
            
        else:
            messagebox.showinfo('Error', 'Please check your OTP again')
            return "Please check your OTP again"
        
    def send_otp_button_click(self):
        to_email = self.emailEn.get()
        if self.check_email_in_database(to_email):
            print("Email Find in database")
            self.generated_otp = self.send_otp_email(to_email)
            print("OTP Send")
            messagebox.showinfo('Success', 'OTP sent to your Email')
        else:
            print("Email not fund in database")
            messagebox.showerror('Error', 'Email not found in the database')

    def check_email_in_database(self, email):
        db = pymysql.connect(host='localhost', user='root', password='root', database='ersdb')
        cur = db.cursor()
        sql = "SELECT COUNT(*) FROM login WHERE email='%s'" % email
        cur.execute(sql)
        count = cur.fetchone()[0]
        db.close()
        return count > 0

    def verify_button_click(self):
        user_input = self.OTP_En.get()
        self.verify_otp(self.generated_otp, user_input) 
       
    def create_forget(self):
        self.canvas2 = tk.Canvas(self.frame, bg="white")
        self.canvas2.place(x=400, y=40, width=350, height=300)
       
        self.heading1 = tk.Label(self.canvas2, text='Forget Account', fg='green', bg='white',width=22, font=('Microsoft YaHei UI Light', 18, 'bold'))
        self.heading1.place(x=5, y=2)
        
        self.emailEn = tk.Entry(self.canvas2, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 13))
        self.emailEn.place(x=30, y=65)
        self.emailEn.insert(0, 'Email')
        self.emailEn.bind('<FocusIn>', self.on_ent1)
        self.emailEn.bind('<FocusOut>', self.on_leve1)
        tk.Canvas(self.canvas2, width=295, height=2, bg='black').place(x=25, y=92)
        
        self.OTP_En = tk.Entry(self.canvas2, width=32, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 10))
        self.OTP_En.place(x=30, y=120)
        self.OTP_En.insert(0, 'OTP')
        self.OTP_En.bind('<FocusIn>', self.otp_click)
        self.OTP_En.bind('<FocusOut>', self.otp_lea)
        tk.Canvas(self.canvas2, width=295, height=2, bg='black').place(x=25, y=144)
        
        self.sendOTP = tk.Button(self.canvas2,width=7, text='OTP', bg='green', fg='white', border=0,command=self.send_otp_button_click)
        self.sendOTP.place(x=265, y=67)
        self.verifyOTP = tk.Button(self.canvas2,width=7, text='Verify', bg='green', fg='white', border=0,command=self.verify_button_click)
        self.verifyOTP.place(x=265, y=120)
       
        self.img = PhotoImage(file="left-arrow.png")
        self.backBTN = tk.Button(self.canvas2, image=self.img, bg='white', border=0, command=self.create_widgets)
        self.backBTN.place(x=10, y=10)

        
    def on_ent1(self, event):
        self.emailEn.delete(0, tk.END)
        
    def on_leve1(self, event):
        name = self.emailEn.get()
        if name == '':
            self.usern.insert(0, 'Email')
            
    def otp_click(self, event):
        self.OTP_En.delete(0, tk.END)
        
    def otp_lea(self, event):
        name = self.OTP_En.get()
        if name == '':
            self.OTP_En.insert(0, 'OTP')

    def create_account_save(self):
        db = pymysql.connect(host='localhost', user='root', password='root', database='ersdb')
        cur = db.cursor()
    
        a = self.usern.get()
        b = self.passn_En.get()
        c = self.mail.get()
    
        if a.strip() and b.strip() and c.strip():  # Check if all values are non-empty
            sql = "select count(*) from login where user='%s'" % a
            cur.execute(sql)
            data = cur.fetchone()
            if data[0] == 0:
                sql = "insert into login (user, password, email) values (%s, %s, %s)"
                values = (a, b, c)
                cur.execute(sql, values)
                messagebox.showinfo('Saved', 'Success')
            else:
                messagebox.showerror('Not Available', 'Try a new name')
            db.commit()
        else:
            messagebox.showerror('Error', 'All fields must be filled')
    
        db.close()
        
    def create_account(self):
        self.canvas1 = tk.Canvas(self.frame, bg="white")
        self.canvas1.place(x=400, y=40, width=350, height=300)
        heading = Label(self.canvas1, text='Create Account', fg='green', bg='white', font=('Microsoft YaHei UI Light', 20, 'bold'))
        heading.place(x=60, y=3)
        
        # User Field
        def user_on_enter(e):
            self.usern.delete(0, tk.END)
        
        def user_on_leave(e):
            name = self.usern.get()
            if name == '':
                self.usern.insert(0, 'Username')
        
        self.usern = Entry(self.canvas1, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 13))
        self.usern.place(x=30, y=65)
        self.usern.insert(0, 'Username')
        self.usern.bind('<FocusIn>', user_on_enter)
        self.usern.bind('<FocusOut>', user_on_leave)
        Canvas(self.canvas1, width=295, height=2, bg='black').place(x=25, y=92)
    
        # Password Field
        def pass_on_enter(e):
            self.passn_En.delete(0, tk.END)
        
        def pass_on_leave(e):
            name = self.passn_En.get()
            if name == '':
                self.passn_En.insert(0, 'Password')
        
        self.passn_En = Entry(self.canvas1, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 13))
        self.passn_En.place(x=30, y=120)
        self.passn_En.insert(0, 'Password')
        self.passn_En.bind('<FocusIn>', pass_on_enter)
        self.passn_En.bind('<FocusOut>', pass_on_leave)
        Canvas(self.canvas1, width=295, height=2, bg='black').place(x=25, y=147)
    
        # Email Field
        def email_on_enter(e):
            self.mail.delete(0, tk.END)
        
        def email_on_leave(e):
            email = self.mail.get()
            if email == '':
                self.mail.insert(0, 'Email')
        
        self.mail = Entry(self.canvas1, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 13))
        self.mail.place(x=30, y=170)
        self.mail.insert(0, 'Email')
        self.mail.bind('<FocusIn>', email_on_enter)
        self.mail.bind('<FocusOut>', email_on_leave)
        Canvas(self.canvas1, width=295, height=2, bg='black').place(x=25, y=200)
    
        # Buttons
        button = Button(self.canvas1, width=40, pady=7, text='Sign up', bg='green', fg='white', border=0, command=self.create_account_save)
        button.place(x=33, y=225)
        label = Label(self.canvas1, text="Back to login page.", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
        label.place(x=90, y=265)
        back_up = Button(self.canvas1, width=6, text='Back', border=0, bg='white', cursor='hand2', fg='green', command=self.create_widgets)
        back_up.place(x=200, y=265)

       
    def create_widgets(self):
        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.place(x=400, y=40, width=350, height=300)
       
        self.heading = tk.Label(self.canvas, text='Sign in', fg='green', bg='white', font=('Microsoft YaHei UI Light', 25, 'bold'))
        self.heading.place(x=105, y=2)
        
        self.usern = tk.Entry(self.canvas, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 13))
        self.usern.place(x=30, y=80)
        self.usern.insert(0, 'username')
        self.usern.bind('<FocusIn>', self.on_ent)
        self.usern.bind('<FocusOut>', self.on_leve)
        tk.Canvas(self.canvas, width=295, height=2, bg='black').place(x=25, y=110)
        
        self.passn_En = tk.Entry(self.canvas, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 10), show='*')
        self.passn_En.place(x=30, y=150)
        self.passn_En.insert(0, 'password')
        self.passn_En.bind('<FocusIn>', self.on_click)
        self.passn_En.bind('<FocusOut>', self.on_lea)
        tk.Canvas(self.canvas, width=295, height=2, bg='black').place(x=25, y=180)
        
        self.button = tk.Button(self.canvas, width=39, pady=9, text='Sign in', bg='green', fg='white', border=0,command=self.che)
        self.button.place(x=35, y=204)
        self.fot_up = tk.Button(self.canvas, width=0, text='Forgot Password', border=-10, bg='white', cursor='hand2', fg='green',command=self.create_forget)
        self.fot_up.place(x=150, y=250)
        self.label = tk.Label(self.canvas, text="Don't have an account.?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
        self.label.place(x=75, y=270)
        self.sign_up = tk.Button(self.canvas, width=8, text='Sign up', border=-10, bg='white', cursor='hand2', fg='green',command=self.create_account)
        self.sign_up.place(x=219, y=270)
        
    def on_ent(self, event):
        self.usern.delete(0, tk.END)
        
    def on_leve(self, event):
        name = self.usern.get()
        if name == '':
            self.usern.insert(0, 'username')
            
    def on_click(self, event):
        self.passn_En.delete(0, tk.END)
        
    def on_lea(self, event):
        name = self.passn_En.get()
        if name == '':
            self.passn_En.insert(0, 'password')
    
    def mailsend(self, get_email):
        from_address = "akshuprety1025@gmail.com"
        to_address = get_email
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Enquiry Registration System"
        msg['From'] = from_address
        msg['To'] = to_address
        
        html = f"""\
            Dear user {to_address},<br>
            Thanks for using ERS (Enquiry Registration System).<br>
            We are sending an email using Python, how fun! We can fill this with HTML, and Gmail supports a decent range of CSS style attributes too - 
            <a href="https://developers.google.com/gmail/design/css#example">Gmail CSS Styles</a>.
        """

        part1 = MIMEText(html, 'html')
        msg.attach(part1)

        username = 'akashuprety1025@gmail.com'
        password = 'precxfifxngccphq'  # It's not recommended to hardcode your password in the code

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(from_address, to_address, msg.as_string())
        server.quit()
        print('Mail sent')

    
    def che(self):
        db = pymysql.connect(host='localhost', user='root', password='root', database='ersdb')
        cur = db.cursor()
        a = self.usern.get()
        b = self.passn_En.get()
        sql = "select email, password from login where user='%s'" % (a)
        cur.execute(sql)
        data = cur.fetchone()
        if data:
            email, password_from_db = data
            print(password_from_db)
            if password_from_db == b:
                print(email)
                email_to_send =email
                self.mailsend(email_to_send)
                messagebox.showinfo('Success', 'Login successful')
               
               #self.root.withdraw()
                self.root.destroy()  
                HomePage()  
                
                    
            else:
                messagebox.showerror('Error', 'Login Failed')
        else:
            messagebox.showerror('Error', 'User not found')
        db.close()
   
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Enquiry Registration System")
    app = SignInApp(root)
    root.mainloop()
