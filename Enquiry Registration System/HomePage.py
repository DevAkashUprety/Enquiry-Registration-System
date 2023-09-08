import tkinter as tk
from tkinter import PhotoImage
from tkinter import font, Menu, PhotoImage
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
import tkinter.scrolledtext as ScrolledText
from datetime import datetime
import tkinter as tk
import pymysql
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import math
import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import filedialog

class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ERS Home")
        self.geometry("1520x760+0+0")
        self.iconbitmap('ErsIcon.ico')
        self.resizable(False, False)
        self.configure(bg='white') 

        self.f = font.Font(family="Lucida Fax", size=12, weight="bold")
        self.f1 = font.Font(family="MS UI Gothic", size=22, weight="bold")
        self.f2 = font.Font(family="Gadugi", size=48, weight="bold")
        
        self.frame = tk.Frame(self, bg="white")
        self.frame.place(x=80, y=30, width=1350, height=640)
        try:
            con = pymysql.connect(host="localhost", user="root", password="root", database="ersdb")
            cursor = con.cursor()
            cursor.execute("SELECT COUNT(*) FROM student")
            total_Students = cursor.fetchone()[0]
        
            cursor.execute("SELECT COUNT(*) FROM apply_leave")
            total_leave = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM attendance")
            total_present = cursor.fetchone()[0]

            cursor.close()
            con.close()
    
            
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

        
        self.emply = tk.Canvas(self.frame, bg="Gold")
        self.emply.place(x=3, y=50, width=300, height=100)
        self.emphd = tk.Label(self.emply, text="Total Student", font=("Arial",13, "bold"), fg="black",bg="Gold")
        self.emphd.place(x=95, y=9)
        self.emphd1 = tk.Label(self.emply,text=str(total_Students), font=("Arial",25, "bold"), fg="black",bg="Gold")
        self.emphd1.place(x=130, y=50)
        
        self.leave = tk.Canvas(self.frame, bg="LightBlue")
        self.leave.place(x=550, y=50, width=300, height=100)
        self.leavehd = tk.Label(self.leave, text="Student Leave", font=("Arial",13, "bold"), fg="black",bg="LightBlue")
        self.leavehd.place(x=95, y=9)
        self.leavehd1 = tk.Label(self.leave, text=str(total_leave), font=("Arial",25, "bold"), fg="black",bg="LightBlue")
        self.leavehd1.place(x=130, y=50)
        
        self.pemp = tk.Canvas(self.frame, bg="lightSalmon")
        self.pemp.place(x=1047, y=50, width=300, height=100)

        self.pemphd = tk.Label(self.pemp, text="Present Student", font=("Arial",13, "bold"), fg="black",bg="lightSalmon")
        self.pemphd.place(x=90, y=9)
        self.pemphd1 = tk.Label(self.pemp, text=str(total_present), font=("Arial",25, "bold"), fg="black",bg="lightSalmon")
        self.pemphd1.place(x=130, y=50)
        
        
        def get_data():
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='root',
                database='ersdb'
            )

            query = "SELECT name, age FROM student"

            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()

            state = [result[0] for result in results]
            pop = [result[1] for result in results]

            connection.close()

            return state, pop

        state, pop = get_data()

        fig, ax = plt.subplots(figsize=(9, 6.5))
        ax.bar(state, pop, color=['r', 'b', 'g', 'y'])
        ax.set_xlabel(' ')
        ax.set_ylabel(' ')

        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()

        canvas.get_tk_widget().place(x=1, y=160)
         
        def get_data_fee():
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='root',
                database='ersdb'
            )

            query = "SELECT month_year, eid FROM fees"

            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()

            state = [result[0] for result in results]
            pop = [result[1] for result in results]

            connection.close()

            return state, pop

        state, pop = get_data_fee()

        fig, ax = plt.subplots(figsize=(9, 6.5))
        ax.bar(state, pop, color=['b', 'g', 'r', 'y'])
        ax.set_xlabel(' ')
        ax.set_ylabel(' ')

        canvas1 = FigureCanvasTkAgg(fig, master=self.frame)
        canvas1.draw()

        canvas1.get_tk_widget().place(x=700, y=160)
        
        
        menubar = tk.Menu(self)

        profile_menu = tk.Menu(menubar, tearoff=0)
        profile_menu.add_command(label="Create Profile", command=self.open_add_Student)
        profile_menu.add_command(label="View Profile", command=self.create_widgets)
        menubar.add_cascade(label="Profile", menu=profile_menu)

        manage_menu = tk.Menu(menubar, tearoff=0)
        manage_menu.add_command(label="Update Details", command=self.create_update_window)
        menubar.add_cascade(label="Manage", menu=manage_menu)

        attendance_menu = tk.Menu(menubar, tearoff=0)
        attendance_menu.add_command(label="Take Attendance", command=self.open_student_attendance)
        attendance_menu.add_command(label="View Attendance", command=self.initialize_widgets)
        menubar.add_cascade(label="Attendance", menu=attendance_menu)

        leave_menu = tk.Menu(menubar, tearoff=0)
        leave_menu.add_command(label="Apply Leave", command=self.ApplyLeave)
        leave_menu.add_command(label="View Leaves", command=self.View_Leave)
        menubar.add_cascade(label="Leave", menu=leave_menu)

        salary_menu = tk.Menu(menubar, tearoff=0)
        salary_menu.add_command(label="Add Fees", command=self.FeeInsert)
        salary_menu.add_command(label="Generate Fees", command=self.feeSlip)
        menubar.add_cascade(label="Fees", menu=salary_menu)

        delete_menu = tk.Menu(menubar, tearoff=0)
        delete_menu.add_command(label="Delete Student", command=self.DateStudent)
        menubar.add_cascade(label="Delete", menu=delete_menu)

        exit_menu = tk.Menu(menubar, tearoff=0)
        exit_menu.add_command(label="Logout", command=self.exit_program)
        menubar.add_cascade(label="Exit", menu=exit_menu)

        
        for menu in [profile_menu, manage_menu, attendance_menu, leave_menu, salary_menu, exit_menu, delete_menu]:
            menu.configure(font=self.f, background="white", foreground="black")

        for item in profile_menu.winfo_children() + manage_menu.winfo_children() + attendance_menu.winfo_children() + \
                    leave_menu.winfo_children() + salary_menu.winfo_children() + exit_menu.winfo_children() + delete_menu.winfo_children():
            item.configure(font=self.f1, background="black", foreground="white")

        self.config(menu=menubar)
        self.canvas = tk.Canvas(self, bg="#DCDCDC")
        self.canvas.place(x=80, y=680, width=1350, height=50)
        self.copyright = tk.Label(self.canvas, text="@ Copyright - 2023", font=("Arial", 9, "bold"), fg="gray",bg="#DCDCDC")
        self.copyright.place(x=1200, y=15)
        self.copyright_note = tk.Label(self.canvas, text="All Rights Reserved", font=("Arial", 9, "bold"), fg="gray",bg="#DCDCDC")
        self.copyright_note.place(x=30, y=15)


