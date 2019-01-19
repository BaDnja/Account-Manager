try:
    # Python 3
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
except ImportError:
    # Python 2
    import Tkinter as tk
    from Tkinter import ttk

from config import Page
import manage
import database
import sqlite3
import random


class FirstView(Page):


    # TODO: Logic of the page

    def loginUser(self):

        username = False
        password = False

        with open('files/user.txt') as myfile:
            if 'Demo' in myfile.read():
                if 'Demo' == self.usernameValue.get():
                    username = True
                else:
                    username = False

        with open('files/user.txt') as myfile:
            if 'demo123' in myfile.read():
                if 'demo123' == self.passwordValue.get():
                    password = True
                else:
                    password = False
        
        if (username == True) and (password == True):
            main = MainView()
            main.show()
        elif len(self.usernameValue.get()) == 0 or len(self.passwordValue.get()) == 0:
            messagebox.showerror("Error", "Fields can't be empty!")
        else:
            messagebox.showerror("Error", "Username or password are incorrect!")
    
    def gotoAboutPage(self):
        aboutPage = AboutApp()

        aboutPage.show()


    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # TODO: UI of the page

        # ------------ Label -------------
        nameLabel = tk.Label(root, text="Name:")
        nameLabel.grid(row=0, column=0, padx=3, pady=5)

        pwLabel = tk.Label(root, text="Password:")
        pwLabel.grid(row=1, column=0, padx=3, pady=5)

        gotoLabel = tk.Label(root, text="How to use? ↓")
        gotoLabel.grid(row=3, column=1, padx=3, pady=5)


        # ------------ Inputs ------------
        self.usernameValue = tk.StringVar(root, value="")
        self.usernameEntry = ttk.Entry(root,
                                    textvariable=self.usernameValue)
        self.usernameEntry.grid(row=0, column=1, padx=3, pady=5)

        self.passwordValue = tk.StringVar(root, value="")
        self.passwordEntry = ttk.Entry(root,
                                    textvariable=self.passwordValue)
        self.passwordEntry.grid(row=1, column=1, padx=3, pady=5)
        # ------------ Buttons -----------
        self.loginButton = ttk.Button(root,
                                        text="Log in",
                                        command=lambda: self.loginUser())

        self.loginButton.grid(row=2, column=1, padx=3, pady=5)

        self.gotoButton = ttk.Button(root,
                                        text="About App",
                                        command=lambda: self.gotoAboutPage())

        self.gotoButton.grid(row=4, column=1, padx=3, pady=5)


