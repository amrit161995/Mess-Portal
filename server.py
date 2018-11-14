from flask import Flask, redirect,url_for, render_template, request, session, json
from datetime import date, time, timedelta
from werkzeug import secure_filename
import model 
import model2

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
      mode = model.getMode(session['user_email'])
      print type(mode)
      if(mode==0):
         name,roll_no = model.getUserNamePassword(session['user_email'])
         return render_template("home.html",username=name,rollNo=roll_no)
      name = getMess(session['user_email'])
      return render_template("Admin_Main.html",username=name)         
   else:
      if request.method == "POST":
         res,msg,mode = model.login(request.form)
         if msg == "1":
            session['user_email'] = request.form['user_email']
            if mode!=0:
               # session['user_email'] = request.form['user_email']
               name = getMess(session['user_email'])
               return render_template('Admin_Main.html',username=name)
            else:
               # session['user_email'] = request.form['user_email']
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

@app.route('/register',methods = ['POST','GET'])
def register():
   if request.method == "POST":
      res,msg = model.register(request.form)
      return render_template("index.html",message=msg)
   else:
      return render_template("index.html")

@app.route('/Home')
def home():
   if 'user_email' in session:
      name,roll_no = model.getUserNamePassword(session['user_email'])
      return render_template('home.html',username=name,rollNo=roll_no)
   else:
      msg = "please login before you access the webApp"
      return render_template('index.html',message=msg)

@app.route('/Menu')
def menu():
   if 'user_email' in session:
      return render_template('Menu.html')
   else:
      return  render_template('index.html')

@app.route('/Team')
def team():
   if 'user_email' in session:
      return render_template('Team.html')
   else:
      # return redirect('localhost:5000/')
      return render_template("index.html")

@app.route('/Home_Content')
def home_content():
   if 'user_email' in session:
      name,roll_no = model.getUserNamePassword(session['user_email'])
      meal = model.getTodayMeal(session['user_email'])
      return render_template('Home_Content.html',username=name,rollno=roll_no,meal=meal)
   else:
      msg = "please login before you access the webApp"
      return  render_template('index.html')

@app.route('/Change_Registration')
def change_registration():
   if 'user_email' in session:
      return render_template('Change_Registration.html',msg="")
   else:
      return  render_template('index.html')

@app.route('/feedback',methods = ['POST','GET'])
def fback():
   print "in feedback"
   image=0
   try:
      if 'user_email' in session:  
         if request.method == 'POST':
            if request.files.get('input-file-preview'):
               image=1
               res = model.fback(request.form,session['user_email'],image)
               f=request.files['input-file-preview']
               name = f.filename
               print name
               fname = name.split('.')
               print len(fname)
               print name
               print res
               print fname[len(fname)-1]
               f.filename=str(res)+'.'+fname[len(fname)-1]
               print f.filename
               f.save("static/feedback_img/"+f.filename) 
            else:
               print "something"
               res = model.fback(request.form,session['user_email'],image)  
         else:
            return render_template('Feedback.html')        
         return render_template('Feedback.html')
      else:
         return  render_template('index.html')
   except:
       return render_template('Feedback.html')

@app.route('/registration_change_date',methods = ['POST'])
def registration_change_date():
   if 'user_email' in session:
      msg = model.changeRegistrationDate(request.form,session['user_email'])
      return render_template('Change_Registration.html',msg = msg)
   else:
      return  render_template('index.html')

@app.route('/registration_change_day',methods = ['POST'])
def registration_change_day():
   if 'user_email' in session:
      msg = model.changeRegistrationDay(request.form,session['user_email'])
      return render_template('Change_Registration.html',msg = msg)
   else:
      return  render_template('index.html')

@app.route('/registration_change_month',methods = ['POST'])
def registration_change_month():
   if 'user_email' in session:
      msg = model.changeRegistrationMonth(request.form,session['user_email'])
      return render_template('Change_Registration.html',msg = msg)
   else:
      return  render_template('index.html')

