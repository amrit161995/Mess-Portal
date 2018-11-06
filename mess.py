import csv
from datetime import date, timedelta

d1 = date(2019,8,1)
d2 = date(2019,7,31)

delta = d2-d1

myData = [["month", "year", "mess", "cancellation_b", "cancellation_l","cancellation_d"]]


l = []
l.append("05")
l.append(2019)
l.append("kadamb-nonveg")
l.append(10)
l.append(10)
l.append(10)
myData.append(l)

l = []
l.append("07")
l.append(2019)
l.append("kadamb-nonveg")
l.append(10)
l.append(10)
l.append(10)
myData.append(l)
myFile = open('example.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(myData)
     
print("Writing complete")