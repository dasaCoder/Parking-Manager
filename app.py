
from tkinter import *

root = Tk()
root.geometry("900x600")

def btn_click(id):
    print(id)

left = Frame(root, borderwidth=2, relief="solid")
right = Frame(root, borderwidth=2, relief="solid")
container = Frame(left, borderwidth=2, relief="solid")
box1 = Frame(right, borderwidth=2, relief="solid")
box2 = Frame(right, borderwidth=2, relief="solid")

label1 = Label(container, text="I could be a canvas, but I'm a label right now")
label2 = Label(left, text="I could be a button")
label3 = Label(left, text="So could I")

x = 0
while( x < 10 ):
    cordinateItem = Frame(box1, relief="solid")
    label4 = Label(cordinateItem, text="I could be your image").grid(row=x, column=0, columnspan=2, padx = 0, pady = 1)
    btnRemove = Button(cordinateItem, text="Delete", cursor="hand2", command= lambda: btn_click(1)).grid(row=x, column=3, columnspan=1, padx = 0, pady = 1)
    cordinateItem.pack(expand=True, fill="both")
    x = x + 1

label5 = Label(box2, text="I could be your setup window")

left.pack(side="left", expand=True, fill="both")
right.pack(side="right", expand=True, fill="both")
container.pack(expand=True, fill="both", padx=5, pady=5)
box1.pack(expand=True, fill="both", padx=10, pady=10)
box2.pack(expand=True, fill="both", padx=10, pady=10)

label1.pack()
label2.pack()
label3.pack()
#label4.pack()
label5.pack()

root.mainloop()