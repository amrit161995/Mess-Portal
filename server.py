from flask import Flask, redirect,url_for, render_template, request, session
import model 

app = Flask(__name__)
app.secret_key ="Demo-CSE505"
 
@app.route("/")
def index():
   msg=""
   return render_template("index.html",message=msg)

@app.route('/login',methods = ['POST'])
def login():
   if request.method == "POST":
      res,msg = model.login(request.form)
      if msg == "1":
         return render_template("home.html",result=res)
      elif msg == "0":
         msg = "Invalid Credentials! Try Again"
      elif msg == "-1":
         msg = "Unexpected Error in login operation"
      return render_template("index.html",message=msg)

@app.route('/register',methods = ['POST'])
def register():
   if request.method == "POST":
      res,msg = model.register(request.form)
      return render_template("index.html",message=msg)

@app.route('/Home')
def home():
   return render_template('home.html')

@app.route('/Menu')
def menu():
   return render_template('Menu.html')

@app.route('/Team')
def team():
   return render_template('Team.html')

@app.route('/Home_Content')
def home_content():
   return render_template('Home_Content.html')

@app.route('/Change_Registration')
def change_registration():
   return render_template('Change_Registration.html')


@app.route('/Feedback')
def feedback():
   return render_template('Feedback.html')

@app.route('/Cancel')
def cancel():
   return render_template('Cancel.html')

@app.route('/View')
def view():
   return render_template('View.html')

@app.route('/Bill')
def bill():
   return render_template('Bill.html')

if __name__ == '__main__':
   app.run(debug = True)