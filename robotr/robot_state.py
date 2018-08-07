from flask import (
    Blueprint, current_app as app, request, make_response, json, abort
)

from robotr.robot import Robot

bp = Blueprint('robot_state', __name__)


@bp.route('/<string:name>', methods=('GET',))
def get(name):
    try:
        robot = Robot(name)
    except Exception as e:
        if hasattr(e, 'message'):
            msg = e.message
        else:
            msg = e
        return api_response({'error': 'Invalid request:' + msg}, 400)

    data = {
        "state": robot.state,
        "robot_name": robot.name,
        "charge": robot.charge
    }

    return api_response(data, 200)


@bp.route('/<string:name>/start', methods=('GET',))
def start(name):
    try:
        robot = Robot(name)
        robot.start()
    except Exception as e:
        if hasattr(e, 'message'):
            msg = e.message
        else:
            msg = e
        return api_response(msg, 400)

    data = {
        "state": robot.state,
        "robot_name": robot.name,
        "charge": robot.charge
    }

    return api_response(data, 200)


@bp.route('/<path:name>/stop', methods=('GET',))
def stop(name):
    print(name)


@bp.route('/<path:name>/status', methods=('GET',))
def status(name):
    print(name)


@bp.route('/<path:name>/recharge', methods=('GET',))
def recharge(name):
    print(name)


@bp.route('create', methods=('GET',))
def create(name):

    print(name)


@bp.route('<path:path>', methods=('GET', 'POST', 'PUT', 'DELETE',))
def missing_request(path):
    abort(400, {'message': 'Invalid request'})


def api_response(data_, status_):
    response_ = app.response_class(
        response=json.dumps(data_),
        status=status_,
        mimetype='application/json'
    )
    return response_
