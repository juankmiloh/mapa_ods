from flask import render_template
from ..controller import controller


@controller.route('/')
def home():
    return render_template("index.html")

@controller.route('/static')
def static_redirect():
    return render_template('index.html')

@controller.route('/ods/&gtjwt')
def static_redirect():
    return render_template('index.html')
