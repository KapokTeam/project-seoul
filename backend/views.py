from flask import Flask, request, jsonify, session
from geopy.geocoders import Nominatim
import requests
import json
from config import firebase_admin
from firebase_admin import db
import random
from bs4 import BeautifulSoup
import xmltodict
import math

def add_member(id, pw, email, nickname):
    a = ["성실한", "진지한"]
    b = ["피카소", "살바도르 달리"]
    
    trim_nickname = str(nickname).replace(' ','')
    trim_email = str(email).replace(' ','')

    if trim_nickname == '' or trim_nickname == None or len(trim_nickname)<2:
        nickname = str(random.choice(a) + " " + random.choice(b))

    if(trim_email == None or trim_email == ''):
        email = 'none'


    ref = db.reference('member') # 기본 가장 상단을 가르킴
    user_ref = ref.push()
    user_ref.set({
        'id' : str(id),
        'password' : str(pw),
        'nickname' : str(nickname),
        'email' : str(email)
        })
    
    # ref.update({'id' : 'development'}) # 해당 변수가 없으면 생성한다.
    return True

def validate_member(id, pw):
    ref = db.reference('member')
    IDExist = ref.order_by_child('id').equal_to(id).get()
    PWExist = ref.order_by_child('password').equal_to(pw).get()
    # NicknameExist = ref.order_by_child('id').equal_to(id).get()
    # EmailExist = ref.order_by_child('email').equal_to(id).get()

    if IDExist:
        # return jsonify({'message': 'Exist ' + result}), 200
        return False
    else:
        # return jsonify({'message': 'NoExist'}), 200
        if PWExist:
            return False
        else:
            return True
    
    # member에서 id가 id인 값을 조회
    # docs = db.collection(u'member')

    
    #for doc in docs:
    #    print(u'{} => {}'.format(doc.id, doc.to_dict()))

def validate_ID(id):
    ref = db.reference('member')
    IDExist = ref.order_by_child('id').equal_to(id).get()

    if IDExist:
        return 'True'
    else:
        return 'False'

def validate_PW(pw):
    ref = db.reference('member')
    PWExist = ref.order_by_child('password').equal_to(pw).get()

    if PWExist:
        return 'True'
    else:
        return 'False'

# def validate_email(email):
#     ref = db.reference('member')

#     if(email == None):
#         email = ' '

#     EmailExist = ref.order_by_child('email').equal_to(email).get()

#     if EmailExist:
#         return 'True'
#     else:
#         return 'False'

def account_Check(id, pw):
    ref = db.reference('member')
    AccountExist = ref.order_by_child('id').equal_to(id).get()

    if AccountExist:
        for key, value in AccountExist.items():
            if value.get('password') == pw:
                session['nickname'] = value.get('nickname')
                return True
    else:
        return False
    
def get_api_total(search):
    # 이전 쿼리에서 가져온 데이터 중에서 6번째 데이터의 'year' 값을 가져옴
    #ref = db.reference('piece').order_by_child('year').limit_to_first(5).get()
    #last_year = list(ref.values())[-1]['year']

    # 'year' 필드가 'last_year' 이상인 데이터 중에서 다섯 번째까지의 데이터를 가져옴
    #ref = db.reference('works').order_by_child('year').start_at(last_year).limit_to_first(5).get()
    #ref = db.reference('piece').order_by_child('year').limit_to_first(5).get()
    # 가져온 데이터를 출력함
    print(search)
    if(search == None):
        ref = db.reference('piece')
        keys = ref.order_by_key().get()
        total = math.ceil(len(keys)/10)
    else:
        ref = db.reference('piece')
        data = ref.order_by_child('year')
        matching_pieces = []
        for item in data.get().values():
            if str(search).lower() in str(item['name']).lower():
                matching_pieces.append(item)
        total = math.ceil(len(matching_pieces)/10)

    return str(total)

# def get_api_piece(cur_page, search):
#     ref = db.reference('piece')

#     # year 필드를 기준으로 내림차순으로 정렬된 데이터 가져오기
#     query = ref.order_by_child('year')

#     data = []
#     for item in query.get().values():
#         data.append(item)

#     data.reverse() 

#     # 데이터 슬라이싱
#     start = (cur_page-1)*10
#     end = cur_page*10
#     sliced_data = data[start:end]

#     # 결과 출력
#     for item in sliced_data:
#         print(item)

#     return "ok"

