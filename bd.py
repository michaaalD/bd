import tkinter as tk
import mysql.connector
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

def print_members(main_menu):
    try:
        # Destroy the main menu window
        main_menu.withdraw()

        my_w = tk.Toplevel()
        my_w.title("Lista Członków")

        # Set your database access credentials
        db_config = {
            "host": "localhost",
            "user": "admin",
            "password": "password",
            "database": "klubdb",
        }
        # Establish a connection to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Create frames for the Treeview and Checkbuttons
        frame = tk.Frame(my_w)
        frame.grid(row=1, column=1, padx=20, pady=20)

        trv_frame = tk.Frame(frame)
        trv_frame.grid(row=0, column=1)

        chk_frame = tk.Frame(frame)
        chk_frame.grid(row=0, column=0)

        trv = ttk.Treeview(trv_frame, selectmode='browse')
        trv.pack()

        # number of columns
        trv["columns"] = ("1", "2", "3", "4", "5", "6", "7")

        # Defining heading
        trv['show'] = 'headings'

        # width of columns and alignment
        trv.column("1", width=30, anchor='c')
        trv.column("2", width=80, anchor='c')
        trv.column("3", width=80, anchor='c')
        trv.column("4", width=80, anchor='c')
        trv.column("5", width=80, anchor='c')
        trv.column("6", width=80, anchor='c')
        trv.column("7", width=80, anchor='c')
        # Headings
        # respective columns
        trv.heading("1", text="id")
        trv.heading("2", text="login")
        trv.heading("3", text="Imie")
        trv.heading("4", text="Nazwisko")
        trv.heading("5", text="Data Urodzenia")
        trv.heading("6", text="Haslo")
        trv.heading("7", text="Rola czlonka")

        cursor.execute("SELECT * from czlonek_klubu")
        r_set = cursor.fetchall()  # Pobierz wszystkie rekordy jako listę

        # Dictionary to hold the Checkbutton states
        checkboxes = {}

        def handle_delete():
            to_delete = [key for key, var in checkboxes.items() if var.get()]
            if to_delete:
                for member_id in to_delete:
                    cursor.execute("UPDATE czlonek_klubu SET czy_aktywny = 0 WHERE ID_czlonekklubu = %s", (member_id,))
                conn.commit()
                # Refresh the window
                my_w.destroy()
                print_members(main_menu)

        row_count = 0  # Starting row for checkbuttons
        for dt in r_set:
            checkbox_var = tk.BooleanVar()
            checkboxes[dt[0]] = checkbox_var
            trv.insert("", 'end', iid=dt[0], text=dt[0],
                       values=(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], dt[6]))
            chk = tk.Checkbutton(chk_frame, variable=checkbox_var)
            chk.grid(row=row_count, column=0, sticky='w')
            row_count += 1

        add_user_button1 = tk.Button(my_w, text="Add User", command=lambda: adding_member(my_w))
        add_user_button1.grid(row=2, column=1, padx=20, pady=20)

        delete_user_button = tk.Button(my_w, text="Delete Selected Users", command=handle_delete)
        delete_user_button.grid(row=3, column=1, padx=20, pady=20)

        # Cancel button
        cancel_button = tk.Button(my_w, text="Powrot do menu glównego",
                                  command=lambda: show_main_menu_coach(my_w))
        cancel_button.grid(row=4, column=1, padx=20, pady=20)

        my_w.mainloop()

        # Zamknięcie połączenia
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")


def adding_boat(window):
    # Database configuration
    db_config = {
        "host": "localhost",
        "user": "admin",
        "password": "password",
        "database": "klubdb",
    }

    # Establish a connection to the database
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

    def add_boat():
        nazwa_lodzi = name_entry.get()
        ilosc_miejsc = seats_entry.get()
        czy_sportowa = Checkbutton1.get()

        if not nazwa_lodzi or not ilosc_miejsc.isdigit():
            print("Invalid input. Please provide correct details.")
            return

        query = "INSERT INTO lodz (Nazwa_lodzi, Ilosc_miejsc, StausLodzi, Czy_sportowa, Liczba_usterek) VALUES (%s, %s, %s, %s, 0)"
        val = (nazwa_lodzi, ilosc_miejsc, 'wolna', czy_sportowa)

        try:
            cursor.execute(query, val)
            conn.commit()
            print("Rekord dodany poprawnie!")
        except mysql.connector.Error as err:
            print(f"Błąd przy dodawaniu rekordu: {err}")

    window.withdraw()
    # Create the main window
    root = tk.Toplevel()
    root.title("Okno dodawania nowej łodzi")

    # Center the window on the screen
    window_width = 400
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Name entry
    name_label = tk.Label(root, text="Nazwa łodzi:")
    name_label.pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    # Seats entry
    seats_label = tk.Label(root, text="Ilość miejsc:")
    seats_label.pack()
    seats_entry = tk.Entry(root)
    seats_entry.pack()

    # Checkbutton for sport boat
    Checkbutton1 = IntVar()
    sport_checkbutton = Checkbutton(root, text="Czy sportowa?", variable=Checkbutton1, onvalue=1, offvalue=0, height=2, width=20)
    sport_checkbutton.pack()

    # Accept button
    accept_button = tk.Button(root, text="Dodaj", command=add_boat)
    accept_button.pack()

    # Return to main menu button
    return_button = tk.Button(root, text="Powrót do menu głównego",
                              command=lambda: [show_main_menu_coach(root)])
    return_button.pack()

    # Cancel button
    cancel_button = tk.Button(root, text="Anuluj", command=lambda: print_boats(root))
    cancel_button.pack()

    root.mainloop()

    # Close the connection when done
    cursor.close()
    conn.close()


