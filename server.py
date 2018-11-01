from flask import Flask, redirect,url_for, render_template, request
import model 

app = Flask(__name__)
app.secret_key ="Demo-CSE505"
 
@app.route("/")
def index():
   msg=""
   return render_template("index.html",message=msg)

@app.route('/register',methods= ['POST'])
def register():
   msg = model.register(request.form)
   return render_template('index.html',message=msg)

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

if __name__ == '__main__':
   app.run(debug = True)