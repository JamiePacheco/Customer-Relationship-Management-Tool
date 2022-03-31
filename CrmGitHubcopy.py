#Import the libraries used in the program
from tkinter import *
from tkinter import ttk
import sqlite3
from sqlite3.dbapi2 import Cursor, connect
from tkinter import messagebox
from tkinter import colorchooser

#Creating the root window and configuring it
root = Tk()
root.title("Customer Service Application")
root.geometry("1000x500")

# Databasew setup
con = sqlite3.connect("Tree_crm.db")

#Create a cursor instance
cur = con.cursor()

#Create Table
cur.execute("""CREATE TABLE if not exists customers (

    first_name text,
    last_name text,
    ID integer,
    Address text,
    city text,
    state text,
    zipcode text
    )
    """)

#Add dummy data
for record in data:
    con.execute("INSERT INTO customers VALUES (:first_name, :last_name, :ID, :Address, :city, :state, :zipcode)",
        {
            "first_name": record[0],
            "last_name": record[1],
            "ID": record[2],
            "Address": record[3],
            "city": record[4],
            "state": record[5],
            "zipcode": record[6]
        }
        )


#Save changes
con.commit()

#Close the connection
con.close()

#Function to query the db at certain intervals
def query_database():

    #Loop throuhg the records in the tree view 
    for record in my_tree.get_children():
        #Delete the record in thge tree view
        my_tree.delete(record)

    #Connect to the db
    con = sqlite3.connect("Tree_crm.db")

    #Create a cursor of the db
    cur = con.cursor()

    #Select all of the rows of the table
    cur.execute("SELECT rowid, * FROM customers")
    #Fetch all of the information  
    records = cur.fetchall()
   
    #Set the count variable to global and declare it to 0
    global count
    count = 0

    #Loop through the records list
    for record in records:
        #If count is divisable by 2 then it is inserted with the even style
        if count % 2 == 0:
            my_tree.insert(parent="", index = "end", iid = count, text = '', values = (record[1],record[2],record[0],record[4],record[5],record[6],record[7],), tags = ("evenrow",))
        #If count isn't divisable by 2 then it is inserted with the odd style
        else:
            my_tree.insert(parent="", index = "end", iid = count, text = '', values = (record[1],record[2],record[0],record[4],record[5],record[6],record[7],), tags = ("oddrow",))
        count += 1

#Create a variable as a style widget
style = ttk.Style()

#Set the theme of the stlye as default
style.theme_use("default")

#Configure the tree view widget with the charactersitcs set
style.configure("Treeview",
    background="#D3D3D3",
    foreground = "black",
    rawheight = 25,
    fieldbackground = "#D3D3D3")

#Map the treeview to when a thing is selected the highlighted color is the hexadecimal color
style.map("Treeview",
    background = [("selected", "#347083")])

#Make a frame and pack it
Tree_Frame = Frame(root)
Tree_Frame.pack(pady=10)

#Makes a scroll bar for the tree view
Tree_Scroll = Scrollbar(Tree_Frame)
Tree_Scroll.pack(side = RIGHT , fill = Y)

#Make a treeview widget inside tree frame and set the yscrollcommand to the tree scroll bar widget 
my_tree = ttk.Treeview(Tree_Frame, yscrollcommand=Tree_Scroll.set)
my_tree.pack()

#Configure the command of the scroll bar
Tree_Scroll.config(command = my_tree.yview)

#Sets the columns to the database columns
my_tree["columns"] = ("First Name", "Last Name", "ID", "Address", "City", "State", "Zipcode")

#Configures the tree view columns
my_tree.column("#0", width = 0, stretch=NO)
my_tree.column("First Name", width = 150, anchor=W)
my_tree.column("Last Name", width =150, anchor=W)
my_tree.column("ID", width = 100,anchor=CENTER)
my_tree.column("Address", width = 140, anchor = CENTER)
my_tree.column("City", width = 140,anchor=CENTER)
my_tree.column("State", width = 140,anchor=CENTER)
my_tree.column("Zipcode", width = 140,anchor=CENTER)

#Changes the headings of the columns
my_tree.heading("#0", text = '', anchor = W)
my_tree.heading("First Name", text = 'First Name', anchor = W)
my_tree.heading("Last Name", text = 'Last Name', anchor = CENTER)
my_tree.heading("ID", text = 'ID', anchor = CENTER)
my_tree.heading("Address", text = 'Address', anchor = CENTER)
my_tree.heading("City", text = 'City', anchor = CENTER)
my_tree.heading("State", text = 'State', anchor = CENTER)
my_tree.heading("Zipcode", text = 'Zipcode', anchor = CENTER)

