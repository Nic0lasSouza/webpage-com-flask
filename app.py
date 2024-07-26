from flask import Flask

app = Flask(__name__)

@app.route("/inicio")
def home():
    return "<h1>hello, flask</h1>"