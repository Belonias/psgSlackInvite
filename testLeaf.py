from flask import Flask, render_template, url_for, flash, redirect

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('landing_page.html')