class MainView(Page):
    #Class Fields
    db_conn = 0
    cursor = 0
    current_user = 0

    def submitAccount(self):
        #Insert account in the db
        self.db_conn = sqlite3.connect("files/usersDatabase.db")
        self.cursor = self.db_conn.cursor()
        self.db_conn.execute("INSERT INTO Users (Name, Username, Email, Password) " +
                            "VALUES ('" +
                            self.name_entry_value.get() + "', '" +
                            self.username_entry_value.get() + "', '" +
                            self.email_entry_value.get() + "', '" +
                            self.password_entry_value.get() + "')")
        self.db_conn.commit()

        #messagebox.showinfo("Info", "Account added successfully!")

        #Clear entry boxes
        self.name_entry.delete(0,"end")
        self.username_entry.delete(0,"end")
        self.email_entry.delete(0,"end")
        self.password_entry.delete(0,"end")

        #Update list box with account list
        self.updateListbox()


    def updateListbox(self):
        #Delete items in the list box
        self.listboxNames.delete(0, "end")

        #Get users from the db
        try:
            self.db_conn = sqlite3.connect("files/usersDatabase.db")
            self.cursor = self.db_conn.cursor()
            result = self.cursor.execute("SELECT ID, Name, Username, Email, Password FROM Users")

            # Receive a list of lists that hold the result
            for row in result:
                user_id = row[0]
                user_Name = row[1]
                user_Username = row[2]
                user_email = row[3]
                user_password = row[4]

                # Put the student in the list box
                self.listboxNames.insert(user_id,
                                     user_Name + " " +
                                     user_Username + " " +
                                     user_email + " " +
                                     user_password)

        except sqlite3.OperationalError:
            #print("The Table Doesn't Exist")
            messagebox.showerror("Error!", "Data doesn't exist!")

        except:
            #print("1: Couldn't Retrieve Data From Database")
            messagebox.showerror("Error!", "Couldn't Retrieve Data From Database.")

        #Clear entry boxes
        self.name_entry.delete(0,"end")
        self.username_entry.delete(0,"end")
        self.email_entry.delete(0,"end")
        self.password_entry.delete(0,"end")

    def loadAccount(self, event=None):

        # Get index selected which is the student ID
        lb_widget = event.widget
        index = str(lb_widget.curselection()[0] + 1)

        # Store the current student index
        self.current_user = index

        # Retrieve student list from the db
        try:
            result = self.cursor.execute("SELECT ID, Name, Username, Email, Password FROM Users WHERE ID=" + index)

            # Receive a list of lists that hold the result
            for row in result:
                user_id = row[0]
                user_Name = row[1]
                user_Username = row[2]
                user_email = row[3]
                user_password = row[4]

                # Set the values in the entries
                self.name_entry_value.set(user_Name)
                self.username_entry_value.set(user_Username)
                self.email_entry_value.set(user_email)
                self.password_entry_value.set(user_password)

        except sqlite3.OperationalError:
            print("The Table Doesn't Exist")

        except:
            print("2 : Couldn't Retrieve Data From Database")

    # Update user info
    def updateAccount(self):

        #Update account records with change made in entry
        try:
            self.db_conn = sqlite3.connect("files/usersDatabase.db")
            self.cursor = self.db_conn.cursor()
            self.db_conn.execute("UPDATE Users SET Name='" +
                                 self.name_entry_value.get() +
                                 "', Username='" +
                                 self.username_entry_value.get() +
                                 "', Email='" +
                                 self.email_entry_value.get() +
                                 "', Password='" +
                                 self.password_entry_value.get() +
                                 "' WHERE ID=" +
                                 self.current_user)
            self.db_conn.commit()
            #messagebox.showinfo("Info", "Account updated successfully!")

        except sqlite3.OperationalError:
            #print("Database couldn't be Updated")
            messagebox.showerror("Error!", "Database couldn't be Updated")
        
        except TypeError:
            messagebox.showerror("Error!", "Load user, make changes\n and then update it.")

        # Clear the entry boxes
        self.name_entry.delete(0, "end")
        self.username_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.password_entry.delete(0, "end")

        # Update list box with account list
        self.updateListbox()

    def deleteAccount(self):
        try:
            # Get index selected which is the student ID
            index = str(self.listboxNames.curselection()[0] + 1)

            self.db_conn.execute("DELETE FROM Users WHERE ID=" + index)
            self.db_conn.commit()
            
            #Clear entry boxes
            self.name_entry.delete(0, "end")
            self.username_entry.delete(0, "end")
            self.email_entry.delete(0, "end")
            self.password_entry.delete(0, "end")

            # Update list box with user list
            self.updateListbox()
            #messagebox.showinfo("Info", "Account deleted successfully!")
        except IndexError:
            messagebox.showerror("Error!", "Please choose account!")


    def generatePassword(self):
        generate = Password()
        generate.lift()

    def exportToCsv(self):


        data = self.cursor.execute("SELECT * FROM Users")

        with open("files/csv data.csv", "w") as write_file:
            for row in data:
                write_file.write(str(row))
                write_file.write("\n")


    def __init__(self):

       root = tk.Tk()

       # -------------- Window placement --------
       width = 530 # width for the window
       height = 280 # height for the window

       # get screen width and height
       screenWidth = root.winfo_screenwidth()
       screenHeight = root.winfo_screenheight()

       # calculate x and y coordinates for the window
       x = (screenWidth/2) - (width/2)
       y = (screenHeight/2) - (height/2)

       # set dimensions and where it is placed
       root.geometry('%dx%d+%d+%d' % (width, height, x, y))
       root.resizable(width=False, height=False)
       # ----------------------------------------------------

        # TODO: UI of the window

       # --- 1st Row Name ---
       name_label = tk.Label(root, text="Name (e.g. Facebook)")
       name_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')
       
       self.name_entry_value = tk.StringVar(root, value="")
       self.name_entry = ttk.Entry(root,
                                  textvariable=self.name_entry_value)
       self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky='W')

       # --- 1st Row Username ---
       username_label = tk.Label(root, text="Username")
       username_label.grid(row=0, column=2, padx=10, pady=10, sticky='W')
       
       self.username_entry_value = tk.StringVar(root, value="")
       self.username_entry = ttk.Entry(root,
                                  textvariable=self.username_entry_value)

       self.username_entry.grid(row=0, column=3, padx=10, pady=10, sticky='W')

        # --- 2nd Row Email ---
       email_label = tk.Label(root, text="Email")
       email_label.grid(row=1, column=0, padx=10, pady=10, sticky='W')

       self.email_entry_value = tk.StringVar(root, value="")
       self.email_entry = ttk.Entry(root,
                                  textvariable=self.email_entry_value)

       self.email_entry.grid(row=1, column=1, padx=10, pady=10, sticky='W')

        # --- 2nd Row Password ---
       password_label = tk.Label(root, text="Password")
       password_label.grid(row=1, column=2, padx=10, pady=10, sticky='W')

       self.password_entry_value = tk.StringVar(root, value="")
       self.password_entry = ttk.Entry(root,
                                     textvariable=self.password_entry_value)

       self.password_entry.grid(row=1, column=3, padx=10, pady=10, sticky='W')

       # --- Listboxes ---
       self.listboxNames = tk.Listbox(root)
       self.listboxNames.bind('<<ListboxSelect>>', self.loadAccount)

       self.listboxNames.grid(row=2, column=0, columnspan=2,
                           padx=10, pady=10, sticky='W'+'E')
    
       #submit
       self.submitButton = ttk.Button(root,
                                        text="Submit Account",
                                        command=lambda: self.submitAccount())

       self.submitButton.grid(row=2, column=2, sticky='N')

       #update
       self.updateButton = ttk.Button(root,
                                        text="Update Account",
                                        command=lambda: self.updateAccount())

       self.updateButton.grid(row=2, column=2, padx=2, pady=2)

       #delete
       self.deleteButton = ttk.Button(root,
                                        text="Delete Account",
                                        command=lambda: self.deleteAccount())

       self.deleteButton.grid(row=2, column=2, sticky='S')

       # Generate password
       self.generatePW = ttk.Button(root,
                                        text="Generate Password",
                                        command=lambda: self.generatePassword())

       self.generatePW.grid(row=2, column=3, sticky='N')

        # Refresh Data
       self.refreshButton = ttk.Button(root,
                                        text="Refresh List",
                                        command=lambda: self.updateListbox())
       self.refreshButton.grid(row=2, column=3, padx=2, pady=2)

       # Export to CSV button
       self.export_button = ttk.Button(root,
                                        text="Export to CSV file",
                                        command=lambda: self.exportToCsv())
       self.export_button.grid(row=2, column=3, sticky='S')
    
       self.updateListbox()

