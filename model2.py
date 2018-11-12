import sqlite3 as sql
from datetime import date, time, timedelta
import model


def getBill(user_email,duration):
	m = date.today().month
	m -= 1
	y = date.today().year
	if m == 0:
		m = 12
		y-=1
	if duration == "week":
		end = date.today()
		start = end - timedelta(days=7)
		end = end - timedelta(days=1)
	elif duration == "month":
	    if m != 12:
	    	d = (date(y,m+1,1)-date(y,m,1)).days
	    else:
	    	d = 31
	    end = date(y,m,d)
	    start = date(y,m,1)
	elif duration == "semister":
		if m >= 7:
			start = date(y,8,1)
			end = date.today()- timedelta(days=1)
		else:
			start = date(y,1,1)
			end = date.today()- timedelta(days=1)
	# print start
	# print end
	rateB = {}
	rateL = {}
	rateD = {}
	rateB["cancelled"] = 0
	rateL["cancelled"] = 0
	rateD["cancelled"] = 0
	countB ={}
	countL ={}
	countD ={}
	countB["south"] = 0
	countB["north"] = 0
	countB["yuktahar"] = 0
	countB["kadamb-veg"] = 0
	countB["kadamb-nonveg"] = 0
	countB["cancelled"] = 0
	countL["south"] = 0
	countL["north"] = 0
	countL["yuktahar"] = 0
	countL["kadamb-veg"] = 0
	countL["kadamb-nonveg"] = 0
	countL["cancelled"] = 0
	countD["south"] = 0
	countD["north"] = 0
	countD["yuktahar"] = 0
	countD["kadamb-veg"] = 0
	countD["kadamb-nonveg"] = 0
	countD["cancelled"] = 0
	total = 0.0
	rC = model.getRecentMessRate(end)
	for l in rC:
		rateB[l[0]]=l[1]
		rateL[l[0]]=l[2]
		rateD[l[0]]=l[3]
	with sql.connect("mess") as con:
	    con.row_factory = sql.Row
	    cur = con.cursor()
	    print "start"
	    cur.execute("SELECT * FROM mess_registration  WHERE  date <= ? and date >= ? and email = ?",(str(end),str(start),user_email))
	    print "got record"
	    rows = cur.fetchall()
	    for row in rows:
	    	try:
			    total+=rateB.get(row["breakfast"])
			    total+=rateL.get(row["lunch"])
			    total+=rateD.get(row["dinner"])
			    t = countB.get(row["breakfast"])
			    t+=1
			    countB[row["breakfast"]] = t
			    t = countL.get(row["lunch"])
			    t+=1
			    countL[row["lunch"]] = t
			    t = countD.get(row["dinner"])
			    t+=1
			    countD[row["dinner"]] = t
		except:
				print row["breakfast"]
				print row["lunch"]
				print row["dinner"]
	# print total
	# print countB
	# print countL
	# print countD
	return (total,countB,countL,countD,start,end)

def getFeedback():
	msg="Failed to get Records"
	rows={}
	with sql.connect("mess") as con:
	    con.row_factory = sql.Row
	    cur = con.cursor()
	    print "start"
	    cur.execute("SELECT * FROM feedback")
	    print "got record"
	    rows = cur.fetchall()
	    if rows:
	    	msg=""
	    else:
	    	msg="No Records Found"
	return (rows,msg)
