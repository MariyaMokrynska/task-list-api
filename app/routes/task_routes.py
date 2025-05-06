from flask import Blueprint, request, abort, make_response, Response
from ..db import db
from .route_utilities import validate_model, update_dict_to_database, add_dict_to_database
from app.models.task import Task


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    task = add_dict_to_database(Task, request_body)
    return {"task": task.to_dict()}, 201


@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task).order_by(Task.id)
    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return tasks_response


@tasks_bp.get("/<id>")
def get_one_task(id):
    task = validate_model(Task, id)
    return {"task": task.to_dict()}


@tasks_bp.put("/<id>")
def update_task(id):
    # task = validate_model(Task, id)
    request_body = request.get_json()

    task = update_dict_to_database(Task, id, request_body)

    return Response(status=204, mimetype="application/json")


@tasks_bp.delete("/<id>")
def delete_task(id):
    task = validate_model(Task, id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