#Make tags for the rows and change the background for them
my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")

#Move row up
def record_up():
    #Sets the rows to the selected row
    rows = my_tree.selection()

    #Loops through the selected row
    for row in rows:
        #Moves the row up one
        my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)

#Move row down
def record_down():
    #Sets the row to the selected row
    rows = my_tree.selection()

    #Loops through the rows revered
    for row in reversed(rows):
        #Moves the row up one in the tree
        my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)

#select record command
def selected_record(e):
    #clear entry boxes
    fn_Entry.delete(0, END)
    ln_Entry.delete(0, END)
    ID_Entry.delete(0, END)
    Address_Entry.delete(0, END)
    City_Entry.delete(0, END)
    State_Entry.delete(0, END)
    Zipcode_Entry.delete(0, END)

    #Grab record Number
    selected = my_tree.focus()
    #Grab record values
    values = my_tree.item(selected, "values")

    #clear entry boxes
    fn_Entry.insert(0, values[0])
    ln_Entry.insert(0, values[1])
    ID_Entry.insert(0, values[2])
    Address_Entry.insert(0, values[3])
    City_Entry.insert(0, values[4])
    State_Entry.insert(0, values[5])
    Zipcode_Entry.insert(0, values[6])

def clear_record():
    #clear entry boxes
    fn_Entry.delete(0, END)
    ln_Entry.delete(0, END)
    ID_Entry.delete(0, END)
    Address_Entry.delete(0, END)
    City_Entry.delete(0, END)
    State_Entry.delete(0, END)
    Zipcode_Entry.delete(0, END)

#Remove selected record
def remove_record():
    #Gets the selected index row
    x = my_tree.selection()[0]

    #connects to the db
    con = sqlite3.connect("Tree_crm.db")

    #Creats a cursor object
    cur = con.cursor()

    #Deletes record where the oid equal the ID
    cur.execute(f"DELETE from customers where oid=({ID_Entry.get()})")

    #Clears the entry boxes
    clear_record()

    #Commits the changes to the db
    con.commit()

    #Closes the connection to the server
    con.close()

    #Deletes the index from the tree
    my_tree.delete(x)

    #Shows a message box for deleted record
    messagebox.showinfo("Deleted", "Record has been deleted")

#remove many records
def remove_many_records():

    #Checks if user wants to delete record
    response = messagebox.askyesno("Delete Records", "This will delete everything selected from the table. Are you sure?")

    #If response is one code runs ele passes
    if response == 1:

        #Sets x to the selected
        x = my_tree.selection()

        #Opens connection to db
        con = sqlite3.connect("Tree_crm.db")

        #Creates a cursor object
        cur = con.cursor()

        #can also use cur.executemany to delete the commands
        #Runs loop on the selected
        for record in x:
            #Gets id of the item tree
            id = my_tree.item(record, "values")[2]
            #Deletes it from the ID
            cur.execute(f"DELETE from customers where oid=({id})")

        #Loops through the selected and deletes it from tree view
        for record in x:
            my_tree.delete(record)

        #commits the changes
        con.commit()

        #Closes the connection
        con.close()

#remove all records
def remove_all_records():

    #Displays message box to user for yes or no
    response = messagebox.askyesno("Delete all Records", "This will delete everything from the table. Are you sure?")

    #If response is 1 then code runs else it passes
    if response == 1:

        #Runs loop through tree records
        for record in my_tree.get_children():
            #deletes the records from the tree
            my_tree.delete(record)

        #Connects to the db
        con = sqlite3.connect("Tree_crm.db")

        #Creates a cursor object
        cur = con.cursor()

        #Drops the table from the customers db
        cur.execute(f"DROP TABLE customers")

        #Clears entries
        clear_record()

        #Commits changes to the db
        con.commit()

        #Closes the connection
        con.close()

        #Deletes the records in the treeview
        for record in my_tree.get_children():
            my_tree.delete(record)

        #displas message box that table was deleted
        messagebox.showinfo("Deleted", "Database has been deleted")

        #Creates the table
        create_table_again()
    else:
        pass
 