def adding_member(window):
    # Database configuration
    db_config = {
        "host": "localhost",
        "user": "admin",
        "password": "password",
        "database": "klubdb",
    }

    # Establish a connection to the database
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit()

    def add_member():
        imie = name_entry.get()
        nazwisko = surname_entry.get()
        login = login_entry.get()
        haslo = haslo_entry.get()
        birthday = birthday_entry.get()
        # czy_zawodnik = Checkbutton1.get()
        # czy_trener = Checkbutton2.get()

        if not imie or not birthday:
            print("Invalid input. Please provide correct details.")
            return

        query = "INSERT INTO czlonek_klubu (Imie, Nazwisko, Login, Haslo, Data_urodzenia) VALUES (%s, %s, %s, %s, %s)"
        val = (imie, nazwisko, login, haslo, birthday)

        try:
            cursor.execute(query, val)
            conn.commit()
            print("Rekord dodany poprawnie!")
        except mysql.connector.Error as err:
            print(f"Błąd przy dodawaniu rekordu: {err}")

    # Create the main window
    window.withdraw()
    root = tk.Toplevel()
    root.title("Okno dodawnia nowego zawodnika")

    # Center the window on the screen
    window_width = 400
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Name entry
    name_label = tk.Label(root, text="Imie:")
    name_label.pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    # Seats entry
    surname_label = tk.Label(root, text="Nazwisko:")
    surname_label.pack()
    surname_entry = tk.Entry(root)
    surname_entry.pack()

    # login entry
    login_label = tk.Label(root, text="Login:")
    login_label.pack()
    login_entry = tk.Entry(root)
    login_entry.pack()

    # haslo entry
    haslo_label = tk.Label(root, text="Haslo:")
    haslo_label.pack()
    haslo_entry = tk.Entry(root)
    haslo_entry.pack()

    # birthday entry
    birthday_label = tk.Label(root, text="Data urodzin(RRRR-MM-DD):")
    birthday_label.pack()
    birthday_entry = tk.Entry(root)
    birthday_entry.pack()

    is_trainer = BooleanVar()
    checkbutton = Checkbutton(root, text="Czy trener?", variable=is_trainer)
    checkbutton.pack()

    # Accept button
    accept_button = tk.Button(root, text="Dodaj", command= add_member)
    accept_button.pack()

    # Return to main menu button
    return_button = tk.Button(root, text="Powrót do menu głównego",
                              command=lambda: [show_main_menu_coach(root)])
    return_button.pack()

    # Cancel button
    cancel_button = tk.Button(root, text="Anuluj", command=lambda: [print_members(root)])
    cancel_button.pack()
    root.mainloop()
    # Close the connection
    cursor.close()
    conn.close()


