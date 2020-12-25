from flask import *
from easyaccomod.owner_models import City,District,Ward,Room,RoomType
from easyaccomod import app
from easyaccomod.forms import SearchForm
from easyaccomod.renter_db import addPriceLog
from easyaccomod.room_models import Like,Comment
from easyaccomod.models import User


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

    cityCode = City.query.filter_by(name = cityName).first_or_404().code
    district = District.query.filter_by(city_code = cityCode).all()
    
    ret =['']
    for _obj in district:
        ret.append(_obj.name)

    return make_response(jsonify(ret),200)

def getStreet(districtName,cityName):
    cityCode = City.query.filter_by(name=cityName).first_or_404().code
    district_id = District.query.filter_by(city_code=cityCode)\
        .filter_by(name=districtName).first_or_404().id
    streetList = Ward.query.filter_by(district_id = district_id).all()
    
    ret = ['']
    for _obj in streetList:
        ret.append(_obj.name)
        
    return make_response(jsonify(ret),200)


def getUserFavoritePost(username):
    user_id =  User.query.filter_by(username=username).first().id
    userFavoritePost = Like.query.filter_by(user_id = user_id)
    # tra ve Query tim kiem tat ca cac bai viet dc thich cua nguoi dung, phuc vu phan trang
    return userFavoritePost

def getRoomByLocation(city,district=None,street=None):
    if(district != None):
        if(street != None):
            res = Room.query.filter_by(city_code = city)\
                .filter_by(district_id = district)\
                    .filter_by(ward_id=street).filter(Room.post.any())
        else:
            res = Room.query.filter_by(city_code = city)\
                .filter_by(district_id = district).filter(Room.post.any())

    else:
        res = Room.query.filter_by(city_code = city).filter(Room.post.any())

    
    
    # GET POST OF ROOMS, AND ELIMINATE ROOM WHICH HAS NO POST
    return res

# def getRoomDetail(obj):
#     result = Room.query.filter_by(city_code = obj["city_code"])\
#         .filter_by(Room.post is not []).all()
#     for i in attrs:
#         print(obj.get(i))
#     return jsonify("succesfull")


# attrs = ["info", "room_type_id", "room_number", "price", "phong_tam", "phong_bep",
#  "gia_dien", "gia_nuoc", "chung_chu", "nong_lanh", "dieu_hoa", "ban_cong", 
#  "tien_ich_khac"]

def getRoomByDetail(obj):
    
    filter_value = []
    filters = ["gia","phong_tam","phong_bep","room_type_id","dieu_hoa","nong_lanh","chung_chu"]
    # phong ngu,phong tam,gia, Dien tich, loai phong (int), dieu hoa,nonglanh,chungchu,bep(Boolean)
    for key in obj:
        if obj[key] is not None:
            for filt in filters:
                if key == filt:
                    filter_value.append(obj[key])
        else :
            filter_value.append("None")
    filter_value = tuple(filter_value)
    # # for i, filt in enumerate(filter_value, 0):
    # #     if filt is not None:
    # #         d = {'Room.{}'.format(filters[i]):filt}  # filter1 = filters[1]
    # #         print(d) 
    # #         res = res.filter(filters[i] )
    # x = 'Room.' + filters[1] + ' >= 2'
    # x = "'" + x + "'"
    res =  Room.query
    if filter_value[0] is not None:
        res =  res.filter(Room.phong_tam >= filter_value[0])
    if filter_value[1] is not None:
        res =  res.filter(Room.phong_bep >= filter_value[1])
    if filter_value[2] is not None:
        res = res.filter(Room.room_type_id == filter_value[2])
    if filter_value[3] is not None:
        res = res.filter(Room.dieu_hoa == filter_value[3])
    if filter_value[4] is not None:
        res = res.filter(Room.nong_lanh == filter_value[4])
    if filter_value[5] is not None:
        res = res.filter(Room.nong_lanh == filter_value[5])
    print(res)
    return res.all()