# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2 
from tkinter import *
import datetime
now = datetime.datetime.now()
#defining the midpoints for the image processing code
def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

# load the image, convert it to grayscale, blur it slightly, and threshold the picture to complete black and white
image = cv2.imread(args["image"])
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
(cnts, _) = contours.sort_contours(cnts)
pixelsPerMetric = None

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
	dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
 
	# if the pixels per metric has not been initialized, then
	# compute it as the ratio of pixels to supplied metric
	# (in this case, cm)
	pixelsPerMetric = 7

    # compute the size of the object
	dimB = dB / pixelsPerMetric
#declering variables
watertemp = 18
length = []
#calculating the mean length of the fish
length.append(dimB)
avglength = np.mean(length)
#calculating the mean length of the fish
fweight = 0.0065*avglength**(3.157)
#making the gui flash red and white in case of short
#this part changes the color to red, waits 1 sec and then runs "scircuitcolor", which
#changes the color back to white and runs "scircuit" again, in an infinite loop
#there is no exit condition since that the fix requires turning off the pi, which will restart the software
def scircuit():
    errorlab.config(text="Short Circuit!!")
    flelab.config(background='red')
    flevar.config(background='red')
    fwelab.config(background='red')
    fwevar.config(background='red')
    wtemplab.config(background='red')
    wtempvar.config(background='red')
    datelab.config(background='red')
    datevar.config(background='red')
    timelab.config(background='red')
    w.config(background='red')
    erlab.config(background='red')
    errorlab.config(background='red')
    master.configure(background='red')
    master.after(1000, scircuitcolor)
def scircuitcolor():
    flelab.config(background='white')
    flevar.config(background='white')
    fwelab.config(background='white')
    fwevar.config(background='white')
    wtemplab.config(background='white')
    wtempvar.config(background='white')
    datelab.config(background='white')
    datevar.config(background='white')
    timelab.config(background='white')
    w.config(background='white')
    erlab.config(background='white')
    errorlab.config(background='white')
    master.configure(background='white')
    master.config(background='white')
    master.after(1000, scircuit)
#here the main gui elements are built.
#declering the master window
master = Tk() 
#declering labels.
flelab = Label(master, text='Fish Length:',  font=("Arial", 36))
#declering the location of the label
flelab.grid(row=0) 
flevar = Label(master, text=(avglength,'cm'), font=("Arial", 36))
flevar.grid(row=0,column=1) 
fwelab = Label(master, text='Fish Weight:',  font=("Arial", 36))
fwelab.grid(row=1) 
fwevar = Label(master, text=(int(fweight),'grams'), font=("Arial", 36))
fwevar.grid(row=1,column=1)
wtemplab = Label(master, text='Water Temperature:',  font=("Arial", 36))
wtemplab.grid(row=2) 
wtempvar = Label(master, text=(watertemp,'C'), font=("Arial", 36))
wtempvar.grid(row=2,column=1)  
datelab = Label(master, text='Date:',  font=("Arial", 36))
datelab.grid(row=3)  
datevar = Label(master, text= now.strftime('%d/%m/%Y'), font=("Arial", 36))
datevar.grid(row=3,column=1)
timelab = Label(master, text='Time:', font=("Arial", 36))
timelab.grid(row=4,column=0)
w = Label(master, text= now.strftime("%H:%M:%S"), font=("Arial", 36))
w.grid(row=4,column=1)
erlab = Label(master, text='Errors:', font=("Arial", 36))
erlab.grid(row=5)
errorlab = Label(master, text='None',font=("Arial", 36))
errorlab.grid(row=5,column=1)
Button(master, text= 'Short!', command= scircuit).grid(row=6)
#defining clock command, which is used to update the time on the gui
def clock():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    w.config(text=time)
    master.after(1000, clock) # run itself again after 1000 ms
#running the "clock" command
clock()
master.mainloop() 