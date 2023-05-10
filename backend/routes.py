from backend import application
from flask import request, render_template, redirect, url_for, jsonify
from backend.views import print_geo_value, get_api_data, add_member, validate_member, validate_ID, validate_PW

@application.route('/', methods=['GET'])
def index():
    return render_template('home.html')

@application.route('/list', methods=['GET'])
def list():
    return render_template('list.html')

@application.route('/patch', methods=['GET'])
def patch():
    return render_template('patch_notes.html')

@application.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@application.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

#멤버 회원가입 조회 => 삽입
@application.route('/member', methods=['POST'])
def member():
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['password']
        email = request.form['email']
        nickname = request.form['nickname']
        # 함수 리턴값으로 조건 건 다음에 리다이렉트 시키기.
        if(validate_member(id, pw)):
            if(add_member(id, pw, email, nickname)):
                return redirect(url_for('login'))
            else:
                return redirect(url_for('signup', alertdata = True))
        else:
            return redirect(url_for('signup', alertdata = True))
    else: 
        return redirect('index')


@application.route('/checkid', methods=['POST'])
def check_id():
    if request.method == 'POST':
        data = request.get_json()
        id = data.get('id')
        return str(validate_ID(id))

@application.route('/checkpw', methods=['POST'])
def check_pw():
    if request.method == 'POST':
        data = request.get_json()
        pw = data.get('pw')
        return str(validate_PW(pw))

@application.route('/getdata')
def getdata():
    return get_api_data()

@application.route('/around')
def around():
    return print_geo_value()

#멤버 삽입
@application.route('/fire')
def add():
    return add_member()

# @application.route('/detail')
# def index():
#     return render_template('home.html')

@application.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error=error), 404