#Update the record
def update_record():
    #Get the selected record
    selected = my_tree.focus()

    #Creates connection to the db
    con = sqlite3.connect("tree_crm.db")

    #Creates a cursor object
    cur = con.cursor()

    #Updates the db
    cur.execute("""UPDATE customers SET
        first_name = :first,
        last_name = :last,
        address = :address,
        city = :city,
        state = :state,
        zipcode = :zipcode

        WHERE oid = :oid""",
        {
            "first": fn_Entry.get(),
            "last": ln_Entry.get(),
            "address": Address_Entry.get(),
            "city": City_Entry.get(),
            "state": State_Entry.get(),
            "zipcode": Zipcode_Entry.get(),
            "oid": ID_Entry.get()
        }
        )

    #Commits changes
    con.commit()

    #closes the connection
    con.close()

    #updates the value of the record inside of the db
    my_tree.item(selected, text = "", values=(fn_Entry.get(), ln_Entry.get(), ID_Entry.get(), Address_Entry.get(), City_Entry.get(), State_Entry.get(), Zipcode_Entry.get()),)

    #Clears the entry boxes
    clear_record()

def add_record_command():

    con = sqlite3.connect("Tree_crm.db")

    cur = con.cursor()

    cur.execute("INSERT INTO customers VALUES (:first, :last, :id, :address, :city, :state, :zipcode)",
        {
            "first": fn_Entry.get(),
            "last": ln_Entry.get(),
            "id": ID_Entry.get(),
            "address": Address_Entry.get(),
            "city": City_Entry.get(),
            "state": State_Entry.get(),
            "zipcode": Zipcode_Entry.get(),
        }
        )

    con.commit()

    con.close()

    fn_Entry.delete(0, END)
    ln_Entry.delete(0, END)
    ID_Entry.delete(0, END)
    Address_Entry.delete(0, END)
    City_Entry.delete(0, END)
    State_Entry.delete(0, END)
    Zipcode_Entry.delete(0, END)

    #clear the tree view
    my_tree.delete(*my_tree.get_children())

    query_database()

def create_table_again():
    con = sqlite3.connect("Tree_crm.db")

    #Create a cursor instance
    cur = con.cursor()

    #Create Table
    cur.execute("""CREATE TABLE if not exists customers (

        first_name text,
        last_name text,
        ID integer,
        Address text,
        city text,
        state text,
        zipcode text
        )
        """)

def Primary_color():
    PrimaryColor = colorchooser.askcolor()
    if PrimaryColor:
        my_tree.tag_configure('evenrow', background=PrimaryColor[1])
 
def Secondary_color():
    SecondaryColor = colorchooser.askcolor()
    if SecondaryColor:
        my_tree.tag_configure('oddrow', background=SecondaryColor[1])

def Highlight_color():
    HighlightColor = colorchooser.askcolor()

    if HighlightColor:
        style.map("Treeview",background = [("selected", HighlightColor[1])])

def search_record(data, criteria):

    Search.destroy()

    con = sqlite3.connect("Tree_crm.db")

    cur = con.cursor()
    cur.execute(f"SELECT rowid, * FROM customers WHERE {criteria} like ?", (str(data),))
    records = cur.fetchall()
 
    for record in my_tree.get_children():
        my_tree.delete(record)

    global count
    count = 0
    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent="", index = "end", iid = count, text = '', values = (record[1],record[2],record[0],record[4],record[5],record[6],record[7],), tags = ("evenrow",))
        else:
            my_tree.insert(parent="", index = "end", iid = count, text = '', values = (record[1],record[2],record[0],record[4],record[5],record[6],record[7],), tags = ("oddrow",))
        count += 1

    con.commit()

    con.close()

def search(field):

    global Search

    Search = Toplevel(root)
    Search.title("Record Search")
    Search.geometry("200x150")

    search_frame = LabelFrame(Search, text="Record Criteria")
    search_frame.pack(padx=10, pady=10)

    search_entry = Entry(search_frame)
    search_entry.pack(pady=10, padx=20)

    search_button = Button(search_frame, text = "Search", command = lambda: search_record(search_entry.get(), field))
    search_button.pack(padx=10, pady=20)

#Frame for the Data Labels and Entries

data_frame = LabelFrame(root, text = "Record")
data_frame.pack(fill = "x", expand = "yes", padx = 20)

fn_label = Label(data_frame, text = "First Name")
fn_label.grid(row = 0, column=0, padx=10, pady=10)
fn_Entry = Entry(data_frame)
fn_Entry.grid(row = 0, column=1, padx=10, pady=10)

