import _tkinter
import tkinter as tk
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk


# Define class for table with scrollbar (TreeViewFrame)
class TreeviewFrame(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.treeview = ttk.Treeview(
            self,
            xscrollcommand=self.hscrollbar.set,
            yscrollcommand=self.vscrollbar.set
        )
        self.hscrollbar.config(command=self.treeview.xview)
        self.hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.vscrollbar.config(command=self.treeview.yview)
        self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview.pack()

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Treeview",
                             background="white",
                             foreground="black",
                             rowheight=15,
                             fieldbackground="white")
        self.style.map("Treeview", background=[('selected', clr1)])


# Define Functions
def init_db(db_name="minishopp.db"):
    conn = sqlite3.connect(database=db_name)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS ms_customers (
        --customer_id INT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        address TEXT,
        phone_number TEXT,
        modified_date INT
    );
    """)
    conn.commit()
    conn.close()


def execute_query(input_query, input_data_dict={}, db_name="minishopp.db"):
    conn = sqlite3.connect(database=db_name)
    c = conn.cursor()
    c.execute(input_query, input_data_dict)
    records = c.fetchall()
    conn.commit()
    conn.close()
    return records


def display_db():
    # Display data from db
    data = execute_query(
        """ SELECT oid, first_name, last_name, address, phone_number, datetime(modified_date,'unixepoch') FROM ms_customers; """)
    # print(data)
    for d in data:
        try:
            tbl_ms_customers.treeview.insert(parent='', index='end', iid=d[0] - 1, values=d)
        except _tkinter.TclError:
            pass

    tbl_ms_customers.pack()


def input_record():
    # Check if mandatory entries are already filled
    global lbl_warning
    lbl_warning.destroy()
    if len(entry_first_name.get()) == 0 or len(entry_phone_number.get()) == 0:
        lbl_warning = tk.Label(frame_entry, text="Insert error: Customer's first name and phone number must be filled.", bg=clr2, fg="red")
        lbl_warning.grid(row=5, column=0, columnspan=2)
        raise Exception("Insert error: Customer's first name and phone number must be filled.")

    # Get current timestamp unix
    modified_date = execute_query(""" SELECT unixepoch('now'); """)[0][0]
    # print(modified_date)
    # Execute query to insert data from entry
    new_record = execute_query("""
        INSERT INTO ms_customers(first_name, last_name, address, phone_number, modified_date) VALUES(
            :first_name,
            :last_name,
            :address,
            :phone_number,
            :modified_date
        )
    """, {
        "first_name": entry_first_name.get(),
        "last_name": entry_last_name.get(),
        "address": entry_address.get(),
        "phone_number": entry_phone_number.get(),
        "modified_date": modified_date
    })

    # Clear the entry
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_phone_number.delete(0, tk.END)
    entry_oid.delete(0, tk.END)

    # Re-display db
    display_db()

def delete_record():
    # Check if mandatory entries are already filled
    global lbl_warning
    lbl_warning.destroy()
    if len(entry_oid.get()) == 0:
        lbl_warning = tk.Label(frame_entry, text="Delete error: Customer's ID number (oid) must be filled.",
                               bg=clr2, fg="red")
        lbl_warning.grid(row=5, column=0, columnspan=2)
        raise Exception("Delete error: Customer's ID number (oid) must be filled.")
    elif not entry_oid.get().isnumeric():
        lbl_warning = tk.Label(frame_entry, text="Delete error: Customer's ID number (oid) must be a valid number.",
                               bg=clr2, fg="red")
        lbl_warning.grid(row=5, column=0, columnspan=2)
        raise Exception("Delete error: Customer's ID number (oid) must be a valid number.")

    oid = int(entry_oid.get())
    # Delete record by oid in db
    execute_query("""
            DELETE FROM ms_customers WHERE oid=:oid
            """, {"oid": oid})

    # Clear the entry
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_phone_number.delete(0, tk.END)
    entry_oid.delete(0, tk.END)

    # Delete row in display table
    global tbl_ms_customers
    tbl_ms_customers.treeview.delete((oid-1,))

    # Re-display db
    display_db()


def clear_entry():
    global lbl_warning
    lbl_warning.destroy()
    # Clear the entry
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_phone_number.delete(0, tk.END)
    entry_oid.delete(0, tk.END)


def prefilled_entry():
    # Check if mandatory entries are already filled
    global lbl_warning
    lbl_warning.destroy()
    if len(entry_oid.get()) == 0:
        lbl_warning = tk.Label(frame_entry, text="Prefilled error: Customer's ID number (oid) must be filled.",
                               bg=clr2, fg="red")
        lbl_warning.grid(row=5, column=0, columnspan=2)
        raise Exception("Prefilled error: Customer's ID number (oid) must be filled.")
    elif not entry_oid.get().isnumeric():
        lbl_warning = tk.Label(frame_entry, text="Prefilled error: Customer's ID number (oid) must be a valid number.",
                               bg=clr2, fg="red")
        lbl_warning.grid(row=5, column=0, columnspan=2)
        raise Exception("Prefilled error: Customer's ID number (oid) must be a valid number.")

    get_record = execute_query("""
    SELECT oid, first_name, last_name, address, phone_number FROM ms_customers WHERE oid=:oid
    """, {"oid": int(entry_oid.get())})[0]
    # print(get_record)

    clear_entry()

    # Fill entries with each corresponding data
    entry_oid.insert(0, get_record[0])
    entry_first_name.insert(0, get_record[1])
    entry_last_name.insert(0, get_record[2])
    entry_address.insert(0, get_record[3])
    entry_phone_number.insert(0, get_record[4])


def update_record():
    # Check if mandatory entries are already filled
    global lbl_warning
    lbl_warning.destroy()
    if len(entry_oid.get()) == 0:
        lbl_warning = tk.Label(frame_entry, text="Update error: Customer's ID number (oid) must be filled.",
                               bg=clr2, fg="red")
        lbl_warning.grid(row=5, column=0, columnspan=2)
        raise Exception("Update error: Customer's ID number (oid) must be filled.")
    elif not entry_oid.get().isnumeric():
        lbl_warning = tk.Label(frame_entry, text="Update error: Customer's ID number (oid) must be a valid number.",
                               bg=clr2, fg="red")
        lbl_warning.grid(row=5, column=0, columnspan=2)
        raise Exception("Update error: Customer's ID number (oid) must be a valid number.")

    oid = int(entry_oid.get())
    # Get current timestamp unix
    modified_date = execute_query(""" SELECT unixepoch('now'); """)[0][0]
    # Update record by oid in db
    execute_query("""
    UPDATE ms_customers SET 
        first_name = :first_name,
        last_name = :last_name,
        address = :address,
        phone_number = :phone_number,
        modified_date = :modified_date
    WHERE oid=:oid
    """, {
        "oid": oid,
        "first_name": entry_first_name.get(),
        "last_name": entry_last_name.get(),
        "address": entry_address.get(),
        "phone_number": entry_phone_number.get(),
        "modified_date": modified_date
    })

    # Clear the entry
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_phone_number.delete(0, tk.END)
    entry_oid.delete(0, tk.END)

    # Delete row in display table
    global tbl_ms_customers
    tbl_ms_customers.treeview.delete((oid-1,))

    # Re-display db
    display_db()




# ------------------------------------------------------------------------------------------------------------------
# Initialization
init_db()
# Color pallete variable: (#015344, #f4cd00, #d1bb09, #aeaa13, #8b981d)
clr1 = "#225245"
clr2 = "#e9cb44"
clr3 = "#6e7f44"
clr3_t2 = "#55447F"
clr3_t1 = "#447F72"
clr3_t3 = "#7F4451"
font1 = ("Arial", 12)
font2 = ("Lucida Sans", 10)

# Root window
root = tk.Tk()
root.title("Minishopp - Customer Relationship Management")
icon = tk.PhotoImage(file="./supplementary/shop_management/minishopp-icon.png")
root.iconphoto(True, icon)
root.geometry("1024x800")
root.configure(background=clr1)

# Load Minishopp logo
logo = ImageTk.PhotoImage(Image.open("./supplementary/shop_management/minishopp.png"))
logo_label = tk.Label(root, image=logo, background=clr1)
logo_label.pack()


# Create table list of products
ms_customers_cols = ("oid", "first_name","last_name","address","phone_number","modified_date")
tbl_ms_customers = TreeviewFrame(width=20)
tbl_ms_customers.treeview.config(show="headings", columns=ms_customers_cols)
for col in ms_customers_cols:
    tbl_ms_customers.treeview.column(col, anchor=tk.CENTER)
    tbl_ms_customers.treeview.heading(col, text=col)
tbl_ms_customers.treeview.column('oid', width=50)

display_db()


# Create frame for entry new data
frame_entry = tk.LabelFrame(root, bg=clr2, border=True)
frame_entry.pack(pady=50)
frame_btn = tk.LabelFrame(frame_entry, bg=clr2, borderwidth=False)

# Create entry to input new customer data
lbl_first_name = tk.Label(frame_entry, text="First Name", anchor=tk.W, font=font1, justify='left', width=20, bg=clr2)
lbl_first_name.grid(row=0, column=0, sticky=tk.W, pady=5)
lbl_last_name = tk.Label(frame_entry, text="Last Name", anchor=tk.W, font=font1, justify='left', width=20, bg=clr2)
lbl_last_name.grid(row=1, column=0, sticky=tk.W, pady=5)
lbl_address = tk.Label(frame_entry, text="Address", anchor=tk.W, font=font1, justify='left', width=20, bg=clr2)
lbl_address.grid(row=2, column=0, sticky=tk.W, pady=5)
lbl_phone_number = tk.Label(frame_entry, text="Phone Number", anchor=tk.W, font=font1, justify='left', width=20, bg=clr2)
lbl_phone_number.grid(row=3, column=0, sticky=tk.W, pady=5)
lbl_oid = tk.Label(frame_entry, text="ID number", anchor=tk.W, font=font1, justify='left', width=20, bg=clr2)
lbl_oid.grid(row=4, column=0, sticky=tk.W, pady=5)
entry_first_name = tk.Entry(frame_entry, width=50, font=font1)
entry_first_name.grid(row=0, column=1, sticky=tk.W, padx=5)
entry_last_name = tk.Entry(frame_entry, width=50, font=font1)
entry_last_name.grid(row=1, column=1, sticky=tk.W, padx=5)
entry_address = tk.Entry(frame_entry, width=50, font=font1)
entry_address.grid(row=2, column=1, sticky=tk.W, padx=5)
entry_phone_number = tk.Entry(frame_entry, width=50, font=font1)
entry_phone_number.grid(row=3, column=1, sticky=tk.W, padx=5)
entry_oid = tk.Entry(frame_entry, width=50, font=font1)
entry_oid.grid(row=4, column=1, sticky=tk.W, padx=5)

frame_btn.grid(row=6, column=0, columnspan=2, pady=10)

btn_input = tk.Button(frame_btn, text="Insert New Record", font=font2, bg=clr3, width=45, command=input_record)
btn_input.grid(row=0, column=1, columnspan=2, padx=10, pady=5)
btn_clear = tk.Button(frame_btn, text="Clear Entry", font=font2, bg=clr3, width=20, command=clear_entry)
btn_clear.grid(row=0, column=0, padx=10)
btn_prefilled = tk.Button(frame_btn, text="Get Prefilled Entry by ID", font=font2, bg=clr3_t1, width=20, command=prefilled_entry)
btn_prefilled.grid(row=1, column=0, padx=10)
btn_update = tk.Button(frame_btn, text="Update Record by ID", font=font2, bg=clr3_t1, width=20, command=update_record)
btn_update.grid(row=1, column=1, padx=10)
btn_delete = tk.Button(frame_btn, text="Delete Record by ID", font=font2, bg=clr3_t2, width=20, command=delete_record)
btn_delete.grid(row=1, column=2, padx=10)

global lbl_warning
lbl_warning = tk.Label(frame_entry, text=".", bg=clr2, fg="red")

# print(tbl_ms_customers.treeview.item(1))
# print(tbl_ms_customers.treeview.get_children())

root.mainloop()