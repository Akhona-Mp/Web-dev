from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask application
app = Flask(__name__)

# Secret key used for encrypting session data
app.secret_key = "akhona"

# Database configurations
# SQLite database named "users.sqlite3" will be created/used
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
# Disable modification tracking to save memory
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Session timeout (user stays logged in for 5 minutes if inactive)
app.permanent_session_lifetime = timedelta(minutes=5)

# Initialize SQLAlchemy for database handling
db = SQLAlchemy(app)


class users(db.Model):
    """
    Database model for storing user information.

    Attributes:
        _id (int): Primary key (unique identifier for each user).
        name (str): Username (up to 100 characters).
        email (str): User email address (up to 100 characters).
    """
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        """
        Constructor for creating a new user instance.

        Args:
            name (str): Username.
            email (str): User's email address.
        """
        self.name = name
        self.email = email


@app.route("/")
def home():
    """
    Render the home page.

    Returns:
        HTML template for the index page.
    """
    return render_template("index.html")


@app.route("/admin")
def admin():
    """
    Redirect admin route to home page instead of returning 404.

    Returns:
        Redirect to home page.
    """
    return redirect(url_for("home"))


@app.route("/view")
def view():
    """
    Display all users stored in the database.

    Returns:
        HTML template displaying all user records.
    """
    return render_template("view.html", values=users.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
    """
    Handle user login functionality.

    POST:
        - Get username from form.
        - Store user in session.
        - If user exists, load email from database.
        - If not, create new user in database.
        - Flash success message and redirect to /user page.

    GET:
        - If user already logged in, flash message and redirect to /user page.
        - Otherwise, render login page.

    Returns:
        Redirects or renders login template.
    """
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]

        # Save username in session
        session["user"] = user

        # Check if user exists in database
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            # Create new user with empty email
            usr = users(user, "")
            db.session.add(usr)      # Stage user for addition
            db.session.commit()      # Commit changes to DB

        flash("You have successfully logged in!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))

        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    """
    Handle user profile page.

    POST:
        - Save/update user's email in database.
        - Flash success message.

    GET:
        - Display user profile with email if available.

    Returns:
        Render user profile page or redirect to login.
    """
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email

            # Update user email in database
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", user=user)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """
    Log out the current user.

    - Clear user and email from session.
    - Flash logout confirmation.
    - Redirect to login page.

    Returns:
        Redirect to login page.
    """
    flash("You are logged out!", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    # Ensure database tables are created before running app
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=7000)
