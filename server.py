from flask import Flask, redirect,url_for, render_template, request
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
         msg = "Invalid Credentials, Please Try Again :("
         return render_template("index.html",message=msg)
      elif msg == "-1":
         msg = "Unexpected error in login operation"
         return render_template("index.html",message=msg)

@app.route('/register',methods = ['POST'])
def register():
   if request.method == "POST":
      res,msg = model.register(request.form)
      if msg == "1":
         msg = "Registration successful"
         return render_template("index.html",message=msg)
      elif msg == "0":
         msg = "User with id ",res['user_email']," is already present, regestration failed!"
         return render_template("index.html",message=msg)
      elif msg == "-1":
         msg = "Unexpected error in login operation"
         return render_template("index.html",message=msg)

@app.route('/Home')
def home():
   return render_template('home.html')

@app.route('/Menu')
def menu():
   return render_template('Menu.html')

if __name__ == '__main__':
   app.run(debug = True)