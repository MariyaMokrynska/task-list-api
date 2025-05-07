from flask import Blueprint, request, Response
from ..db import db
from .route_utilities import validate_model, update_dict_to_database, add_dict_to_database
from app.models.goal import Goal

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@goals_bp.post("")
def create_goal():
    request_body = request.get_json()
    goal = add_dict_to_database(Goal, request_body)
    return {"goal": goal.to_dict()}, 201


@goals_bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    goals_response = []
    for goal in goals:
        goals_response .append(goal.to_dict())
    return goals_response


@goals_bp.get("/<id>")
def get_one_goal(id):
    goal = validate_model(Goal, id)
    return {"goal": goal.to_dict()}


@goals_bp.put("/<id>")
def update_goal(id):
    request_body = request.get_json()
    goal = update_dict_to_database(Goal, id, request_body)
    return Response(status=204, mimetype="application/json")


@goals_bp.delete("/<id>")
def delete_goal(id):
    goal = validate_model(Goal, id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
