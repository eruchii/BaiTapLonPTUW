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

def getRoomByCity(city):

    # Query with the parameter
    res = Room.query.filter_by(city_code = city).filter(Room.post.any())

    # if res.count() == 0:
    #     return make_response(jsonify("Can't find your perfect home"),200)
    return res

def getUserFavoritePost(username):
    user_id =  User.query.filter_by(username=username).first().id
    userFavoritePost = Like.query.filter_by(user_id = user_id)
    # tra ve Query tim kiem tat ca cac bai viet dc thich cua nguoi dung, phuc vu phan trang
    return userFavoritePost

def getRoomByLocation(city,district,street):
    res = Room.query.filter_by(city_code = city)\
        .filter_by(district_id = district)\
            .filter_by(ward_id=street).filter(Room.post.any())
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
