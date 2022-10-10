from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_CyKor():
    return "hello_CyKor"
