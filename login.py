from tkinter import *
from tkinter import messagebox
from billing import BillingWindow
from database import Database

class LoginPage:
    def __init__(self, win):
        self.win = win
        self.win.geometry("1350x750+0+0")
        self.win.title("Restaurant Billing System")

        self.win.state('zoomed')  
        self.win.bind("<Configure>", lambda event: self.win.update_idletasks())  

        self.title_label = Label(self.win, text="Restaurant Billing System", font=("Arial", 35, 'bold'), bg="Lightgrey", bd=8, relief=GROOVE)
        self.title_label.pack(side=TOP, fill=X)

        self.main_frame = Frame(self.win, bg="Lightgrey", bd=6, relief=GROOVE)
        self.main_frame.place(x=250, y=150, width=800, height=450)

        self.login_lbl = Label(self.main_frame, text="Login", bd=6, relief=GROOVE, anchor=CENTER, bg="Lightgrey", font=('sans-serif', 25, 'bold'))
        self.login_lbl.pack(side=TOP, fill=X)

        self.entry_frame = LabelFrame(self.main_frame, text="Enter Details", bd=6, relief=GROOVE, bg='Lightgrey', font=('sans-serif', 18))
        self.entry_frame.pack(fill=BOTH, expand=True)

        # Variables
        self.username = StringVar()
        self.password = StringVar()

        # Username Entry
        Label(self.entry_frame, text="Enter Username: ", bg="Lightgrey", font=('sans-serif', 15)).grid(row=0, column=0, padx=2, pady=2)
        self.entus_ent = Entry(self.entry_frame, font=('sans-serif', 15), bd=6, textvariable=self.username)
        self.entus_ent.grid(row=0, column=1, padx=2, pady=2)

        # Password Entry
        Label(self.entry_frame, text="Enter Password: ", bg="Lightgrey", font=('sans-serif', 15)).grid(row=1, column=0, padx=2, pady=2)
        self.entpass_ent = Entry(self.entry_frame, font=('sans-serif', 15), bd=6, textvariable=self.password, show="*")
        self.entpass_ent.grid(row=1, column=1, padx=2, pady=2)

        # Buttons
        self.button_frame = LabelFrame(self.entry_frame, text="Options", font=('Arial', 15), bg="Lightgrey", bd=7, relief=GROOVE)
        self.button_frame.place(x=20, y=150, width=500, height=150)

        self.login_btn = Button(self.button_frame, text="Login", font=('Arial', 15), bd=5, width=15, command=self.check_login)
        self.login_btn.grid(row=0, column=0, padx=20, pady=2)

        self.billing_btn = Button(self.button_frame, text="Billing", font=('Arial', 15), bd=5, width=15, command=self.billing)
        self.billing_btn.grid(row=0, column=1, padx=20, pady=2)
        self.billing_btn.config(state="disabled")

        self.reset_btn = Button(self.button_frame, text="Reset", font=('Arial', 15), bd=5, width=15, command=self.reset)
        self.reset_btn.grid(row=1, column=0, padx=20, pady=2)

        self.change_btn = Button(self.button_frame, text="Change Password", font=('Arial', 15), bd=5, width=15,command=self.change)
        self.change_btn.grid(row=1, column=1, padx=20, pady=2)

    def check_login(self):
        db = Database()
        user = db.verify_login(self.username.get(), self.password.get())
        if user:
            self.billing_btn.config(state="normal")
        else:
            messagebox.showerror(title="Login Failed!", message="Invalid username or password")

    def reset(self):
        self.username.set("")
        self.password.set("")

    def change(self):
        new_window = Toplevel(self.win)
        new_window.geometry("550x300+500+200") 
        new_window.title("Change Password")

        self.passw = Label(new_window, text="Enter new password:", font=("Arial", 15), anchor="w")
        self.passw.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.passw_entry = Entry(new_window, font=('Arial', 15))
        self.passw_entry.grid(row=0, column=1, padx=10, pady=5)

        self.re_passw = Label(new_window, text="Re-enter new password:", font=("Arial", 15), anchor="w")
        self.re_passw.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.re_passw_entry = Entry(new_window, font=('Arial', 15))
        self.re_passw_entry.grid(row=1, column=1, padx=10, pady=5)

        def change_passw():
            new_pass = self.passw_entry.get()
            re_pass = self.re_passw_entry.get()
        
            if not new_pass or not re_pass:
                messagebox.showerror("Error", "Password fields cannot be empty",parent=new_window)
                return

            if len(new_pass) > 8 or len(re_pass) > 8:
                messagebox.showerror("Error", "Password must be of lenth 8 or less",parent=new_window)
                return
        
            if new_pass != re_pass:
                messagebox.showerror("Error", "Passwords do not match!",parent=new_window)
                return
        
            db = Database()
            success = db.change_password(self.win,new_pass) 
        
            if success:
                messagebox.showinfo("Success", "Password changed successfully!",parent=new_window)
                new_window.destroy()
            

        self.insert_button = Button(new_window, text="Change Password",font=('Arial',15),bd=5,width=15,height=1,command=change_passw)
        self.insert_button.grid(row=3, columnspan=2, pady=8)

    def billing(self):
        if not hasattr(self, 'billing_window'):  
            self.billing_window = BillingWindow(Toplevel(self.win))  
        else:
            self.billing_window.win.deiconify()  