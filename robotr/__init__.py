import os
import time
from threading import (
    Thread, ThreadError
)

from flask import (
    Flask, request, json, jsonify
)

from . import config


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'robotr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # load states allowed for the robots

    from . import db
    # register db initiator
    db.init_app(app)

    from . import server
    # register server control blueprint
    app.register_blueprint(server.bp, url_prefix='/server/')

    from . import robot_state
    # register states blueprint
    app.register_blueprint(robot_state.bp, url_prefix='/robot/')

    from . import config
    app.robots_config = config.init_config()

    # simple discharging daemon thread

    # charging maintenance thread

    def handle_charging():

        with app.app_context():

            db_connection = db.get_db()

            while True:
                time.sleep(1)
                db_connection.execute('UPDATE robot '
                                      'SET charge = charge + 1 '
                                      'WHERE state = "charging" and charge < 100')

                db_connection.execute('UPDATE robot '
                                      'SET charge = charge - 1 '
                                      'WHERE state = "started" and charge > 0')
                db_connection.commit()


                db_connection.execute('UPDATE robot '
                                      'SET state = "charging" '
                                      'WHERE state = "started" and charge = 0')

                db_connection.execute('UPDATE robot '
                                      'SET state = "stopped" '
                                      'WHERE state = "charging" and charge = 100')
                db_connection.commit()

    try:
        thread_charge = Thread(name='handle_charging', target=handle_charging)
        thread_charge.setDaemon(True)
        thread_charge.start()

    except ThreadError as error:
        print(error)

    # handle missing
    @app.errorhandler(404)
    @app.errorhandler(405)
    def _handle_api_error(ex):
        if request.path.startswith('/'):
            return ex
        else:
            return ex

    @app.errorhandler(400)
    def _handle_missing(error):
        data = jsonify({'message': error.description['message']})
        response = app.response_class(
            response=data,
            status=400,
            mimetype='application/json'
        )
        return response

    return app