from flask import Blueprint, request, Response, make_response, abort
from ..db import db
from .route_utilities import validate_model, update_dict_to_database, add_dict_to_database
from app.models.goal import Goal
from app.models.task import Task

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@goals_bp.get("/<id>/tasks")
def get_task_with_goal(id):
    goal = validate_model(Goal, id)
    return goal.to_dict(withRelationship=True)


@goals_bp.post("/<goal_id>/tasks")
def create_task_with_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    request_body["id"] = goal.id

    try:
        goal.tasks.clear()
        for task_id in request_body['task_ids']:
            task = validate_model(Task, task_id)
            task.goal_id = goal.id

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    # db.session.add(new_task)
    db.session.commit()

    return make_response(request_body, 200)


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
