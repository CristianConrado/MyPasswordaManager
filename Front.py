import tkinter as tk
import ctypes
import tkinter.messagebox as messagebox
lib = ctypes.CDLL("./database.so")
lib.wrapping_checkSite.restype = ctypes.py_object
lib2 = ctypes.CDLL("./libpasswordcreator.so")
import tkinter as tk

def setUpWindow(main):
    pantalla_ancho = main.winfo_screenwidth()
    pantalla_alto = main.winfo_screenheight()

    x = (pantalla_ancho // 2) - (800 // 2)
    y = (pantalla_alto // 2) - (600 // 2)
    main.geometry(f"{800}x{600}+{x}+{y}")
    main.configure(bg='#7395AE', padx=20, pady=20)

    # Configure grid weights to center widgets
    main.grid_columnconfigure(0, weight=1)
    main.grid_columnconfigure(1, weight=1)
    main.grid_columnconfigure(2, weight=1)
    main.resizable(0, 0)



def create_password_manager_main_window():
    main = tk.Tk()  # Main window
    main.title("Password Manager")
    setUpWindow(main)

    # Title label
    title = tk.Label(main, text="Password Manager", font=("TimesNewRoman", 24), bg='#7395AE', fg='#303C6C')
    title.grid(row=0, column=0, columnspan=3, pady=(20, 40), sticky="n")

    # Username
    tk.Label(main, text="Username", bg='#7395AE',fg='#303C6C', font="TimesNewRoman").grid(row=2, column=1, sticky="w", padx=5, pady=5)
    user = tk.Entry(main, border=0,fg='#303C6C', font="TimesNewRoman")
    user.grid(row=2, column=1, padx=5, pady=5)

    # Password
    tk.Label(main, text="Password", bg='#7395AE',fg='#303C6C', font="TimesNewRoman").grid(row=4, column=1, sticky="w", padx=5, pady=5)
    pw = tk.Entry(main, show="*",border=0,fg='#303C6C', font="TimesNewRoman")
    pw.grid(row=4, column=1, padx=5, pady=5)

    # Buttons
    tk.Button(main, text="Login", command=lambda: create_password_manager_loggedIn_window(main, user.get(), pw.get()), fg="white",border=0, font="TimesNewRoman", bg= '#4D6D9A', relief="sunken").grid(row=5, column=1, pady=(20, 5))
    tk.Button(main, text="Sign Up", command=lambda: create_password_manager_Sign_Up_window(main), fg="white",border=0, font="TimesNewRoman", bg= '#4D6D9A', relief="sunken").grid(row=6, column=1, pady=5)

    main.mainloop()


def create_password_manager_Sign_Up_window(main):
    main.destroy()
    signUp = tk.Tk()
    signUp.title("Sign Up")
    setUpWindow(signUp)

    tk.Label(signUp, text="Create a New Account", font=("TimesNewRoman", 16), bg='#7395AE').grid(row=0, column=0, columnspan=3, pady=(10, 20))

    tk.Label(signUp, text="Username:", bg='#7395AE',fg='#303C6C', font="TimesNewRoman").grid(row=2, column=1, sticky="w")
    user = tk.Entry(signUp,border=0,fg='#303C6C', font="TimesNewRoman")
    user.grid(row=2, column=1, pady=(0, 10))

    tk.Label(signUp, text="Password:", bg='#7395AE',fg='#303C6C', font="TimesNewRoman").grid(row=4, column=1, sticky="w")
    pw = tk.Entry(signUp, show="*",border=0,fg='#303C6C', font="TimesNewRoman")
    pw.grid(row=4, column=1, pady=(0, 20))

    tk.Button(signUp, text="Sign Up", command=lambda: signUp_user(signUp, user.get(), pw.get()), fg="white",border=0, font="TimesNewRoman", bg= '#4D6D9A', relief="sunken").grid(row=5, column=1)

    signUp.mainloop()

def signUp_user(main, user, pw):
    if lib.checkUser(user.encode('utf-8'), pw.encode('utf-8')):
        messagebox.showerror("Error", "User already exists")
        return
    lib.addUser(user.encode('utf-8'), pw.encode('utf-8'))
    create_password_manager_loggedIn_window(main, user, pw)

def create_password_manager_loggedIn_window(main, user, pw):
    res = lib.checkUser(user.encode('utf-8'), pw.encode('utf-8'))
    if not res:
        messagebox.showerror("Error", "Invalid username or password")
        return

    main.destroy()
    LoggedIn = tk.Tk()
    setUpWindow(LoggedIn)
    tk.Label(LoggedIn, text="Welcome " + user+"!").grid(row=0, column=0, columnspan=3, pady=(10, 30))

    tk.Button(LoggedIn, text="Check Password", width=20, command=lambda: create_password_manager_checkPassword_window(LoggedIn, res,user,pw), fg="white",border="0", font="TimesNewRoman", bg= '#4D6D9A', relief="sunken").grid(row=1, column=1, pady=10)
    tk.Button(LoggedIn, text="Create Password", width=20, command=lambda: create_password_manager_createPassword_window(LoggedIn,res,user,pw), fg="white",border="0", font="TimesNewRoman", bg= '#4D6D9A', relief="sunken").grid(row=2, column=1, pady=10)

    LoggedIn.mainloop()

def create_password_manager_createPassword_window(main,id,user,pw):
    main.destroy()
    create = tk.Tk()
    create.title("Create New Password")
    setUpWindow(create)
    tk.Button(create, text="Back", command=lambda: create_password_manager_loggedIn_window(create,user,pw), fg="white",border="0", font="TimesNewRoman", bg= '#4D6D9A', relief="sunken").grid(row=0, column=0)
    tk.Label(create, text="New Site:",bg='#7395AE',fg='#303C6C', font="TimesNewRoman").grid(row=1, column=1, sticky="w")
    site = tk.Entry(create,border=0,fg='#303C6C', font="TimesNewRoman")
    site.grid(row=1, column=1)

    tk.Button(create, text="Create", command=lambda: site.get(), fg="white",border="0", font="TimesNewRoman", bg= '#4D6D9A', relief="sunken").grid(row=2, column=1,pady=20)

    create.mainloop()

def create_password_manager_checkPassword_window(main, id,user,pw):
    main.destroy()
    
    check = tk.Tk()
    check.title("Look Up Password")
    tk.Button(check, text="Back", command=lambda: create_password_manager_loggedIn_window(check,user,pw), fg="white",border="0", font="TimesNewRoman", bg= '#4D6D9A', relief="sunken").grid(row=0, column=0)
    setUpWindow(check)
    check.grid_rowconfigure(0, weight=1)  # Top spacer
    check.grid_rowconfigure(3, weight=1)  # Bottom spacer
    tk.Label(check, text="Enter Site:",bg='#7395AE',fg='#303C6C', font="TimesNewRoman").grid(row=0, column=1, sticky="w")
    site = tk.Entry(check,border=0,fg='#303C6C', font="TimesNewRoman", width=15)
    site.grid(row=0, column=1)
    
    tk.Button(check, text="Check", command=lambda: create_password_manager_writePassword_window(check, site.get(), id,user,pw), fg="white",border="0", font="TimesNewRoman", bg= '#4D6D9A', relief="sunken").grid(row=1, column=1,pady=20)

    check.mainloop()


def create_password_manager_writePassword_window(main, site, id,user,pw):
    if site == "":
        messagebox.showerror("Error", "Please enter a site")
        return
    password = lib.wrapping_checkSite(site.encode('utf-8'), str(id).encode('utf-8'))
    if password == "":
        messagebox.showerror("Error", "No password found for this site")
        return

    main.destroy()
    write = tk.Tk()
    write.title("Your Password")
    setUpWindow(write)
    tk.Button(write, text="Back", command=lambda: create_password_manager_checkPassword_window(write,id,user,pw), fg="white",border="0", font="TimesNewRoman", bg= '#4D6D9A', relief="sunken").grid(row=0, column=0)
    write.grid_rowconfigure(0, weight=1)  # Top spacer
    write.grid_rowconfigure(3, weight=1)  # Bottom spacer

    tk.Label(write, text="Site:", bg='#7395AE',fg='#303C6C', font=("TimesNewRoman",16)).grid(row=0, column=0, sticky="e")
    tk.Label(write, text=site, bg='#7395AE',fg='#303C6C', font=("TimesNewRoman",16)).grid(row=0, column=1, sticky="w")

    tk.Label(write, text="Password:", bg='#7395AE',fg='#303C6C', font=("TimesNewRoman",16)).grid(row=1, column=0, sticky="e")
    tk.Label(write, text=" "+password, bg='#7395AE',fg='#303C6C', font=("TimesNewRoman",16)).grid(row=1, column=1, sticky="w")
   

    write.mainloop()


def create_password_manager_CreatePassword(site, id):
    lib.createPasswordPy(site,id)
    tk.messagebox.showinfo("Success", "Password created successfully")

if __name__ == "__main__":
    create_password_manager_main_window()
