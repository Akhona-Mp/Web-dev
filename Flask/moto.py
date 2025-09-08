from flask import Flask, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)
DATABASE = "batabase.db"

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
def bike_detail(bike_id):
    return render_template("bike_detail.html", bike=bike)

def get_db():
    db = getattr(g, '_database',None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# --------------------------
#   Route to Bike Details
# --------------------------
@app.route("/bikes/<int:bike_id>")
def bike_detail(bike_id):
    db = get_db()
    cur = db.execute("SELECT * FROM bikes WHERE id = ?", (bike_id,))
    bike = cur.fetchone()
    
    if bike is None:
        return "<h1>Bike not found</h1>", 404

    return render_template("bike_detail.html", bike=bike)