class AboutApp(Page):
    # ---- UI ----
    def __init__(self, *args, **kwargs):
        root = tk.Tk()
        
        # -------------- Window placement --------
        width = 1000 # width of the window
        height = 1000 # heigth of the window

        # get screen width and height
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()

        # calculate x and y coordinates of the window
        x = (screenWidth/2) - (width/2)
        y = (screenHeight/2) - (height/2)

        # dimensions and placement
        root.geometry('%dx%d+%d+%d' % (width, height, x, y))
        root.resizable(width=False, height=False)
        # ----------------------------------------------------

        root.title(string="About App")
        

        loginLabel = tk.Label(root, text="\n--LOG IN PAGE--\n")
        loginLabel.config(font=("Roboto", 20))
        loginLabel.pack()

        log1Label = tk.Label(root, text="| Username: Demo | Password: demo123 |")
        log1Label.config(font=("Lora", 13))
        log1Label.pack()

        main1Label = tk.Label(root, text="\n--MAIN PAGE--\n")
        main1Label.config(font=("Lora", 20))
        main1Label.pack()

        main11Label = tk.Label(root, text= "|Adding account|\nProvide entries with data and click 'Submit' button")
        main11Label.config(font=("Lora", 13))
        main11Label.pack()

        main2Label = tk.Label(root, text="\n|Updating account|\nClicking on account in a list will load entries with data, make changes and click 'Update' button" )
        main2Label.config(font=("Lora", 13))
        main2Label.pack()

        main3Label = tk.Label(root, text="\n|Deleting account|\nClicking on account in a list will load entries with data, click 'Delete' button" )
        main3Label.config(font=("Lora", 13))
        main3Label.pack()

        main4Label = tk.Label(root, text="\n|Refresh|\nClicking on 'Refresh' button will clear entries and update list with accounts" )
        main4Label.config(font=("Lora", 13))
        main4Label.pack()

        main5Label = tk.Label(root, text="\n|Export accounts|\nClicking on 'Export' button will save all accounts to CSV file which can be also opened as a txt file" )
        main5Label.config(font=("Lora", 13))
        main5Label.pack()

        main6Label = tk.Label(root, text="\n|Generating Random Password|\nClicking on 'Generate Password' button will open a new window which is explained below" )
        main6Label.config(font=("Lora", 13))
        main6Label.pack()

        gen1Label = tk.Label(root, text="\n--GENERATE PASSWORD PAGE--\n" )
        gen1Label.config(font=("Roboto", 20))
        gen1Label.pack()

        gen11Label = tk.Label(root, text="|Choosing Password Strength|\nStrength types: Weak, Medium, Strong, Ultimate")
        gen11Label.config(font=("Lora", 13))
        gen11Label.pack()
        
        gen2Label = tk.Label(root, text="\n||Weak Password||\nLength: 1-10; Including: Lowecase Letters, Uppercase Letters and Digits" )
        gen2Label.config(font=("Lora", 10))
        gen2Label.pack()

        gen3Label = tk.Label(root, text="\n||Medium Password||\nLength: 11-20; Including: Lowecase Letters, Uppercase Letters, Digits and Symbols" )
        gen3Label.config(font=("Lora", 10))
        gen3Label.pack()

        gen4Label = tk.Label(root, text="\n||Strong Password||\nLength: 21-40; Including: Lowecase Letters, Uppercase Letters, Digits, Symbols and Ambiguous Characters" )
        gen4Label.config(font=("Lora", 10))
        gen4Label.pack()

        gen5Label = tk.Label(root, text="\n||Ultimate Password||\nLength: 41-80; Including: Same as 'Strong Password'" )
        gen5Label.config(font=("Lora", 10))
        gen5Label.pack()

        root.mainloop()

