# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
from tkinter import *
from threading import Timer
import datetime
now = datetime.datetime.now()
length = []
global fweight
global avglength
def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

    


def scircuit():
    activelab.config(text="Short Circuit!!")
    flelab.config(background='red')
    flevar.config(background='red')
    fwelab.config(background='red')
    fwevar.config(background='red')
    datelab.config(background='red')
    datevar.config(background='red')
    timelab.config(background='red')
    w.config(background='red')
    erlab.config(background='red')
    activelab.config(background='red')
    master.configure(background='red')
    master.after(1000, scircuitcolor)
def scircuitcolor():
    flelab.config(background='white')
    flevar.config(background='white')
    fwelab.config(background='white')
    fwevar.config(background='white')
    datelab.config(background='white')
    datevar.config(background='white')
    timelab.config(background='white')
    w.config(background='white')
    erlab.config(background='white')
    activelab.config(background='white')
    master.configure(background='white')
    master.config(background='white')
    master.after(1000, scircuit)
#defining the feeding system
#turning on the feeding relay
#time on is dependent on the weight of the fish
def feeder():
    activelab.config(text="Feeding...")
    avglength = np.mean(length)
    fweight = 0.0065*avglength**(3.157)
    master.after(int(fweight), feedfinish)
#turning the feeding relay off
def feedfinish():
    activelab.config(text="Working!")

#constructing the gui
#declering the master window
master = Tk() 
#declering labels
flelab = Label(master, text='Fish Length:',  font=("Arial", 36))
#declering the location of the labels
flelab.grid(row=0) 
flevar = Label(master, text='Waiting...', font=("Arial", 36))
flevar.grid(row=0,column=1) 
fwelab = Label(master, text='Fish Weight:',  font=("Arial", 36))
fwelab.grid(row=1) 
fwevar = Label(master, text='Waiting...', font=("Arial", 36))
fwevar.grid(row=1,column=1)
datelab= Label(master, text='Date:',  font=("Arial", 36))
datelab.grid(row=2)  
datevar = Label(master, text= now.strftime('%d/%m/%Y'), font=("Arial", 36))
datevar.grid(row=2,column=1)
timelab = Label(master, text='Time:', font=("Arial", 36))
timelab.grid(row=3,column=0)
w = Label(master, text= now.strftime("%H:%M:%S"), font=("Arial", 36))
w.grid(row=3,column=1)
erlab = Label(master, text='State:', font=("Arial", 36))
erlab.grid(row=4)
activelab = Label(master, text='Working!',font=("Arial", 36))
activelab.grid(row=4,column=1)
sbutton = Button(master, text= 'Short!', command= scircuit)
sbutton.grid(row=5)
feedbutton = Button(master, text='Feed!', command= feeder)
feedbutton.grid(row=5,column=1)

# load the image, convert it to grayscale, blur it slightly, and threshold the picture to complete black and white
image = cv2.imread('desktop/medsilvercarp.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)
ret,thresh1 = cv2.threshold(gray,30,255,cv2.THRESH_BINARY)

# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(thresh1, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
    
# find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
        
# sort the contours from left-to-right and initialize the
# 'pixels per metric' calibration variable
# compute it as the ratio of pixels to supplied metric
    # (in this case, cm)
(cnts, _) = contours.sort_contours(cnts)
pixelsPerMetric = 7

# loop over the contours individually
for c in cnts:
    # if the contour is not sufficiently large, ignore it
    if cv2.contourArea(c) < 100:
        continue
    # compute the rotated bounding box of the contour
    orig = image.copy()
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")

	# order the points in the contour such that they appear
	# in top-left, top-right, bottom-right, and bottom-left
	# order, then draw the outline of the rotated bounding
	# box
    box = perspective.order_points(box)
    cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

	# loop over the original points and draw them
    for (x, y) in box:
        cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)


    # unpack the ordered bounding box, then compute the midpoint
    # between the top-left and top-right coordinates, followed by
    # the midpoint between bottom-left and bottom-right coordinates
    (tl, tr, br, bl) = box
    (tltrX, tltrY) = midpoint(tl, tr)
    (blbrX, blbrY) = midpoint(bl, br)
    # compute the midpoint between the top-left and top-right points,
    # followed by the midpoint between the top-righ and bottom-right
    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)

   # draw the midpoints on the image
    cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

    # draw lines between the midpoints
    cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
        (255, 0, 255), 2)
    
    # compute the Euclidean distance between the midpoints
    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

    # if the pixels per metric has not been initialized, then
    # compute it as the ratio of pixels to supplied metric
    # (in this case, cm)
    pixelsPerMetric = 7

    # compute the size of the object
    dimA = dA / pixelsPerMetric
    dimB = dB / pixelsPerMetric

    cv2.putText(orig, "{:.1f}cm".format(dimB),
	    (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
	    0.65, (255, 255, 255), 2)

	# show the output image
    cv2.imshow("Fish", orig)
    cv2.waitKey(0)

    length.append(dimB)
    avglength = np.mean(length)
    fweight = 0.0065*avglength**(3.157)
    flevar.config(text=("%0.2f" % avglength, 'cm'))
    fwevar.config(text=(int(fweight) / 1000, 'Kg'))

#defining the clock in the gui
def clock():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    w.config(text=time)
    datevar.config(text=now.strftime('%d/%m/%Y'))
    master.after(1000, clock) # run itself again after 1000 ms
#running the clock function
clock()

master.mainloop() 