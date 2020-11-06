from flask import *
from easyaccomod import app

owner_bp = Blueprint("owner", __name__, template_folder='templates/owner')

@owner_bp.route("/api/register")
def api_register():
    return "cac"

@owner_bp.route("/register")
def register():
    return "cac"