#importing modules
import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
from tkinter import PhotoImage
from tkinter import messagebox
from PIL import Image, ImageTk
import pyodbc
from datetime import datetime, timedelta
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import smtplib
from email.message import EmailMessage
import os
import google.generativeai as genai
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



genai.configure(api_key = "AIzaSyA-PrkWvJGBVKG0AR49D5C0ssCTdz7Idps")
model = genai.GenerativeModel("gemini-2.0-flash")

#creating the window
app = ttk.Window()
app.geometry("1500x800")
app.title("SMART HOTELS")
app.resizable(False, False)


conn = pyodbc.connect(r'''
    DRIVER={ODBC Driver 17 for SQL Server};
    SERVER=(localdb)\MSSQLLocalDB;
    DATABASE=hotel_management;
-    Trusted_Connection=yes;
''')

cursor = conn.cursor()

print("connected to database")

menus = {
    "Indian": {
        "Breakfast": [
            {"name": "Chole Bhature", "price": 6, "image": "chole_bhature.png"},
            {"name": "Aloo Paratha", "price": 5, "image": "aloo_paratha.png"},
            {"name": "Poori Sabzi", "price": 5, "image": "poori_sabzi.png"}
        ],
        "Lunch": [
            {"name": "Chicken Biryani", "price": 11, "image": "chicken_biryani.png"},
            {"name": "Pulao", "price": 8, "image": "pulao.png"},
            {"name": "Butter Chicken & Garlic Naan", "price": 12, "image": "butter_chicken.png"},
            {"name": "Lamb Korma", "price": 13, "image": "lamb_korma.png"},
            {"name": "Goan Fish Curry", "price": 12, "image": "fish_curry.png"}
        ],
        "Dinner": [
            {"name": "Chana Masala", "price": 9, "image": "chana_masala.png"},
            {"name": "Keema", "price": 11, "image": "keema.png"},
            {"name": "Vegetable Pulao", "price": 8, "image": "veg_pulao.png"},
            {"name": "Paneer Butter Masala", "price": 10, "image": "paneer_butter.png"},
            {"name": "Fish Fry", "price": 12, "image": "fish_fry.png"},
            {"name": "Lamb Rogan Josh", "price": 13, "image": "rogan_josh.png"}
        ],
        "Drinks": [
            {"name": "Mango Lassi", "price": 4, "image": "mango_lassi.png"},
            {"name": "Masala Chaas", "price": 3, "image": "chaas.png"},
            {"name": "Nimbu Pani", "price": 3, "image": "nimbu_pani.png"},
            {"name": "Jaljeera", "price": 3, "image": "jaljeera.png"}
        ]
    },

    "British": {
        "Breakfast": [
            {"name": "Full English Breakfast", "price": 8, "image": "full_english.png"},
            {"name": "Eggs Benedict", "price": 7, "image": "eggs_benedict.png"},
            {"name": "Scotch Pancakes", "price": 6, "image": "pancakes.png"}
        ],
        "Lunch": [
            {"name": "Fish and Chips", "price": 10, "image": "fish_chips.png"},
            {"name": "Jacket Potato", "price": 6, "image": "jacket_potato.png"},
            {"name": "Coronation Chicken Sandwich", "price": 7, "image": "coronation_chicken.png"},
            {"name": "Steak and Ale Pie", "price": 11, "image": "steak_ale.png"},
            {"name": "Chicken Mushroom Pie", "price": 10, "image": "chicken_pie.png"}
        ],
        "Dinner": [
            {"name": "Roast Dinner", "price": 12, "image": "roast_dinner.png"},
            {"name": "Shepherd’s Pie", "price": 10, "image": "shepherds_pie.png"},
            {"name": "Bangers and Mash", "price": 9, "image": "bangers.png"},
            {"name": "Toad in the Hole", "price": 9, "image": "toad_hole.png"},
            {"name": "Chicken and Leek Pie", "price": 10, "image": "leek_pie.png"},
            {"name": "Fish Pie", "price": 11, "image": "fish_pie.png"}
        ],
        "Drinks": [
            {"name": "Cloudy Lemonade", "price": 3, "image": "lemonade.png"},
            {"name": "Irn Bru", "price": 3, "image": "irn_bru.png"},
            {"name": "Barley Water", "price": 2, "image": "barley.png"},
            {"name": "Dandelion & Burdock", "price": 3, "image": "dandelion.png"}
        ]
    },

    "Italian": {
        "Breakfast": [
            {"name": "Cornetto", "price": 4, "image": "cornetto.png"},
            {"name": "Fette Biscottate", "price": 3, "image": "biscottate.png"},
            {"name": "Pane Burro e Marmellata", "price": 4, "image": "bread_jam.png"}
        ],
        "Lunch": [
            {"name": "Margherita Pizza", "price": 9, "image": "pizza.png"},
            {"name": "Panini", "price": 7, "image": "panini.png"},
            {"name": "Caprese Salad", "price": 7, "image": "caprese.png"},
            {"name": "Pasta Bolognese", "price": 10, "image": "bolognese.png"},
            {"name": "Chicken Alfredo Pasta", "price": 11, "image": "alfredo.png"}
        ],
        "Dinner": [
            {"name": "Lasagna", "price": 11, "image": "lasagna.png"},
            {"name": "Risotto", "price": 10, "image": "risotto.png"},
            {"name": "Chicken Parmigiana", "price": 12, "image": "parmigiana.png"},
            {"name": "Seafood Pasta", "price": 13, "image": "seafood_pasta.png"},
            {"name": "Pizza Quattro Formaggi", "price": 11, "image": "quattro.png"},
            {"name": "Osso Buco", "price": 14, "image": "osso_buco.png"}
        ],
        "Drinks": [
            {"name": "Peach Iced Tea", "price": 3, "image": "iced_tea.png"},
            {"name": "Chinotto", "price": 3, "image": "chinotto.png"},
            {"name": "Crodino", "price": 3, "image": "crodino.png"}
        ]
    }
}

#manually creating a placeholder since tkinter does not have anything for placeholders
def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(foreground="gray")

#when user clicks on the entry entry it will get rid of the palce holder
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(foreground="black")

