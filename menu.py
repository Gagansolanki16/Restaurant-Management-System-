from tkinter import *
import tkinter as tk
from tkinter import messagebox, simpledialog
from database import Database
from billing import BillingWindow

class Menu:
    def __init__(self, win, billing_window):
        self.win = win
        self.win.geometry("800x600+400+100")
        self.win.title("Restaurant Billing System")

        self.title_label = Label(self.win, text="Restaurant Billing System", font=("Arial", 35, 'bold'),bg="Lightgrey", bd=8, relief=GROOVE)
        self.title_label.pack(side=TOP, fill=X)

        self.db = Database()
        self.billing_window = billing_window

        self.menu_frame = Frame(self.win)
        self.menu_frame.pack(pady=20)

        self.menu_items = [] 
        self.menu_vars = []   

        try:
            items = self.db.fetch_menu_items()  
            if not items:
                Label(self.menu_frame, text="No menu items found!", font=("Arial", 14)).pack()
                return

            for item in items:
                var = IntVar()
                item_name = item[1]
                item_cost = int(item[2]) 

                chk = Checkbutton(self.menu_frame, text=item_name, variable=var, font=("Arial", 14),
                                  command=lambda i=item_name, v=var, c=item_cost: self.ask_quantity(i, v, c))
                chk.pack(anchor="w")

                self.menu_vars.append(var)
                self.menu_items.append(chk)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load menu: {str(e)}", parent=self.win)

    def ask_quantity(self, item_name, var, cost):
        if var.get() == 1:
            quantity = simpledialog.askinteger("Quantity", f"Enter quantity for {item_name}:", minvalue=1)
            if quantity is None:
                var.set(0)  
            else:
                self.billing_window.add_item(item_name, quantity, cost)  
