from flask import render_template, redirect, url_for, flash, request, abort,jsonify, make_response
from flask_login import login_user, current_user, logout_user, login_required
from easyaccomod.owner_models import City,District,Ward
from easyaccomod import app
from easyaccomod.forms import SearchForm
from easyaccomod.renter_routes import getDistrict,getCity,getStreet,getRoom



@app.route("/renter/search",methods = ['POST','GET'])
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



