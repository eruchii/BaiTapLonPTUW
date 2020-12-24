from flask import Blueprint
from flask import render_template
from easyaccomod.forms import SearchForm
from easyaccomod.owner_models import City
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    cities = City.query.all()
    form = SearchForm(cities)
    return render_template("/renterFrontPage.html",form = form)

@main.route('/about')
def about():
    return render_template("about.html")