#-------------------------------------------------Add Student----------------
    def open_add_Student(self):

        self.frame = tk.Frame(self, bg="white")
        self.frame.place(x=80, y=30, width=1350, height=640)
        self.body= tk.Canvas(self.frame,bg="#FAF9F6")
        self.body.place(x=100, y=50, width=1130, height=400)

        self.id1 = tk.Label(self.body, text="New Student Details",width=65, font=("Arial", 22), fg="black",bg="#FAF9F6")
        self.id1.place(x=2, y=2)

        self.id2 = tk.Label(self.body, text="Name", font=("Arial", 18), fg="black",bg="#FAF9F6")
        self.id2.place(x=80, y=60)
        self.t1 = tk.Entry(self.body,width=25, font=("Arial",15))
        self.t1.place(x=250, y=60)

        self.id3 = tk.Label(self.body, text="Father Name", font=("Arial", 18), fg="black",bg="#FAF9F6")
        self.id3.place(x=560, y=60)
        self.t2 = tk.Entry(self.body,width=25, font=("Arial",15))
        self.t2.place(x=730, y=60)

        self.id4 = tk.Label(self.body, text="Age",font=("Arial", 18), fg="black",bg="#FAF9F6")
        self.id4.place(x=80, y=110)
        self.t3 = tk.Entry(self.body, width=25, font=("Arial", 15))
        self.t3.place(x=250, y=110)

    
        self.id5 = tk.Label(self.body, text="Date of Birth", font=("Arial", 18), fg="black",bg="#FAF9F6")
        self.id5.place(x=560, y=110)
        self.t4 = tk.Entry(self.body,width=25, font=("Arial",15))
        self.t4.place(x=730, y=110)

        self.id6 = tk.Label(self.body, text="Address", font=("Arial", 18), fg="black",bg="#FAF9F6")
        self.id6.place(x=80, y=160)
        self.t5 = tk.Entry(self.body,width=25, font=("Arial",15))
        self.t5.place(x=250, y=160)

        self.id7 = tk.Label(self.body, text="Phone", font=("Arial", 18), fg="black",bg="#FAF9F6")
        self.id7.place(x=560, y=160)
        self.t6 = tk.Entry(self.body,width=25, font=("Arial",15))
        self.t6.place(x=730, y=160)

        self.id8 = tk.Label(self.body, text="Email Id", font=("Arial",18), fg="black",bg="#FAF9F6")
        self.id8.place(x=80, y=210)
        self.t7 = tk.Entry(self.body,width=25, font=("Arial",15))
        self.t7.place(x=250, y=210)

        self.id9 = tk.Label(self.body, text="Education", font=("Arial", 18), fg="black",bg="white")
        self.id9.place(x=560, y=210)
        self.t8 = tk.Entry(self.body,width=25, font=("Arial",15))
        self.t8.place(x=730, y=210)

        self.id10 = tk.Label(self.body, text="Job Post", font=("Arial", 18), fg="black",bg="#FAF9F6")
        self.id10.place(x=80, y=260)
        self.t9 = tk.Entry(self.body,width=25, font=("Arial",15))
        self.t9.place(x=250, y=260)

        self.id11 = tk.Label(self.body, text="Aadhar No", font=("Arial", 18), fg="black",bg="#FAF9F6")
        self.id11.place(x=560, y=260)
        self.t10 = tk.Entry(self.body,width=25, font=("Arial",15))
        self.t10.place(x=730, y=260)
        
        
        self.id12 = tk.Label(self.body, text="Student ID", font=("Arial", 18), fg="black",bg="#FAF9F6")
        self.id12.place(x=80, y=310)
      
        random_student_id = str(random.randint(100000, 999999))
        self.t11 = tk.Entry(self.body, width=25, font=("Arial", 15))
        self.t11.insert(0, random_student_id)
        self.t11.config(state=tk.DISABLED)
        self.t11.place(x=250, y=310)

      
        self.b = tk.Button(self.body, text="Submit", bg="green", fg="white", font=("Arial", 13),border=0, command=self.submitee)
        self.b.place(x=780, y=350,width=100)
        
        self.b1 = tk.Button(self.body, text="Cancel", bg="red", fg="white", font=("Arial", 13),border=0, command=self.cancel)
        self.b1.place(x=900, y=350,width=100)
           
    def submitee(self):
        name = self.t1.get()
        fname = self.t2.get()
        age = self.t3.get()
        dob = self.t4.get()
        address = self.t5.get()
        phone = self.t6.get()
        email = self.t7.get()
        education = self.t8.get()
        post = self.t9.get()
        aadhar = self.t10.get()
        eid = self.t11.get()

        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="ersdb"
            )

            cursor = con.cursor()

            query = "INSERT INTO  student (name, fname, age, dob, address, phone, email, education, post, aadhar, eid) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            data = (name, fname, age, dob, address, phone, email, education, post, aadhar, eid)

            cursor.execute(query, data)

            con.commit()

            messagebox.showinfo("Success", "Details Successfully Inserted")

            cursor.close()
            con.close()
          
        except mysql.connector.Error as err:
            print("Error executing SQL query:", err)
            name = self.t1.get()
        
        self.t1.delete(0, tk.END)
        self.t2.delete(0, tk.END)
        self.t3.delete(0, tk.END)
        self.t4.delete(0, tk.END)
        self.t5.delete(0, tk.END)
        self.t6.delete(0, tk.END)
        self.t7.delete(0, tk.END)
        self.t8.delete(0, tk.END)
        self.t9.delete(0, tk.END)
        self.t10.delete(0, tk.END)
        self.t11.delete(0, tk.END)

    def cancel(self):
        self.destroy()
        HomePage()

