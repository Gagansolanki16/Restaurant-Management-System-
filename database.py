import mysql.connector
from tkinter import messagebox

class Database:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="restaurant1"
        )
        self.mycursor = self.mydb.cursor()

    def verify_login(self, username, password):
        query = "SELECT * FROM admin WHERE username = %s AND password = %s"
        self.mycursor.execute(query, (username, password))
        return self.mycursor.fetchone()
    
    def save_bill(self,billno,cname,cno,date,total):
        self.mycursor.execute("INSERT INTO bills VALUES (%s, %s, %s, %s, %s)",(billno,cname,cno,date,total))
        self.mydb.commit()


    
    def fetch_item_price(self, item_name):
        try:
            self.mycursor.execute("SELECT cost FROM menu WHERE item_name = %s", (item_name,))
            result = self.mycursor.fetchone()
            if result:
                return result[0]
            else:
                return ""
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
            return ""
        
    def insert_menu_item(self,win, item_id, item_name, cost):
        try:
            self.mycursor.execute("INSERT INTO menu (id, item_name, cost) VALUES (%s, %s, %s)",(item_id, item_name, cost))
            self.mydb.commit()
            return True
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "ID already exists! Try a different one.",parent=win)
            return False
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}",parent=win)
            return False
        
    def change_password(self,win,new_password):
        try:
            self.mycursor.execute("UPDATE admin SET password= %s", (new_password,))
            self.mydb.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error changing password", f"Error: {e}",parent=win)
            return False
        
    def fetch_menu_items(self):
        self.mycursor.execute("SELECT id, item_name, cost FROM menu")  
        return self.mycursor.fetchall()
    
    def check_bill_exists(self, bill_no):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM bills WHERE Bill_no = ?", (bill_no,))
            result = self.cursor.fetchone()
            return result[0] > 0  
        except Exception as e:
            return False
