import sqlite3 as sql
from datetime import date, time, timedelta

# A model that supports following interface:
# create() : creates a users table in database if not already there
# getAll() : fetch information on all users
# addUser(request) : add a new user from request object to database if not already present
# deleteUser(request) : delete an existing user represented by request object from the database


# def getAll():
#   msg = "Records were fetched successfully"
#   try:  
#     with sql.connect("database.db") as con:
#       con.row_factory = sql.Row
#       cur = con.cursor()
#       cur.execute("select * from users where name is not null") 
#       rows = cur.fetchall()
#       for row in rows:
#            print "row=" +  row["name"]
#       return (rows,msg)
#   except:
#       print "connection failed"
#       return ([], "connection failed")
 
def login(user):
  try:
   msg = "1"
   with sql.connect("mess") as con:
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("SELECT * FROM user_credentials  WHERE email = ? and password = ?", (user['user_email'], user['password']))
      print "execute"
      row = cur.fetchone()
      if row:
        mode = row["mode"]
        if mode:
          return(user,msg,1)
        else:  
          return(user,msg,0)
      else:
        msg = "0"
        return  (user, msg,0)
  except:
      msg = "-1"
      print msg
      return ({}, msg,0)

def fback(user,email,image):
  with sql.connect("mess") as con:
    cur = con.cursor()
    cur.execute("INSERT INTO feedback (email,mess,suggestion,description,image) VALUES (?,?,?,?,?)",(email,user['optradio'],user['suggestion'],user['description'],image))
    return email

def cancelMeal(user,email):
  with sql.connect("mess") as con:
    cur = con.cursor()
    f = user['from'].split('-')
    t = user['to'].split('-')
    start = date(int(f[0]),int(f[1]),int(f[2]))
    end = date(int(t[0]),int(t[1]),int(t[2]))
    today = date.today()
    delta = end-start
    if(delta.days>=0):
      for i in range(delta.days+1):
        if not user.get('uncancel'):
          if user.get('meal_b'):
            cur.execute("UPDATE mess_registration SET breakfast = ? WHERE email = ? and date = ?",("cancelled",email,str(start + timedelta(i))))
          if user.get('meal_l'):
            cur.execute("UPDATE mess_registration SET lunch = ? WHERE email = ? and date = ?",("cancelled",email,str(start + timedelta(i))))
          if user.get('meal_d'):
            cur.execute("UPDATE mess_registration SET dinner = ? WHERE email = ? and date = ?",("cancelled",email,str(start + timedelta(i))))
        else:
          cur.execute("SELECT * FROM user_details WHERE email = ?",(email,))
          row = cur.fetchone()
          if user.get('meal_b'):
            cur.execute("UPDATE mess_registration SET breakfast = ? WHERE email = ? and date = ?",(row[6],email,str(start + timedelta(i))))
          if user.get('meal_l'):
            cur.execute("UPDATE mess_registration SET lunch = ? WHERE email = ? and date = ?",(row[6],email,str(start + timedelta(i))))
          if user.get('meal_d'):
            cur.execute("UPDATE mess_registration SET dinner = ? WHERE email = ? and date = ?",(row[6],email,str(start + timedelta(i))))

def changeRegistrationDate(user,email):
  with sql.connect("mess") as con:
    cur = con.cursor()
    f = user['from'].split('-')
    t = user['to'].split('-')
    start = date(int(f[0]),int(f[1]),int(f[2]))
    end = date(int(t[0]),int(t[1]),int(t[2]))
    today = date.today()
    delta = end-start
    if(delta.days>=0 and (start-today).days>=2):
      for i in range(delta.days+1):
        if user.get('meal_b'):
          cur.execute("UPDATE mess_registration SET breakfast = ? WHERE email = ? and date = ?",(user['mess'],email,str(start + timedelta(i))))
        if user.get('meal_l'):
          cur.execute("UPDATE mess_registration SET lunch = ? WHERE email = ? and date = ?",(user['mess'],email,str(start + timedelta(i))))
        if user.get('meal_d'):
          cur.execute("UPDATE mess_registration SET dinner = ? WHERE email = ? and date = ?",(user['mess'],email,str(start + timedelta(i))))