#--------------------------------------------------------View Student------------------

    def create_widgets(self):
        self.framee = tk.Frame(self.frame, bg="white")
        self.framee.place(x=0, y=10, width=1350, height=700)
        self.ma= tk.Frame(self.framee ,bg="#FAF9F6")
        self.ma.place(x=50, y=30, width=1250, height=580)
        self.body= tk.Canvas(self.ma,bg="#F9F6EE")
        self.body.place(x=20, y=30, width=610, height=145)
        
        self.l2 = tk.Label(self.body, text="Student Id", font=("Arial",18), fg="black",bg="#F9F6EE")
        self.l2.place(x=20, y=20)

        self.t = tk.Entry(self.body,font=("Arial",16),width=47,bg="#FAF9F6")
        self.t.place(x=20, y=55,)
        self.b1 = ttk.Button(self.body, text="Search",style="Green.TButton",command=self.search)
        self.b2 = ttk.Button(self.body, text="Close",style="Red.TButton",command=self.cncl)
        self.b1.place(x=420, y=100)
        self.b2.place(x=510, y=100)
        
        self.tree = ttk.Treeview(self.ma, columns=("Student ID", "Name", "Father Name", "E-mail"), show="headings")
        self.tree.heading("Student ID", text="Student ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Father Name", text="Father Name")
        self.tree.heading("E-mail", text="E-mail")
        
        self.tree.column("Student ID", minwidth=100, width=100, stretch=False)
        self.tree.column("Name", minwidth=150, width=120, stretch=False)
        self.tree.column("Father Name", minwidth=200, width=152, stretch=False)
        self.tree.column("E-mail", minwidth=80, width=200, stretch=False)
        self.tree.place(x=650, y=30, width=575, height=530)
        self.load_att()
    
    def print_data(self):
        messagebox.showinfo("Print", "Printed successfully")
    def cncl(self):
        self.destroy()
        HomePage()
    
    def view_Student_data(self,Eid):
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="ersdb"
            )
            cursor = con.cursor()
    
            query = "SELECT * FROM student WHERE eid='" + Eid + "'"
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                name = result[1]
                father = result[2]
                age = result[3]
                dob = result[4]
                address = result[5]
                phone = result[6]
                email = result[7]
                education = result[8]
                post = result[9]
                aadhar = result[10]
            else:
                messagebox.showinfo("Error", "Employee ID not found")
                con.close()
                return
    
            con.close()
    
            self.bod = tk.Canvas(self.ma, bg="#DCDCDC")
            self.bod.place(x=50, y=195, width=550, height=365)
    
            self.id8 = tk.Label(self.bod, text="Student Details",width=38, font=("Arial", 18), fg="gray", bg="#DCDCDC")
            self.id8.place(x=2, y=2)
    
            self.id = tk.Label(self.bod, text="Student Id", font=("Arial", 12), bg="#DCDCDC")
            self.id.place(x=100, y=50)
            self.aid = tk.Label(self.bod, text=Eid, font=("Arial", 12), bg="#DCDCDC")
            self.aid.place(x=330, y=50)
    
            self.id1 = tk.Label(self.bod, text="Name", font=("Arial", 12), bg="#DCDCDC")
            self.id1.place(x=100, y=80)
            self.aid1 = tk.Label(self.bod, text=name, font=("Arial", 12), bg="#DCDCDC")
            self.aid1.place(x=330, y=80)
    
            self.id2 = tk.Label(self.bod, text="Father's Name", font=("Arial", 12), bg="#DCDCDC")
            self.id2.place(x=100, y=110)
            self.aid2 = tk.Label(self.bod, text=father, font=("Arial", 12), bg="#DCDCDC")
            self.aid2.place(x=330, y=110)
    
            self.id3 = tk.Label(self.bod, text="Address", font=("Arial", 12), bg="#DCDCDC")
            self.id3.place(x=100, y=140)
            self.aid3 = tk.Label(self.bod, text=address, font=("Arial", 12), bg="#DCDCDC")
            self.aid3.place(x=330, y=140)
    
            self.id4 = tk.Label(self.bod, text="Mobile No", font=("Arial", 12), bg="#DCDCDC")
            self.id4.place(x=100, y=170)
            self.aid4 = tk.Label(self.bod, text=phone, font=("Arial", 12), bg="#DCDCDC")
            self.aid4.place(x=330, y=170)
    
            self.id5 = tk.Label(self.bod, text="Email Id", font=("Arial", 12), bg="#DCDCDC")
            self.id5.place(x=100, y=200)
            self.aid5 = tk.Label(self.bod, text=email, font=("Arial", 12), bg="#DCDCDC")
            self.aid5.place(x=330, y=200)
    
            self.id6 = tk.Label(self.bod, text="Education", font=("Arial", 12), bg="#DCDCDC")
            self.id6.place(x=100, y=230)
            self.aid6 = tk.Label(self.bod, text=education, font=("Arial", 12), bg="#DCDCDC")
            self.aid6.place(x=330, y=230)
    
            self.id7 = tk.Label(self.bod, text="Job Post", font=("Arial", 12), bg="#DCDCDC")
            self.id7.place(x=100, y=260)
            self.aid7 = tk.Label(self.bod, text=post, font=("Arial", 12), bg="#DCDCDC")
            self.aid7.place(x=330, y=260)
    
            self.id8 = tk.Label(self.bod, text="Aadhar No", font=("Arial", 12), bg="#DCDCDC")
            self.id8.place(x=100, y=290)
            self.aid8 = tk.Label(self.bod, text=aadhar, font=("Arial", 12), bg="#DCDCDC")
            self.aid8.place(x=330, y=290)
    
            self.b1 = tk.Button(self.bod, text="Print",bg="green",width=10, border=0,command=self.print_data)
            self.b1.place(x=150, y=330)
    
            self.b2 = tk.Button(self.bod, text="Cancel",bg="red",width=10,border=0,command=self.cancel1)
            self.b2.place(x=300, y=330)
    
        except mysql.connector.Error as err:
            print("Error executing SQL query:", err)
    
        
    def search(self):
        student_id = self.t.get()
        messagebox.showinfo("Succsess", f"Searching for Student ID: {student_id}")
        self.view_Student_data(student_id)
        
    def cancel1(self):
        self.bod.destroy()
   
    def print_data(self):
        student_details = [
            ("Student ID:", self.aid.cget('text')),
            ("Name:", self.aid1.cget('text')),
            ("Father's Name:", self.aid2.cget('text')),
            ("Address:", self.aid3.cget('text')),
            ("Mobile No:", self.aid4.cget('text')),
            ("Email Id:", self.aid5.cget('text')),
            ("Education:", self.aid6.cget('text')),
            ("Job Post:", self.aid7.cget('text')),
            ("Aadhar No:", self.aid8.cget('text'))
        ]
    
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Workbook", "*.xlsx"), ("Plain Text", "*.txt"), ("PDF", "*.pdf"), ("All Files", "*.*")],
            title="Save Student Details"
        )
    
        if file_path:
            if file_path.endswith(".xlsx"):
                workbook = openpyxl.Workbook()
                sheet = workbook.active
                sheet.title = "Student Details"
    
                for row_data in student_details:
                    sheet.append(row_data)
    
                try:
                    workbook.save(file_path)
                    messagebox.showinfo("Success", "Data saved successfully")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while saving: {e}")
    
            elif file_path.endswith(".txt"):
                with open(file_path, "w") as file:
                    for detail in student_details:
                        file.write(f"{detail[0]} {detail[1]}\n")
    
                messagebox.showinfo("Success", "Data saved successfully")
    
            elif file_path.endswith(".pdf"):
                c = canvas.Canvas(file_path, pagesize=letter)
                y = 750
    
                for detail in student_details:
                    c.drawString(100, y, f"{detail[0]} {detail[1]}")
                    y -= 20
    
                c.save()
                messagebox.showinfo("Success", "Data saved successfully")

  
            
