from flask import *
from easyaccomod.owner_models import City,District,Ward,Room,RoomType
from easyaccomod import app
from easyaccomod.forms import SearchForm


# Dinh viet ham de reuse nhung bi bug

# def filter( _list, parameter,value): 
#     x = 0
#     print(parameter)
#     while x < len(_list):
#         print(_list[x].parameter)
#         if (_list[x].parameter != value):
#             del(_list[x])
#             x-=1
#         x+=1
#     return _list

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

def getRoom(payload):

    # prepare filter
    city_code = City.query.filter_by(name = payload[0]["city"]).first().code
    district_id = District.query.filter_by(name = payload[1]["district"]).first().id
    street_id = Ward.query.filter_by(name = payload[2]["street"]).first().id
    
    nearBy = payload[3]['near']
    #print(nearBy)
    price = int(payload[4]['price'])
    #print(price)
    roomTypeId = RoomType.query.filter_by(name = payload[5]['roomType']).first()
    if roomTypeId != None:
        roomTypeId = roomTypeId.id
    area = int(payload[6]['area'])
    #print(area)
    phongTam = int (payload[7]['phong_tam'])
    #print(phongTam)
    nong_lanh = payload[8]['nong_lanh']
    #print(nong_lanh)
    dieu_hoa = payload[9]['dieu_hoa']
    #print(dieu_hoa)
    ban_cong = payload[10]['ban_cong']
    #print(ban_cong)
    chung_chu = payload[11]['chung_chu']
    #print(chung_chu )
    giaDien = int(payload[12]['gia_dien'])
    #print(giaDien)
    giaNuoc = int(payload[13]['gia_nuoc'])
    #print(giaNuoc)
    tienIchKhac = payload[14]['tien_ich_khac']
    #print(tienIchKhac)

    ## Query time 
    if city_code != None:
        res = Room.query.filter_by(city_code=city_code).all()
    # quan
    if district_id != None and res != None:
        x = 0
        while x < len(res) :
            if res[x].district_id != district_id:
                del(res[x])
                x-=1
            x+=1
    
    # pho
    if street_id != None and res != None:
        x = 0
        while x < len(res) :
            if res[x].ward_id != street_id:
                del(res[x])
                x-=1
            x+=1
    
    #gia tien
    if  price != None and res != None:
        x = 0
        while x < len(res) :
            if res[x].price != price:
                del(res[x])
                x-=1
            x+=1
    
    # loai phong
    if roomTypeId != None and res != None:
        x = 0
        while x < len(res) :
            if res[x].room_type_id != roomTypeId:
                del(res[x])
                x-=1
            x+=1

    # so phong tam        
    if phongTam != None and res != None:
        x = 0
        while x < len(res) :
            if res[x].phong_tam != phongTam:
                del(res[x])
                x-=1
            x+=1

    # binh nong lanh        
    if nong_lanh != None and res != None:
        x = 0
        while x < len(res) :
            if res[x].nong_lanh != nong_lanh:
                del(res[x])
                x-=1
            x+=1

    # dieu hoa
    if dieu_hoa != None and res != None:
        x = 0
        while x < len(res) :
            if res[x].dieu_hoa != dieu_hoa:
                del(res[x])
                x-=1
            x+=1

    # ban cong        
    if ban_cong != None and res != None:
        x = 0
        while x < len(res) :
            if res[x].ban_cong != ban_cong:
                del(res[x])
                x-=1
            x+=1

    # chung chu        
    if chung_chu != None and res != None:
        x = 0
        while x < len(res) :
            if res[x].chung_chu != chung_chu:
                del(res[x])
                x-=1
            x+=1

    # gia dien        
    if giaDien != None and res != None: 
        x = 0
        while x < len(res) :
            if res[x].gia_dien != giaDien:
                del(res[x])
                x-=1
            x+=1

    # gia nuoc           
    if giaNuoc != None and res != None: 
        x = 0
        while x < len(res) :
            if res[x].gia_nuoc != giaNuoc:
                del(res[x])
                x-=1
            x+=1

    # tien ich khac           
    if tienIchKhac != None and res != None:
        x = 0
        while x < len(res) :
            if res[x].info.find(tienIchKhac) == -1:
                del(res[x])
                x-=1
            x+=1
    # print(res == [])
    # res = District.query.filter_by(city_code = city_code).all()
    # print(res)
    # print('--------------------------------------------------------------')
    # for districts in res:
    #     print(districts.name)

    if res == []:
        return make_response(jsonify("Can't find your perfect home"),200)
    else:
        ret = []
        for _obj in res:
            ret.append(res)
        return make_response(jsonify(ret),200)


