from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
import requests
import json
from config import firebase_admin
from firebase_admin import db
import random

def get_geo_value(address):
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(address)
    crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}

    return crd

def print_geo_value():
    crd = get_geo_value("서울특별시 마포구 상암동 478-1")
    return str(crd['lat']) + " & " + str(crd['lng'])

def get_api_data():
    url = 'http://openapi.seoul.go.kr:8088/6e467277426a61633339737752416b/xml/tvGonggongAllArt/1/5/'

    response = requests.get(url)
    print(response.text)

    return "json?"

def add_member(id, pw, email, nickname):
    a = ["성실한", "진지한"]
    b = ["피카소", "살바도르 달리"]
    
    trim_nickname = str(nickname).replace(' ','')
    trim_email = str(email).replace(' ','')

    if trim_nickname == '' or trim_nickname == None or len(trim_nickname)<2:
        nickname = str(random.choice(a) + " " + random.choice(b))

    if(trim_email == None or trim_email == ''):
        email = False


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