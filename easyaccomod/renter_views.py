from flask import *
from flask_login import login_user, current_user, logout_user, login_required
from easyaccomod.owner_models import City,District,Ward
from easyaccomod.room_models import Like,Comment
from easyaccomod import app
from easyaccomod.forms import SearchForm
from easyaccomod.renter_routes import getDistrict,getCity,getStreet,getUserFavoritePost,getRoomByLocation
from easyaccomod.renter_db import addLike,removeLike,addComment,getRoomById,getPostByRoomID
import datetime

renter_bp = Blueprint("renter",__name__,template_folder='templates/renter')
# Index Page
@renter_bp.route("/",methods = ['POST','GET'])
def frontPageDisplay():
    cities = City.query.all()
    form = SearchForm(cities)
    if request.method == 'POST':
      # Get Data out of the post
      city = request.form.getlist('city')
      district = request.form.getlist('district')
      street = request.form.getlist('street')
      
      city_code = City.query.filter_by(name = city[0]).first().code
      district_id = District.query.filter_by(name = district[0]).first().id
      street_id = Ward.query.filter_by(name = street[0]).first().id
      # Pass it to search()
      return redirect(url_for('renter.search',city=city_code,district=district_id,street=street_id))
    return render_template("/renterFrontPage.html",form = form)


# Search Page
@renter_bp.route("/search/<city>/", methods=['POST', "GET"])
@renter_bp.route("/search/<city>/<district>/", methods=['POST', "GET"])
@renter_bp.route("/search/<city>/<district>/<street>/",methods=['POST','GET'])
def search(city,district=None,street=None):
  currentDateTime = datetime.datetime.utcnow()
  
  if (request.method == "POST"):
    try:
      # Take Data from POST from
      city = request.form.getlist('city')
      district = request.form.getlist('district')
      street = request.form.getlist('street')
      
    except:
      return jsonify({"status":"Error","msg":"Problem searching"})

  # Get Room se tra ve list cac Room hop le, tu do" vut vao template
  page = request.args.get('page',1,type=int)
  # GET ROOM
  rooms = getRoomByLocation(city,district,street)
  rooms = rooms.paginate(page=page,per_page=5)
  
  city = City.query.filter_by(code = city).first()
  district = District.query.filter_by(id = district).first()
  street = Ward.query.filter_by(id = street).first()
  
  return render_template("renter/renterSearchPage.html",rooms = rooms, dateTime = currentDateTime,city = city,district=district,street=street)


@renter_bp.route("/api/addLike",methods=["POST","GET"])
@login_required
def add_Like():

    data = request.get_json()
    res = {}
    res["status"] = "Error"
    res["msg"] = "Can't like this room"
    try:
      status,msg = addLike(data["user_id"],data["room_id"])
      if status:
          res["status"] = "Success"
      else :
          res["status"] = "Fail"
      res["msg"] = msg
      return jsonify(res)
    except:
      return jsonify(res)

# Remove Like

@renter_bp.route("/api/removeLike",methods=["POST"])
@login_required
def remove_Like():
    data = request.get_json()
    res = {}
    res["status"] = "Error"
    res["msg"] = "Can't like this room"
    try:
      status,msg = removeLike(data["user_id"],data["room_id"])
      
      if status:
        res["status"] = "Success"
      else :
        res["status"] = "Fail"
      res["msg"] = msg
      
      return jsonify(res)
    
    except:
      return jsonify(res)

# Add Comment
@renter_bp.route("/api/Comment", methods = ["POST","GET"])
@login_required
def add_Comment():
  data = request.get_json()
  res = {}
  res["status"] = "Error"
  res["msg"] = "Can't Comment"
  try:
    status,msg = addComment(data["user_id"],data["post_id"],data["content"])
    if (status):
      res["status"] = "Succesfully Added"
    else:
      res["status"] = "Fail"
    res["msg"] = msg
    return jsonify(res)
  except:
    return jsonify(res)


@renter_bp.route("/api/getDistrict",methods=["POST"])
def getDistrictAPI():
  req = request.get_json()
  # request handler
  return getDistrict(req.get('city'))

@renter_bp.route("/api/getStreet",methods=["POST"])
def getStreetAPI():
  req = request.get_json()
  # request handler
  return getStreet(req['district'],req['city'])


@renter_bp.route("/api/getRoomById",methods=["POST","GET"])
@login_required
def getRoom():
  res = {}
  res["status"] = "error"
  res["msg"] = "co loi xay ra"
  res["data"] = {}
  req = request.get_json()
  status, resp = getRoomById(req["room_id"])
  if(status == "error"):
    res["status"] = status
    res["msg"] = resp
    return jsonify(res)
  attrs = ["image","info", "room_type_id", "room_number", "price", "phong_tam", "phong_bep", "gia_dien", "gia_nuoc", "chung_chu", "nong_lanh", "dieu_hoa", "ban_cong", "tien_ich_khac"]
  res["data"]["city"] = resp.city_code
  res["data"]["district"] = resp.ward_id
  res["data"]["ward"] = resp.ward_id
  res["data"]["location"] = resp.getLocation()
  for attr in attrs:
    res["data"][attr] = getattr(resp, attr)
    res["status"] = "success"
    res["msg"] = "thanh cong"
  return jsonify(res)

@renter_bp.route("/api/getPostByRoomID",methods=["POST"])
def getPost():
  data = request.get_json()
  res = {}
  res["status"] = "Error"
  res["msg"] = "co loi xay ra"
  res["data"] = {}
  try:
    status,resp = getPostByRoomID(data["room_id"])
    if (status == "success"):
      res["status"] = "Succesfully Added"
      res["msg"] = "thanh cong"
      res["data"]["like"] = resp.getLike()
      res["data"]["comment"] = resp.getAllComment()
      res["data"]["id"] = resp.id
    else:
      res["status"] = "Fail"
    return jsonify(res)
  except:
    return jsonify(res)

@renter_bp.route("/<username>/favorite")
@login_required
def getFavoritePost(username):
  page = request.args.get('page')
  posts = getUserFavoritePost(username).paginate(page=page,per_page=5)

  return render_template("renter/renterSearchPage.html",posts = posts)


@renter_bp.route("/api/testPaginationFetch",methods=["POST"])
@login_required
def testPaginationFetch():
  page = int(request.get_json().get('page'))
  print(page)
  citys = testPage().paginate(page=page,per_page=5)
  ret =[]
  print(citys.iter_pages())
  for city in citys.items:
    item ={}
    item['code']  = city.code
    item['name'] = city.name
    ret.append(item)
  return jsonify(ret)