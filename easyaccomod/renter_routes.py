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
    
    ret =['Tất cả các quận']
    for _obj in district:
        ret.append(_obj.name)

    return make_response(jsonify(ret),200)

def getStreet(cityName,districtName = None):
    cityCode = City.query.filter_by(name=cityName).first_or_404().code
    print(districtName is None)
    if districtName is not None:
        district_id = District.query.filter_by(city_code=cityCode)\
            .filter_by(name=districtName).first_or_404().id
        streetList = Ward.query.filter_by(district_id = district_id).all()
    else :
        streetList = Ward.query.filter_by(city_code=cityCode).all()
    
    ret = ['Tất cả các phường']
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

def getRoomByDetail(obj,city,district=None,street=None):
    filter_value = {}
    
    filters = ''
    # Price ,area,roomType,,kitchenRoomType,numberOfBedRoom,bathRoomType,numberOfBathRoom,dieu_hoa,nong_lanh,host
    for key in obj:
        if obj[key] is not None and obj[key] != '':
            filter_value[key] = obj[key]
            filters+=key +","
        else :
            filter_value[key] = "None"
    # Query
    
    
    res =  Room.query.filter(Room.city_code == city.code)
    if district is not None:
        res =  Room.query.filter(Room.district_id == district.id)
    if street is not None:
        res =  Room.query.filter(Room.ward_id == street.id)
    try:
        x = filter_value["Price"]
        fPos = x.index('-')
        lower =  int(x[0:fPos])
        
        sPost = x.rindex(' ')
        upper = int(x[fPos+1:sPost])
    except:
        pass
    
    
# Price ,area,roomType,,kitchenRoomType,numberOfBedRoom,bathRoomType,numberOfBathRoom,dieu_hoa,nong_lanh,host
# Integer field : Price, area, numberOfBedRoom,numberOfBathRoombathRoomType,kitchenRoomType
    if (filters.find("Price") != -1):
        res = res.filter(Room.price >= lower*1000000).filter(Room.price <= upper*1000000)
    if (filters.find("area") != -1):
        filter_value["area"] = int(filter_value["area"])
        res = res.filter(Room.dien_tich >= filter_value["area"])
    if (filters.find("numberOfKitchenRoom") != -1):
        filter_value["numberOfKitchenRoom"] = int(filter_value["numberOfKitchenRoom"])
        res =  res.filter(Room.phong_bep >= filter_value["numberOfKitchenRoom"])
    if (filters.find("numberOfBathRoom") != -1):
        filter_value["numberOfBathRoom"] = int(filter_value["numberOfBathRoom"])
        res =  res.filter(Room.phong_tam >= filter_value["numberOfBathRoom"])
    if (filters.find("bathRoomType") != -1):
        filter_value["bathRoomType"] = int(filter_value["bathRoomType"])
        res = res.filter(Room.loai_phong_tam == filter_value["bathRoomType"])
    if (filters.find("kitchenRoomType") != -1):
        filter_value["kitchenRoomType"] = int(filter_value["kitchenRoomType"])
        res = res.filter(Room.loai_phong_bep == filter_value["kitchenRoomType"])
    if (filters.find("dieu_hoa") != -1):
        res = res.filter(Room.dieu_hoa == True)
    if (filters.find("nong_lanh") != -1):
        res = res.filter(Room.nong_lanh == True)
    if (filters.find("host") != -1):
        res = res.filter(Room.chung_chu == True)
    if (filters.find("roomType") != -1):
        filter_value["roomType"] = int(filter_value["roomType"])
        res = res.filter(Room.room_type_id == filter_value["roomType"])

    return res.filter(Room.post.any())