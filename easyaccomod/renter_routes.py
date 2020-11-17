from flask import *
from easyaccomod.owner_models import City,District,Ward,Room,RoomType
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

    # prepare filter
    city_code = City.query.filter_by(name = payload[0]["city"]).first().code
    district_id = District.query.filter_by(name = payload[1]["district"]).first().id
    street_id = Ward.query.filter_by(name = payload[2]["street"]).first().id
    
    nearBy = payload[3]['near']
    print(nearBy)
    price = int(payload[4]['price'])
    print(price)
    roomTypeId = RoomType.query.filter_by(name = payload[5]['roomType']).first()
    if roomTypeId != None:
        roomTypeId = roomTypeId.id
    area = int(payload[6]['area'])
    print(area)
    phongTam = int (payload[7]['phong_tam'])
    print(phongTam)
    nong_lanh = payload[8]['nong_lanh']
    print(nong_lanh)
    dieu_hoa = payload[9]['dieu_hoa']
    print(dieu_hoa)
    ban_cong = payload[10]['ban_cong']
    print(ban_cong)
    chung_chu = payload[11]['chung_chu']
    print(chung_chu )
    giaDien = int(payload[12]['gia_dien'])
    print(giaDien)
    giaNuoc = int(payload[13]['gia_nuoc'])
    print(giaNuoc)
    tienIchKhac = payload[14]['tien_ich_khac']
    print(tienIchKhac)

    ## Query time 
    if city_code != None:
        res = Room.query.filter_by(city_code=city_code).all()
    if district_id != None:
        res = Room.query.filter_by(district_id = district_id).all()
    if street_id != None:
        res = Room.query.filter_by(ward_id = street_id).all()
    if  price != None:
        res = Room.query.filter_by(price = price).all()
    if roomTypeId != None:
        res = Room.query.filter_by(room_type_id = roomTypeId).all()
    if phongTam != None:
        res = Room.query.filter_by(phong_tam = phongTam).all()
    if nong_lanh != None:
        res = Room.query.filter_by(nong_lanh = nong_lanh).all()
    if dieu_hoa != None:
        res = Room.query.filter_by(dieu_hoa = dieu_hoa).all()
    if ban_cong != None:
        res = Room.query.filter_by(ban_cong = ban_cong).all()
    if chung_chu != None:
        res = Room.query.filter_by(chung_chu = chung_chu).all()
    if giaDien != None: 
        res = Room.query.filter_by(gia_dien= giaDien).all()
    if giaNuoc != None: 
        res = Room.query.filter_by(gia_nuoc = giaNuoc).all()
    if tienIchKhac != None:
        res = Room.query.filter_by(tien_ich_khac = tienIchKhac).all()

    if res == []:
        return make_response(jsonify("Can't find your perfect home"),200)
    else:
        ret = []
        for _obj in res:
            ret.append(res)
        return make_response(jsonify(ret),200)
