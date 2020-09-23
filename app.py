
from tkinter import *
import mysql.connector
from mysql.connector import Error
from PIL import ImageTk, Image
import json

import cv2  
import imutils
from imutils import perspective 
from imutils.video import count_frames
import numpy as np
from matplotlib import pyplot as plt 
import time
from ferramentas import image_utils
from svm import SVM
import datetime

root = Tk()
root.geometry("800x400")

path = 'videos/p2.mp4'
vs = cv2.VideoCapture(path)

# hold new cords of slot
new_slot = []

#update gui
def updateDeleteSlot(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    cordinates = getCordData()

    for row in cordinates:
        cordinateItem = Frame(box1, relief="solid")
        cordinateItem.grid_rowconfigure(9, weight=1)
        cordinateItem.grid_columnconfigure(4, weight=1)

        Label(cordinateItem, text=row[1], height=2).grid(row=x, column=0, columnspan=2, padx=5, pady=5)
        Button(cordinateItem, text="Delete", cursor="hand2", command= lambda: btn_delete_slot(row[0],box1)).grid(row=x, column=4, columnspan=1, padx=5, pady=5)
        cordinateItem.pack(expand=True, fill="both")

def btn_delete_slot(id,frame):
    print(id)
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='parking',
                                            user='dbuser',
                                            password='123')
        sql_select_Query =  "DELETE FROM `slots` WHERE `slots`.`id` = "+ str(id)
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)

        updateDeleteSlot(frame)

    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

## get parking slot coordinates from db
def getCordData():
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='parking',
                                            user='dbuser',
                                            password='123')
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

