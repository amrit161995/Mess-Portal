import sqlite3 as sql

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
      cur = con.cursor()
      cur.execute("SELECT * FROM user_credentials  WHERE email = ? and password = ?", (user['user_email'], user['password']))
      print "execute"
      row = cur.fetchone()
      if row:
        return(user,msg)
      else:
        msg = "0"
        return  (user, msg)
  except:
      msg = "-1"
      print msg
      return ({}, msg)

  
def register(user):
  try:
   msg = "1"
   with sql.connect("mess") as con:
      cur = con.cursor()
      print "start"
      print user['user_email']
      cur.execute("SELECT * FROM user_credentials  WHERE email = ? and mode = ?", (user['user_email'],0))
      print "select"
      row = cur.fetchone()
      if row:
         print "User with id %s is already present, regestration failed!"%(user['user_email'])
         msg="0"
      else:
         cur.execute("INSERT INTO user_credentials (email,password) VALUES (?,?)",(user['user_email'],user['password']))
         print "insert 1"
         cur.execute("INSERT INTO user_details (email,full_name,roll_no)  VALUES (?,?,?)",(user['user_email'],user['fullname'],user['roll_no']))            
         print "insert 2"
         con.commit()
         print "Record successfully added"
      return  (user, msg)
  except:
      msg = "-1"
      print "Unexpected Error in insert operation"
      return ({}, msg)

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
 