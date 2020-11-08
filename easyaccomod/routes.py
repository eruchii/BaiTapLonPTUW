from easyaccomod.forms import  SearchForm
from easyaccomod import app
from flask import render_template
from flask_login import login_required
from easyaccomod.owner_models import City


@app.route("/search")
@login_required
def search():
    cities = City.query.all()
    form = SearchForm(cities) 
    return render_template("searchRoom.html",form = form)
    