@app.route('/registration_change_particular_day',methods = ['POST'])
def registration_change_particular_day():
   if 'user_email' in session:
      print "1"
      msg = model.changeRegistrationParticularDay(request.form,session['user_email'])
      print "2"
      return render_template('Change_Registration.html',msg = msg)
   else:
      return  render_template('index.html')

@app.route('/cancel_meal',methods = ['POST'])
def cancel_meal():
   if 'user_email' in session:
      msg = model.cancelMeal(request.form,session['user_email'])
      return render_template('Change_Registration.html',msg = msg)
   else:
      return  render_template('index.html')

@app.route('/Feedback')
def feedback():
   if 'user_email' in session:
      return render_template('Feedback.html')
   else:
      return  render_template('index.html')

@app.route('/Cancel')
def cancel():
   if 'user_email' in session:
      return render_template('Cancel.html')
   else:
      return  render_template('index.html')

@app.route('/View')
def view():
   if 'user_email' in session:
      breakfast,lunch,dinner = model.getRegisteredMess(session['user_email'])
      return render_template('View.html',b_mess=breakfast,l_mess=lunch,d_mess=dinner)
   else:
      return  render_template('index.html')

@app.route('/Bill')
def bill():
   if 'user_email' in session:
      rateCard = model.getRecentMessRate(date.today())
      cancellations_allowed = model.getCancellationsAllowed()
      # cancellations_did = model.getTotalCancelled(session['user_email'])
      weekBill,countB,countL,countD,wstart,wend,cancellations_did = model2.getBill(session['user_email'],"week")
      monthBill,McountB,McountL,McountD,mstart,mend,cancellations_did = model2.getBill(session['user_email'],"month")
      semBill,ScountB,ScountL,ScountD,sstart,send,cancellations_did = model2.getBill(session['user_email'],"semister")
      return render_template('Bill.html',rateCard=rateCard,cancellations_did=cancellations_did,cancellations_allowed=cancellations_allowed,weekBill=weekBill,countB=countB,countD=countD,countL=countL,wstart=wstart,wend=wend,monthBill=monthBill,McountB=McountB,McountL=McountL,McountD=McountD,mstart=mstart,mend=mend,semBill=semBill,ScountB=ScountB,ScountL=ScountL,ScountD=ScountD,sstart=sstart,send=send)
   else:
      return  render_template('index.html')

@app.route('/logout')
def logout():
   msg=""
   if 'user_email' in session:
      email = session.pop('user_email')
      msg = "Logout successful"
   else:
      msg = ""
   return render_template('index.html',message=msg)

@app.route('/Billing_Rates')
def billing_rates():
   if 'user_email' in session:
      return render_template('Billing_Rates.html')
   else:
      return render_template('index.html')

@app.route('/Mess_Rules')
def mess_rules():
   if 'user_email' in session:
      return render_template('Mess_Rules.html')
   else:
      return render_template('index.html')

