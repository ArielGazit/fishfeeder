from tkinter import *
import datetime 
now = datetime.datetime.now()
master = Tk() 
Label(master, text='Fish Length:',  font=("Arial", 36)).grid(row=0) 
Label(master, text='Fish Weight:',  font=("Arial", 36)).grid(row=1) 
Label(master, text='37 cm', font=("Arial", 36)).grid(row=0,column=1) 
Label(master, text='560 grams', font=("Arial", 36)).grid(row=1,column=1) 
Label(master, text='Water Temperature:',  font=("Arial", 36)).grid(row=2) 
Label(master, text='Date:',  font=("Arial", 36)).grid(row=3) 
Label(master, text='18° C', font=("Arial", 36)).grid(row=2,column=1) 
Label(master, text= now.strftime('%d/%m/%Y'), font=("Arial", 36)).grid(row=3,column=1)
Label(master, text='Time:', font=("Arial", 36)).grid(row=4,column=0)
w = Label(master, text= now.strftime("%H:%M:%S"), font=("Arial", 36))
w.grid(row=4,column=1)
def clock():
    time = datetime.datetime.now().strftime("Time: %H:%M:%S")
    w.config(text=time)
    #lab['text'] = time
    master.after(1000, clock) # run itself again after 1000 ms
clock()
master.mainloop() 
