
from tkinter import *
import mysql.connector
from mysql.connector import Error
from PIL import ImageTk, Image

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

def generateVideo():
    path = 'videos/p2.mp4'
    vs = cv2.VideoCapture(path)
    fps = 12
    capSize = (640,360)
    #capSize = (1920,1080)
    #fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter()
    success = out.open('./teste5.mp4',fourcc,fps,capSize,True)

    num_frames = count_frames(path)
    print(num_frames)

    get_point = 0  
    i = 0 

    while i < num_frames:
        ret, frame = vs.read()

        frame = imutils.resize(frame, width=450)  

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("gray ", gray )

        gau = cv2.GaussianBlur(gray, (7, 7), 0)
        #cv2.imshow("gau ", gau )

        
        # Not work yet

        if get_point == True:
            number_of_places = 2 # Defini o numero de vagas que voce ira selecionar 
            boxes = image_utils.getSpotsCoordiantesFromImage(frame, number_of_places)
            boxes = asarray(boxes)
            print(boxes)
            check = False

        else:
            box1 = np.array([(130.14516129032256, 226.74999999999994), (85.68951612903224, 223.12096774193543), (121.97983870967742, 175.0362903225806), (155.5483870967742, 179.57258064516125)])       
            box2 = np.array ([(137.4032258064516, 225.84274193548384), (166.43548387096774, 173.22177419354836), (210.89112903225805, 177.758064516129), (196.375, 226.74999999999994)])
            
            boxes = [box1, box2]
        #print('afdasdf')
        #print(box1[0].shape)

        img_resize = image_utils.getRotateRect(gau, boxes)
        feature = image_utils().extract_features(img_resize)

        '''feature1 = feature.reshape(-1, 1)
        score0 = SVM().predict(feature1)
        score1 = SVM().predict(feature[1])

        print (score0, score1)'''
        timestamp = datetime.datetime.now()

        score = SVM().predict(feature)

        if score[0] == 0: 
            cv2.polylines(frame,np.int32([box1]), True ,(0,0,255),2  )
            saida = False
            i = 0

            

        else:
            cv2.polylines(frame,np.int32([box1]),True,(0,255,0), 2)

            if saida == False:
                cv2.putText(frame, timestamp.strftime(" Saida as: %d %m %Y %I:%M:%S"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0),2)
                i += 1
                if i > 100: 
                    saida = True


        if score[1] == 0: 
            cv2.polylines(frame,np.int32([box2]), True ,(0,0,255),2  )
            


        else:
            cv2.polylines(frame,np.int32([box2]),True,(0,255,0), 2)
            cv2.putText(frame, timestamp.strftime(" %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 2.35, (0, 0, 255), 5)



        

        cv2.imshow("frame", frame)

        key = cv2.waitKey(1) & 0xFF
        # Se a tecla 'q' for pressionada, finaliza com o loop
        if key == ord("q"):
            break

        if key == ord('p'):
            hist = cv2.calcHist([a[1]], [0], None, [256], [0,256])
            plt.plot(hist)
            plt.show()


        i += 1 


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

generateVideo()

root.mainloop()