#------------------------------------------------------update-----------------------------------------
    
    def populate_combobox(self, combobox):
        try:
            con = pymysql.connect(host="localhost", user="root", password="root", database="ersdb")
            cursor = con.cursor()
            cursor.execute("SELECT eid FROM student")
            rows = cursor.fetchall()
            combobox['values'] = [row[0] for row in rows]
            cursor.close()
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))
    
    def populate_Student_data(self, event, combobox, entries):
        eid = combobox.get()
        try:
            con = pymysql.connect(host="localhost", user="root", password="root", database="ersdb")
            cursor = con.cursor()
            cursor.execute(f"SELECT * FROM student WHERE eid='{eid}'")
            student_data = cursor.fetchone()
            cursor.close()
            con.close()
    
            if student_data:
                for i, entry in enumerate(entries):
                    entry.delete(0, tk.END)
                    entry.insert(0, student_data[i+1])
            else:
                messagebox.showerror("Error", "Student ID not found.")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))
    
    def update_dataa(self, combobox, entries):
        eid = combobox.get()
        name = entries[0].get()
        fname = entries[1].get()
        age = entries[2].get()
        dob = entries[3].get()
        address = entries[4].get()
        phone = entries[5].get()
        email = entries[6].get()
        education = entries[7].get()
        post = entries[8].get()
        aadhar = entries[9].get()
    
        try:
            con = pymysql.connect(host="localhost", user="root", password="root", database="ersdb")
            cursor = con.cursor()
            query = f"UPDATE student SET name='{name}', fname='{fname}', age='{age}', dob='{dob}', address='{address}', phone='{phone}', email='{email}', education='{education}', post='{post}', aadhar='{aadhar}' WHERE eid='{eid}'"
            rows_affected = cursor.execute(query)
            con.commit()
            cursor.close()
            con.close()
    
            if rows_affected == 1:
                messagebox.showinfo("Success", "Data updated successfully.")
            else:
                messagebox.showerror("Error", "Please fill all details carefully.")

        except Exception as ex:
            messagebox.showerror("Error", str(ex))
    
    def cancel(self):
        self.destroy()
        HomePage()  # Replace 'HomePage()' with the appropriate call to go back to the homepage.
    
    def create_update_window(self):
        f = ("Arial", 15, "bold")
        f1 = ("Arial", 11, "bold")
        self.frame = tk.Frame(self, bg="white")
        self.frame.place(x=80, y=30, width=1350, height=640)  # Adjust the width and height as needed
    
        self.canv = tk.Canvas(self.frame, bg="#FAF9F6")
        self.canv.place(x=150, y=50, width=1000, height=550)  # Adjust the width and height as needed
        
        tk.Label(self.canv, text="STUDENT UPDATE", font=25, bg="green", fg="white", width=95).place(x=0, y=0)
       
        tk.Label(self.canv, text="Student ID", font=f1, bg="#FAF9F6").place(x=250, y=70)
        self.ch = ttk.Combobox(self.canv, width=55)
        self.ch.place(x=438, y=70, width=300, height=25)  # Adjust the width and height as needed
        self.ch.bind("<<ComboboxSelected>>", lambda event: self.populate_Student_data(event, self.ch, self.entries))
    
        self.label_list = [
            "Name", "Father's Name", "Age", "Date of Birth", "Address",
            "Phone", "E-mail", "Education", "Job Post", "Aadhar"
        ]
    
        self.entries = []
        for row, label_text in enumerate(self.label_list, 1):
            tk.Label(self.canv, text=label_text, font=f1, bg="#FAF9F6").place(x=250, y=75+row*35)
            entry = tk.Entry(self.canv, font=f1, width=44)
            entry.place(x=440, y=75+row*35, width=300, height=25)  # Adjust the width and height as needed
            self.entries.append(entry)
    
        ttk.Button(self.canv, text="Update Data", command=lambda: self.update_dataa(self.ch, self.entries)).place(x=350, y=130+12*30, width=100, height=30) 
        ttk.Button(self.canv, text="Back", command=self.cancel).place(x=550, y=130+12*30, width=100, height=30) 
    
        self.populate_combobox(self.ch)

#__________________________UpdateEnd____________________________

#============================== Attendance =============================
           
    def open_student_attendance(self): 
        self.font = ("senserif", 15, "bold")
        self.frm = tk.Frame(self, bg="white")
        self.frm.place(x=80, y=30, width=1350, height=640)
        
        self.cavs = tk.Canvas(self.frm, bg="#FAF9F6")
        self.cavs.place(x=50, y=20, width=1250, height=600)
        
        
        self.label_ = tk.Label(self.cavs, text="Attendance", font=self.font,width=105,bg="Green",fg="white").place(x=0,y=0)
        
        self.label_1 = tk.Label(self.cavs,bg="#FAF9F6", text="Select Student ID", font=self.font)
        self.label_2 = tk.Label(self.cavs,bg="#FAF9F6", text="First Half", font=self.font)
        self.label_3 = tk.Label(self.cavs,bg="#FAF9F6", text="Second Half", font=self.font)
        self.label_4 = tk.Label(self.cavs,bg="#FAF9F6", text="Name", font=self.font)
        self.label_5 = tk.Label(self.cavs,bg="#FAF9F6", text="E-mail", font=self.font)

        self.textfield_1 = ttk.Entry(self.cavs, font=self.font)
        self.textfield_2 = ttk.Entry(self.cavs, font=self.font)
        self.textfield_1.config(state=tk.DISABLED)
        self.textfield_2.config(state=tk.DISABLED)

        self.choice_2 = ttk.Combobox(self.cavs, values=["Present", "Absent"], font=self.font)
        self.choice_3 = ttk.Combobox(self.cavs, values=["Present", "Absent"], font=self.font)

        self.button_submit = ttk.Button(self.cavs, text="Submit", command=self.submit_dataIn, style="Green.TButton")
        self.button_close = ttk.Button(self.cavs, text="Close", command=self.close_application, style="Red.TButton")

        self.choice_1 = ttk.Combobox(self.cavs, font=self.font)
        self.students_ids()

        self.label_1.place(x=260, y=80)
        self.choice_1.place(x=480, y=80,width=500)
        self.label_4.place(x=260, y=120)
        self.textfield_1.place(x=480, y=120,width=500)
        self.label_5.place(x=260, y=160)
        self.textfield_2.place(x=480, y=160,width=500)
        self.label_2.place(x=260, y=200)
        self.choice_2.place(x=480, y=200,width=500)
        self.label_3.place(x=260, y=240)
        self.choice_3.place(x=480, y=240,width=500)
        self.button_submit.place(x=450, y=290)
        self.button_close.place(x=760, y=290)


        self.choice_1.bind("<<ComboboxSelected>>", self.load_student_data)
        
            
           
        
        self.tree = ttk.Treeview(self.cavs, columns=("Student ID", "Name", "Father Name", "E-mail", "Address", "Cource","Phone No"), show="headings")
        self.tree.heading("Student ID", text="Student ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Father Name", text="Father Name")
        self.tree.heading("E-mail", text="E-mail")
        self.tree.heading("Address", text="Address")
        self.tree.heading("Cource", text="Cource")
        self.tree.heading("Phone No", text="Phone No")
        
        self.tree.column("Student ID", minwidth=100, width=140, stretch=False)
        self.tree.column("Name", minwidth=150, width=144, stretch=False)
        self.tree.column("Father Name", minwidth=200, width=152, stretch=False)
        self.tree.column("E-mail", minwidth=80, width=200, stretch=False)
        self.tree.column("Address", minwidth=80, width=250, stretch=False)
        self.tree.column("Cource", minwidth=150, width=111, stretch=False)
        self.tree.column("Phone No", minwidth=150, width=200, stretch=False)
        self.tree.place(x=25, y=330, width=1200, height=250)
        self.load_att()

    def students_ids(self):
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="ersdb"
                )
                cursor = connection.cursor()
                cursor.execute("SELECT eid FROM student")
                student_ids = cursor.fetchall()
                self.choice_1["values"] = [eid[0] for eid in student_ids]
                cursor.close()
                connection.close()
            except Exception as ex:
                print("Database Error"+ex)
    
    def load_student_data(self, event):
            try:
                eid = self.choice_1.get()
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="ersdb"
                )
                cursor = connection.cursor()
                cursor.execute("SELECT name, email FROM student WHERE eid=%s", (eid,))
                student_data = cursor.fetchone()
                if student_data:
                    self.textfield_1.config(state=tk.NORMAL)
                    self.textfield_2.config(state=tk.NORMAL)
                    self.textfield_1.delete(0, tk.END)
                    self.textfield_1.insert(0, student_data[0])
                    self.textfield_2.delete(0, tk.END)
                    self.textfield_2.insert(0, student_data[1])
                    self.textfield_1.config(state=tk.DISABLED)
                    self.textfield_2.config(state=tk.DISABLED)
                else:
                    self.textfield_1.config(state=tk.NORMAL)
                    self.textfield_2.config(state=tk.NORMAL)
                    self.textfield_1.delete(0, tk.END)
                    self.textfield_2.delete(0, tk.END)
                    self.textfield_1.config(state=tk.DISABLED)
                    self.textfield_2.config(state=tk.DISABLED)
                cursor.close()
                connection.close()
                
            except Exception as ex:
                print(ex)
                messagebox.showerror("Error", str(ex))
            
            
    
    def submit_dataIn(self):
            ch_eid = self.choice_1.get()
            ch_first_half = self.choice_2.get()
            ch_second_half = self.choice_3.get()
            name = self.textfield_1.get()
            email = self.textfield_2.get()
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="ersdb"
                )
                cursor = connection.cursor()
    
                # Start a transaction
                connection.start_transaction()
    
                query = "INSERT INTO attendance (eid, name, email, first_half, second_half, day_time) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (ch_eid, name, email, ch_first_half, ch_second_half, dt)
                cursor.execute(query, values)
                connection.commit()
    
                # Commit the transaction
                connection.commit()
    
                cursor.close()
                connection.close()
                tk.messagebox.showinfo("Success", "Done Attendance")
                
            except mysql.connector.Error as err:
                # Rollback the transaction in case of error
                if 'connection' in locals():
                    connection.rollback()
                print(f"Error: {err}")
                tk.messagebox.showerror("Error", f"Error: {err}")
    
    def close_application(self):
                if tk.messagebox.askyesno("Confirmation", "Are you sure you want to close?"):
                    self.destroy()
                    HomePage()
                    
    
    def load_att(self):
        try:
            connection = mysql.connector.connect(host="localhost", port=3306, database="ersdb", user="root", password="root")
            cursor = connection.cursor()
            query = "SELECT * FROM student"
            cursor.execute(query)
            records = cursor.fetchall()
            
            for record in records:
                sid = record[11]
                name = record[1]
                fname = record[2]
                email = record[7]
                address = record[5]
                course = record[8]
                phone = record[6]
                
                self.tree.insert("", "end", values=(sid, name, fname, email, address, course, phone))
       
        except mysql.connector.Error as e:
            print("Error while connecting to MySQL:", e)
            messagebox.showerror("Error", "Error while connecting to MySQL")
        
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                


