import sqlite3 as sql
from datetime import date, time, timedelta
import model


def getBill(user_email,duration):
	m = date.today().month
	m -= 1
	y = date.today().year
	ca=[]
	cd=[]
	if m == 0:
		m = 12
		y-=1
	if duration == "week":
		end = date.today()
		start = end - timedelta(days=7)
		end = end - timedelta(days=1)
		cd = model.getTotalCancelled(user_email,"")
	elif duration == "month":
	    if m != 12:
	    	d = (date(y,m+1,1)-date(y,m,1)).days
	    else:
	    	d = 31
	    end = date(y,m,d)
	    start = date(y,m,1)
	    cd = model.getTotalCancelled(user_email,"")
	elif duration == "semister":
		if m >= 7:
			start = date(y,8,1)
			end = date.today()- timedelta(days=1)
		else:
			start = date(y,1,1)
			end = date.today()- timedelta(days=1)
		cd = model.getTotalCancelled(user_email,"semister")
	ca = model.getCancellationsAllowed()
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
	dmess=getDefaultMess(user_email)
	if cd[0]>ca[0]:
		total = total + (cd[0]-ca[0])*rateB[dmess]
	if cd[1]>ca[1]:
		total = total + (cd[1]-ca[1])*rateB[dmess]
	if cd[2]>ca[2]:
		total = total + (cd[2]-ca[2])*rateB[dmess]
	print countB
	print countL
	print countD
	return (total,countB,countL,countD,start,end,cd)

def getDefaultMess(email):
	mess=""
	with sql.connect("mess") as con:
	    con.row_factory = sql.Row
	    cur = con.cursor()
	    print "start"
	    cur.execute("SELECT * FROM user_details where email = ?",(email,))
	    row =cur.fetchone()
	    mess = row["default_mess"]
	return mess

def getFeedback(email):
	msg="Failed to get Records"
	rows={}
	with sql.connect("mess") as con:
	    con.row_factory = sql.Row
	    cur = con.cursor()
	    print "start"
	    cur.execute("SELECT * FROM user_credentials where email = ?",(email,))
	    row =cur.fetchone()
	    mess = row["mode"]
	    cur.execute("SELECT * FROM feedback where mess = ? ORDER BY date desc",(mess,))
	    print "got record"
	    rows = cur.fetchall()
	    if rows:
	    	msg=""
	    else:
	    	msg="No Records Found"
	return (rows,msg)

def getRate(mess):
	rate=[]
	rows={}
	with sql.connect("mess") as con:
	    con.row_factory = sql.Row
	    cur = con.cursor()
	    print "start"
	    cur.execute("SELECT * FROM mess_properties where mess = ? ORDER BY date desc",(mess,))
	    rows =cur.fetchall()
	    for row in rows:
	    	if mess == row['mess']:
	    		rate.append(row['breakfast_price'])
	    		rate.append(row['lunch_price'])
	    		rate.append(row['dinner_price'])
	return rate

def changeRate(form,mess):
	month=form['month']
	year=date.today().year
	if int(month) < 8:
		year+=1
	dt=date(int(year),int(month),1)
	print str(dt.month).zfill(2)
	msg="update failed"
	with sql.connect("mess") as con:
	    con.row_factory = sql.Row
	    cur = con.cursor()
	    print "start"
	    cur.execute("insert into mess_properties (date,mess,breakfast_price,lunch_price,dinner_price,cancellation_b,cancellation_l,cancellation_d) values (?,?,?,?,?,?,?,?)",(str(dt),mess,form['b_rate'],form['l_rate'],form['d_rate'],form['breakfast_cancel'],form['lunch_cancel'],form['dinner_cancel']))
	    cur.execute("UPDATE mess_cancellation SET cancellation_b = ? WHERE month = ? and year = ? and mess = ?",(form['breakfast_cancel'],str(dt.month).zfill(2),year,mess))
	    cur.execute("UPDATE mess_cancellation SET cancellation_l = ? WHERE month = ? and year = ? and mess = ?",(form['lunch_cancel'],str(dt.month).zfill(2),year,mess))
	    cur.execute("UPDATE mess_cancellation SET cancellation_d = ? WHERE month = ? and year = ? and mess = ?",(form['dinner_cancel'],str(dt.month).zfill(2),year,mess))
	    msg="Updated Successfully!"
	return msg

def getAllCA(mess):
	listBCA=[]
	listLCA=[]
	listDCA=[]
	year=2018
	with sql.connect("mess") as con:
	    con.row_factory = sql.Row
	    cur = con.cursor()
	    print "start"
	    for mo in range(1,13):
	    	print mo
	    	if mo < 8:
	    		year=date.today().year+1
	    	else:
	    		year=date.today().year
	    	print year
    		cur.execute("SELECT * from mess_cancellation where month = ? and year = ? and mess = ?",(str(mo).zfill(2),year,mess))
    		row=cur.fetchone()
    		if row:
				listBCA.append(row["cancellation_b"])
				listLCA.append(row["cancellation_l"])
				listDCA.append(row["cancellation_d"])
	return (listBCA,listLCA,listDCA)