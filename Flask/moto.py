from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for("index"))

@app.route("/bikes")
def bikes():
    return render_template("bikes.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/bikes/<id>")
def bike_detail():
    return render_template("bike_detail.html")
