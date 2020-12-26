from flask import Blueprint
from flask import render_template
from flask import request,redirect,url_for
from easyaccomod.forms import SearchForm
from easyaccomod.owner_models import City,District,Ward
main = Blueprint('main', __name__)

@main.route('/',methods=["POST","GET"])
@main.route('/home',methods=["POST","GET"])
def home():
    cities = City.query.all()
    form = SearchForm(cities)
    if request.method == 'POST':
      # Get Data out of the post
      city = request.form.getlist('city')
      district = request.form.getlist('district')
      street = request.form.getlist('street')
      district_id = None
      street_id = None
      city_code = City.query.filter_by(name = city[0]).first().code
      if (district[0] !='Tất cả các quận' ):
        district_id = District.query.filter_by(name = district[0]).first().id
      if (street[0] != 'Tất cả các phường'):
        street_id = Ward.query.filter_by(name = street[0]).first().id
      # Pass it to search()
      return redirect(url_for('renter.search',city=city_code,district=district_id,street=street_id))
    return render_template("/renterFrontPage.html",form = form)

@main.route('/about')
def about():
    return render_template("about.html")
