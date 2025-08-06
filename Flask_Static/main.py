from flask import Flask, render_template
from second import second

app = Flask(__name__)
app.register_blueprint(second, url_prefix="/admin")

# @app.route("/home")
@app.route("/")
def home():
    return "<h1>Tests</h1>"

if __name__ == "__main__":
    app.run(debug=True)

