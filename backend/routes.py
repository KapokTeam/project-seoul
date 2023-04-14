from backend import application
from flask import render_template

@application.route('/')
def index():
    return render_template('home.html')

@application.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error=error), 404