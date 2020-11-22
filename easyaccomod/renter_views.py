from flask import *
from flask_login import login_user, current_user, logout_user, login_required
from easyaccomod.owner_models import City,District,Ward
from easyaccomod.room_models import Like,Comment
from easyaccomod import app
from easyaccomod.forms import SearchForm
from easyaccomod.renter_routes import getDistrict,getCity,getStreet,getRoom
from easyaccomod.renter_db import addLike
renter = Blueprint("renter", __name__, template_folder='templates/renter')

@renter.route("/renter/search",methods = ['POST','GET'])
@login_required
def search():
    cities = City.query.all()
    form = SearchForm(cities) 
    print(request)
    if (request.method == "POST"):
        req = request.get_json()
  
        # request handler
        if (req[0] == 'city'):
          return getDistrict(req[1])
        elif (req[0] == 'district'):
          return getStreet(req[1])
        elif (req[0] == 'submit'):
          return getRoom(req[1])
        else:
          res = make_response(jsonify("loirequest"),200)
          return res
    return render_template("searchRoom.html",form = form)

@renter.route("/renter/api/addLike",method=["POST"])
@login_required
def addLike():
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

@renter.route("/renter/api/removeLike",method=["POST"])
@login_required
def removeLike():
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

# @renter.route("/renter/api/Comment")
# @login_required
# def addComment():
#   data = request.get_json()
#     res = {}
#     res["status"] = "Error"
#     res["msg"] = "Can't like this room"


