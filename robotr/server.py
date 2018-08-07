import os
import signal
from threading import Thread
from flask import (
    Blueprint, json, current_app as app, request
)


bp = Blueprint('server', __name__)


@bp.route('/health', methods=['GET'])
def index():
    data = {'message': 'Server is running'}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )

    return response


@bp.route('/stop', methods=['GET'])
def terminate_server():
    def handle_terminate(value):
        import time
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGTERM)

    thread = Thread(target=handle_terminate, kwargs={'value': request.args.get('value', 1)})

    data = {'message': 'Server shutting down...'}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    thread.start()

    return response