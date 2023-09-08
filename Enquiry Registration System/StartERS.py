import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
from loginpage import *


class EnquiryRegistrationSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1520x780+0+0')
        self.root.configure(bg='white')
        self.root.iconbitmap('ErsIcon.ico')
        self.root.resizable(False, False)

        self.txt = tk.Label(root, text='Enquiry Registration System', bg='white', fg='light green', font=('arial', 45, 'bold'))
        self.txt.place(x=350, y=450)

        self.img = tk.PhotoImage(file='Ers.png')
        tk.Label(root, image=self.img, bg='white').place(x=600, y=90)

        self.progress_label = tk.Label(root, text="Loading.....", font=("Trebuchet Ms", 13, "bold"), fg='green', bg='white')
        self.progress_label.place(x=700, y=650)

        progress = ttk.Style()
        progress.theme_use('clam')
        progress.configure("red.Horizontal.TProgressbar", background="green")

        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=900, mode='determinate',
                                        style="red.Horizontal.TProgressbar")
        self.progress.place(x=320, y=680)

        self.i = 0
        self.load()

    def load(self):
        if self.i <= 20:
            txt0 = 'Loading....' + (str(5 * self.i) + '%')
            self.progress_label.config(text=txt0)
            self.progress_label.after(600, self.load)
            self.progress['value'] = 5 * self.i
            self.i += 1
        else:
            self.top()

    def top(self):
        self.root.withdraw()
        os.system("python loginpage.py")
        self.root.destroy()
        
        
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Enquiry Registration System")
    app = EnquiryRegistrationSystem(root)
    root.mainloop()
