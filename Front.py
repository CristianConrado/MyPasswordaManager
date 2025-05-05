import tkinter as tk
import ctypes
import tkinter.messagebox as messagebox
lib = ctypes.CDLL("./database.so")
lib.wrapping_checkSite.restype = ctypes.py_object

def create_password_manager_main_window():
    main = tk.Tk() #Main window
    main.title("Password Manager")
    main.geometry("300x200")  # Set the window size
    main.resizable(True,True)
    main.configure(bg="lightblue")  # Set the background color
    main.configure(padx=20, pady=20) 
    res =lib.connect_to_database() # Connect to the database

    tk.Label(main, text="Password Manager",background="lightblue").grid(row=0, column=1,) # Title label

    tk.Label(main, text="Username",background="lightblue").grid(row=1, column=0)  # Username label
    user = tk.Entry(main)
    user.grid(row=1, column=1)

    tk.Label(main, text="Password",background="lightblue").grid(row=2, column=0)  # Password label
    pw = tk.Entry(main, show="*")
    pw.grid(row=2, column=1)

    tk.Button(main, text="Login", command=lambda: create_password_manager_loggedIn_window(main,user.get(),pw.get())).grid(row=3, column=1)  # Login button
    tk.Button(main, text="Sign Up", command=lambda:create_password_manager_Sign_Up_window(main)).grid(row=3, column=0)  # Login button
    

    main.mainloop()

def create_password_manager_Sign_Up_window(main):
    main.destroy() # Destroy the main window
    signUp = tk.Tk() #signUp window
    signUp.title("Sign Up")
    signUp.geometry("300x200")  # Set the window size
    signUp.resizable(True,True)
    signUp.configure(bg="lightblue")  # Set the background color
    signUp.configure(padx=20, pady=20) 

    tk.Label(signUp, text="Enter your user",background="lightblue").grid(row=0, column=1,) # Title label

    tk.Label(signUp, text="Username",background="lightblue").grid(row=1, column=0)  # Username label
    user = tk.Entry(signUp)
    user.grid(row=1, column=1)
    #TODO: Check if the username is already in the file

    tk.Label(signUp, text="Password",background="lightblue").grid(row=2, column=0)  # Password label
    pw = tk.Entry(signUp, show="*")
    pw.grid(row=2, column=1)

    
    tk.Button(signUp, text="Sign Up", command=lambda: signUp_user(signUp,user.get(),pw.get())).grid(row=3, column=1)  # Login button

    signUp.mainloop()

def signUp_user(main,user, pw):
    if(lib.checkUser(user.encode('utf-8'), pw.encode('utf-8'))): # Check if the user is in the database ENCODE TO SEND TO C
        messagebox.showerror("Error", "User already exists")
        return
    print(user,pw)
    lib.addUser(user.encode('utf-8'), pw.encode('utf-8')) # Add the user to the database ENCODE TO SEND TO C

    create_password_manager_loggedIn_window(main, user, pw) # Create the logged in window


def create_password_manager_loggedIn_window(main, user, pw):
    res = lib.checkUser(user.encode('utf-8'), pw.encode('utf-8'))
    if(not res): # Check if the user is in the database ENCODE TO SEND TO C
        messagebox.showerror("Error", "Invalid username or password")
        return
    
    main.destroy() # Destroy the main window
    LoggedIn = tk.Tk() #signUp window
    LoggedIn.title("Password Manager")
    LoggedIn.geometry("300x200")  # Set the window size
    LoggedIn.resizable(True,True)
    LoggedIn.configure(bg="lightblue")  # Set the background color
    LoggedIn.configure(padx=20, pady=20)

    tk.Button(LoggedIn, text="Check", command=lambda:create_password_manager_checkPassword_window(LoggedIn,res)).grid(padx= 100) 
    tk.Button(LoggedIn, text="Create", command=lambda:create_password_manager_createPassword_window(LoggedIn)).grid(pady= 30) 

    LoggedIn.mainloop()

def create_password_manager_createPassword_window(main):
    main.destroy() # Destroy the main window
    create = tk.Tk() #signUp window
    create.title("New Password")
    create.geometry("300x200")  # Set the window size
    create.resizable(True,True)
    create.configure(bg="lightblue")  # Set the background color
    create.configure(padx=20, pady=20)

    tk.Label(create, bg= "lightblue",text="Site:").grid(row=1, column=0)
    site = tk.Entry(create)
    site.grid(row=1, column=1)
    tk.Button(create, text="Create", command=lambda: read_entry_text(site)).grid(column = 1, row=2)  # Check button TODO: Check if the website is already in the file
    #TODO: Save the password to a file
    create.mainloop()

def create_password_manager_checkPassword_window(main,id):
    print(id)
    main.destroy() # Destroy the main window
    check = tk.Tk() #signUp window
    check.title("Look for Password")
    check.geometry("300x200")  # Set the window size
    check.resizable(True,True)
    check.configure(bg="lightblue")  # Set the background color
    check.configure(padx=20, pady=20)

    tk.Label(check, bg= "lightblue",text="Site:").grid(row=1, column=0)
    site = tk.Entry(check)
    site.grid(row=1, column=1)
    tk.Button(check, text="Check", command=lambda:create_password_manager_writePassword_window(main,site.get(),id)).grid(column = 1, row=2)  # Check button TODO: Check if the website is already in the file
    #TODO: show the password from the file
    check.mainloop()

def read_entry_text(entry):
    return entry.get()

def create_password_manager_writePassword_window(main, site, id):  # Output the password FROM the database
    if site == "":
        messagebox.showerror("Error", "Please enter a site")
        return
    password = lib.wrapping_checkSite(site.encode('utf-8'), str(id).encode('utf-8'))
    if password == b' ' :  # Check if the site is in the database
        messagebox.showerror("Error", "No password found for this site")
        return
    # Create a new window to display the password
    write = tk.Tk()
    write.title("Password")
    write.geometry("300x200")  # Set the window size
    write.resizable(True, True)
    write.configure(bg="lightblue")  # Set the background color
    write.configure(padx=20, pady=20)
    tk.Label(write, bg="lightblue", text="Site:").grid(row=1, column=0)
    tk.Label(write, bg="lightblue", text=site).grid(row=1, column=1)  # Display the site
    tk.Label(write, bg="lightblue", text="Password:").grid(row=2, column=0)
    tk.Label(write, bg="lightblue", text=password).grid(row=2, column=1)  # Display the password


    write.mainloop()

if __name__ == "__main__":
    create_password_manager_main_window()
