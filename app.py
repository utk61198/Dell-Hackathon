from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/utkarsh/codes/hackathon/database.db'
db = SQLAlchemy(app)
product_list=[]
uname_temp=""
passw_temp=""
mail_temp=""
input_val={}
temp_val=""


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))
    product=db.Column(db.String(80))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/firstpage")
def firstpage():
	return render_template("firstpage.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
    	global uname_temp
    	global passw_temp

        uname = request.form["uname"]
        passw = request.form["passw"]
        uname_temp=uname
        passw_temp=passw
        
        login = user.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return redirect(url_for("firstpage"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']
        

        register = user(username = uname, email = mail, password = passw,product = "")
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/products",methods=["GET","POST"])
def products():
    global passw_temp
    global uname_temp
    if request.method=="POST":
        text=request.form['cartbt']
        product_list.append(text)
        print(product_list)
        login=user.query.filter_by(username=uname_temp,password=passw_temp).first()
        login.product=login.product+"`"+text
        db.session.commit()
    return render_template("products.html")

@app.route("/cart",methods=["GET","POST"])
def cart():
    global uname_temp
    global passw_temp
    temp=user.query.filter_by(username=uname_temp,password=passw_temp).first()
    temp_p=temp.product
    final_list = temp_p.split('`')
    return render_template("cart.html",data=final_list)


@app.route("/choose",methods=["POST"])
def choose():
    global input_val
    global temp_val
    if request.method == "POST":
        input_val = dict(utype_of_product = request.form['caBrands'], purchase_interval=request.form['pint_id'], purchase_data = request.form['pdate_id'], warranty_expiry = request.form['warr_id'], faulty_software=request.form['fsoft_id'], faulty_hardware = request.form['fhard_id'], last_backup = request.form['lback_id'], antivirus_purchase = request.form['apurch_id'], services_used = request.form[sused_id], number_of_tickets_raised =request.form['not_id'], update_period =request.form['uper_id'], last_update = request.form['ludate_id'], wired_wireless=request.form['wir_id'])
        

    return render_template("choose.html")

@app.route("/recommendation",methods=["GET","POST"])
def recommendation():
	return render_template("recommendation.html",data=temp_val)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
