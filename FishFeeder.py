#Meow!
#Declering some important veriables. 
#lengthinput is set to float as values might not be an integer
#listlength decleres how many values we store before taking the avg length
lenthinput = float
listlength=5
n = 0
fishlength = []
while n < listlength :
    #for testing purpuse im using user input, in future will use image recognition 
    lengthinput = float(input())
    fishlength.append(lengthinput)
    n += 1
#declering the avg length
avglength = (sum(fishlength)/len(fishlength))
#calculating the avg weight
weight = 0.0065 * (avglength ** 3.1572)
print("avg length: " + str(avglength))
print("avg weight: " + str(weight))