class Password(Page):

    def generate(self, length, data, pw=""):
        for i in range(int(length)):
            if str(i) not in pw:
                pw += random.choice(data)

            #Set it to password entry value
            self.passwordValue.set(pw)

    def passwordCallback(self):
        ''' Get value from drop menu and generate password for that option'''
        symbols = ['@', '#', '$', '&', '*', '_', '-', ':', ';', ',', '.', '?', '/', '!', '%', '+', '|']
        lowercaseLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        uppercaseLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        ambiguousCharacters = ['{', '}', '[', ']', '<', '>', '(', ')']

        passwordData = []
        password = ""
        passwordValue = self.variable.get()
        passwordLength = 0

        if passwordValue == "Weak":
            passwordLength = random.randint(5, 11)
            passwordData.extend(lowercaseLetters + uppercaseLetters + digits)
            self.generate(passwordLength, passwordData, password)
        elif passwordValue == "Medium":
            passwordLength = random.randint(11, 21)
            passwordData.extend(lowercaseLetters + uppercaseLetters + digits + symbols)
            self.generate(passwordLength, passwordData, password)
        elif passwordValue == "Strong":
            passwordLength = random.randint(21, 41)
            passwordData.extend(lowercaseLetters + uppercaseLetters + digits + symbols + ambiguousCharacters)
            self.generate(passwordLength, passwordData, password)
        elif passwordValue == "Ultimate":
            passwordLength = random.randint(41, 81)
            passwordData.extend(lowercaseLetters + uppercaseLetters + digits + symbols + ambiguousCharacters)
            self.generate(passwordLength, passwordData, password)
        else:
            messagebox.showerror("Error!", "No password strength choosen!")

    def __init__(self, *args, **kwargs):

        root = tk.Tk()

        # Labels
        pwLabel = tk.Label(root, text="Your password:")
        pwLabel.grid(row=0, column=0, padx=3, pady=3, sticky="E")

        pwstrengthLabel = tk.Label(root, text="Choose Password Strenght:")
        pwstrengthLabel.grid(row=1, column=0, padx=3, pady=3, sticky="E")

        cpLabel = tk.Label(root, text="Copy and Paste Your Password,\nthen close this window.")
        cpLabel.grid(row=2, column=0, padx=3, pady=3, sticky="E")

        # Entry
        self.passwordValue = tk.StringVar(root, value="")
        self.passwordEntry = ttk.Entry(root,
                                    textvariable=self.passwordValue)
        self.passwordEntry.grid(row=0, column=1, padx=3, pady=3)

        # Menu
        values = ["Weak", "Medium", "Strong", "Ultimate"]
        self.variable = tk.StringVar(root)
        self.variable.set("Weak") # default value

        menu = tk.OptionMenu(root, self.variable, *values)
        menu.grid(row=1, column=1, padx=3, pady=3)
        
        # Button
        self.generateButon = ttk.Button(root,
                                        text="Generate Password",
                                        command=lambda: self.passwordCallback())
        self.generateButon.grid(row=2, column=1, padx=3, pady=3)
        
        root.title(string="Password Generator")
        root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    main = FirstView(root)
    root.title(string="Account Manager")
    
    # --------------- Window placement -------------
    width = 200 # width for the window
    height = 200 # height for the window

    # get screen width and height
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()

    # calculate x and y coordinates for the window
    x = (screenWidth/2) - (width/2)
    y = (screenHeight/2) - (height/2)

    # set dimensions and where it is placed
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    root.resizable(width=False, height=False)
    # --------------------------------------------

    # -------- Managing files ---------
    manage.makeFilesPath()
    manage.txtFile()
    database.setupDatabase()

    root.mainloop()