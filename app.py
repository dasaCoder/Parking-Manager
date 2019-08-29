
from tkinter import *
import mysql.connector
from mysql.connector import Error
from PIL import ImageTk, Image

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

## load image of parking slot to main canvas
def btn_add_slot(canv):
    image = Image.open("images/girl.jpg")
    image = image.resize((500, 300))
    image = ImageTk.PhotoImage(image)

    #canv.grid(row=2, column=3)
    #canv.create_image(20, 20, anchor=NW, image=image)
    canv.configure(image=image)
    canv.image = image
    canv.pack()



left = Frame(root, borderwidth=2, relief="solid")
right = Frame(root, borderwidth=2, relief="solid")
container = Frame(left, borderwidth=2, relief="solid")
box1 = Listbox(right, borderwidth=2, relief="solid")
box2 = Frame(right, borderwidth=2, relief="solid")

label1 = Label(container)
label2 = Label(left, text="I could be a button")
label3 = Label(left, text="So could I")

# image = Image.open("images/girl.png")
# image = image.resize((500, 300))
# image = ImageTk.PhotoImage(image)
# l=Label(container,image=image)
# l.pack()
canv = Canvas(container, width=500, height=300, bg='white')

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
box2.grid_columnconfigure(6, weight=1)
label5 = Label(box2, text="Controls").grid(row=0, column=0)
lable6 = Label(box2, text="Add new parking slot").grid(row=1, column=0, columnspan=3, padx=5, pady=5)
btnAddCord = Button(box2, text= "Add Slot", cursor= "hand2", command= lambda: btn_add_slot(label1)).grid(row=1, column=3, padx=5, pady=5)

left.pack(side="left", expand=True, fill="both")
right.pack(side="right", expand=True, fill="both")
container.pack(expand=True, fill="both", padx=5, pady=5)
box1.pack(fill="both", padx=1, pady=1)
box2.pack(expand=True, fill="both", padx=10, pady=10)

#label1.pack()
label2.pack()
label3.pack()

root.mainloop()