#-----------------------------------------View Attendance------------------------------------------------
    def initialize_widgets(self):
            self.frm = tk.Frame(self, bg="white")
            self.frm.place(x=80, y=30, width=1350, height=640)
            
            self.cavs = tk.Canvas(self.frm, bg="#FAF9F6")
            self.cavs.place(x=50, y=50, width=1250, height=520)
            
            self.font = font.Font(family="MS UI Gothic", size=16, weight="bold")
            self.font1 = font.Font(family="Lucida Fax", size=22, weight="bold")
        
            self.tree = ttk.Treeview(self.cavs, columns=("Student ID", "Name", "Email", "First Half", "Second Half", "Date Time"), show="headings")
            self.tree.heading("Student ID", text="Student ID")
            self.tree.heading("Name", text="Name")
            self.tree.heading("Email", text="Email")
            self.tree.heading("First Half", text="First Half")
            self.tree.heading("Second Half", text="Second Half")
            self.tree.heading("Date Time", text="Date Time")
            self.tree.column("Student ID", minwidth=100, width=180, stretch=False)
            self.tree.column("Name", minwidth=150, width=180, stretch=False)
            self.tree.column("Email", minwidth=200, width=250, stretch=False)
            self.tree.column("First Half", minwidth=80, width=200, stretch=False)
            self.tree.column("Second Half", minwidth=80, width=200, stretch=False)
            self.tree.column("Date Time", minwidth=150, width=185, stretch=False)
            self.tree.place(x=20, y=60, width=1200, height=350)
        
            self.label1 = tk.Label(self.cavs, text="Search any Student", font=self.font1, fg="white",width=66, bg="pink")
            self.label1.place(x=2, y=2)
        
            self.label2 = tk.Label(self.cavs, text="Student Id", font=self.font, fg="Gray",bg="#FAF9F6")
            self.label2.place(x=350, y=435)
        
            self.entry = tk.Entry(self.cavs, font=self.font,width=40,bg="#F9F6EE")
            self.entry.place(x=475, y=435)
        
            self.search_button = ttk.Button(self.cavs, text="Search", command=self.search_studeFind)
            self.search_button.place(x=880, y=470)
        
            self.load_records()
    def load_records(self):
        try:
            connection = mysql.connector.connect(host="localhost", port=3306, database="ersdb", user="root", password="root")
            cursor = connection.cursor()
            query = "SELECT * FROM attendance"
            cursor.execute(query)
            records = cursor.fetchall()
            for record in records:
                self.tree.insert("", "end", values=record)
        except Error as e:
            print("Error while connecting to MySQL:", e)
            messagebox.showerror("Error","Error while connecting to MySQL")
    
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def search_studeFind(self):
        student_id = self.entry.get()
        self.tree.delete(*self.tree.get_children())
        try:
            connection = mysql.connector.connect(host="localhost", port=3306, database="ersdb", user="root", password="root")
            cursor = connection.cursor()
            query = "SELECT * FROM  attendance WHERE eid=%s"
            cursor.execute(query, (student_id,))
            records = cursor.fetchall()
            
            if not records:
                messagebox.showinfo("No Data Found", "No records found for the given Student ID.")
            else:
                for record in records:
                    self.tree.insert("", "end", values=record)
        
        except Error as e:
            print("Error while connecting to MySQL:", e)
            messagebox.showerror("Error","Error while connecting to MySQL")
    
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
#----------------------------------------------------------------Apply Leave---------------------------------------------

    def ApplyLeave(self):
        self.font = ("Arial", 20, "bold")
        self.font1 = ("Arial", 16, "bold")
        self.frame = tk.Frame(self, bg="White")
        self.frame.place(x=80, y=30, width=1350, height=640)
        
        self.canvas = tk.Frame(self.frame, bg="#FAF9F6")
        self.canvas.place(x=130, y=50, width=1100, height=460)

        self.label_1 = tk.Label(self.canvas, text="Apply Student Leave", font=self.font,bg="pink",width="65",fg="white")
        self.label_2 = tk.Label(self.canvas, text="Select Student ID", font=self.font1,bg="#FAF9F6")
        self.label_3 = tk.Label(self.canvas, text="Name", font=self.font1,bg="#FAF9F6")
        self.label_4 = tk.Label(self.canvas, text="Email", font=self.font1,bg="#FAF9F6")
        self.label_5 = tk.Label(self.canvas, text="Start Date", font=self.font1,bg="#FAF9F6")
        self.label_6 = tk.Label(self.canvas, text="End Date", font=self.font1,bg="#FAF9F6")
        self.label_7 = tk.Label(self.canvas, text="Leave Reason", font=self.font1,bg="#FAF9F6")

        self.choice_1 = ttk.Combobox(self.canvas, font=self.font1,width=30)
        self.choice_1.bind("<<ComboboxSelected>>", self.load_stu_data)

        self.tf1 = tk.Entry(self.canvas, font=self.font1,width=32)
        self.tf2 = tk.Entry(self.canvas, font=self.font1,width=32)
        self.tf3 = tk.Entry(self.canvas,font=self.font1,width=32)
        self.tf4 = tk.Entry(self.canvas, font=self.font1,width=32)

        self.bt1 = ttk.Button(self, text="Submit", command=self.submit_data, style="Green.TButton")
       
        self.ch2 = ttk.Combobox(self.canvas, values=[
            "Health Issue", "Family Member Health Issue", "Function/ Celebration",
            "Party", "Personal Issue", "Dating", "Other's"], font=self.font1,width=30)

        self.load_employee_ids()

        self.label_1.place(x=0, y=0)
        self.label_2.place(x=230, y=80)
        self.choice_1.place(x=480, y=80)
        self.label_3.place(x=230, y=130)
        self.tf1.place(x=480, y=130)
        self.label_4.place(x=230, y=180)
        self.tf2.place(x=480, y=180)
        self.label_5.place(x=230, y=230)
        self.tf3.place(x=480, y=230)
        self.label_6.place(x=230, y=280)
        self.tf4.place(x=480, y=280)
        self.label_7.place(x=230, y=330)
        self.ch2.place(x=480, y=330)
        self.bt1.place(x=600, y=480)
       

    def load_employee_ids(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="ersdb"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT eid FROM student")
            student_ids = cursor.fetchall()
            self.choice_1["values"] = [eid[0] for eid in student_ids]
            cursor.close()
            connection.close()
        except Exception as ex:
            print("Database not Connect"+ex)

    def load_stu_data(self, event):
        try:
            eid = self.choice_1.get()
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="ersdb"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT name, email FROM student WHERE eid=%s", (eid,))
            student_data = cursor.fetchone()
            if student_data:
                self.tf1.config(state=tk.NORMAL)
                self.tf2.config(state=tk.NORMAL)
                self.tf1.delete(0, tk.END)
                self.tf1.insert(0, student_data[0])
                self.tf2.delete(0, tk.END)
                self.tf2.insert(0, student_data[1])
                self.tf1.config(state=tk.DISABLED)
                self.tf2.config(state=tk.DISABLED)
            else:
                self.tf1.config(state=tk.NORMAL)
                self.tf2.config(state=tk.NORMAL)
                self.tf1.delete(0, tk.END)
                self.tf2.delete(0, tk.END)
                self.tf1.config(state=tk.DISABLED)
                self.tf2.config(state=tk.DISABLED)
            cursor.close()
            connection.close()
        except Exception as ex:
            print(ex)

    def submit_data(self):
        eid = self.choice_1.get()
        name = self.tf1.get()
        email = self.tf2.get()
        startdt = self.tf3.get()
        enddt = self.tf4.get()
        reason = self.ch2.get()
        apply_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="ersdb"
            )
            cursor = connection.cursor()

            query = "INSERT INTO apply_leave VALUES(%s, %s, %s, %s, %s, %s, %s)"
            values = (eid, name, email, startdt, enddt, reason, apply_dt)

            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "Successfully Applyed leave")
        except Exception as ex:
            print(ex)
            messagebox.showerror("Error", "Please fill all the details carefully")

  