def print_boats(main_menu):
    try:
        main_menu.withdraw()
        my_w = tk.Toplevel()
        # Set your database access credentials
        db_config = {
            "host": "localhost",
            "user": "admin",
            "password": "password",
            "database": "klubdb",
        }
        # Establish a connection to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        trv = ttk.Treeview(my_w, selectmode='browse')
        trv.grid(row=1, column=1, padx=20, pady=20, rowspan=3)

        # number of columns
        trv["columns"] = ("1", "2", "3", "4", "5", "6")

        # Defining heading
        trv['show'] = 'headings'

        # width of columns and alignment
        trv.column("1", width=30, anchor='c')
        trv.column("2", width=80, anchor='c')
        trv.column("3", width=80, anchor='c')
        trv.column("4", width=80, anchor='c')
        trv.column("5", width=80, anchor='c')
        trv.column("6", width=80, anchor='c')

        # Headings for respective columns
        trv.heading("1", text="ID")
        trv.heading("2", text="Nazwa_lodzi")
        trv.heading("3", text="Ilosc_miejsc")
        trv.heading("4", text="Status_lodzi")
        trv.heading("5", text="Czy sportowa")
        trv.heading("6", text="Liczba_usterek")

        cursor.execute("SELECT * FROM lodz")
        r_set = cursor.fetchall()  # Pobierz wszystkie rekordy jako listę

        for dt in r_set:
            trv.insert("", 'end', iid=dt[0], text=dt[0], values=(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5]))

        add_user_button1 = tk.Button(my_w, text="Add Boat", command=lambda:[adding_boat(my_w)])
        add_user_button1.grid(row=1, column=2, padx=20, pady=20, sticky='n')

        add_user_button2 = tk.Button(my_w, text="Delete Boat", command=handle_option7)
        add_user_button2.grid(row=2, column=2, padx=20, pady=20, sticky='n')

        # Cancel button
        # Cancel button
        cancel_button = tk.Button(my_w, text="Powrot do menu glównego",
                                  command=lambda: [show_main_menu_coach(my_w)])
        cancel_button.grid(row=4, column=2, padx=20, pady=20)

        my_w.mainloop()

        # Close the connection
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")


def delete_user(user_id):
    try:
        # Set your database access credentials
        db_config = {
            "host": "localhost",
            "user": "admin",
            "password": "password",
            "database": "klubdb",
        }

        # Establish a connection to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Update the user's activity status to inactive
        query = "UPDATE czlonek_klubu SET czy_aktywny = 0 WHERE ID_czlonekklubu = %s"
        cursor.execute(query, (user_id,))
        conn.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "User has been set to inactive")
        else:
            messagebox.showerror("Error", "User not found")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        messagebox.showerror("Database Error", f"Database connection error: {err}")


def check_login(username, password, root):
    try:
        # Set your database access credentials
        db_config = {
            "host": "localhost",
            "user": "admin",
            "password": "password",
            "database": "klubdb",
        }

        # Establish a connection to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check the login and password, and if the account is active
        query = "SELECT ID_czlonekklubu, czy_aktywny FROM czlonek_klubu WHERE Login = %s AND Haslo = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            user_id, is_active = result
            if is_active:
                # Show the main menu for the coach
                show_main_menu_coach(root)
            else:
                messagebox.showerror("Login Error", "Account is not active")
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")


def show_main_menu():
    # Create the main menu window
    main_menu = tk.Tk()
    main_menu.title("Main Menu")

    # Center the window on the screen
    window_width = 400
    window_height = 300
    screen_width = main_menu.winfo_screenwidth()
    screen_height = main_menu.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    main_menu.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Add menu options (you can customize this further)
    label = tk.Label(main_menu, text="Witaj w menu glownym!")
    label.pack()

    # Example menu options
    button1 = tk.Button(main_menu, text="Kalendarz", command=handle_option1)
    button1.pack()

    button2 = tk.Button(main_menu, text="Zaplanuj trening", command=handle_option2)
    button2.pack()

    button5 = tk.Button(main_menu, text="Wyloguj", command=handle_option5)
    button5.pack()

    # Przycisk dodawania użytkownika
    def add_user():
        # Tutaj dodaj logikę dodawania użytkownika do bazy danych
        print("Dodawanie użytkownika...")

    add_user_button = tk.Button(main_menu, text="Dodaj użytkownika", command=add_user)
    add_user_button.pack()

    # Add more menu options here...

    main_menu.mainloop()


def show_main_menu_coach(window):
    window.withdraw()
    # Create the main menu window
    main_menu = tk.Toplevel()
    main_menu.title("Main Menu")

    # Center the window on the screen
    window_width = 400
    window_height = 300
    screen_width = main_menu.winfo_screenwidth()
    screen_height = main_menu.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    main_menu.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Add menu options (you can customize this further)
    label = tk.Label(main_menu, text="Witaj w menu glownym!")
    label.pack()

    # Example menu options (you can add more buttons or labels)
    button1 = tk.Button(main_menu, text="Kalendarz", command=handle_option1)
    button1.pack()

    button2 = tk.Button(main_menu, text="Zaplanuj trening", command=handle_option2)
    button2.pack()

    button3 = tk.Button(main_menu, text="Lista członków", command=lambda: print_members(main_menu))
    button3.pack()

    button4 = tk.Button(main_menu, text="Lista łodzi", command=lambda: print_boats(main_menu))
    button4.pack()

    button5 = tk.Button(main_menu, text="Wyloguj", command=lambda: [login_window(main_menu)])
    button5.pack()

    # Przycisk dodawania użytkownika
    def add_user():
        # Tutaj dodaj logikę dodawania użytkownika do bazy danych
        print("Dodawanie użytkownika...")

        add_user_button = tk.Button(my_w, text="Add User", command=handle_option1())
        add_user_button.grid(row=1, column=2, padx=100)

    main_menu.mainloop()


