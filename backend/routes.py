from backend import application
from flask import render_template
from backend.views import print_geo_value, get_api_data

@application.route('/')
def index():
    return render_template('home.html')

@application.route('/list')
def list():
    return render_template('list.html')

@application.route('/getdata')
def getdata():
    return get_api_data()

@application.route('/patch')
def patch():
    return render_template('patch_notes.html')

@application.route('/around')
def around():
    return print_geo_value()


# @application.route('/detail')
# def index():
#     return render_template('home.html')

@application.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error=error), 404