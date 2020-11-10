from flask import render_template, redirect, url_for, flash, request, abort,jsonify, make_response
from flask_login import login_user, current_user, logout_user, login_required
from easyaccomod.owner_models import City,District,Ward
from easyaccomod import app
from easyaccomod.forms import SearchForm



@app.route("/renter/search",methods = ['POST','GET'])
@login_required
def search():
    cities = City.query.all()
    form = SearchForm(cities) 
    print(request)
    if (request.method == "POST"):
        req = request.get_json()

        if (req[0] == 'city'):
          cityCode = City.query.filter_by(name = req[1]).first().code
          
          district = District.query.filter_by(city_code = cityCode).all()
          ret =['']
          for _obj in district:
            ret.append(_obj.name)
          res = make_response(jsonify(ret),200)       
          return res
        
        elif (req[0] == 'district'):
          districtCode = District.query.filter_by(name=req[1]).first().id
          streetList = Ward.query.filter_by(district_id = districtCode).all()
          ret = ['']
          for _obj in streetList:
            ret.append(_obj.name)
          res = make_response(jsonify(ret),200)
          return res
    
    return render_template("searchRoom.html",form = form)