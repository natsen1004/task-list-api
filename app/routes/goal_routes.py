from flask import Blueprint, request, abort, make_response
from app.models.goal import Goal
from ..db import db
from .route_utilities import validate_model, get_model_with_filters
from app.models.task import Task


bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))
        
    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()

    response = {
        "goal": new_goal.to_dict()  
    }
    return response, 201

@bp.get("")
def get_all_goal():
    return get_model_with_filters(Goal, request.args)

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    if not goal:
        abort(make_response({"message": f"goal_id {goal_id} not found"}, 404))
    goal_response = {
        "goal": goal.to_dict()  
    }

    return goal_response, 200


@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    if not goal:
        abort(make_response({"message": f"goal_id {goal_id} not found"}, 404))
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    response = {
        "goal": goal.to_dict()  
    }

    return response, 200

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    if not goal:
        abort(make_response({"message": f"goal_id {goal_id} not found"}, 404))
    
    db.session.delete(goal)
    db.session.commit()

    response = {
        "details": f'Goal {goal.id} "{goal.title}" successfully deleted'
    }

    return response, 200
