
from tkinter import *
import mysql.connector
from mysql.connector import Error

root = Tk()
root.geometry("900x600")

def btn_delete_cord(id):
    print(id)

## get parking slot coordinates from db
def getCordData():
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='parking',
                                            user='root',
                                            password='')
        sql_select_Query = "select * from slots"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        print("Total number of rows in Laptop is: ", cursor.rowcount)
        print("\nPrinting each laptop record")

        return records
        # for row in records:
        #     print("Id = ", row[0], )
        #     print("Name = ", row[1])
        #     print("Coordinates  = ", row[2], "\n")
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")


left = Frame(root, borderwidth=2, relief="solid")
right = Frame(root, borderwidth=2, relief="solid")
container = Frame(left, borderwidth=2, relief="solid")
box1 = Listbox(right, borderwidth=2, relief="solid")
box2 = Frame(right, borderwidth=2, relief="solid")

label1 = Label(container, text="I could be a canvas, but I'm a label right now")
label2 = Label(left, text="I could be a button")
label3 = Label(left, text="So could I")

x = 0
cordinates = getCordData()
for row in cordinates:
    cordinateItem = Frame(box1, relief="solid")
    cordinateItem.grid_rowconfigure(9, weight=1)
    cordinateItem.grid_columnconfigure(4, weight=1)

    label4 = Label(cordinateItem, text=row[1], height=2).grid(row=x, column=0, columnspan=2, padx=5, pady=5)
    #label4 = Label(cordinateItem, text=row[2]).grid(row=x, column=2, columnspan=2, padx = 0, pady = 1)
    btnRemove = Button(cordinateItem, text="Delete", cursor="hand2", command= lambda: btn_delete_cord(row[0])).grid(row=x, column=4, columnspan=1, padx=5, pady=5)
    cordinateItem.pack(expand=True, fill="both")
    x = x + 1

## 
label5 = Label(box2, text="I could be your setup window")

left.pack(side="left", expand=True, fill="both")
right.pack(side="right", expand=True, fill="both")
container.pack(expand=True, fill="both", padx=5, pady=5)
box1.pack(fill="both", padx=1, pady=1)
box2.pack(expand=True, fill="both", padx=10, pady=10)

label1.pack()
label2.pack()
label3.pack()
#label4.pack()
label5.pack()

root.mainloop()