from backend import application
from flask import request, render_template, redirect, url_for, jsonify, session
from backend.views import print_geo_value, get_api_total, add_member, validate_member, validate_ID, validate_PW, account_Check, create_api_data, update_api_data
from firebase_admin import db

@application.route('/', methods=['GET'])
def index():
    return render_template('home.html')
    # if 'nickname' in session:
    #     return session['nickname']
    # else:
    #     return render_template('home.html')

@application.route('/list', methods=['GET', 'POST'])
def list():
    if request.method == 'GET' or request.method == 'POST':
        page = request.args.get('page')
        firstpage = False

        if page is None:
            page = 1
            firstpage = True
        else:
            page = int(page)
 
        page = int(page)

        search = request.args.get('searchquery') 
        if search is None:
            search = None

        total = int(get_api_total(search))
        x = 0
        start = 0
        end = 0

        if firstpage is True:
            if(page < 1):
                page = 1
            elif(page>total):
                page = total

            x = (page//10) # 10 // 10 = 1

            if(page%10==0):
                start = ((x-1)*10)+1
                end = ((x)*10)+1
            else:
                start = (x*10)+1
                end = ((x+1)*10)+1

            if(end > total):
                end = total+1

            return redirect(url_for('list', page=1, searchquery=search))
        elif page > total:
            if(page < 1):
                page = 1
            elif(page>total):
                page = total

            x = (page//10) # 10 // 10 = 1

            if(page%10==0):
                start = ((x-1)*10)+1
                end = ((x)*10)+1
            else:
                start = (x*10)+1
                end = ((x+1)*10)+1

            if(end > total):
                end = total+1

            return redirect(url_for('list', page=total, searchquery=search))
        elif page < 1:
            if(page < 1):
                page = 1
            elif(page>total):
                page = total

            x = (page//10) # 10 // 10 = 1

            if(page%10==0):
                start = ((x-1)*10)+1
                end = ((x)*10)+1
            else:
                start = (x*10)+1
                end = ((x+1)*10)+1

            if(end > total):
                end = total+1

            return redirect(url_for('list', page=1, searchquery=search))

        if(page < 1):
            page = 1
        elif(page>total):
            page = total
        x = (page//10) # 10 // 10 = 1
        if(page%10==0):
            start = ((x-1)*10)+1
            end = ((x)*10)+1
        else:
            start = (x*10)+1
            end = ((x+1)*10)+1
        if(end > total):
            end = total+1

        ref = db.reference('piece')
        query = ref.order_by_child('year')

        if search:
            matching_pieces = []
            for item in query.get().values():
                if search in item['name']:
                    matching_pieces.append(item)
            matching_pieces.reverse()
            start2 = (page-1)*10
            end2 = page*10
            sliced_data = matching_pieces[start2:end2]
        else:
            data = []
            for item in query.get().values():
                data.append(item)
            data.reverse() 
            # 데이터 슬라이싱
            start2 = (page-1)*10
            end2 = page*10
            sliced_data = data[start2:end2]

        return render_template('list.html', start=start, end=end, current_page=page, total=total, data=sliced_data, searchquery=search)

@application.route('/patch', methods=['GET'])
def patch():
    return render_template('patch_notes.html')

@application.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@application.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@application.route('/logout', methods=['GET'])
def logout():
    session.pop('nickname', None)
    return redirect('/')

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
        return redirect('/')


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

@application.route('/accountcheck', methods=['POST'])
def accountcheck():
    id = request.form['id']
    pw = request.form['password']
    if (account_Check(id, pw)):
        return redirect('/')
    else:
        return redirect(url_for('login', alertdata = True))

# @application.route('/getdata', methods=['GET'])
# def getdata():
#     cur_page = request.args.get('page')

#     if cur_page:
#         try:
#             cur_page = int(cur_page)
#         except ValueError:
#             cur_page = 1
#     else:
#         cur_page = 1
    
#     return get_api_piece(int(cur_page))

@application.route('/createpiece')
def createpiece():
    return create_api_data()

@application.route('/updatepiece')
def updatepiece():
    return update_api_data()



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