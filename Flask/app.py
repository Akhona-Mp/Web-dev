from flask import Flask,redirect,url_for,render_template,request,session
from datetime import timedelta

app = Flask(__name__)
# Secret key for decripting
app.secret_key = "akhona"
# Using permanent time ,am able to set a session timer
app.permanent_session_lifetime = timedelta(seconds=30)

@app.route("/")
def home():
    return render_template("index.html")


#Allow for redirecting instead of a 404!,takes you back to the homepage.
#E.g "url/admin" ,this will take you to the home page 
@app.route("/")
def admin():
    return redirect(url_for("home"))

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]

        # Sessions this store data about the user in the for of a dic
        session["user"] = user

        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug=True)

