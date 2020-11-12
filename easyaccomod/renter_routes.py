from flask import *
from easyaccomod.owner_models import City,District,Ward,Room
from easyaccomod import app
from easyaccomod.forms import SearchForm

def getCity():
    city = City.query.all()
    return city

def getDistrict(cityName):
          cityCode = City.query.filter_by(name = cityName).first().code
          
          district = District.query.filter_by(city_code = cityCode).all()
         
          ret =['']
          for _obj in district:
            ret.append(_obj.name)
          
          res = make_response(jsonify(ret),200)       
          
          return res

def getStreet(districtName):
    districtCode = District.query.filter_by(name=districtName).first().id
    streetList = Ward.query.filter_by(district_id = districtCode).all()
    ret = ['']
    for _obj in streetList:
        ret.append(_obj.name)
        res = make_response(jsonify(ret),200)
    return res

def getResult(payload):
    city_code = City.query.filter_by(name = payload[0]["city"]).first().code
    district_id = District.query.filter_by(name = payload[1]["district"]).first().id
    street_id = Ward.query.filter_by(name = payload[2]["street"]).first().id
    
    res = Room.query.filter_by(city_code=city_code).all()
    while res != None:
        res = Room.query.filter_by(district_id = district_id).all()
        res = Room.query.filter_by(ward_id = street_id).all()
        res = Room.query.filter_by(price = payload[4]['price']).all()
        res = Room.query.filter_by(room_type_id = 3).all()
        res = Room.query.filter_by(phong_tam = int( payload[7]['phong_tam'] ) ).all()
        res = Room.query.filter_by(nong_lanh = payload[8]['nong_lanh']).all()
        res = Room.query.filter_by(dieu_hoa = payload[9]['dieu_hoa']).all()
        res = Room.query.filter_by(ban_cong = payload[10]['ban_cong']).all()
        res = Room.query.filter_by(chung_chu = payload[11]['chung_chu']).all()
        res = Room.query.filter_by(gia_dien= payload[12]['gia_dien']).all()
        res = Room.query.filter_by(nong_lanh = payload[13]['gia_nuoc']).all()
        res = Room.query.filter_by(nong_lanh = payload[14]['tien_ich_khac']).all()
    if res == None:
        return make_response(jsonify("Can't find your perfect home"),200)
    else:
        ret = []
        for _obj in res:
            ret.append(res)
        return make_response(jsonify(ret),200)