def update_api_data():
    return "json?"

def create_api_data():
    ref = db.reference('')
    # piece_ref = ref.update(data_list)
    # user_ref.set()
    #user_ref = ref.push()
    #user_ref.set({
    #    'id' : str(id),
    #    'password' : str(pw),
    #    'nickname' : str(nickname),
    #    'email' : str(email)
    #    })

    url1 = 'http://openapi.seoul.go.kr:8088/6e467277426a61633339737752416b/xml/tvGonggongArt/1/1000/'
    url2 = 'http://openapi.seoul.go.kr:8088/6e467277426a61633339737752416b/xml/tvGonggongAllArt/1/1000/'
    url3 = 'http://openapi.seoul.go.kr:8088/6e467277426a61633339737752416b/xml/gongGongArtEtc/1/1000/'
    
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    response3 = requests.get(url3)
    
    xml_data1 = xmltodict.parse(response1.text)  
    xml_data2 = xmltodict.parse(response2.text)
    xml_data3 = xmltodict.parse(response3.text)      
    
    #data_list = []
        # data = 
        # data_list.append({item['GA_KNAME']: data})

    for item in xml_data2['tvGonggongAllArt']['row']:
        name = str(item['GA_KNAME'])
        name = name.replace('/', '_').replace('(', '_').replace(')', '_').replace('.', '_').replace('$', '_').replace('#', '_').replace('[', '_').replace(']', '_')

        ref.child('piece').child(name).set({
            'name': item['GA_KNAME'],
            'year': item['GA_INS_DATE'],
            'address': item['GA_ADDR'],
            'description': 'none',
        })

        # data = 
        # data_list.append({item['GA_KNAME']: data})
    for item in xml_data1['tvGonggongArt']['row']:
        name = str(item['GA_KNAME'])
        name = name.replace('/', '_').replace('(', '_').replace(')', '_').replace('.', '_').replace('$', '_').replace('#', '_').replace('[', '_').replace(']', '_')

        if item['GA_DETAIL'] == '' or item['GA_DETAIL'] == ' ' or item['GA_DETAIL'] == None:
            ref.child('piece').child(name).set({
            'name': item['GA_KNAME'],
            'year': item['GA_INS_DATE'],
            'address': item['GA_ADDR1'],
            'description': 'none',
            })
        else:
            ref.child('piece').child(name).set({
            'name': item['GA_KNAME'],
            'year': item['GA_INS_DATE'],
            'address': item['GA_ADDR1'],
            'description': item['GA_DETAIL'],
            })  

    for item in xml_data3['gongGongArtEtc']['row']:
        name = str(item['GA_KNAME'])
        name = name.replace('/', '_').replace('(', '_').replace(')', '_').replace('.', '_').replace('$', '_').replace('#', '_').replace('[', '_').replace(']', '_')

        if item['GA_DETAIL'] == '' or item['GA_DETAIL'] == ' ' or item['GA_DETAIL'] == None:
            ref.child('piece').child(name).set({
            'name': item['GA_KNAME'],
            'year': item['GA_INS_DATE'],
            'address': item['GA_ADDR1'],
            'description': 'none',
            })
        else:
            ref.child('piece').child(name).set({
            'name': item['GA_KNAME'],
            'year': item['GA_INS_DATE'],
            'address': item['GA_ADDR1'],
            'description': item['GA_DETAIL'],
            })  
          
        # data_list.append({item['GA_KNAME']: data})

    # 추출한 데이터를 JSON으로 변환
    #json_data = json.dumps(data_list, ensure_ascii=False)

    # soup = BeautifulSoup(response2.text, 'xml')

    # rows = soup.find_all('row')
    # data = []
    # for row in rows:
    #     item = {}
    #     item['작품명'] = row.GA_KNAME.text
    #     item['연도'] = row.GA_INS_DATE.text
    #     item['주소'] = row.GA_ADDR.text
    #     item['상세설명'] = 'none'
    #     data.append(item)

    #print(data_list)
    
    #json_data = json.dumps(data_list, ensure_ascii=False)

    #with open('json/artlist.json', 'w', encoding='utf-8') as f:
    #    f.write(json_data)

    return "Update"


def get_geo_value(address):
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(address)
    crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}

    return crd

def print_geo_value():
    crd = get_geo_value("서울특별시 마포구 상암동 478-1")
    return str(crd['lat']) + " & " + str(crd['lng'])
