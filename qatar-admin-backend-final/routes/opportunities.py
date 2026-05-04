from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import Opportunity
from extensions import db

opportunity = Blueprint("opportunity", __name__)

@opportunity.route("/", methods=["GET"])
@login_required
def get_all():
    data = Opportunity.query.filter_by(admin_id=current_user.id).all()
    return jsonify([o.__dict__ for o in data])

@opportunity.route("/", methods=["POST"])
@login_required
def create():
    data = request.json
    opp = Opportunity(**data, admin_id=current_user.id)
    db.session.add(opp)
    db.session.commit()
    return jsonify({"message": "Created"})

@opportunity.route("/<int:id>", methods=["PUT"])
@login_required
def update(id):
    o = Opportunity.query.get_or_404(id)
    if o.admin_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    for k, v in data.items():
        setattr(o, k, v)
    db.session.commit()
    return jsonify({"message": "Updated"})

@opportunity.route("/<int:id>", methods=["DELETE"])
@login_required
def delete(id):
    o = Opportunity.query.get_or_404(id)
    if o.admin_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(o)
    db.session.commit()
    return jsonify({"message": "Deleted"})