def changeRegistrationDay(user,email):
  with sql.connect("mess") as con:
    cur = con.cursor()    
    end = date(2019,7,31)
    start = date.today() + timedelta(days=2)
    delta = end - start
    for i in range(delta.days+1):
      if str((start + timedelta(i)).weekday())==str(user['day']):
        if user.get('meal_b'):
          cur.execute("UPDATE mess_registration SET breakfast = ? WHERE email = ? and date = ?",(user['mess'],email,str(start + timedelta(i))))
        if user.get('meal_l'):
          cur.execute("UPDATE mess_registration SET lunch = ? WHERE email = ? and date = ?",(user['mess'],email,str(start + timedelta(i))))
        if user.get('meal_d'):
          cur.execute("UPDATE mess_registration SET dinner = ? WHERE email = ? and date = ?",(user['mess'],email,str(start + timedelta(i))))

def changeRegistrationMonth(user,email):
  with sql.connect("mess") as con:
    cur = con.cursor() 
    y = date.today().year
    m = int(user['month'])
    if m!=12:
      d = (date(y,m+1,1)-date(y,m,1)).days
    else:
      d = 31
    end = date(y,m,d)
    if date.today().month==m and date.today().year==y:
      start = date.today() + timedelta(days=2)
    else:
      start = date(y,m,1)
    delta = end - start
    # print type(user.get('unregister'))
    for i in range(delta.days+1):
      if user.get('unregister'):
        # print "unregister"
        cur.execute("SELECT * FROM user_details WHERE email = ?",(email,))
        row = cur.fetchone()
        cur.execute("UPDATE mess_registration SET breakfast = ? WHERE email = ? and date = ?",(row[6],email,str(start + timedelta(i))))
        cur.execute("UPDATE mess_registration SET lunch = ? WHERE email = ? and date = ?",(row[6],email,str(start + timedelta(i))))
        cur.execute("UPDATE mess_registration SET dinner = ? WHERE email = ? and date = ?",(row[6],email,str(start + timedelta(i))))
      else:
        # print "register"        
        cur.execute("UPDATE mess_registration SET breakfast = ? WHERE email = ? and date = ?",(user['mess'],email,str(start + timedelta(i))))
        cur.execute("UPDATE mess_registration SET lunch = ? WHERE email = ? and date = ?",(user['mess'],email,str(start + timedelta(i))))
        cur.execute("UPDATE mess_registration SET dinner = ? WHERE email = ? and date = ?",(user['mess'],email,str(start + timedelta(i))))

  
def register(user):
  try:
   msg = "Registration Successful!"
   with sql.connect("mess") as con:
      cur = con.cursor()
      print "start"
      print user['user_email']
      cur.execute("SELECT * FROM user_credentials  WHERE email = ? and mode = ?", (user['user_email'],0))
      print "select"
      row = cur.fetchone()
      if row:
         msg="User with id %s is already present, regestration failed!"%(user['user_email'])
         print  msg
      else:
         cur.execute("INSERT INTO user_credentials (email,password) VALUES (?,?)",(user['user_email'],user['password']))
         print "insert 1"
         default_mess = 'north'
         cur.execute("INSERT INTO user_details (email,full_name,roll_no,default_mess,monthly_mess)  VALUES (?,?,?,?,0)",(user['user_email'],user['fullname'],user['roll_no'],default_mess))            
         print "insert 2"
         end = date(2019,7,31)
         start = date.today()
         delta = end - start
         
         for i in range(delta.days+1):
          cur.execute("INSERT INTO mess_registration (email,date,breakfast,lunch,dinner)  VALUES (?,?,?,?,?)",(user['user_email'],str(start + timedelta(i)),default_mess,default_mess,default_mess))            







         con.commit()
         print "Record successfully added"
      return  (user, msg)
  except:
      msg = "Unexpected Error in insert operation"
      print msg
      return ({}, msg)

def getUserNamePassword(user_email):
  name=""
  rollno=0
  with sql.connect("mess") as con:
      con.row_factory = sql.Row
      cur = con.cursor()
      print "start"
      print user_email
      cur.execute("SELECT * FROM user_details  WHERE email = ?",[user_email])
      print "got it"
      row = cur.fetchone()
      name=row["full_name"]
      print "got name"
      rollno=row["roll_no"]
      print "got roll no"
  return (name,rollno)

