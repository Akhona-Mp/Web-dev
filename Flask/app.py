from flask import Flask,redirect,url_for,render_template,request

app = Flask(__name__)

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
        user = request.form["nm"]
        return redirect(url_for("user",usr=user))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == "__main__":
    app.run(debug=True)

