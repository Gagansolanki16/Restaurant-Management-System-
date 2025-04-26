from tkinter import *
from datetime import datetime
from tkinter import messagebox
from database import Database
import random
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class BillingWindow:
    def __init__(self,win):
        self.win = win
        self.win.geometry("1300x750+0+0")
        self.win.title("Restaurant Billing System")

        self.title_label = Label(self.win,text="Restaurant Billing System",font=("Arial",35,'bold'),bg="Lightgrey",bd=8,relief=GROOVE)
        self.title_label.pack(side=TOP,fill=X)

        def on_resize(event):
            self.win.update_idletasks()


        self.win.state('zoomed')  
        self.win.bind("<Configure>", on_resize)

        db = Database()

        #==============================Variables================================

        bill_no = random.randint(100,999)
        bill_no_tk = IntVar()
        bill_no_tk.set(bill_no)

        Calc_var = StringVar()

        cust_nm = StringVar()
        cust_co = StringVar()
        date_pr = StringVar()
        item_pur = StringVar()
        item_qty = StringVar()
        cost = StringVar()

        date_pr.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        self.total_list = []
        self.grd_total = 0

        #===========================================================================

        #==============================Functions================================

        def default_bill():
            self.bill_txt.insert(END,"\t\t\tSwaad Restaurant")
            self.bill_txt.insert(END,"\n\t\t123, Modi Compound Railway Road,Bharuch")
            self.bill_txt.insert(END,"\n\t\t\tContact - +917896541230")
            self.bill_txt.insert(END,"\n=======================================================================")
            self.bill_txt.insert(END,f"\nBill Number: {bill_no_tk.get()}")
        

        def gen_bill():
            if cust_nm.get == "" or cust_co.get() == "" or len(cust_co.get()) != 10 or cust_co.get()[0] not in "6789" or cust_co.get().isdigit() == 0:
                messagebox.showerror("Error!","Please enter all details correctly",parent=self.win)
            else:
                self.bill_txt.insert(END,f"\nCustomer Name: {cust_nm.get()}")
                self.bill_txt.insert(END,f"\nCustomer Contact: {cust_co.get()}")
                self.bill_txt.insert(END,f"\nDate: {date_pr.get()}")
                self.bill_txt.insert(END,"\n=======================================================================")
                self.bill_txt.insert(END,"\nProduct Name\t\t      Quantity\t\t       Cost\t\t        Total")
                self.bill_txt.insert(END,"\n=======================================================================")
                
                self.add_btn.config(state=NORMAL)
                self.total_btn.config(state=NORMAL)
                self.gen_bill_btn.config(state=DISABLED)

        def add_pur():
            if item_pur.get() == "" or item_qty.get() == "" or item_qty.get().isdigit() == 0:
                messagebox.showerror("Error!","Please enter all details correctly",parent=self.win)
            else:
                qty = int(item_qty.get())
                cone = int(cost.get())
                total = qty * cone
                self.total_list.append(total)
                self.bill_txt.insert(END,f"\n{item_pur.get()}\t\t      {item_qty.get()}\t\t       {cost.get()}\t\t        ₹{total}")


        def clear():
            cust_nm.set("")
            cust_co.set("")
            item_pur.set("")
            item_qty.set("")
            cost.set("")

        def reset():
            self.total_list.clear()
            self.grd_total = 0
            self.add_btn.config(state=DISABLED)
            self.total_btn.config(state=DISABLED)
            self.save_bill_btn.config(state=DISABLED)
            self.gen_bill_btn.config(state=NORMAL)
            self.bill_txt.delete("1.0",END)

            while True:
                new_bill_no = random.randint(100, 999)
                if not db.check_bill_exists(new_bill_no):  
                    break

            bill_no_tk.set(new_bill_no)
            date_pr.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            default_bill()

        def total():
            for item in self.total_list:
                self.grd_total = self.grd_total + item
            self.bill_txt.insert(END,"\n=======================================================================")
            self.bill_txt.insert(END,f"\t\t\t\t\t\t\tGrand Total : ₹{self.grd_total}")
            self.bill_txt.insert(END,"\n=======================================================================")
            self.save_bill_btn.config(state=NORMAL)

        def logout():
            self.win.destroy()

        def save():
            user_choice = messagebox.askyesno("Confirm?", f"Do you want to save the bill {bill_no_tk.get()}", parent=self.win)
            if user_choice > 0:
                self.bill_content = self.bill_txt.get("1.0",END)

            try:
                pdf_path = f"{sys.path[0]}/bills/{bill_no_tk.get()}.pdf"
                c = canvas.Canvas(pdf_path, pagesize=letter)
                c.setFont("Helvetica", 12)

            
                y_position = 750  
                for line in self.bill_content.split("\n"):
                    c.drawString(50, y_position, line)
                    y_position -= 20  

                c.save() 
                db.save_bill(bill_no_tk.get(), cust_nm.get(), cust_co.get(), date_pr.get(), self.grd_total)
                messagebox.showinfo("Success", f"Bill {bill_no_tk.get()} has been saved", parent=self.win)

            except Exception as e:
                messagebox.showerror("Error!", f"Error: {e}")
            
        def text_change(event):
            item = item_pur.get()
            cost.set(db.fetch_item_price(item) or "")

        def menu():
            from menu import Menu
            new_window = Toplevel(self.win)
            app = Menu(new_window, self)
        

        def insert():
            new_window = Toplevel(self.win)
            new_window.geometry("400x300+500+200") 
            new_window.title("Insert New Item")

            # Labels and Entry Fields
            self.item_id_label = Label(new_window, text="Item ID:", font=("Arial", 15), anchor="w")
            self.item_id_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

            self.item_id_entry = Entry(new_window, font=('Arial', 15))
            self.item_id_entry.grid(row=0, column=1, padx=10, pady=5)

            self.item_name_label = Label(new_window, text="Item Name:", font=("Arial", 15), anchor="w")
            self.item_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

            self.item_name_entry = Entry(new_window, font=('Arial', 15))
            self.item_name_entry.grid(row=1, column=1, padx=10, pady=5)

            self.insert_cost_label = Label(new_window, text="Cost:", font=("Arial", 15), anchor="w")
            self.insert_cost_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

            self.cost_entry = Entry(new_window, font=('Arial', 15))
            self.cost_entry.grid(row=2, column=1, padx=10, pady=5)

            def insert_item():
                if self.item_id_entry.get() == "" or self.item_name_entry.get() == "" or self.cost_entry.get() == "":
                    messagebox.showerror("Error!", "Enter all details", parent=new_window)
                else:
                    success = db.insert_menu_item(self.win,self.item_id_entry.get(), self.item_name_entry.get(), self.cost_entry.get())
                    if success:
                        messagebox.showinfo("Success", "Item inserted successfully", parent=new_window)
                        new_window.destroy()

            # Insert Button
            self.insert_button = Button(new_window, text="Insert in Menu",font=('Arial',15),bd=5,width=12,height=1,command=insert_item)
            self.insert_button.grid(row=3, columnspan=2, pady=8)

        #======================================================================


        #=============================Entry====================================

        self.entry_frame = LabelFrame(self.win,text="Enter Details",background="Lightgrey",font=('Arial',20),bd=7,relief=GROOVE)
        self.entry_frame.place(x=20,y=95,width=600,height=650)

        #Bill number
        self.bill_no_lbl = Label(self.entry_frame,text="Bill Number: ",font=("Arial",15),bg="Lightgrey", anchor="w")
        self.bill_no_lbl.grid(row=0,column=0,padx=2,pady=2, sticky="w")

        self.bill_no_ent = Entry(self.entry_frame,bd=5,textvariable=bill_no_tk,font=('Arial',15))
        self.bill_no_ent.grid(row=0,column=1,padx=2,pady=2)
        self.bill_no_ent.config(state=DISABLED)

        #Customer Number
        self.cust_nm_lbl = Label(self.entry_frame,text="Customer Name: ",font=("Arial",15),bg="Lightgrey", anchor="w")
        self.cust_nm_lbl.grid(row=1,column=0,padx=2,pady=2, sticky="w")

        self.cust_nm_ent = Entry(self.entry_frame,bd=5,textvariable=cust_nm,font=('Arial',15))
        self.cust_nm_ent.grid(row=1,column=1,padx=2,pady=2)

        #Customer Contact
        self.cust_no_lbl = Label(self.entry_frame,text="Customer Number: ",font=("Arial",15),bg="Lightgrey", anchor="w")
        self.cust_no_lbl.grid(row=2,column=0,padx=2,pady=2, sticky="w")

        self.cust_no_ent = Entry(self.entry_frame,bd=5,textvariable=cust_co,font=('Arial',15))
        self.cust_no_ent.grid(row=2,column=1,padx=2,pady=2)

        #Date
        self.date_lbl = Label(self.entry_frame,text="Date: ",font=("Arial",15),bg="Lightgrey", anchor="w")
        self.date_lbl.grid(row=3,column=0,padx=2,pady=2, sticky="w")

        self.date_ent = Entry(self.entry_frame,bd=5,textvariable=date_pr,font=('Arial',15))
        self.date_ent.grid(row=3,column=1,padx=2,pady=2)
        self.date_ent.config(state=DISABLED)

        #Item Purchased
        self.item_pur_lbl = Label(self.entry_frame,text="Item Purchased: ",font=("Arial",15),bg="Lightgrey", anchor="w")
        self.item_pur_lbl.grid(row=4,column=0,padx=2,pady=2, sticky="w")

        self.item_pur_ent = Entry(self.entry_frame,bd=5,textvariable=item_pur,font=('Arial',15))
        self.item_pur_ent.grid(row=4,column=1,padx=2,pady=2)
        self.item_pur_ent.bind("<KeyRelease>", text_change)

        #Quantity
        self.qty_lbl = Label(self.entry_frame,text="Quantity: ",font=("Arial",15),bg="Lightgrey", anchor="w")
        self.qty_lbl.grid(row=5,column=0,padx=2,pady=2, sticky="w")

        self.qty_ent = Entry(self.entry_frame,bd=5,textvariable=item_qty,font=('Arial',15))
        self.qty_ent.grid(row=5,column=1,padx=2,pady=2)


        #Cost
        self.cost_lbl = Label(self.entry_frame,text="Cost of One: ",font=("Arial",15),bg="Lightgrey", anchor="w")
        self.cost_lbl.grid(row=6,column=0,padx=2,pady=2, sticky="w")

        self.cost_ent = Entry(self.entry_frame,bd=5,textvariable=cost,font=('Arial',15))
        self.cost_ent.grid(row=6,column=1,padx=2,pady=2)
        self.cost_ent.config(state=DISABLED)


        #Menu
        self.menu_btn = Button(self.entry_frame,text="Menu",font=('Arial',15),bd=5,width=18,height=2,justify=CENTER,command=menu)
        self.menu_btn.place(x=25,y=300)

        self.insert_btn = Button(self.entry_frame,text="Insert new item",font=('Arial',15),bd=5,width=18,height=2,justify=CENTER,command=insert)
        self.insert_btn.place(x=238,y=300)

        #Buttons
        self.button_frame = LabelFrame(self.entry_frame,font=('Arial',15),bg="Lightgrey",bd=7,relief=GROOVE)
        self.button_frame.place(x=20,y=375,width=435,height=230)

        self.add_btn = Button(self.button_frame,text="Add",font=('Arial',15),bd=5,width=11,height=2,command=add_pur)
        self.add_btn.grid(row=1,column=0,padx=2,pady=2)

        self.clear_btn = Button(self.button_frame,text="Clear",font=('Arial',15),bd=5,width=11,height=2,command=clear)
        self.clear_btn.grid(row=0,column=1,padx=2,pady=2)

        self.reset_btn = Button(self.button_frame,text="Reset",font=('Arial',15),bd=5,width=11,height=2,command=reset)
        self.reset_btn.grid(row=0,column=2,padx=2,pady=2)

        self.gen_bill_btn = Button(self.button_frame,text="Generate Bill",font=('Arial',15),bd=5,width=11,height=2,command=gen_bill)
        self.gen_bill_btn.grid(row=0,column=0,padx=2,pady=2)

        self.total_btn = Button(self.button_frame,text="Total",font=('Arial',15),bd=5,width=11,height=2,command=total)
        self.total_btn.grid(row=1,column=1,padx=2,pady=2)

        self.save_bill_btn = Button(self.button_frame,text="Save Bill",font=('Arial',15),bd=5,width=11,height=2,command=save)
        self.save_bill_btn.grid(row=1,column=2,padx=2,pady=2)

        self.logout = Button(self.button_frame,text="Logout",font=('Arial',15),bd=5,width=37,height=2,justify=CENTER,command=logout)
        self.logout.grid(row=2,columnspan=3)


        self.add_btn.config(state=DISABLED)
        self.total_btn.config(state=DISABLED)
        self.save_bill_btn.config(state=DISABLED)

        #==============================Calculator================================================================
        
        self.calc_frame = Frame(self.win,bd=8,background="lightgrey",relief=GROOVE)
        self.calc_frame.place(x=750,y=110,width=605,height=295)

        self.num_ent = Entry(self.calc_frame,bd=15,background="lightgrey",textvariable=Calc_var,font=('Arial',15),width=50,justify="right")
        self.num_ent.grid(row=0,column=0,columnspan=11)

        def press_btn(event):
            text=event.widget.cget("text")
            if text == "=":
                if Calc_var.get().isdigit():
                    value = int(Calc_var.get())
                else:
                    value = eval(self.num_ent.get())
            
                Calc_var.set(value)
                self.num_ent.update()

            elif text == "C":
                Calc_var.set("")
                self.num_ent.update()
            else:
                Calc_var.set(Calc_var.get() + text)
                self.num_ent.update()


        self.btn7 = Button(self.calc_frame,bg="lightgrey",text="7",bd=6,width=11,height=1,font=('Arial',15))
        self.btn7.grid(row=1,column=0,padx=4,pady=2)
        self.btn7.bind("<Button-1>", press_btn)

        self.btn8 = Button(self.calc_frame,bg="lightgrey",text="8",bd=6,width=11,height=1,font=('Arial',15))
        self.btn8.grid(row=1,column=1,padx=2,pady=2)
        self.btn8.bind("<Button-1>", press_btn)

        self.btn9 = Button(self.calc_frame,bg="lightgrey",text="9",bd=6,width=11,height=1,font=('Arial',15))
        self.btn9.grid(row=1,column=2,padx=2,pady=2)
        self.btn9.bind("<Button-1>", press_btn)

        self.btnadd = Button(self.calc_frame,bg="lightgrey",text="+",bd=6,width=11,height=1,font=('Arial',15))
        self.btnadd.grid(row=1,column=3,padx=2,pady=2)
        self.btnadd.bind("<Button-1>", press_btn)

        self.btn4 = Button(self.calc_frame,bg="lightgrey",text="4",bd=6,width=11,height=1,font=('Arial',15))
        self.btn4.grid(row=2,column=0,padx=4,pady=2)
        self.btn4.bind("<Button-1>", press_btn)

        self.btn5 = Button(self.calc_frame,bg="lightgrey",text="5",bd=6,width=11,height=1,font=('Arial',15))
        self.btn5.grid(row=2,column=1,padx=2,pady=2)
        self.btn5.bind("<Button-1>", press_btn)

        self.btn6 = Button(self.calc_frame,bg="lightgrey",text="6",bd=6,width=11,height=1,font=('Arial',15))
        self.btn6.grid(row=2,column=2,padx=2,pady=2)
        self.btn6.bind("<Button-1>", press_btn)

        self.btnsub = Button(self.calc_frame,bg="lightgrey",text="-",bd=6,width=11,height=1,font=('Arial',15))
        self.btnsub.grid(row=2,column=3,padx=2,pady=2)
        self.btnsub.bind("<Button-1>", press_btn)

        self.btn1 = Button(self.calc_frame,bg="lightgrey",text="1",bd=6,width=11,height=1,font=('Arial',15))
        self.btn1.grid(row=3,column=0,padx=4,pady=2)
        self.btn1.bind("<Button-1>", press_btn)

        self.btn2 = Button(self.calc_frame,bg="lightgrey",text="2",bd=6,width=11,height=1,font=('Arial',15))
        self.btn2.grid(row=3,column=1,padx=2,pady=2)
        self.btn2.bind("<Button-1>", press_btn)

        self.btn3 = Button(self.calc_frame,bg="lightgrey",text="3",bd=6,width=11,height=1,font=('Arial',15))
        self.btn3.grid(row=3,column=2,padx=2,pady=2)
        self.btn3.bind("<Button-1>", press_btn)

        self.btnmul = Button(self.calc_frame,bg="lightgrey",text="*",bd=6,width=11,height=1,font=('Arial',15))
        self.btnmul.grid(row=3,column=3,padx=2,pady=2)
        self.btnmul.bind("<Button-1>", press_btn)

        self.btnC = Button(self.calc_frame,bg="lightgrey",text="C",bd=6,width=11,height=1,font=('Arial',15))
        self.btnC.grid(row=4,column=0,padx=4,pady=2)
        self.btnC.bind("<Button-1>", press_btn)

        self.btn0 = Button(self.calc_frame,bg="lightgrey",text="0",bd=6,width=11,height=1,font=('Arial',15))
        self.btn0.grid(row=4,column=1,padx=2,pady=2)
        self.btn0.bind("<Button-1>", press_btn)

        self.btneq = Button(self.calc_frame,bg="lightgrey",text="=",bd=6,width=11,height=1,font=('Arial',15))
        self.btneq.grid(row=4,column=2,padx=2,pady=2)
        self.btneq.bind("<Button-1>", press_btn)

        self.btndiv = Button(self.calc_frame,bg="lightgrey",text="/",bd=6,width=11,height=1,font=('Arial',15))
        self.btndiv.grid(row=4,column=3,padx=2,pady=2)
        self.btndiv.bind("<Button-1>", press_btn)

        #========================================================================================================

        #==============================================Bill Frame================================================

        self.bill_frame = LabelFrame(self.win,text="Bill Area",font=('Arial',18),bg="lightgrey",bd=8,relief=GROOVE)
        self.bill_frame.place(x=750,y=420,width=605,height=320)

        self.y_scroll = Scrollbar(self.bill_frame,orient="vertical")
        self.bill_txt = Text(self.bill_frame,bg="white",yscrollcommand=self.y_scroll.set)

        self.y_scroll.config(command=self.bill_txt.yview)
        self.y_scroll.pack(side=RIGHT,fill=Y)
        self.bill_txt.pack(fill=BOTH,expand=True)

        default_bill()

    def add_item(self,item_name,qty,item_cost):
            total = qty * item_cost
            self.total_list.append(total)
            self.bill_txt.insert(END, f"\n{item_name}\t\t      {qty}\t\t       {item_cost}\t\t        ₹{total}")
            messagebox.showinfo("Added", f"{qty} x {item_name} added to bill!",parent=self.win)