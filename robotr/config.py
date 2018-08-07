import os.path
import json
from flask import current_app as app
config = {}


def check_conf_format(json_data, fields):
        try:
            for elem in json_data:
                for field in fields:
                    if elem.get(field) is None:
                        raise ValueError("Configuration error: missing <" + field + "> field")
        except ValueError as error:

            response = app.response_class(
                response=json.dumps(error),
                status=203,
                mimetype='application/json'
            )

            return response
        return json_data


def init_config():
    register = {
        'robots': {'file': 'config_robots.json', 'fields': {'name', 'id', 'charge'}},
        'states': {'file': 'config_states.json', 'fields': {'state', 'permitted'}}
    }

    for r, file_config in register.items():

        with open(os.path.dirname(__file__) + "\\" + file_config['file']) as f:
            config[r] = json.load(f)

        check_conf_format(config[r], file_config['fields'])

    return config

