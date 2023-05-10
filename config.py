#seoul-data-competition
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("seoul-data-competition-firebase-adminsdk-w7mvx-d788c60cbb.json")

firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://seoul-data-competition-default-rtdb.firebaseio.com/' 
    #'databaseURL' : '데이터 베이스 url'
})