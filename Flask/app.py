from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Secret key for decripting
app.secret_key = "akhona"

# Database cofigurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'  #"users" is the name of the table
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Using permanent time ,am able to set a session timer
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

# Model to store information in
class users(db.Model): #db inheritense
    _id = db.Column("id",db.Integer,primary_key=True)
    name = db.Column(db.String(100))#Amount of chars
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
def home():
    return render_template("index.html")

#Allow for redirecting instead of a 404!,takes you back to the homepage.
#E.g "url/admin" ,this will take you to the home page 
@app.route("/admin")
def admin():
    return redirect(url_for("home"))

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        
        # Sessions this store data about the user in the for of a dic
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()
        if found_user :
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            #Add user to data base
            db.session.add(usr)     #Stages the adding of usrs
            db.session.commit()             #This is to finalize the adding of users

        flash("You have succesfully loged in!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already loged in!")
            return redirect(url_for("user"))
        
        return render_template("login.html")

@app.route("/user" ,methods=["POST","GET"])
def user():
    email=None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html",user=user)
    else:
        flash("You are not loged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    # Info from a previous page onto another  e.g Message you recieve After loging out succesfully
    flash("You are logged out!","info")   #Second paremeter has 3 catagories info,warning,error
    session.pop("user",None)   
    session.pop("email",None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

