from ..db import db
from flask import abort, make_response
from app.models.task import Task


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if model is None:
        response = {"message": f"Task {model_id} not found"}
        abort(make_response(response, 404))

    return model


def add_dict_to_database(cls, data):
    try:
        new_instance = cls.from_dict(data)
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_instance)
    db.session.commit()

    return new_instance


def update_dict_to_database(cls, id, data):
    new_instance = cls.from_dict(data)

    old_instance = validate_model(cls, id)
    if old_instance is None:
        return None

    old_instance.update(new_instance)
    db.session.commit()

    return old_instance