#-------------------------------------------------------View Leave______________________________________________    
    
    def View_Leave(self):       
        self.f = ("MS UI Gothic", 17, "bold")
        self.f1 = ("Lucida Fax", 20, "bold")
        
        self.frame = tk.Frame(self, bg="white")
        self.frame.place(x=80, y=30, width=1350, height=640)
        
        self.canvas = tk.Frame(self.frame, bg="#FAF9F6")
        self.canvas.place(x=100, y=50, width=1150, height=540)

        self.l1 = tk.Label(self.canvas, text="Search any Student", font=self.f1,fg="white",width=65, bg="pink")
        self.l1.place(x=0, y=0)

        self.l2 = tk.Label(self.canvas, text="Student ID", font=19, fg="Gray",bg="#FAF9F6")
        self.l2.place(x=250, y=430)

        self.tf1 = tk.Entry(self.canvas, font=self.f,width=40,bg="#F9F6EE")
        self.tf1.place(x=380, y=430)

        self.bt1 = ttk.Button(self.canvas, text="Search", command=self.search1_Stu, style="Black.TButton")
        self.bt1.place(x=830, y=470)

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="ersdb"
            )
            cursor = connection.cursor()
            query = "select * from apply_leave"
            cursor.execute(query)
            records = cursor.fetchall()

            self.x = ["Student ID", "Name", "Email", "Start Date", "End Date", "Reason", "Apply Date"]
            self.y = [list(record) for record in records]

            cursor.close()
            connection.close()

            self.t = ttk.Treeview(self.canvas, columns=self.x, show="headings")
            self.t.column("Student ID", minwidth=100, width=150, stretch=False)
            self.t.column("Name", minwidth=150, width=150, stretch=False)
            self.t.column("Email", minwidth=200, width=150, stretch=False)
            self.t.column("Start Date", minwidth=80, width=150, stretch=False)
            self.t.column("End Date", minwidth=80, width=150, stretch=False)
            self.t.column("Reason", minwidth=150, width=200, stretch=False)
            self.t.column("Apply Date", minwidth=150, width=160, stretch=False)
            
            for col in self.x:
                self.t.heading(col, text=col)
                self.t.column(col, anchor=tk.CENTER)
            for data in self.y:
                self.t.insert("", tk.END, values=data)

        except Exception as ex:
            print("ERROR"+ex)
            self.y = []
            self.t = ttk.Treeview(self.canvas, columns=self.x, show="headings")
            for col in self.x:
                self.t.heading(col, text=col)
                self.t.column(col, anchor=tk.CENTER)

        self.js = ttk.Scrollbar(self.canvas, orient=tk.VERTICAL, command=self.t.yview)
        self.t.configure(yscrollcommand=self.js.set)
        self.t.place(x=10,y=60,width=1125,height=320)
        self.js.place(x=1117, y=61, height=317)
        
        self.style = ttk.Style()
        self.style.configure("Black.TButton", foreground="black", background="white")

    def search1_Stu(self):
        eid = self.tf1.get()
        if eid:
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="ersdb"
                )
                cursor = connection.cursor()
                query = "select * from apply_leave where eid=%s"
                cursor.execute(query, (eid,))
                records = cursor.fetchall()

                if records:
                    self.y = [list(record) for record in records]
                    self.t.delete(*self.t.get_children())
                    for data in self.y:
                        self.t.insert("", tk.END, values=data)
                else:
                    messagebox.showinfo("No Records", "No records found for the given Student ID.")
            except Exception as ex:
                print("Database Error"+ex)
        else:
            messagebox.showwarning("Empty Field", "Please enter Student ID for search.")

    
