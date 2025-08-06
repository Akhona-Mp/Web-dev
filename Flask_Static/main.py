from flask import Flask, render_template
from second import second

app = Flask(__name__)
app.register_blueprint(second, url_prefix="/admin")



