from geopy.geocoders import Nominatim
import requests
import json

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