#________________________________________Fees insert--------------------------------------    
    def FeeInsert(self):
        self.frame = tk.Frame(self, bg="white")
        self.frame.place(x=80, y=30, width=1350, height=640)

        self.canvas = tk.Frame(self.frame, bg="#FAF9F6")
        self.canvas.place(x=120, y=50, width=1100, height=540)
        f = ("Arial", 14, "bold")
        f1 = ("Arial", 20, "bold")
        
        self.label = tk.Label(self.canvas, text="Fees Record Insert",bg="pink", font=25,width=100).place(x=0,y=0)
        self.label1 = tk.Label(self.canvas, text="Select Student ID",bg="#FAF9F6", font=f)
        self.label2 = tk.Label(self.canvas, text="Name",bg="#FAF9F6", font=f)
        self.label3 = tk.Label(self.canvas, text="E-mail",bg="#FAF9F6", font=f)
        self.label4 = tk.Label(self.canvas, text="Java",bg="#FAF9F6", font=f)
        self.label5 = tk.Label(self.canvas, text="Python",bg="#FAF9F6", font=f)
        self.label6 = tk.Label(self.canvas, text="PHP", bg="#FAF9F6" ,font=f)
        self.label7 = tk.Label(self.canvas, text="Web Development",bg="#FAF9F6", font=f)
        self.label8 = tk.Label(self.canvas, text="Dot Net",bg="#FAF9F6", font=f)
        self.label9 = tk.Label(self.canvas, text="Select Month",bg="#FAF9F6", font=f)
        self.label10 = tk.Label(self.canvas, text="Select Year",bg="#FAF9F6", font=f)
       
        self.choice1 = ttk.Combobox(self.canvas, font=f, state="readonly",width=35)
        self.populate_stu_ids()

        self.choice2 = ttk.Combobox(self.canvas,width=35, font=f, values=[
            "January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"
        ])

        self.choice3 = ttk.Combobox(self.canvas,width=35, font=f, values=[
            "2023", "2024", "2025", "2026", "2027", "2028", "2029",
            "2030", "2031", "2032", "2033", "2034", "2035", "2036"
        ])

        self.text1 = tk.Entry(self.canvas, font=f,width=37)
        self.text2 = tk.Entry(self.canvas, font=f,width=37)
        self.text3 = tk.Entry(self.canvas, font=f,width=37)
        self.text4 = tk.Entry(self.canvas, font=f,width=37)
        self.text5 = tk.Entry(self.canvas, font=f,width=37)
        self.text6 = tk.Entry(self.canvas, font=f,width=37)
        self.text7 = tk.Entry(self.canvas, font=f,width=37)

        self.text1.config(state="readonly")
        self.text2.config(state="readonly")

       
        self.button1 = ttk.Button(self.canvas, text="Submit",command=self.submitii_data)
       
        self.label1.place(x=250, y=80)
        self.choice1.place(x=480, y=80)
        self.label2.place(x=250, y=120)
        self.text1.place(x=480, y=120)
        self.label3.place(x=250, y=160)
        self.text2.place(x=480, y=160)
        self.label4.place(x=250, y=200)
        self.text3.place(x=480, y=200)
        self.label5.place(x=250, y=240)
        self.text4.place(x=480, y=240)
        self.label6.place(x=250, y=280)
        self.text5.place(x=480, y=280)
        self.label7.place(x=250, y=320)
        self.text6.place(x=480, y=320)
        self.label8.place(x=250, y=360)
        self.text7.place(x=480, y=360)
        self.label9.place(x=250, y=400)
        self.choice2.place(x=480, y=400)
        self.label10.place(x=250, y=440)
        self.choice3.place(x=480, y=440)
        self.button1.place(x=810, y=490)
        
        
        self.choice1.bind("<<ComboboxSelected>>", self.get_student_info)

    def populate_stu_ids(self):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="root", database="ersdb")
            cursor = connection.cursor()
            query = "SELECT eid FROM student"
            cursor.execute(query)
            student_ids = [result[0] for result in cursor.fetchall()]
            self.choice1['values'] = student_ids
            cursor.close()
            connection.close()
        except Exception as ex:
            print("Database Error"+ex)

    def get_student_info(self, event):
        student_id = self.choice1.get()
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="root", database="ersdb")
            cursor = connection.cursor()
            query = f"SELECT name, email FROM student WHERE eid = '{student_id}'"
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                name, email = result
                self.text1.config(state="normal")
                self.text2.config(state="normal")
                self.text1.delete(0, tk.END)
                self.text2.delete(0, tk.END)
                self.text1.insert(0, name)
                self.text2.insert(0, email)
                self.text1.config(state="readonly")
                self.text2.config(state="readonly")
            cursor.close()
            connection.close()
        except Exception as ex:
            print("Database Error"+ex)

    def submitii_data(self):
            Eid = self.choice1.get()
            name = self.text1.get()
            email = self.text2.get()
            try:
                java = float(self.text3.get())
                python = float(self.text4.get())
                php = float(self.text5.get())
                web = float(self.text6.get())
                basic = float(self.text7.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values.")
                return
    
            month = self.choice2.get() + " " + self.choice3.get()
    
            if not (Eid and name and email and month):
                messagebox.showerror("Error", "Please fill all details correctly.")
                return                                                           
                        
            try:
                db_connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='root',
                    database='ersdb'
                )
    
                cursor = db_connection.cursor()
    
                query = "INSERT INTO fees (eid, name, email, java, python, php, web, basic,month_year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                data = (Eid, name, email, java, python, php, web, basic, month)
    
                cursor.execute(query, data)
    
                db_connection.commit()
    
                cursor.close()
                db_connection.close()
    
                messagebox.showinfo("Success", "Your data successfully inserted")
    
            except Exception as ex:
                messagebox.showerror("Error", "Please fill all details correctly: " + str(ex))
                print(ex)
    