ln_label = Label(data_frame, text = "Last Name")
ln_label.grid(row = 0, column=2, padx=10, pady=10)
ln_Entry = Entry(data_frame)
ln_Entry.grid(row = 0, column=3, padx=10, pady=10)

ID_label = Label(data_frame, text = "ID")
ID_label.grid(row = 0, column=4, padx=10, pady=10)
ID_Entry = Entry(data_frame)
ID_Entry.grid(row = 0, column=5, padx=10, pady=10)

Address_label = Label(data_frame, text = "Address")
Address_label.grid(row = 1, column=0, padx=10, pady=10)
Address_Entry = Entry(data_frame)
Address_Entry.grid(row = 1, column=1, padx=10, pady=10)

City_label = Label(data_frame, text = "City")
City_label.grid(row = 1, column=2, padx=10, pady=10)
City_Entry = Entry(data_frame)
City_Entry.grid(row = 1, column=3, padx=10, pady=10)

State_label = Label(data_frame, text = "State")
State_label.grid(row = 1, column=4, padx=10, pady=10)
State_Entry = Entry(data_frame)
State_Entry.grid(row = 1, column=5, padx=10, pady=10)

Zipcode_label = Label(data_frame, text = "Zipcode")
Zipcode_label.grid(row = 1, column=6, padx=10, pady=10)
Zipcode_Entry = Entry(data_frame)
Zipcode_Entry.grid(row = 1, column=7, padx=10, pady=10)

#Frame for the command buttons
Button_Frame = LabelFrame(root, text = "Commands")
Button_Frame.pack(fill="x", expand="yes", padx=20)

#Buttons inside of the button frame
update_button = Button(Button_Frame, text="Update Record", command = update_record)
update_button.grid(row = 0, column=0, padx=10, pady=10)

add_button = Button(Button_Frame, text="Add Record",command = add_record_command)
add_button.grid(row = 0, column=1, padx=10, pady=10)

remove_all_button = Button(Button_Frame, text="Remove All Records", command=remove_all_records)
remove_all_button.grid(row = 0, column=2, padx=10, pady=10)

remove_one_button = Button(Button_Frame, text="Remove Record", command = remove_record)
remove_one_button.grid(row = 0, column=3, padx=10, pady=10)

remove_many_button = Button(Button_Frame, text="Remove Records", command = remove_many_records)
remove_many_button.grid(row = 0, column=4, padx=10, pady=10)

move_up_button = Button(Button_Frame, text="Move Record Up", command = record_up)
move_up_button.grid(row = 0, column=5, padx=10, pady=10)

move_down_button = Button(Button_Frame, text="Move Record Down", command = record_down)
move_down_button.grid(row = 0, column=6, padx=10, pady=10)

clear_record_button = Button(Button_Frame, text="Clear Record", command = clear_record)
clear_record_button.grid(row = 0, column=7, padx=10, pady=10)

topmenu = Menu(root)
root.config(menu=topmenu)

Option_menu = Menu(topmenu, tearoff=0)
topmenu.add_cascade(label="Options", menu=Option_menu)

Option_menu.add_command(label="Primary Color", command = Primary_color)
Option_menu.add_command(label="Secondary Color", command = Secondary_color)
Option_menu.add_command(label="Highlight color", command = Highlight_color)
Option_menu.add_separator()
Option_menu.add_command(label="Exit", command = root.quit)

Search_menu = Menu(topmenu, tearoff=0)
topmenu.add_cascade(label = "Search", menu=Search_menu)

Search_menu.add_command(label="Search First Name", command = lambda: search("first_name"))
Search_menu.add_command(label="Search Last Name", command = lambda: search("last_name"))
Search_menu.add_command(label="Search ID", command = lambda: search("ID"))
Search_menu.add_command(label="Search Address", command = lambda: search("Address"))
Search_menu.add_command(label="Search City", command = lambda: search("city"))
Search_menu.add_command(label="Search State", command = lambda: search("state"))
Search_menu.add_command(label="Search Zipcode", command = lambda: search("zipcode"))
S
Search_menu.add_separator()
Search_menu.add_command(label="Reset", command = query_database)

#Bind the treeview
my_tree.bind("<ButtonRelease-1>", selected_record)

#pulls data from database from start
query_database()

root.mainloop()
