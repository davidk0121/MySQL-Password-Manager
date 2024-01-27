import random
import string
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import mysql.connector

class DatabasePM(Frame):

    def __init__(self, master):
        """ Initialize Frame. """
        super(DatabasePM, self).__init__(master)  
        self.grid()
        self.create_widgets()

        if not self.table_exists("user_data"):
                self.create_newTable()

    def table_exists(self, table_name):
        connection = mysql.connector.connect(
            user="root",
            password="in020121",
            database="passwords"
        )
        cursor = connection.cursor()
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cursor.fetchone()
        connection.close()
        return result is not None

    def create_newTable(self):
        connection = mysql.connector.connect(
            user="root",
            password="in020121",
            database="passwords"
        )
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE user_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                website VARCHAR(255) NOT NULL,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        ''')
        connection.close()

    def create_widgets(self):
        # blank labels
        self.label_blank0 = Label(self, text="").grid(row = 0, column = 0, sticky = W)
        self.label_blank1 = Label(self, text="Fill all three entries to use Save or Delete:", bg="#4b4b4b").grid(row =5, column = 0, columnspan=2, sticky = W)
        self.label_blank3 = Label(self, text="").grid(row =7, column = 0, sticky = W)
        self.label_blank4 = Label(self, text="").grid(row =10, column = 0, sticky = W)
        self.label_blank5 = Label(self, text="").grid(row =11, column = 0, sticky = W)
        self.label_blank6 = Label(self, text="").grid(row =8, column = 0, sticky = W)

        # Website entry
        self.label_Web = Label(self, text="Website:").grid(row = 1, column = 0, sticky = W) 
        self.entry_Web = Entry(self)
        self.entry_Web.grid(row = 1, column = 1, sticky = W)
        
        # User ID entry
        self.label_ID = Label(self, text="User ID:").grid(row = 2, column = 0, sticky = W)
        self.entry_ID = Entry(self)
        self.entry_ID.grid(row = 2, column = 1, sticky = W) 

        # Password entry
        self.label_PW = Label(self, text="Password:").grid(row = 3, column = 0, sticky = W)
        self.entry_PW = Entry(self)
        self.entry_PW.grid(row = 3, column = 1, sticky = W)

        # Generate Password button
        self.btn_Generate = Button(self,text="Generate Password",fg="Blue",command=self.generate_password).grid(row = 3, column = 2, sticky = W)

        # Save button
        self.btnSave = Button(self,text="Save",fg="Blue",command=self.saveData).grid(row = 6, column = 0, sticky = W)
        
        # Clear button
        self.btnClear = Button(self,text="Clear",fg="Blue",command=self.clear_text).grid(row = 6, column = 2, sticky = W)
        
        # Close button
        self.btnClose = Button(self,text="Close Tab",command=self.close,fg="Blue").grid(row = 13, column = 2, sticky = W)
        
        # Load Data button
        self.btnLoadData = Button(self,text="Load Data",fg="Blue",command=self.loadData).grid(row = 13, column = 0, sticky = W)

        # Delete button
        self.btn_delete = Button(self,text="Delete",fg="Blue",command=self.delete).grid(row = 6, column = 1, sticky = W)

        # Search by Website
        self.label_blank5 = Label(self, text="Search by Website:").grid(row =9, column = 0, sticky = W)
        self.entry_searchWeb = Entry(self)
        self.entry_searchWeb.grid(row = 9, column = 1, sticky = W)
        self.btn_searchWeb = Button(self,text="Search",fg="Blue",command=self.searchWeb).grid(row = 9, column = 2, sticky = W)

        # Search by ID
        self.label_blank6 = Label(self, text="Search by ID:").grid(row =10, column = 0, sticky = W)
        self.entry_searchID = Entry(self)
        self.entry_searchID.grid(row = 10, column = 1, sticky = W)
        self.btn_searchID = Button(self,text="Search",fg="Blue",command=self.searchID).grid(row = 10, column = 2, sticky = W)

    ## Generate Password
    def generate_password(self):
        password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(16))
        self.entry_PW.insert(0, password)
    
    ## Save
    def saveData(self):
        try:
            website = self.entry_Web.get()
            username = self.entry_ID.get()
            password = self.entry_PW.get()

            self.executeSQL(website,username,password)

            messagebox.showinfo('Success', 'Data added successfully')
        except Exception as e:
            messagebox.showerror('Error', str(e))
    
    ## Save side function
    def executeSQL(self,website,username,password):
        connection = mysql.connector.connect(
            user="root",
            password="in020121",
            database="passwords"
        )
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO user_data (website, username, password) 
                          VALUES (%s, %s, %s)''', (website, username, password))
        connection.commit()
        connection.close()

    ## Clear
    def clear_text(self):
        self.entry_Web.delete(0, END)
        self.entry_ID.delete(0, END)
        self.entry_PW.delete(0, END)
        self.entry_Web.focus_set()

    ## Close
    def close(self):
        root.destroy()
    
    ## Load Data
    def loadData(self):
        try:
            results = self.loadDataFromDB()

            messagebox.showinfo('Data', results)
        except Exception as e:
            messagebox.showerror('Error', str(e))
    
    ## Load Data side function
    def loadDataFromDB(self):
        connection = mysql.connector.connect(
            user="root",
            password="in020121",
            database="passwords"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT website, username, password FROM user_data")
        rows = cursor.fetchall()

        result = ''
        for row in rows:
            result += str(row) + '\n'

        connection.close()
        return result

    ## Search - Search by Website
    def searchWeb(self):
        try:
            keyword = self.entry_searchWeb.get()
            records = self.connectWeb(keyword)

            if records:
                messagebox.showinfo('Success', 'Records found')
                for record in records:
                    print(f"Website: {record[0]}\nUsername: {record[1]}\nPassword: {record[2]}\n\n")
            else:
                messagebox.showinfo('Success', 'No records found')
        except Exception as e:
            messagebox.showerror('Error', str(e))
    
    ## Search by Website side function
    def connectWeb(self,keyword):
        connection = mysql.connector.connect(
            user="root",
            password="in020121",
            database="passwords"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT website, username, password FROM user_data WHERE website LIKE %s", ('%' + keyword + '%',))
        record = cursor.fetchall()
        connection.close()
        return record

    ## Search - Search by ID
    def searchID(self):
        try:
            keyword = self.entry_searchID.get()
            records = self.connectID(keyword)

            if records:
                messagebox.showinfo('Success', 'Records found')
                for record in records:
                    print(f"Website: {record[0]}\nUsername: {record[1]}\nPassword: {record[2]}\n\n")
            else:
                messagebox.showinfo('Success', 'No records found')
        except Exception as e:
            messagebox.showerror('Error', str(e))
    
    ## Search by ID side function
    def connectID(self,keyword):
        connection = mysql.connector.connect(
            user="root",
            password="in020121",
            database="passwords"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT website, username, password FROM user_data WHERE username LIKE %s", ('%' + keyword + '%',))
        record = cursor.fetchall()
        connection.close()
        return record

    ## Delete
    def delete(self):
        try:
            website = self.entry_Web.get()
            username = self.entry_ID.get()
            password = self.entry_PW.get()

            self.deleteSQL(website,username,password)
            messagebox.showinfo('Success', 'Account deleted successfully')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    ## Delete side function
    def deleteSQL(self, website, username):
        connection = mysql.connector.connect(
            user="root",
            password="in020121",
            database="passwords"
        )
        cursor = connection.cursor()
        cursor.execute("DELETE FROM user_data WHERE website LIKE %s AND username LIKE %s", ('%' + website + '%', '%' + username + '%'))
        connection.close()
        connection.commit()

root = Tk()
root.title("WebKey Manager")
root.configure(background="#323231")
root.geometry("600x400")
app = DatabasePM(root)
root.mainloop()