def btn_add_slot(name):
    print(name)
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='parking',
                                            user='dbuser',
                                            password='123')
        sql_select_Query = "INSERT INTO `slots` (`name`, `slot`) VALUES ('"+ name +"', '"+ json.dumps(new_slot[-4:]) +"');"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)

        updateDeleteSlot(box1)

    except Error as e:
        print("Error adding data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

## load image of parking slot to main canvas
def loadParkingImage(canv):
    image = Image.open("images/slot.png")
    image = image.resize((450,250))
    image = ImageTk.PhotoImage(image)

    #canv.grid(row=2, column=3)
    #canv.create_image(20, 20, anchor=NW, image=image)
    canv.configure(image=image)
    canv.image = image
    canv.pack()

## check whether the given value is minimun in array
def checkMinimum(list1, val): 
      
    # traverse in the list 
    for x in list1: 
  
        # compare with all the values 
        # with val 
        if val>= x: 
            return False 
    return True

## update status window
def updateStatusWindow(message, color):
    print("update status")
    for item in statusWindow.winfo_children():
        item.destroy()

    Label(statusWindow, text=message, bg=color, fg="white", height=2,width=50).pack(fill=BOTH, expand=1)
    statusWindow.pack()
    root.update()

def generateVideo(boxes, statusWindow):
    path = 'videos/p2.mp4'
    vs = cv2.VideoCapture(path)
    fps = 12
    capSize = (640,360)

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    out = cv2.VideoWriter()
    success = out.open('./teste5.mp4',fourcc,fps,capSize,True)

    num_frames = count_frames(path)
    #print(num_frames)

    get_point = 0  
    i = 0 

    try:
        while i < num_frames:
            ret, frame = vs.read()

            frame = imutils.resize(frame, width=450)  

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #cv2.imshow("gray ", gray )

            gau = cv2.GaussianBlur(gray, (7, 7), 0)

            img_resize = image_utils.getRotateRect(gau, boxes)
            feature = image_utils().extract_features(img_resize)

            timestamp = datetime.datetime.now()

            score = SVM().predict(feature)

            available_slots = []

            for index,scr in enumerate(score):
                if scr == 0: 
                    cv2.polylines(frame,np.int32([boxes[index]]), True ,(0,0,255),2  )
                    s = False
                    i = 0
                else:
                    ## if the parking slot is availble

                    slot_first_x_cord = float(boxes[index][1][0])

                    if(checkMinimum(available_slots, slot_first_x_cord)):
                        cv2.polylines(frame,np.int32([boxes[index]]),True,(255,0,0), 2)

                        if s == False:
                            cv2.putText(frame, timestamp.strftime(" Available: %d %m %Y %I:%M:%S"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,0,0),2)

                            i += 1
                            if i > 100: 
                                s = True
                    
                    else:
                        cv2.polylines(frame,np.int32([boxes[index]]),True,(0,255,0), 2)

                        if s == False:
                            cv2.putText(frame, timestamp.strftime(" Available: %d %m %Y %I:%M:%S"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,255,0),2)
                            i += 1
                            if i > 100: 
                                s = True 

                    msg = "Parking slots are available "
                    clr = 'green'
                    updateStatusWindow(msg,clr)                   

                    available_slots.append(slot_first_x_cord)

            if not available_slots:
                msg = "Parking slots are not available " 
                clr = 'red'
                updateStatusWindow(msg,clr)     

            cv2.imshow("frame", frame)

            key = cv2.waitKey(10) & 0xFF

            if key == ord("q"):
                break

            if key == ord('p'):
                hist = cv2.calcHist([a[1]], [0], None, [256], [0,256])
                plt.plot(hist)
                plt.show()


            i += 1 
    except KeyboardInterrupt:
        pass

def loadVideo(statusWindow):
    c = getCordData()
    y = 0
    b = []
    for r in c:
        b.append(np.array(json.loads(r[2])))
    
    generateVideo(b,statusWindow)

left = Frame(root, borderwidth=2, relief="solid")
right = Frame(root, borderwidth=2, relief="solid")
container = Frame(left, borderwidth=2, relief="solid")

statusWindow = Frame(right, borderwidth=2, relief="solid")
statusWindow.pack()
box1 = Listbox(right, borderwidth=2, relief="solid")
box2 = Frame(right, borderwidth=2, relief="solid")

label2 = Label(left, text="Parking Management System",  font = (30)).pack()
label3 = Label(left, text="Project of MIT kelaniya").pack()
#label1 = Label(container)

canv = Canvas(container, width=500, height=300, bg='white')

x = 0
boxes = []
cordinates = getCordData()
for row in cordinates:
    cordinateItem = Frame(box1, relief="solid")
    cordinateItem.grid_rowconfigure(9, weight=1)
    cordinateItem.grid_columnconfigure(4, weight=1)

    Label(cordinateItem, text=row[1], height=2).grid(row=x, column=0, columnspan=2, padx=5, pady=5)
    #label4 = Label(cordinateItem, text=row[2]).grid(row=x, column=2, columnspan=2, padx = 0, pady = 1)
    Button(cordinateItem, text="Delete", cursor="hand2", command= lambda: btn_delete_slot(row[0],box1)).grid(row=x, column=4, columnspan=1, padx=5, pady=5)
    cordinateItem.pack(expand=True, fill="both")
    #print(row[2])
    boxes.append(np.array(json.loads(row[2])))
    x = x + 1

## 
box2.grid_columnconfigure(6, weight=1)

label5 = Label(box2, text="Controls").grid(row=0, column=0)

lable6 = Label(box2, text="Add new parking slot").grid(row=1, column=0, columnspan=3, padx=5, pady=5)
txtSlotName = Entry(box2)
txtSlotName.grid(row=1, column=3, columnspan=1, padx=5, pady=5)
btnAddCord = Button(box2, text= "Add Slot", cursor= "hand2", command= lambda: btn_add_slot(txtSlotName.get())).grid(row=1, column=4, padx=5, pady=5)

# lable6 = Label(box2, text="Reset new parking slot Coordinates").grid(row=2, column=0, columnspan=3, padx=5, pady=5)
# btnAddCord = Button(box2, text= "Reset", cursor= "hand2", command= lambda: btn_reset_slot()).grid(row=2, column=3, padx=5, pady=5)

lable6 = Label(box2, text="Open Monitor").grid(row=2, column=0, columnspan=3, padx=5, pady=5)
btnAddCord = Button(box2, text= "Open", cursor= "hand2", command= lambda: loadVideo(statusWindow)).grid(row=2, column=3, padx=5, pady=5)


left.pack(side="left", expand=True, fill="both")
right.pack(side="right", expand=True, fill="both")
container.pack(expand=True, fill="both", padx=5, pady=5)
box1.pack(fill="both", padx=1, pady=1)
box2.pack(expand=True, fill="both", padx=10, pady=10)

#print(boxes)
#generateVideo(boxes)

frame = Frame(container, bd=2, relief=SUNKEN)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
xscroll = Scrollbar(frame, orient=HORIZONTAL)
xscroll.grid(row=1, column=0, sticky=E+W)
yscroll = Scrollbar(frame)
yscroll.grid(row=0, column=1, sticky=N+S)
canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set,width=450)
canvas.grid(row=0, column=0, sticky=N+S+E+W)
xscroll.config(command=canvas.xview)
yscroll.config(command=canvas.yview)
frame.pack(fill=BOTH,expand=1)


img = ImageTk.PhotoImage(Image.open("images/slot.png"))
canvas.create_image(0,0,image=img,anchor="nw")
canvas.config(scrollregion=canvas.bbox(ALL))

#function to be called when mouse is clicked
def printcoords(event):
    #outputting x and y coords to console
    cord = [event.x,event.y]
    updateSlot(cord)

def updateSlot(cord):
    new_slot.append(cord)
    print(new_slot)

#mouseclick event
canvas.bind("<Button 1>",printcoords)

root.mainloop()