def handle_option1():
    # Implement the logic for Option 1
    print("Option 1 selected")


def handle_option2():
    # Implement the logic for Option 2
    print("Option 2 selected")


def handle_option3():
    # Implement the logic for Option 2
    print_members()


def handle_option4():
    # Implement the logic for Option 2
    print_boats()


def handle_option5():
    # Implement the logic for Option 2
    login_window()


def handle_option6():
    # Implement the logic for Option 2

    def boat_list():
        try:
            # Create the login window
            root = tk.Tk()
            root.title("Okno dodawnia nowej lodzi")

            # Center the window on the screen
            window_width = 400
            window_height = 300
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            root.geometry(f"{window_width}x{window_height}+{x}+{y}")

            name_label = tk.Label(root, text="Nazwa lodzi:")
            name_label.place(x=window_width / 2, y=window_height / 2)
            name_label.pack()
            name_entry = tk.Entry(root)
            name_entry.pack()

            seats_label = tk.Label(root, text="Ilosc miejsc:")
            seats_label.place(x=window_width / 2, y=window_height / 2)
            seats_label.pack()
            seats_entry = tk.Entry(root, show="*")  # Hide entered characters
            seats_entry.pack()

            db_config = {
                "host": "localhost",
                "user": "admin",
                "password": "password",
                "database": "klubdb",
            }
            # Establish a connection to the database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("SELECT * from lodz")
            r_set = cursor.fetchall()  # Pobierz wszystkie rekordy jako listę

            for dt in r_set:
                trv.insert("", 'end', iid=dt[0], text=dt[0],
                           values=(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5]))
            add_user_button1 = tk.Button(root, text="Add Boat", command=handle_option6())
            add_user_button1.grid(row=2, column=2, padx=20, pady=20)

            add_user_button2 = tk.Button(root, text="Delete Boat", command=handle_option7())
            add_user_button2.grid(row=3, column=2, padx=20, pady=20)
            my_w.mainloop()

            # Cancel button
            cancel_button = tk.Button(root, text="Anuluj", command=lambda: [show_main_menu_coach(root)])
            cancel_button.grid(row=4, column=2, padx=20, pady=20, sticky='n')

            # Zamknięcie połączenia
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")

    boat_list()


def handle_option7():
    # Implement the logic for Option 2
    delete_boat()


def login_window(window):
    # Create the login window
    window.withdraw()
    root = tk.Toplevel()
    root.title("Okno logowania klubu wioslarskiego Odra")

    # Center the window on the screen
    window_width = 400
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Username field
    login_label = tk.Label(root, text="Nazwa uzytkownika:")
    login_label.place(x=window_width / 2, y=window_height / 2)
    login_label.pack()
    login_entry = tk.Entry(root)
    login_entry.pack()

    # Password field
    password_label = tk.Label(root, text="Haslo:")
    password_label.place(x=window_width / 2, y=window_height / 2)
    password_label.pack()
    password_entry = tk.Entry(root, show="*")  # Hide entered characters
    password_entry.pack()

    # Login button
    def login():
        entered_username = login_entry.get()
        entered_password = password_entry.get()
        check_login(entered_username, entered_password,root)

    login_button = tk.Button(root, text="Login", command=login)
    login_button.pack()
    root.mainloop()

if __name__ == "__main__":
    # print_members()
    # print_boats()
    # show_main_menu_coach()
    """
    db_config = {
        "host": "localhost",
        "user": "admin",
        "password": "password",
        "database": "klubDB",
    }

    # Establish a connection to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Check the login and password
    query = "SELECT * FROM czlonek_klubu "
    cursor.execute(query)
    for x in cursor:
        print(x)
"""

    # show_main_menu_coach()
"""
    # Create the login window
    root = tk.Tk()
    root.title("Okno logowania klubu wioslarskiego Odra")

    # Center the window on the screen
    window_width = 400
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Username field
    login_label = tk.Label(root, text="Nazwa uzytkownika:")
    login_label.place(x=window_width / 2, y=window_height / 2)
    login_label.pack()
    login_entry = tk.Entry(root)
    login_entry.pack()

    # Password field
    password_label = tk.Label(root, text="Haslo:")
    password_label.place(x=window_width / 2, y=window_height / 2)
    password_label.pack()
    password_entry = tk.Entry(root, show="*")  # Hide entered characters
    password_entry.pack()


    # Login button
    def login():
        entered_username = login_entry.get()
        entered_password = password_entry.get()
        check_login(entered_username, entered_password)


    login_button = tk.Button(root, text="Login", command=login)
    login_button.pack()
    root.mainloop()
"""
root = tk.Tk()

login_window(root)