def getRegisteredMess(user_email):
  breakfast=""
  lunch=""
  dinner=""
  with sql.connect("mess") as con:
      con.row_factory = sql.Row
      cur = con.cursor()
      print "start"
      print user_email
      cur.execute("SELECT * FROM mess_registration  WHERE email = ?",[user_email])
      print "got it"
      row = cur.fetchall()
      breakfast={}
      lunch = {}
      dinner = {}
      for i in range(len(row)):
        # print row[i]["date"]
        breakfast[row[i]["date"]] = row[i]["breakfast"]
        lunch[row[i]["date"]] = row[i]["lunch"]
        dinner[row[i]["date"]] = row[i]["dinner"]
      # print breakfast
      # print "got breakfast"
      # lunch=row[3]
      # print "got lunch"
      # dinner=row[4]
      # print "got dinner"      
  return (breakfast,lunch,dinner)

def getTodayMeal(user_email):
  meal = []
  with sql.connect("mess") as con:
      con.row_factory = sql.Row
      cur = con.cursor()
      print "start"
      print user_email
      curD = date.today()
      print date.today()
      cur.execute("SELECT * FROM mess_registration  WHERE email = ? and date = ?",(user_email,str(curD)))
      print "got todays meal"
      row = cur.fetchone()
      meal.append(row["breakfast"])
      meal.append(row["lunch"])
      meal.append(row["dinner"])     
  return (meal)

def getRecentMessRate(rateDate):
  rateCard = []
  with sql.connect("mess") as con:
    con.row_factory = sql.Row
    cur = con.cursor()
    print "start"
    print rateDate
    cur.execute("SELECT * FROM mess_properties  WHERE  date <= ? and mess = ? ORDER BY date DESC",(str(rateDate),"south"))
    print "got south"
    row = cur.fetchone()
    l = []
    l.append(row["mess"])
    l.append(row["breakfast_price"])
    l.append(row["lunch_price"])
    l.append(row["dinner_price"])
    rateCard.append(l)

    cur.execute("SELECT * FROM mess_properties  WHERE  date <= ? and mess = ? ORDER BY date DESC",(str(rateDate),"north"))
    print "got North"
    row = cur.fetchone()
    l = []
    l.append(row["mess"])
    l.append(row["breakfast_price"])
    l.append(row["lunch_price"])
    l.append(row["dinner_price"])
    rateCard.append(l)

    cur.execute("SELECT * FROM mess_properties  WHERE  date <= ? and mess = ? ORDER BY date DESC",(str(rateDate),"yuktahar"))
    print "got yuktahar"
    row = cur.fetchone()
    l = []
    l.append(row["mess"])
    l.append(row["breakfast_price"])
    l.append(row["lunch_price"])
    l.append(row["dinner_price"])
    rateCard.append(l)

    cur.execute("SELECT * FROM mess_properties  WHERE  date <= ? and mess = ? ORDER BY date DESC",(str(rateDate),"kadamb-veg"))
    print "got kadamb veg"
    row = cur.fetchone()
    l = []
    l.append(row["mess"])
    l.append(row["breakfast_price"])
    l.append(row["lunch_price"])
    l.append(row["dinner_price"])
    rateCard.append(l)

    cur.execute("SELECT * FROM mess_properties  WHERE  date <= ? and mess = ? ORDER BY date DESC",(str(rateDate),"kadamb-nonveg"))
    print "got kadamb non-veg"
    row = cur.fetchone()
    l = []
    l.append(row["mess"])
    l.append(row["breakfast_price"])
    l.append(row["lunch_price"])
    l.append(row["dinner_price"])
    rateCard.append(l)
  return rateCard

def getCancellationsAllowed():
  curD = date.today()
  ca = []
  with sql.connect("mess") as con:
    con.row_factory = sql.Row
    cur = con.cursor()
    print "start"
    cur.execute("SELECT * FROM mess_properties  WHERE  date <= ? ORDER BY date DESC",[str(curD)])
    print "got ca"
    row = cur.fetchone()
    ca.append(row["cancellation_b"])
    ca.append(row["cancellation_l"])
    ca.append(row["cancellation_d"])
    # print ca
  return ca




def deleteUser(user):
 try:
   print "inside deleteuser"
   msg = "Record successfully deleted"
   with sql.connect("database.db") as con:
      cur = con.cursor()
      cur.execute("DELETE FROM users  WHERE id = ? and name = ?", (user['id'], user['name']))
      con.commit()
      print "user deleted"
      return (user, msg)
 except:
      msg = "error in delete operation"
      print "in delete - exception handler"
      return ({}, msg)