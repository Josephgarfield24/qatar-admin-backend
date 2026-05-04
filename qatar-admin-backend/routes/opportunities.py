from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import Opportunity
from extensions import db

opportunity = Blueprint("opportunity", __name__)

@opportunity.route("/", methods=["GET"])
@login_required
def get_all():
    data = Opportunity.query.filter_by(admin_id=current_user.id).all()
    return jsonify([o.name for o in data])

@opportunity.route("/", methods=["POST"])
@login_required
def create():
    data = request.json
    opp = Opportunity(name=data["name"], duration=data["duration"],
                      start_date=data["start_date"], description=data["description"],
                      skills=data["skills"], category=data["category"],
                      future_opportunities=data["future_opportunities"],
                      admin_id=current_user.id)
    db.session.add(opp)
    db.session.commit()
    return jsonify({"message": "Created"})
