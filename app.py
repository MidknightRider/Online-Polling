from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()

app = Flask(__name__)


@app.route("/")
@app.route("/<name>")
def hello_world(name=None) -> str:
    return render_template("index.html", name=name)