@app.after_request
def after_request(response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    # redirect("index.html")
    return response

@app.route('/Admin_Main')
def admin_main():
   if 'user_email' in session:
      return render_template('Admin_Main.html')
   else:
      return render_template('index.html')

@app.route('/View_Feedback')
def view_feedback():
   if 'user_email' in session:
      data,msg = model2.getFeedback(session['user_email'])
      return render_template('View_Feedback.html',data=data,msg=msg)
   else:
      return render_template('index.html')

@app.route('/Update_Mess_Rules')
def update_mess_rules():
   if 'user_email' in session:
      return render_template('Update_Mess_Rules.html',msg="")
   else:
      return render_template('index.html')

@app.route('/Update_Billing_Rules')
def update_billing_rules():
   if 'user_email' in session:
      return render_template('Update_Billing_Rules.html')
   else:
      return render_template('index.html')

@app.route('/Update_Meal_Rates')
def update_meal_rates():
   if 'user_email' in session:
      mess=getMess(session['user_email'])
      mode=model.getMode(session['user_email'])
      rate=model2.getRate(mode)
      bca,lca,dca=model2.getAllCA(mode)
      return render_template('Update_Meal_Rates.html',mess=mess,rate=rate,bca=json.dumps(bca),lca=json.dumps(lca),dca=json.dumps(dca))
   else:
      return render_template('index.html')

@app.route('/Update_Menu')
def update_menu():
   if 'user_email' in session:
      mess=getMess(session['user_email'])
      mess=mess+".pdf"
      return render_template('Update_Menu.html',mess=mess)
   else:
      return render_template('index.html')

@app.route('/Dashboard')
def dashboard():
   if 'user_email' in session:
      monthlyRegistered,registered = model.dashboard()
      print registered
      return render_template('Dashboard.html',mR = monthlyRegistered, r=registered)
   else:
      return render_template('index.html')

@app.route('/dashboard2', methods=['POST'])
def dashboard2():
   if 'user_email' in session:
      mess = request.form['mess']
      registered = model.barChart(mess)
      print "inside dashboard2"
      print registered
      d = json.dumps(registered)
      print "JSON"
      # print d[]
      return d
   else:
      return render_template('index.html')

@app.route('/UploadMessRules',methods = ['POST'])
def uploadMessRules():
   if 'user_email' in session:
      msg=""
      if request.method == 'POST':
            f = request.files['input-file-preview']
            f.filename="MessRules.pdf"
            f.save("static/"+f.filename)
            msg = "Mess Rules Updated Successfully"
      return render_template('Update_Mess_Rules.html',msg=msg)
   else:
      return render_template('index.html')

@app.route('/UploadBillingRules',methods = ['POST'])
def uploadBillingRules():
   if 'user_email' in session:
      msg=""
      if request.method == 'POST':
            f = request.files['input-file-preview']
            f.filename="BillingRates.pdf"
            f.save("static/"+f.filename)
            msg = "Billing Rules Updated Successfully"
      return render_template('Update_Billing_Rules.html',msg=msg)
   else:
      return render_template('index.html')

@app.route('/UploadMenu',methods = ['POST'])
def uploadMenu():
   if 'user_email' in session:
      msg=""
      name=""
      if request.method == 'POST':
            f = request.files['input-file-preview']
            name=getMess(session['user_email'])
            f.filename=name+".pdf"
            f.save("static/"+f.filename)
            msg = "Mess Menu Updated Successfully"
            mess=getMess(session['user_email'])
            mess=mess+".pdf"
      return render_template('Update_Menu.html',msg=msg,mess=mess)
   else:
      return render_template('index.html')


@app.route('/UpdateRateAndCA',methods=['POST'])
def updateRateAndCA():
   if 'user_email' in session:
      mess=model.getMode(session['user_email'])
      print mess
      msg= model2.changeRate(request.form,mess)
      mess=getMess(session['user_email'])
      mode=model.getMode(session['user_email'])
      rate=model2.getRate(mode)
      bca,lca,dca=model2.getAllCA(mode)
      return render_template('Update_Meal_Rates.html',mess=mess,rate=rate,msg=msg,bca=json.dumps(bca),lca=json.dumps(lca),dca=json.dumps(dca))
   else:
      return  render_template('index.html')

def getMess(email):
   name=""
   mode =model.getMode(session["user_email"])
   if mode == "north":
      name="North"
   elif mode == "south":
      name="South"
   elif mode == "yukthar":
      name="Yuktahar"
   elif mode == "kadamb-veg":
      name="VegNBH"
   elif mode == "kadamb-nonveg":
      name="NonVegNBH"
   return name
# @app.route('/logout')
# def logout():
#    # remove the username from the session if it is there
#    session.pop('user_email', None)
#    return redirect(url_for('/'))

if __name__ == '__main__':
   app.run(debug = True)