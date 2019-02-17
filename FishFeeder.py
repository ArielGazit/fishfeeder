from tkinter import *
import datetime
now = datetime.datetime.now()
avglength = 60
fweight = 0.0065*avglength**(3.157)
master = Tk() 
Label(master, text='Fish Length:',  font=("Arial", 36)).grid(row=0) 
Label(master, text='Fish Weight:',  font=("Arial", 36)).grid(row=1) 
Label(master, text=(avglength,'cm'), font=("Arial", 36)).grid(row=0,column=1) 
fishwlab = Label(master, text=(int(fweight),'grams'), font=("Arial", 36))
fishwlab.grid(row=1,column=1)
Label(master, text='Water Temperature:',  font=("Arial", 36)).grid(row=2) 
Label(master, text='Date:',  font=("Arial", 36)).grid(row=3) 
Label(master, text='18° C', font=("Arial", 36)).grid(row=2,column=1) 
Label(master, text= now.strftime('%d/%m/%Y'), font=("Arial", 36)).grid(row=3,column=1)
Label(master, text='Time:', font=("Arial", 36)).grid(row=4,column=0)
w = Label(master, text= now.strftime("%H:%M:%S"), font=("Arial", 36))
w.grid(row=4,column=1)
Label(master, text='Errors:', font=("Arial", 36)).grid(row=5)
errorlab = Label(master, text='None',font=("Arial", 36))
errorlab.grid(row=5,column=1)
def clock():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    w.config(text=time)
    master.after(1000, clock) # run itself again after 1000 ms
def shortcircuit():
    errorlab.config(text="Short Circuit!!")
clock()
master.mainloop() 