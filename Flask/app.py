from flask import Flask,redirect,url_for,render_template

app = Flask(__name__)

@app.route("/<name>")
def home(name):
    return render_template("index.html",content=name)

@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

#Allow for redirecting instead of a 404!,takes you back to the homepage.
#E.g "url/admin" ,this will take you to the home page 
@app.route("/admin")
def admin():
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run()