#if the user does not type anything it will insert the placeholder back into the entry box
    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(foreground="gray")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def send_invoice_email(to_email, customer_name, pdf_path):
    try:
        sender_email = "rehansheraz61@gmail.com"
        sender_password = "pzkvpilptcibwnqo"
        
        msg = EmailMessage()
        msg["Subject"] = "Your SMART HOTELS Invoice"
        msg["From"] = sender_email
        msg["To"] = to_email

        msg.set_content(
            f"""
        Dear {customer_name},

        Thank you for booking with SMART HOTELS.

        Please find your invoice attached.

        Kind regards,
        SMART HOTELS
        """
        )
        # Attach PDF
        with open(pdf_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(pdf_path)
            
        msg.add_attachment(file_data, maintype = "application", subtype = "pdf", filename = file_name,)
        
        # Send email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        print("Invoice email sent")

    except Exception as e:
        print("Email failed:", e)


def clear_app():
    for widget in app.winfo_children():
        widget.destroy()

def receptionist(username):
        for widget in app.winfo_children():
            widget.destroy()
            
        dashboard = ctk.CTkFrame(app, fg_color="white", width = 1500, height = 800)
        dashboard.place(x = 0, y = 0)
        
        ctk.FontManager.load_font(r"C:\Users\rehan\Documents\Uni\year_3\wednesdays\FINAL YEAR PROJECT\Pacifico-Regular.ttf") 
        custom_font = ctk.CTkFont(family="Pacifico", size=30)

        welcome = ctk.CTkLabel(dashboard, text=f"Welcome {username}", font=custom_font, text_color="white", fg_color="#3B8ED0", width=1600, height=60, anchor = "w", padx = 600)
        welcome.place(x=0, y=0)

        info_display = ctk.CTkFrame(dashboard, fg_color = "white", width = 1380, height = 730, corner_radius = 0)
        info_display.place(x = 140, y = 60)

        def clear_info():
            for widget in info_display.winfo_children():
                widget.destroy()
        
        #sidebar inside the dashboard
        sidebar = ctk.CTkFrame(dashboard, fg_color ="#E8E8E8",width = 140, height = 740, corner_radius = 0)
        sidebar.place(x = 0 ,y = 40)

        def view_existing():
            try:
                clear_info()

                query = """SELECT booking_id, first_name, last_name,arrival_date, checkout_date, room_type, requests FROM bookings"""
                cursor.execute(query)
                rows = cursor.fetchall()

                # Create frame to hold table + scrollbar
                table_frame = ttk.Frame(info_display)
                table_frame.place(x = 50, y = 40, width = 1250, height = 550)

                columns = ("ID", "First Name", "Last Name", "Check In", "Check Out", "Room Type", "Requests")

                tree = ttk.Treeview(table_frame, columns = columns, show = "headings", height = 20)

                # Column formatting
                tree.column("ID", width = 70, anchor  = "center")
                tree.column("First Name", width = 130, anchor = "center")
                tree.column("Last Name", width = 130, anchor = "center")
                tree.column("Check In", width = 120, anchor = "center")
                tree.column("Check Out", width = 120, anchor = "center")
                tree.column("Room Type", width = 140, anchor = "center")
                tree.column("Requests", width = 300, anchor = "w")

                for col in columns:
                    tree.heading(col, text=col)
                    
                # Scrollbar
                scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)
                scrollbar.pack(side="right", fill="y")
                tree.pack(fill="both", expand=True)

                # Insert data (formatted)
                for index, row in enumerate(rows):
                    check_in = row.arrival_date.strftime("%d/%m/%Y")
                    check_out = row.checkout_date.strftime("%d/%m/%Y")

                    values = (row.booking_id, row.first_name, row.last_name, check_in, check_out, row.room_type, row.requests)

                    # Alternating row colours
                    if index % 2 == 0:
                        tree.insert("", "end", values = values, tags = ("evenrow",))
                    else:
                        tree.insert("", "end", values = values, tags = ("oddrow",))

                tree.tag_configure("evenrow", background = "#f2f2f2")
                tree.tag_configure("oddrow", background = "white")

            except pyodbc.Error as e:
                print("Database error:", e)
        
        def new_booking():
            for widget in info_display.winfo_children():
                widget.destroy()

            def generate_invoice(data):
                styles = getSampleStyleSheet()
                elements = []

                #define the prices of the rooms
                prices = {
                    "standard £150": 150,
                    "deluxe £250": 250,
                    "suite £400": 400
                }

                #gets the arrival date and checkout date and calculates how mant nights have been stayed, then multiplies it with the price of the room 
                arrival = datetime.strptime(data["arrival"], "%Y-%m-%d")
                checkout = datetime.strptime(data["checkout"], "%Y-%m-%d")
                nights = (checkout - arrival).days

                room_price = prices.get(data["room"], 0)
                total = room_price * nights

                #title
                elements.append(Paragraph("SMART HOTELS INVOICE", styles["Title"]))
                elements.append(Spacer(1, 12))

                #booking information on the top left of the invoice
                guest_info = Paragraph(
                    f"""
                    Guest: {data['first_name']} {data['last_name']}<br/>
                    Arrival: {data['arrival']}<br/>
                    Checkout: {data['checkout']}<br/>
                    Nights: {nights}<br/>
                    Room: {data['room']}
                    """,
                    styles["Normal"]
                )
                elements.append(guest_info)
                elements.append(Spacer(1, 12))

                #information that will be included in the table 
                table_data = [
                    ["Description", "Amount"],
                    [f"Room charge ({nights} nights)", f"£{room_price * nights}"],
                    ["Total", f"£{total}"],
                ]

                #creating the table
                table = Table(table_data, colWidths=[300, 120])
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ]))
                elements.append(table)

                #creating and saving the file
                filename = f"invoice_{data['first_name']}_{data['last_name']}.pdf"
                pdf_path = filename
                
                doc = SimpleDocTemplate(filename, pagesize=A4)
                doc.build(elements)

                print(f"Invoice generated: {filename}")
                
                customer_email = data["email"]
                customer_name = f"{data['first_name']} {data['last_name']}"
                pdf_file = filename

                send_invoice_email(customer_email, customer_name, pdf_file)
                                    
            def assign_room(arrival, checkout):

                all_rooms = list(range(1, 31)) 

                query = """SELECT room_number FROM bookings WHERE NOT (checkout_date <= ? OR arrival_date >= ?)"""

                cursor.execute(query, (arrival, checkout))
                booked_rooms = [row.room_number for row in cursor.fetchall()]

                for room in all_rooms:
                    if room not in booked_rooms:
                        return room

                return None
                                                
            def submit_booking():
                try:
                    first_name = firstname_entry.get()
                    last_name = lastname_entry.get()
                    arrival = arrival_date_combo.get()
                    check_out = checkout_date_combo.get()
                    contact = contact_entry.get()
                    email = email_entry.get()
                    room = room_type_combo.get()
                    requests = requests_entry.get()
                    card_number = card_number_entry.get()
                    room_number = assign_room(arrival, check_out)
                    room_status = "available"

                    if room_number is None:
                        print("Hotel fully booked")
                        return

                    
                    query = """INSERT INTO bookings (first_name, last_name, arrival_date, checkout_date, contact_number, email, room_type, requests, card_number, room_number, room_status) VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
                    cursor.execute(query, (first_name, last_name, arrival, check_out, contact, email, room, requests, card_number, room_number, room_status))

                    conn.commit()
                    print("booking submitted")
                    booking_data = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "arrival": arrival,
                        "checkout": check_out,
                        "room": room,
                        "email": email
                    }

                    generate_invoice(booking_data)

                    tk.Label(info_display, text = f"Booking confrimed for room number {room_number} and invoice has been emailed to the customer").place(x = 300, y = 650)

                except pyodbc.Error as e:
                    print("SQL Server error:", e)
                    error = tk.Label(app, text = "make sure all fields have been entered correctly")
                    error.place(x = 300, y = 650)

            tk.Label(info_display, text = "first name:", font = ("Segoe UI", 14), bg = "white").place(x = 300, y = 100)
            tk.Label(info_display, text = "last name:", font = ("Segoe UI", 14), bg = "white").place(x = 300, y = 150)
            tk.Label(info_display, text = "arrival date:", font = ("Segoe UI", 14), bg = "white").place(x = 300, y = 200)
            tk.Label(info_display, text = "checkout date:", font = ("Segoe UI", 14), bg = "white").place(x = 300, y = 250)
            tk.Label(info_display, text = "contact number:", font = ("Segoe UI", 14), bg = "white").place(x = 300, y = 300)
            tk.Label(info_display, text = "email:", font = ("Segoe UI", 14), bg = "white").place(x = 300, y = 350)
            tk.Label(info_display, text = "room type:", font = ("Segoe UI", 14), bg = "white").place(x = 300, y = 400)
            tk.Label(info_display, text = "requests:", font = ("Segoe UI", 14), bg = "white").place(x = 300, y = 450)
            tk.Label(info_display, text = "card number:", font = ("Segoe UI", 14), bg = "white").place(x = 300, y = 500)

            firstname_entry = ttk.Entry(info_display, width= 35, bootstyle = "dark")
            firstname_entry.place(x = 500, y = 100)
            
            lastname_entry = ttk.Entry(info_display, width= 35, bootstyle = "dark")
            lastname_entry.place(x = 500, y = 150)

            today = datetime.today()
            date_options = [
                (today + timedelta(days = i)).strftime("%Y-%m-%d")
                for i in range(1, 15)
            ]
            arrival_date_combo = ttk.Combobox(info_display, values = date_options, width = 33, state = "readonly", bootstyle = "dark")
            arrival_date_combo.place(x = 500, y = 200)
            arrival_date_combo.set("Select date")
            
            checkout_date_combo = ttk.Combobox(info_display, values = date_options, width = 33, state = "readonly", bootstyle = "dark")
            checkout_date_combo.place(x = 500, y = 250)
            checkout_date_combo.set("Select date")
            
            contact_entry =ttk.Entry(info_display, width= 35, bootstyle = "dark")
            contact_entry.place(x = 500, y = 300)
            
            email_entry = ttk.Entry(info_display, width= 35, bootstyle = "dark")
            email_entry.place(x = 500, y = 350)

            rooms = ["standard £150", "deluxe £250", "suite £400"]
            room_type_combo = ttk.Combobox(info_display, values = rooms, width = 33, state = "readonly", bootstyle = "dark")
            room_type_combo.place(x = 500, y = 400)
            room_type_combo.set("Select room")
            
            requests_entry =ttk.Entry(info_display, width= 35, bootstyle = "dark")
            requests_entry.place(x = 500, y = 450)
            
            card_number_entry =ttk.Entry(info_display, width= 35, bootstyle = "dark")
            card_number_entry.place(x = 500, y = 500)

            ttk.Button(info_display, text = "SUBMIT BOOKING", width = 60, bootstyle = "danger", command = submit_booking).place(x = 300, y = 575)




        def register():
            clear_info()

            title = ctk.CTkLabel(info_display, text = "Add New Employee", font = ("Arial", 20, "bold"))
            title.place(x = 300, y = 80)

            name_label = ttk.Label(info_display, text = "Full Name:")
            name_label.place(x = 200, y = 150)

            name = ttk.Entry(info_display, width = 40)
            name.place(x = 350, y = 150)

            role_label = ttk.Label(info_display, text = "Job Title:")
            role_label.place(x = 200, y = 200)

            role = ["receptionist", "chef", "manager", "housekeeping"]
            role_combo = ttk.Combobox(info_display, values = role, width = 38, state = "readonly", bootstyle = "dark")
            role_combo.place(x = 350, y = 200)
            role_combo.set("Select user type")

            salary_label = ttk.Label(info_display, text = "Yearly Salary (£):")
            salary_label.place(x = 200, y = 250)

            salary = ttk.Entry(info_display, width = 40)
            salary.place(x = 350, y = 250)

            email_label = ttk.Label(info_display, text = "Email:")
            email_label.place(x = 200, y = 300)

            email = ttk.Entry(info_display, width = 40)
            email.place(x = 350, y = 300)

            contact_label = ttk.Label(info_display, text = "Contact Number:")
            contact_label.place(x = 200, y = 350)

            contact = ttk.Entry(info_display, width = 40)
            contact.place(x = 350, y = 350)

            password_label = ttk.Label(info_display, text = "Password:")
            password_label.place(x = 200, y = 400)

            password = ttk.Entry(info_display, width = 40)
            password.place(x = 350, y = 400)

            # Submit
            def submit():
                try:
                    query = """INSERT INTO staff_logins (username, job_title, yearly_salary, email, contact_number, password) VALUES (?,?,?,?,?,?)"""

                    cursor.execute(query, (name.get(), role_combo.get(), salary.get(), email.get(), contact.get(), password.get()))

                    conn.commit()

                    tk.Label(info_display, text = "Employee Added Successfully", fg = "green").place(x = 350, y = 470)

                except:
                    tk.Label(info_display, text = "Make sure the form is filled in correctly", fg = "red").place(x = 350, y = 470)

            add_btn = ctk.CTkButton(info_display, text = "Add Employee", command = submit)
            add_btn.place(x = 350, y = 450)



        # Sidebar
        sidebar = ctk.CTkFrame(dashboard, fg_color="#3B8ED0", width=180, height=740, corner_radius=0)
        sidebar.place(x=0, y=0)

        # Title / Logo
        ctk.CTkLabel(sidebar, text="🏨 Smart Hotels", font=("Segoe UI", 18, "bold"), text_color="black").place(x=20, y=30)

        # Reusable button style
        def sidebar_button(y, text, command):
            return ctk.CTkButton(sidebar, text=text, command=command, fg_color="black", hover_color="#333333", text_color="white", corner_radius=8, width=160, height=40, anchor="w").place(x=10, y=y)

        # Buttons (same spacing style as others)
        sidebar_button(100, "🆕  New Booking", new_booking)
        sidebar_button(150, "📋  Existing Bookings", view_existing)
        sidebar_button(200, "👤  Register Staff", register)
        sidebar_button(320, "🚪  Logout", login_screen)


def housekeeping(username):
    for widget in app.winfo_children():
        widget.destroy()
        
    dashboard = ctk.CTkFrame(app, fg_color="white", width=1500, height=800)
    dashboard.place(x=0, y=0)
    
    ctk.FontManager.load_font(r"C:\Users\rehan\Documents\Uni\year_3\wednesdays\FINAL YEAR PROJECT\Pacifico-Regular.ttf") 
    custom_font = ctk.CTkFont(family="Pacifico", size=30)

    welcome = ctk.CTkLabel(dashboard, text=f"Welcome {username}", font=custom_font, text_color="white", fg_color="#3B8ED0", width=1900, height=60, anchor = "w", padx = 600)
    welcome.place(x=0, y=0)

    info_display = ctk.CTkFrame(dashboard, fg_color="white", width=1380, height=730, corner_radius=0)
    info_display.place(x=140, y=60)

    def clear_info():
        for widget in info_display.winfo_children():
            widget.destroy()       

    def room_status_board():
        clear_info()
        today = datetime.today().strftime("%Y-%m-%d")

        update_query = """UPDATE bookings SET room_status = 'Needs Cleaning' WHERE checkout_date = ? AND room_status = 'Occupied'"""
        cursor.execute(update_query, (today,))
        conn.commit()

        query = """SELECT room_number, room_status FROM bookings WHERE room_number IS NOT NULL"""
        cursor.execute(query)
        rows = cursor.fetchall()

        room_status_dict = {row.room_number: row.room_status for row in rows}

        grid_frame = ctk.CTkFrame(info_display, fg_color="transparent")
        grid_frame.place(relx=0.65, rely=0.5, anchor="e")  

        row_pos = 0
        col_pos = 0

        for room in range(1, 31):
            status = room_status_dict.get(room, "Clean")

            if status == "Occupied":
                color = "#3B8ED0"
                button_command = None
            elif status == "Complete":
                color = "#E74C3C"
                button_command = lambda r=room: mark_room_clean(r)
            else:
                color = "#2ECC71"
                button_command = None

            room_button = ctk.CTkButton(grid_frame, text=f"Room {room}\n{status}", width=120, height=70, fg_color=color, command=button_command)

            room_button.grid(row=row_pos, column=col_pos, padx=15, pady=15)

            col_pos += 1
            if col_pos == 5:
                col_pos = 0
                row_pos += 1

    def mark_room_clean(room):
        query = """UPDATE bookings SET room_status = 'Clean' WHERE room_number = ?"""
        cursor.execute(query, (room,))
        conn.commit()
        
        room_status_board()  


    sidebar = ctk.CTkFrame(dashboard, fg_color="#3B8ED0", width=180, height=740, corner_radius=0)
    sidebar.place(x=0, y=30)

    # Title / Logo
    ctk.CTkLabel(sidebar, text="🏨 Smart Hotels", font=("Segoe UI", 18, "bold"), text_color="black").place(x=20, y=0)

    def sidebar_button(y, text, command):
        return ctk.CTkButton(sidebar,text=text, command=command, fg_color="black", hover_color="#333333", text_color="white", corner_radius=8, width=160, height=40, anchor="w").place(x=10, y=y)

    # Buttons for housekeeping
    sidebar_button(100, "🛏️  Room Status", room_status_board)
    sidebar_button(320, "🚪  Logout", login_screen)



def kitchen_staff(username):

    for widget in app.winfo_children():
        widget.destroy()

    dashboard = ctk.CTkFrame(app, fg_color = "white", width = 1500, height = 800)
    dashboard.place(x = 0, y = 0)

    ctk.FontManager.load_font(r"C:\Users\rehan\Documents\Uni\year_3\wednesdays\FINAL YEAR PROJECT\Pacifico-Regular.ttf") 
    custom_font = ctk.CTkFont(family="Pacifico", size=30)

    welcome = ctk.CTkLabel(dashboard, text=f"Welcome {username}", font=custom_font, text_color="white", fg_color="#3B8ED0", width=1900, height=60, anchor = "w", padx = 600)
    welcome.place(x=0, y=0)

    info_display = ctk.CTkFrame(dashboard, fg_color = "white", width = 1380, height = 730)
    info_display.place(x = 140, y = 60)

    def clear_info():
        for widget in info_display.winfo_children():
            widget.destroy()

    selected_id = None

    def get_selected_order(event):
        nonlocal selected_id

        selected_item = tree.focus()

        if not selected_item:
            return

        values = tree.item(selected_item)["values"]

        if values:
            selected_id = int(values[0])

    def view_food_orders():

        clear_info()

        query = """SELECT order_id, room_number, meal_type, food_item, order_status FROM food_orders WHERE order_status = 'Pending'"""

        cursor.execute(query)
        rows = cursor.fetchall()

        columns = ("Order ID", "Room", "Meal", "Food", "Status")

        global tree
        tree = ttk.Treeview(info_display, columns = columns, show = "headings", height = 20)

        for col in columns:
            tree.heading(col, text = col)
            tree.column(col, anchor = "center")

        tree.place(x = 100, y = 50)

        for row in rows:
            tree.insert("", "end", values=(row.order_id, row.room_number, row.meal_type, row.food_item, row.order_status))
            
        tree.bind("<<TreeviewSelect>>", get_selected_order)

        approve_btn = ctk.CTkButton(info_display, text = "Approve Order ✔", fg_color = "#2ECC71", hover_color = "#27AE60", command = lambda: approve_order())
        approve_btn.place(x = 300, y = 500)

        reject_btn = ctk.CTkButton(info_display, text = "Reject Order ✖", fg_color = "#E74C3C", hover_color = "#C0392B", command = lambda: reject_order())
        reject_btn.place(x = 500, y = 500)

    def approve_order():

        if selected_id is None:
            return

        query = "UPDATE food_orders SET order_status='Approved' WHERE order_id=?"
        cursor.execute(query, (selected_id,))
        conn.commit()

        view_food_orders()


    def reject_order():

        if selected_id is None:
            return

        query = "UPDATE food_orders SET order_status='Rejected' WHERE order_id=?"
        cursor.execute(query, (selected_id,))
        conn.commit()

        view_food_orders()

    def view_order_history():

        clear_info()

        query = """SELECT order_id, room_number, meal_type, food_item, order_status FROM food_orders WHERE order_status != 'Pending' ORDER BY order_time DESC"""

        cursor.execute(query)
        rows = cursor.fetchall()

        columns = ("Order ID", "Room", "Meal", "Food", "Status")

        tree = ttk.Treeview(info_display, columns = columns, show = "headings", height = 20)

        for col in columns:
            tree.heading(col, text = col)
            tree.column(col, anchor = "center")

        tree.place(x = 100, y = 50)

        for row in rows:
            tree.insert("", "end", values=(row.order_id, row.room_number, row.meal_type, row.food_item, row.order_status))

    # Sidebar
    sidebar = ctk.CTkFrame(dashboard, fg_color="#3B8ED0", width=180, height=740, corner_radius=0)
    sidebar.place(x=0, y=55)

    ctk.CTkLabel(sidebar, text="🏨 Smart Hotels", font=("Segoe UI", 18, "bold"), text_color="black").place(x=20, y=30)

    def sidebar_button(y, text, command):
        return ctk.CTkButton(sidebar, text=text, command=command, fg_color="black", hover_color="#333333", text_color="white", corner_radius=8, width=160, height=40, anchor="w").place(x=10, y=y)

    sidebar_button(100, "🍽️  View Orders", view_food_orders)
    sidebar_button(150, "📜  Order History", view_order_history)
    sidebar_button(320, "🚪  Logout", login_screen)

    

def manager(username):

    for widget in app.winfo_children():
        widget.destroy()

    dashboard = ctk.CTkFrame(app, fg_color = "white", width = 1500, height = 800)
    dashboard.place(x = 0, y = 0)

    ctk.FontManager.load_font(r"C:\Users\rehan\Documents\Uni\year_3\wednesdays\FINAL YEAR PROJECT\Pacifico-Regular.ttf") 
    custom_font = ctk.CTkFont(family="Pacifico", size=30)

    welcome = ctk.CTkLabel(dashboard, text=f"Welcome {username}", font=custom_font, text_color="white", fg_color="#3B8ED0", width=1900, height=60, anchor = "w", padx = 600)
    welcome.place(x=0, y=0)

    info_display = ctk.CTkFrame(dashboard, fg_color = "white", width = 1380, height = 730)
    info_display.place(x = 140, y = 60)

    def clear_info():
        for widget in info_display.winfo_children():
            widget.destroy()


    def revenue_ai_dashboard():
        clear_info()


        title = ctk.CTkLabel(info_display, text="Revenue Dashboard", font=("Arial", 26, "bold"))
        title.place(x=300, y=30)

        cursor.execute("""
            SELECT 
                DATEPART(WEEK, arrival_date) AS week_number,
                SUM(
                    CAST(REPLACE(SUBSTRING(room_type, CHARINDEX('£', room_type), LEN(room_type)), '£', '') AS INT)
                    * DATEDIFF(DAY, arrival_date, checkout_date)
                ) AS revenue
            FROM bookings
            GROUP BY DATEPART(WEEK, arrival_date)
            ORDER BY week_number
        """)

        data = cursor.fetchall()

        if not data:
            tk.Label(info_display, text="No data available").place(x=350, y=200)
            return

        weeks = [row[0] for row in data]
        revenue = [float(row[1]) for row in data]

        fig, ax = plt.subplots()
        ax.plot(weeks, revenue, marker = 'o')
        ax.set_title("Weekly Revenue")
        ax.set_xlabel("Week")
        ax.set_ylabel("Revenue (£)")

        canvas = FigureCanvasTkAgg(fig, master = info_display)
        canvas.draw()
        canvas.get_tk_widget().place(x = 25, y = 100, width = 770, height = 550)

        try:

            prompt = f"""
            You are a hotel revenue analyst.

            Here is weekly revenue data:
            Weeks: {weeks}
            Revenue: {revenue}

            Predict the next 6 weeks of revenue.

            Give a weekly estimate like:
            Week 1: £...
            Week 2: £...
            ...
            Week 6: £...

            i just want the numbers and just a short explanation at the end sayinh why you have come up with this forecast
            """

            response = model.generate_content(prompt)

            ai_text = response.text

        except Exception as e:
            ai_text = f"AI Error: {e}"

        ai_label = ctk.CTkTextbox(info_display, width = 450, height = 450)
        ai_label.place(x = 600, y = 100)

        ai_label.insert("1.0", ai_text)


    def send_payslip_email(to_email, employee_name, pdf_path):
        try:
            sender_email = "rehansheraz61@gmail.com"
            sender_password = "pzkvpilptcibwnqo"

            msg = EmailMessage()
            msg["Subject"] = "Your SMART HOTELS Payslip"
            msg["From"] = sender_email
            msg["To"] = to_email

            msg.set_content(f"""
    Dear {employee_name},

    Please find your payslip attached.

    Kind regards,
    SMART HOTELS
    """)

            with open(pdf_path, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(pdf_path)

            msg.add_attachment(file_data, maintype = "application", subtype = "pdf", filename = file_name)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(sender_email, sender_password)
                smtp.send_message(msg)

            print("Payslip email sent")

        except Exception as e:
            print("Email failed:", e)
            
    def generate_payslip(emp):
        styles = getSampleStyleSheet()
        elements = []

        yearly_salary = float(emp.yearly_salary)
        monthly_salary = yearly_salary / 12

        tax = monthly_salary * 0.2
        net_pay = monthly_salary - tax

        elements.append(Paragraph("SMART HOTELS PAYSLIP", styles["Title"]))
        elements.append(Spacer(1, 12))

        emp_info = Paragraph(f"""
        Employee: {emp.username}<br/>
        Role: {emp.job_title}<br/>
        """, styles["Normal"])

        elements.append(emp_info)
        elements.append(Spacer(1, 12))

        table_data = [
            ["Description", "Amount"],
            ["Monthly Salary", f"£{monthly_salary:.2f}"],
            ["Tax (20%)", f"-£{tax:.2f}"],
            ["Net Pay", f"£{net_pay:.2f}"],
        ]

        table = Table(table_data, colWidths = [300, 120])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        elements.append(table)

        filename = f"payslip_{emp.username}.pdf"

        doc = SimpleDocTemplate(filename, pagesize = A4)
        doc.build(elements)

        print(f"Payslip generated: {filename}")

        send_payslip_email(emp.email, emp.username, filename)

    def generate_payslip_UI():
        clear_info()

        title = ctk.CTkLabel(info_display, text = "Generate Payslips", font = ("Arial", 20, "bold"))
        title.place(x = 300, y = 50)

        # Treeview
        tree = ttk.Treeview(info_display, columns = ("Name", "Role", "Salary"), show = "headings")

        tree.heading("Name", text = "Name")
        tree.heading("Role", text = "Role")
        tree.heading("Salary", text = "Salary")

        tree.column("Name", width = 200)
        tree.column("Role", width = 150)
        tree.column("Salary", width = 120)

        tree.place(x = 200, y = 120, width = 600, height = 400)

        # Load data
        cursor.execute("""SELECT username, job_title, yearly_salary, email  FROM staff_logins""")
        employees = cursor.fetchall()

        employee_map = {}

        for emp in employees:
            item_id = tree.insert("", "end", values = (emp.username, emp.job_title, f"£{emp.yearly_salary}"))
            employee_map[item_id] = emp

        def send_selected():
            selected = tree.selection()

            if not selected:
                tk.Label(info_display, text = "Select an employee first", fg = "red").place(x = 350, y = 550)
                return

            emp = employee_map[selected[0]]

            try:
                generate_payslip(emp)
                tk.Label(info_display, text = "Payslip sent ✓", fg = "green").place(x = 350, y = 550)
            except Exception as e:
                print(e)
                tk.Label(info_display, text = "Error sending payslip", fg = "red").place(x = 350, y = 550)

        ctk.CTkButton(info_display, text = "Send Payslip", command = send_selected).place(x = 350, y = 500)

    
    def view_employees():
        clear_info()

        cursor.execute("SELECT username, job_title, yearly_salary, contact_number FROM staff_logins")
        rows = cursor.fetchall()

        tree = ttk.Treeview(info_display, columns = ("Name", "Role", "Salary", "Contact_Number"), show = "headings")

        tree.heading("Name", text = "Name")
        tree.heading("Role", text = "Role")
        tree.heading("Salary", text = "Salary")
        tree.heading("Contact_Number", text = "Contact Number")

        tree.column("Name", width = 150)
        tree.column("Role", width = 150)
        tree.column("Salary", width = 100)
        tree.column("Contact_Number", width = 150)

        tree.place(x = 200, y = 100, width = 805, height = 400)

        for row in rows:
            tree.insert("", "end", values  = (row.username, row.job_title, row.yearly_salary, row.contact_number))


    def add_employee():
        clear_info()

        title = ctk.CTkLabel(info_display, text = "Add New Employee", font = ("Arial", 20, "bold"))
        title.place(x = 300, y = 80)

        name_label = ttk.Label(info_display, text = "Full Name:")
        name_label.place(x = 200, y = 150)

        name = ttk.Entry(info_display, width = 40)
        name.place(x = 350, y = 150)

        role_label = ttk.Label(info_display, text = "Job Title:")
        role_label.place(x = 200, y = 200)

        role = ["receptionist", "chef", "manager", "housekeeping"]
        role_combo = ttk.Combobox(info_display, values = role, width = 38, state = "readonly", bootstyle = "dark")
        role_combo.place(x = 350, y = 200)
        role_combo.set("Select user type")

        salary_label = ttk.Label(info_display, text = "Yearly Salary (£):")
        salary_label.place(x = 200, y = 250)

        salary = ttk.Entry(info_display, width = 40)
        salary.place(x = 350, y = 250)

        email_label = ttk.Label(info_display, text = "Email:")
        email_label.place(x = 200, y = 300)

        email = ttk.Entry(info_display, width = 40)
        email.place(x = 350, y = 300)

        contact_label = ttk.Label(info_display, text = "Contact Number:")
        contact_label.place(x = 200, y = 350)

        contact = ttk.Entry(info_display, width = 40)
        contact.place(x = 350, y = 350)

        password_label = ttk.Label(info_display, text = "Password:")
        password_label.place(x = 200, y = 400)

        password = ttk.Entry(info_display, width = 40)
        password.place(x = 350, y = 400)

        # Submit
        def submit():
            try:
                query = """INSERT INTO staff_logins (username, job_title, yearly_salary, email, contact_number, password) VALUES (?,?,?,?,?,?)"""

                cursor.execute(query, (name.get(), role_combo.get(), salary.get(), email.get(), contact.get(), password.get()))

                conn.commit()

                tk.Label(info_display, text = "Employee Added Successfully", fg = "green").place(x = 350, y = 470)

            except:
                tk.Label(info_display, text = "Make sure the form is filled in correctly", fg = "red").place(x = 350, y = 470)

        add_btn = ctk.CTkButton(info_display, text = "Add Employee", command = submit)
        add_btn.place(x = 350, y = 450)

    def remove_employee():
        clear_info()

        title = ctk.CTkLabel(info_display, text = "Remove Employee", font = ("Arial", 20, "bold"))
        title.place(x = 300, y = 100)

        info = ttk.Label(info_display, text = "Enter Employee Username to Remove:")
        info.place(x = 370, y = 200)

        emp_id = ttk.Entry(info_display, width = 40)
        emp_id.place(x = 350, y = 240)

        def delete():
            try:
                query = "DELETE FROM staff_logins WHERE username = ?"
                cursor.execute(query, (emp_id.get(),))
                conn.commit()

                tk.Label(info_display, text = "Employee Removed Successfully", fg = "green").place(x = 350, y = 320)

            except Exception as e:
                tk.Label(info_display, text = f"Error: {e}", fg = "red").place(x = 350, y = 320)

        delete_btn = ctk.CTkButton(info_display, text = "Remove Employee", fg_color = "red", command = delete)
        delete_btn.place(x = 350, y = 280)


        # Sidebar
    sidebar = ctk.CTkFrame(dashboard, fg_color="#3B8ED0", width=180, height=740, corner_radius=0)
    sidebar.place(x=0, y=55)

    ctk.CTkLabel(sidebar, text="🏨 Smart Hotels", font=("Segoe UI", 18, "bold"), text_color="black").place(x=20, y=30)

    def sidebar_button(y, text, command):
        return ctk.CTkButton(sidebar, text=text, command=command, fg_color="black", hover_color="#333333", text_color="white", corner_radius=8, width=160, height=40, anchor="w").place(x=10, y=y)

    sidebar_button(100, "📊  Revenue AI", revenue_ai_dashboard)
    sidebar_button(150, "💰  Payslips", generate_payslip_UI)
    sidebar_button(200, "👥  Employees", view_employees)
    sidebar_button(250, "➕  Add Employee", add_employee)
    sidebar_button(300, "❌  Remove Employee", remove_employee)
    sidebar_button(380, "🚪  Logout", login_screen)


basket = []
def customer(email_input):
    for widget in app.winfo_children():
        widget.destroy()

    dashboard = ctk.CTkFrame(app, fg_color="white", width=1500, height=800)
    dashboard.place(x=0, y=0)

    ctk.FontManager.load_font(r"C:\Users\rehan\Documents\Uni\year_3\wednesdays\FINAL YEAR PROJECT\Pacifico-Regular.ttf") 
    custom_font = ctk.CTkFont(family="Pacifico", size=30)

    welcome = ctk.CTkLabel(dashboard, text=f"Welcome  to  smart  hotels", font=custom_font, text_color="white", fg_color="#3B8ED0", width=1900, height=60, anchor = "w", padx = 600)
    welcome.place(x=0, y=0)

    info_display = ctk.CTkFrame(dashboard, fg_color="white", width=1380, height=730)
    info_display.place(x=140, y=60)



    def clear_info():
        for widget in info_display.winfo_children():
            try:
                widget.destroy()
            except:
                pass

    def view_booking():
        clear_info()

        # Title
        title = ctk.CTkLabel(info_display, text="My Booking", font=("Arial", 26, "bold"))
        title.place(x=350, y=40)

        # Card container
        frame = ctk.CTkFrame(info_display, width=500, height=350, corner_radius=15)
        frame.place(x=250, y=120)

        # Fetch booking that is not complete
        query = """SELECT room_number, arrival_date, checkout_date, room_type, room_status 
                   FROM bookings 
                   WHERE email = ? AND room_status != 'Complete'"""
        cursor.execute(query, (email_input,))
        row = cursor.fetchone()

        if row:
            status_color = "white"

            if row.room_status == "Occupied":
                status_color = "green"
            elif row.room_status == "Needs Cleaning":
                status_color = "orange"
            elif row.room_status == "Booked":
                status_color = "blue"

            # Labels (clean layout)
            ctk.CTkLabel(frame, text="Room Number:", font=("Arial", 14, "bold")).place(x=50, y=40)
            ctk.CTkLabel(frame, text=row.room_number, font=("Arial", 14)).place(x=250, y=40)

            ctk.CTkLabel(frame, text="Room Type:", font=("Arial", 14, "bold")).place(x=50, y=80)
            ctk.CTkLabel(frame, text=row.room_type, font=("Arial", 14)).place(x=250, y=80)

            ctk.CTkLabel(frame, text="Arrival Date:", font=("Arial", 14, "bold")).place(x=50, y=120)
            ctk.CTkLabel(frame, text=row.arrival_date, font=("Arial", 14)).place(x=250, y=120)

            ctk.CTkLabel(frame, text="Checkout Date:", font=("Arial", 14, "bold")).place(x=50, y=160)
            ctk.CTkLabel(frame, text=row.checkout_date, font=("Arial", 14)).place(x=250, y=160)

            ctk.CTkLabel(frame, text="Status:", font=("Arial", 14, "bold")).place(x=50, y=200)
            ctk.CTkLabel(frame, text=row.room_status, font=("Arial", 14, "bold"), text_color=status_color).place(x=250, y=200)

        else:
            ctk.CTkLabel(frame, text="No active booking found", font=("Arial", 16)).place(x=130, y=150)

    def check_in_out_ui():
        clear_info()

        title = ctk.CTkLabel(info_display, text = "Guest Check-In / Check-Out", font = ("Arial", 26, "bold"))
        title.place(x = 300, y = 40)

        frame = ctk.CTkFrame(info_display, width = 500, height = 300, corner_radius = 15)
        frame.place(x = 250, y = 120)

        subtitle = ctk.CTkLabel(frame, text = "Manage your stay", font = ("Arial", 16))
        subtitle.place(x = 150, y = 20)

        status_label = ctk.CTkLabel(frame, text = "", font = ("Arial", 14))
        status_label.place(x = 150, y = 220)

        def check_in():
            today_date = datetime.today().date()

            cursor.execute("""SELECT arrival_date, room_status FROM bookings WHERE email = ?""", (email_input,))
            result = cursor.fetchone()
            
            if result is None:
                status_label.configure(text="No booking found", text_color="red")
                return

            arrival_date, room_status = result

            if room_status == "Complete":
                status_label.configure(text="Cannot check in: already checked out", text_color="red")
                return

            if today_date < arrival_date:
                status_label.configure(text="You cannot check in before your arrival date", text_color="red")
                return

            cursor.execute("""UPDATE bookings SET room_status = 'Occupied' WHERE email = ? AND arrival_date = ?""",
                           (email_input, arrival_date.strftime("%Y-%m-%d")))
            conn.commit()

            status_label.configure(text="Checked in successfully", text_color="green")


        def check_out():
            
            cursor.execute("""SELECT room_status FROM bookings WHERE email = ?""", (email_input,))
            result = cursor.fetchone()

            if result is None:
                status_label.configure(text="No booking found", text_color="red")
                return

            current_status = result[0]

            if current_status != "Occupied":
                status_label.configure(text="You must check in before checking out", text_color="red")
                return

            cursor.execute("""UPDATE bookings SET room_status = 'Complete' WHERE email = ?""", (email_input,))
            conn.commit()

            status_label.configure(text="Checked out successfully", text_color="orange")

    
        checkin_btn = ctk.CTkButton(frame,text="Check In", width=180, height=40, fg_color="#2ecc71", hover_color="#27ae60", command=check_in)
        checkin_btn.place(x=50, y=120)

        checkout_btn = ctk.CTkButton(frame, text="Check Out", width=180, height=40, fg_color="#e74c3c", hover_color="#c0392b", command=check_out)
        checkout_btn.place(x=260, y=120)

    def order_food():
        clear_info()

        selected_cuisine = None

        def update_basket_display():
            for widget in basket_items_frame.winfo_children():
                widget.destroy()

            total = 0

            for item in basket:
                text = f"{item['name']} - £{item['price']}"

                ctk.CTkLabel(basket_items_frame, text=text, text_color="white").pack(anchor="w", padx=10, pady=2)

                total += item["price"]

            basket_total_label.configure(text=f"Total: £{total}")


        def create_basket_ui():
            global basket_frame, basket_items_frame, basket_total_label

            basket_frame = ctk.CTkFrame(info_display, width=280, height=350, fg_color="#3B8ED0")
            basket_frame.place(x=775, y=30)

            # Title
            ctk.CTkLabel(basket_frame, text="Basket", font=("Arial", 18, "bold"), text_color="white").pack(pady=10)

            # Scrollable items area
            basket_items_frame = ctk.CTkScrollableFrame(basket_frame, width=250, height=350, fg_color="#2F76B5")
            basket_items_frame.pack(pady=10, fill="both", expand=True)

            # Total label
            basket_total_label = ctk.CTkLabel(basket_frame, text="Total: £0", font=("Arial", 14, "bold"), text_color="white")
            basket_total_label.pack(pady = 8)

            # Checkout button
            ctk.CTkButton(basket_frame, text="Checkout", fg_color="white", text_color="black", command=checkout).pack(pady=10)

            update_basket_display()


        def add_to_basket(item, meal, cuisine):
            basket.append({"name": item["name"], "price": item["price"], "meal": meal, "cuisine": cuisine})
            update_basket_display() 


        def checkout():
            if not basket:
                messagebox.showwarning("Basket Empty", "Your basket is empty.")
                return

            cursor.execute("""SELECT room_number, room_status FROM bookings WHERE email = ?""", (email_input,))
            
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Error", "No booking found.")
                return

            room_number, room_status = result

            if room_status.lower() != "occupied":
                messagebox.showerror("Not Checked In", "You must be checked in to order food.") 
                return

            for item in basket:
                query = """INSERT INTO food_orders(room_number, customer_name, meal_type, food_item, order_status, order_time) VALUES (?,?,?,?,?,GETDATE())"""

                cursor.execute(query, (room_number, email_input, item["meal"], f"{item['cuisine']} - {item['name']}", "Pending"))

            conn.commit()
            basket.clear()
            update_basket_display()

            messagebox.showinfo("Success", "Order placed successfully!")

        def show_meals(cuisine):
            nonlocal selected_cuisine
            selected_cuisine = cuisine
            clear_info()
            create_basket_ui() 

            tk.Label(info_display, text=f"{cuisine} Menu", font=("Arial", 18, "bold")).place(x=400, y=50)

            meals = ["Breakfast", "Lunch", "Dinner", "Drinks"]

            x = 80
            for meal in meals:
                ctk.CTkButton(info_display, text=meal, command=lambda m=meal: show_food(cuisine, m)).place(x=x, y=200)
                x += 150

            ctk.CTkLabel(info_display, text = "7am - 12pm                           12pm - 6pm                           6pm - 11pm                           7am - 11pm", font=("Arial", 12, "bold")).place(x = 110, y = 150)


        def show_food(cuisine, meal):
            clear_info()
            create_basket_ui()

            foods = menus.get(cuisine, {}).get(meal, [])

            x = 50
            y = 30

            MAX_X = 700

            for item in foods:
                # Card frame
                frame = ctk.CTkFrame(info_display, width=220, height=240, corner_radius=15, fg_color="#2B2B2B")
                frame.place(x=x, y=y)
                frame.pack_propagate(False)

                # IMAGE
                try:
                    img = Image.open(item["image"])
                    img = img.resize((140, 110))
                    photo = ImageTk.PhotoImage(img)

                    img_label = ctk.CTkLabel(frame, image=photo, text="")
                    img_label.image = photo
                    img_label.pack(pady=10)
                except:
                    ctk.CTkLabel(frame, text="No Image", text_color="white").pack(pady=20)

                # NAME
                ctk.CTkLabel(frame, text=item["name"], font=("Arial", 14, "bold"), text_color="white").pack()

                # PRICE
                ctk.CTkLabel(frame, text=f"£{item['price']}", text_color="white", font=("Arial", 13)).pack(pady=2)

                # BUTTON
                ctk.CTkButton(frame, text="Add", fg_color="#3B8ED0", hover_color="#2F76B5", command=lambda i=item: add_to_basket(i, meal, cuisine)).pack(pady=10)

                # GRID POSITIONING
                x += 240

                if x > MAX_X:
                    x = 50
                    y += 280

        def get_suggestion():
            preference = user_input.get()

            try:
                prompt = f"""
                Available menu:
                {menus}

                Customer request: {preference}

                Recommend ONE dish and where to find it on the menu, do not give any explaination.
                """

                response = model.generate_content(prompt)
                output_label.configure(text=f"Suggestion: {response.text}")

            except Exception as e:
                print(e)

        create_basket_ui()

        tk.Label(info_display, text="Select Cuisine", font=("Arial", 18)).place(x=400, y=50)

        x = 200
        x_flag = 300

        for cuisine in menus.keys():
            try:
                img = Image.open(f"{cuisine}.png")
                img = img.resize((80, 50))
                photo = ImageTk.PhotoImage(img)
            except:
                photo = None

            if photo:
                flag_label = tk.Label(info_display, image=photo)
                flag_label.image = photo
                flag_label.place(x=x_flag, y=220)

            ctk.CTkButton(info_display, text=cuisine, command=lambda c=cuisine: show_meals(c)).place(x=x, y=290)

            x += 150
            x_flag += 170


        ctk.CTkLabel(info_display, text="Don't know what to eat? Get an AI suggestion!").place(x = 150, y = 380)
        
        user_input = ctk.CTkEntry(info_display, width=300)
        user_input.place(x = 150, y = 420)
        user_input.insert(0, "e.g. I want something spicy")

        output_label = ctk.CTkLabel(info_display, text="", wraplength=500)
        output_label.place(x = 150, y = 480)
        
        ctk.CTkButton(info_display, text="Get suggestion", command=get_suggestion).place(x=550, y=420)


        

    def booking_history():
        clear_info()

        # Title
        ctk.CTkLabel(info_display, text="Booking History", font=("Arial", 24, "bold"), text_color="white").place(x=200, y=40)

        query = """SELECT room_number, arrival_date, checkout_date, room_type FROM bookings WHERE email = ? ORDER BY arrival_date DESC"""

        cursor.execute(query, (email_input,))
        rows = cursor.fetchall()

        # Style
        style = ttk.Style()

        style.configure("Treeview",background="#2B2B2B", foreground="white",rowheight=35, fieldbackground="#2B2B2B", bordercolor="#3B8ED0", borderwidth=1)

        style.configure("Treeview.Heading", background="#3B8ED0", foreground="white", font=("Arial", 12, "bold"))

        style.map("Treeview", background=[("selected", "#3B8ED0")])

        # Frame (container)
        frame = ctk.CTkFrame(info_display, fg_color="transparent")
        frame.place(x=180, y=100)

        # Scrollbar
        scrollbar = ctk.CTkScrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        # Table
        tree = ttk.Treeview(frame, columns=("Room", "Arrival", "Checkout", "Type"), show="headings", yscrollcommand=scrollbar.set, height=12)

        scrollbar.configure(command=tree.yview)

        # Headings
        tree.heading("Room", text="Room No.")
        tree.heading("Arrival", text="Arrival Date")
        tree.heading("Checkout", text="Checkout Date")
        tree.heading("Type", text="Room Type")

        # Column sizing
        tree.column("Room", width=120, anchor="center")
        tree.column("Arrival", width=220, anchor="center")
        tree.column("Checkout", width=220, anchor="center")
        tree.column("Type", width=220, anchor="center")

        tree.pack()

        # Insert data with striping
        for i, row in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", "end", values=(row.room_number, row.arrival_date, row.checkout_date, row.room_type), tags=(tag,))

        # Row colors
        tree.tag_configure("even", background="#2B2B2B")
        tree.tag_configure("odd", background="#242424")










    sidebar = ctk.CTkFrame(dashboard, fg_color="#3B8ED0", width=180, height=740, corner_radius=0)
    sidebar.place(x = 0, y = 55)

    # Title / Logo
    ctk.CTkLabel(sidebar, text="🏨 Smart Hotels", font=("Segoe UI", 18, "bold"), text_color="black").place(x=20, y=30)

    def sidebar_button(y, text, command):
        return ctk.CTkButton(sidebar, text=text, command=command, fg_color="black", hover_color="#333333", text_color="white", corner_radius=8, width=160, height=40, anchor="w").place(x=10, y=y)

    # Buttons with emojis
    sidebar_button(100, "📖  My Booking", view_booking)
    sidebar_button(150, "🛎️  Check In/Out", check_in_out_ui)
    sidebar_button(200, "🍽️  Order Food", order_food)
    sidebar_button(250, "📜  History", booking_history)
    sidebar_button(320, "🚪  Logout", login_screen)

            

def get_details():
    username = username_entry.get()
    password = password_entry.get()

    SQL_check = """SELECT username, job_title FROM staff_logins WHERE username = ? AND password = ?"""
    
    cursor.execute(SQL_check, (username, password))
    outcome = cursor.fetchone()

    if outcome:
        job_title = outcome.job_title  

        # Call correct function based on role
        if job_title == "housekeeping":
            housekeeping(username)

        elif job_title == "chef":
            kitchen_staff(username)

        elif job_title == "manager":
            manager(username)

        elif job_title == "receptionist":
            receptionist(username)

    else:
        error = ttk.Label(app, text="Invalid username or password")
        error.place(x = 175, y = 600)

def customer_login_screen():
    def register_customer():
        def submit():

            try:
                first = name.get()
                last = last_name.get()
                pwd = password.get()
                mail = email.get()
                post = postcode.get()
                addr = address.get()
                phone = contact.get()

                query = """INSERT INTO customers (first_name, last_name, password, email, postcode, address, contact_number) VALUES (?,?,?,?,?,?,?)"""

                cursor.execute(query, (first, last, pwd, mail, post, addr, phone))
                conn.commit()

                tk.Label(app, text="Customer registered successfully").place(x = 75, y = 750)

            except pyodbc.Error as e:
                print("Database error:", e)
                
        clear_app()
        #log in title label
        label = ttk.Label(app, text = "Account creation")
        label.place(x = 130, y = 100)
        label.config(font = ("arial", 20, "bold"))
        
        label = ttk.Label(app, text = "Fill in the form below to register")
        label.place(x = 75, y = 240)
        label.config(font = ("arial", 10))
    
        
        image = Image.open("hotel_image.jpg")
        image = image.resize((750, 800))
        photo = ImageTk.PhotoImage(image)

        # Display image in label
        image_label = tk.Label(app, image=photo)
        image_label.image = photo 
        image_label.place(x = 750, y = 0)


        name = ttk.Entry(app, width = 50, show = "")
        name.place(x = 75, y = 275)
        add_placeholder(name, "First name")

        last_name = ttk.Entry(app, width = 50, show = "")
        last_name.place(x = 75, y = 325)
        add_placeholder(last_name, "Last name")

        password = ttk.Entry(app, width = 50, show = "")
        password.place(x = 75, y = 375)
        add_placeholder(password, "Password")

        email = ttk.Entry(app, width = 50, show = "")
        email.place(x = 75, y = 425)
        add_placeholder(email, "Email")

        postcode = ttk.Entry(app, width = 50, show = "")
        postcode.place(x = 75, y = 475)
        add_placeholder(postcode, "Postccode")

        address = ttk.Entry(app, width = 50, show = "")
        address.place(x = 75, y = 525)
        add_placeholder(address, "Address")

        contact = ttk.Entry(app, width = 50, show = "")
        contact.place(x = 75, y = 575)
        add_placeholder(contact, "Contact number")

        submit = ctk.CTkButton(app, text = "Create account!", corner_radius = 20, command = submit)
        submit.place(x = 150, y = 500)

        login = ctk.CTkButton(app, text = "Back to Login Page", corner_radius = 20, command = customer_login_screen)
        login.place(x  = 150, y = 550)

        
    def customer_login():

        email_input = username_entry.get()
        password_input = password_entry.get()

        try:
            query = """SELECT * FROM customers WHERE email = ? AND password = ?"""

            cursor.execute(query, (email_input, password_input))
            user = cursor.fetchone()

            if user:
                customer(email_input)
            else:
                tk.Label(app, text="Invalid email or password, please try again!").place(x=75, y=630)
                
        except pyodbc.Error as e:
            print("Database error:", e)
            
    clear_app()
    
    global username_entry, password_entry
    #log in title label
    label = ttk.Label(app, text = "Customer Login Page")
    label.place(x = 130, y = 100)
    label.config(font = ("arial", 20, "bold"))
    
    image = Image.open("hotel_image.jpg")
    image = image.resize((750, 800))
    photo = ImageTk.PhotoImage(image)

    # Display image in label
    image_label = tk.Label(app, image = photo)
    image_label.image = photo 
    image_label.place(x = 750, y = 0)

    # Username field
    username_entry = ttk.Entry(app, width = 50)
    username_entry.place(x = 75, y = 275)
    add_placeholder(username_entry, "Email")

    # Password field
    password_entry = ttk.Entry(app, width = 50, show = "")  
    password_entry.place(x = 75, y = 325)
    add_placeholder(password_entry, "Password")

    entry_button = ctk.CTkButton(app, text = "Log in", corner_radius = 20, command = customer_login)
    entry_button.place(x = 150, y = 360)

    switch_btn = ctk.CTkButton(app, text="Switch to Staff", corner_radius=20, command=login_screen)
    switch_btn.place(x = 150, y = 400)

    new_user = ttk.Label(app, text = "Dont have an account yet? Click below to register")
    new_user.place(x = 75, y = 375)

    register = ctk.CTkButton(app, text = "Register Here", corner_radius = 20, command = register_customer)
    register.place(x = 150, y = 450)


def login_screen():
    clear_app()
    global username_entry, password_entry

    #log in title label
    label = ttk.Label(app, text = "Staff Login Page")
    label.place(x = 130, y = 100)
    label.config(font = ("arial", 20, "bold"))
    
    image = Image.open("hotel_image.jpg")
    image = image.resize((750, 800))
    photo = ImageTk.PhotoImage(image)

    # Display image in label
    image_label = tk.Label(app, image=photo)
    image_label.image = photo 
    image_label.place(x=750, y = 0)

    # Username field
    username_entry = ttk.Entry(app, width=50)
    username_entry.place(x=75, y=275)
    add_placeholder(username_entry, "Username")

    # Password field
    password_entry = ttk.Entry(app, width=50, show="")  
    password_entry.place(x=75, y=325)
    add_placeholder(password_entry, "Password")

    #entry button to submit credentials
    entry_button = ctk.CTkButton(app, text = "Log in", corner_radius = 20, command = get_details)
    entry_button.place(x = 150, y = 360)

    customer = ctk.CTkButton(app, text = "Switch to Customer", corner_radius = 20, command = customer_login_screen)
    customer.place(x = 150, y = 400)

    new_user = ttk.Label(app, text = "Dont have an account yet?\n Ask an existing member of staff to create you one!")
    new_user.place(x = 75, y = 375)

login_screen()

app.mainloop()
  
