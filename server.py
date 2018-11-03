from flask import Flask, redirect,url_for, render_template, request, session
import model 

app = Flask(__name__)
app.secret_key ="Demo-CSE505"
 
@app.route("/")
def index():
   msg=""
   if 'user_email' in session:
      res=session['user_email']
      name,roll_no = model.getUserNamePassword(session['user_email'])
      return render_template("home.html",username=name,rollNo=roll_no)
   else:
      return render_template("index.html",message=msg)

@app.route('/login',methods = ['POST','GET'])
def login():
   if 'user_email' in session:
      name,roll_no = model.getUserNamePassword(session['user_email'])
      return render_template("home.html",username=name,rollNo=roll_no)
   else:
      if request.method == "POST":
         res,msg = model.login(request.form)
         if msg == "1":
            session['user_email'] = request.form['user_email']
            name,roll_no = model.getUserNamePassword(session['user_email'])
            return render_template("home.html",username=name,rollNo=roll_no)
         elif msg == "0":
            msg = "Invalid Credentials! Try Again"
         elif msg == "-1":
            msg = "Unexpected Error in login operation"
         return render_template("index.html",message=msg)
      else:
         msg=""
         return render_template("index.html",message=msg)      

@app.route('/register',methods = ['POST'])
def register():
   if request.method == "POST":
      res,msg = model.register(request.form)
      return render_template("index.html",message=msg)

@app.route('/Home')
def home():
   if 'user_email' in session:
      name,roll_no = model.getUserNamePassword(rsession['user_email'])
      return render_template('home.html',username=name,rollNo=roll_no)
   else:
      msg = "please login before you access the webApp"
      return render_template('index.html',message=msg)

@app.route('/Menu')
def menu():
   if 'user_email' in session:
      return render_template('Menu.html')
   else:
      return redirect('localhost:5000/')

@app.route('/Team')
def team():
   if 'user_email' in session:
      return render_template('Team.html')
   else:
      return redirect('localhost:5000/')

@app.route('/Home_Content')
def home_content():
   if 'user_email' in session:
      name,roll_no = model.getUserNamePassword(session['user_email'])
      return render_template('Home_Content.html',username=name,rollno=roll_no)
   else:
      msg = "please login before you access the webApp"
      # return render_template('index.html',message=msg)
      return redirect('localhost:5000/')

@app.route('/Change_Registration')
def change_registration():
   if 'user_email' in session:
      return render_template('Change_Registration.html')
   else:
      return redirect('localhost:5000/')

@app.route('/Feedback')
def feedback():
   if 'user_email' in session:
      return render_template('Feedback.html')
   else:
      return redirect('localhost:5000/')

@app.route('/Cancel')
def cancel():
   if 'user_email' in session:
      return render_template('Cancel.html')
   else:
      return redirect('localhost:5000/')

@app.route('/View')
def view():
   if 'user_email' in session:
      return render_template('View.html')
   else:
      return redirect('localhost:5000/')

@app.route('/Bill')
def bill():
   if 'user_email' in session:
      return render_template('Bill.html')
   else:
      return redirect('localhost:50000/')

@app.route('/logout')
def logout():
   msg=""
   if 'user_email' in session:
      email = session.pop('user_email')
      msg = "Logout successfull"
   else:
      msg = "You are already logged out"
   return render_template('index.html',message=msg)

@app.route('/Billing_Rates')
def billing_rates():
   return render_template('Billing_Rates.html')

@app.route('/Mess_Rules')
def mess_rules():
   return render_template('Mess_Rules.html')

if __name__ == '__main__':
   app.run(debug = True)