#-------------------------------------------fee slip--------------------------------------     

    def feeSlip(self):
        self.frame = tk.Frame(self, bg="white")
        self.frame.place(x=80, y=30, width=1350, height=640)
        self.f = ("Arial", 16, "bold")

        self.canvas = tk.Canvas(self.frame, bg="#FAF9F6")
        self.canvas.place(x=230, y=50, width=890, height=540)
        
        self.l1 = tk.Label(self.canvas, text="Student Id",bg="#FAF9F6", font=self.f)
        self.l2 = tk.Label(self.canvas, text="Month",bg="#FAF9F6", font=self.f)
        self.l3 = tk.Label(self.canvas, text="Year",bg="#FAF9F6", font=self.f)

        self.ch1 = ttk.Combobox(self.canvas)
        self.populate_student_ids()

        self.ch2 = ttk.Combobox(self.canvas, values=["January", "February", "March", "April", "May", "June", "July", "August",
                                                   "September", "October", "November", "December"])
        self.ch2.set("July")

        self.ch3 = ttk.Combobox(self.canvas, values=["2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030", "2031",
                                                   "2032", "2033", "2034", "2035", "2036"])
        self.ch3.set("2023")

        self.ch1['font'] = self.ch2['font'] = self.ch3['font'] = self.f

        self.bt1 = ttk.Button(self.canvas, text="Print", command=self.print_pay_slip)
       
        self.l1.grid(row=0, column=0, padx=10, pady=10)
        self.ch1.grid(row=0, column=1, padx=10, pady=10)
        self.l2.grid(row=1, column=0, padx=10, pady=10)
        self.ch2.grid(row=1, column=1, padx=10, pady=10)
        self.l3.grid(row=2, column=0, padx=10, pady=10)
        self.ch3.grid(row=2, column=1, padx=10, pady=10)
        self.bt1.grid(row=3, column=1, padx=10, pady=10)
       
        self.ta = tk.Text(self.canvas, font=self.f, width="72", height="13")
        self.ta.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def populate_student_ids(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="ersdb"
            )
            cursor = connection.cursor()
            query = "SELECT eid FROM student"
            cursor.execute(query)
            student_ids = [row[0] for row in cursor.fetchall()]
            self.ch1['values'] = student_ids
            cursor.close()
            connection.close()
        except Exception as ex:
            print("Database Error"+ex)

    def print_pay_slip(self):
        self.ta.delete("1.0", tk.END)
        self.ta.insert(tk.END, "---------------------------------Fees Slip-------------------------------\n")
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="ersdb"
            )
            cursor = connection.cursor()
            eid = self.ch1.get()
            month_year = self.ch2.get() + " " + self.ch3.get()

            q1 = f"SELECT * FROM student WHERE eid='{eid}'"
            cursor.execute(q1)
            student_details = cursor.fetchone()

            if student_details:
                self.ta.insert(tk.END, f"Student Id : {student_details[11]}")
                self.ta.insert(tk.END, f"\nStudent Name : {student_details[1]}")
                self.ta.insert(tk.END, f"\nStudent Email : {student_details[7]}")
                self.ta.insert(tk.END, "\n....................................................................")

            q2 = f"SELECT * FROM fees WHERE month_year='{month_year}' AND eid='{eid}'"
            cursor.execute(q2)
            fee_details = cursor.fetchone()
            if not fee_details:
                self.ta.insert(tk.END, "\n....................................................................")
                self.ta.insert(tk.END, "\nRecord not found of this month and year.\n")
                self.ta.insert(tk.END, "\n....................................................................")
                self.ta.insert(tk.END, "\nPlease add the fee of this month and year for this record.\n")
            else:
                java = float(fee_details[4])
                python = float(fee_details[5])
                php = float(fee_details[6])
                web = float(fee_details[7])
                Dot_net = float(fee_details[8])

                self.ta.insert(tk.END, f"\n\nJava : {java}")
                self.ta.insert(tk.END, f"\n\nPython : {python}")
                self.ta.insert(tk.END, f"\n\nPHP : {php}")
                self.ta.insert(tk.END, f"\n\nWeb Developer : {web}")
                self.ta.insert(tk.END, f"\n\nDot Net : {Dot_net}")

                self.ta.insert(tk.END, "\n--------------------------------------------------------------------")
                grossSalary = java + python + php + web + Dot_net
                gst = (grossSalary * 2.1) / 100
                total_fee= grossSalary + gst
                self.ta.insert(tk.END, f"\nGross Fees : {grossSalary}")
                self.ta.insert(tk.END, f"\nTotal : {total_fee}")
                self.ta.insert(tk.END, f"\nGST 2.1% : {gst}")

            cursor.close()
            connection.close()
        except Exception as ex:
            print("Database Error"+ex)

 
#-----------------------------------------Date Student-------------------------------------------------- 
 
    def DateStudent(self):
        self.frame = tk.Frame(self, bg="white")
        self.frame.place(x=80, y=30, width=1350, height=640)
        
        self.canvas = tk.Canvas(self.frame, bg="#FAF9F6")
        self.canvas.place(x=120, y=50, width=1100, height=420)
        self.f = ("MS UI Gothic", 17, "bold")
        self.f1 = ("Lucida Fax", 20, "bold")
        self.bg_color = "white"
        self.fg_color = "black"
        self.button_bg_color = "black"
        self.button_fg_color = "white"
        self.pink_color = "pink"
        self.grey_color = "grey"
        self.black_color = "black"

        
        self.conn = pymysql.connect(host="localhost", user="root", password="root", database="ersdb")
        self.cur = self.conn.cursor()

        self.x = ["Student ID", "Name", "Email", "Age", "Date of Birth", "Post"]
        self.y = []
        self.fetch_data()

        self.t = ttk.Treeview(self.canvas, columns=self.x, show="headings",height=10)
        for col in self.x:
            self.t.heading(col, text=col)
            self.t.column(col, anchor=tk.CENTER)
            self.t.column(col, width=177)
        for data in self.y:
            self.t.insert("", "end", values=data)
        self.t.place(x=15,y=55)

        self.l1 = tk.Label(self.canvas, text="Delete Student Record", font=self.f1, fg=self.fg_color, bg=self.pink_color)
        self.l1.place(x=0,y=0,width=1100)

        self.l2 = tk.Label(self.canvas, text="Student Id", font=self.f, fg=self.grey_color,bg="#FAF9F6")
        self.l2.place(x=290,y=320)

        self.tf1 = tk.Entry(self.canvas, font=self.f,width=30,bg="#F9F6EE")
        self.tf1.place(x=490,y=320)

        self.bt1 = ttk.Button(self.canvas, text="Delete",command=self.delete_student)
        self.bt1.place(x=810,y=360)

    def fetch_data(self):
        self.cur.execute("SELECT eid,name,email,age,dob,post FROM student")
        self.y = self.cur.fetchall()

    def delete_student(self):
        eid = self.tf1.get()
        if eid:
            try:
                self.cur.execute("DELETE FROM student WHERE eid=%s", (eid,))
                self.conn.commit()
                self.cur.execute("DELETE FROM attendance WHERE eid=%s", (eid,))
                self.conn.commit()
                self.cur.execute("DELETE FROM apply_leave WHERE eid=%s", (eid,))
                self.conn.commit()
                self.cur.execute("DELETE FROM fees WHERE eid=%s", (eid,))
                self.conn.commit()
                messagebox.showinfo("Success", "Successfully Deleted.")
                
            except Exception as ex:
                messagebox.showerror("Error", "Delete unsuccessful. Error: " + str(ex))
        else:
            messagebox.showwarning("Warning", "Please enter the Student ID.")

    def on_closing(self):
        self.cur.close()
        self.conn.close()
        self.destroy()

#---------------------------------------------------Exit code-----------------------------------------
       

    def exit_program(self):
        self.destroy()

if __name__ == "__main__":
    app = HomePage()
    app.mainloop()
