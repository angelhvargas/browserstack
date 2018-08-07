from time import sleep


class Robot:
    """ Class Robot, does define the structure of the robots and his states
        Attributes:
        identifier (string): is the id of the given robot.
    """
    def __init__(self, name):

        data = self.get(name)

        if not data:
            raise Exception("robot: " + name + 'does not exists')

        self.id = data['id']
        self.name = data['name']
        self.charge = data['charge']
        self.state = data['state']

    @staticmethod
    def get(name):
        from robotr import (
            config, db
        )
        robots_config = config.config['robots']

        robot_setup = [element for element in robots_config if element['name'] == name]
        try:
            # first check if robot have global config state
            if not robot_setup[0]["id"]:
                raise Exception("robot not configured")
            robot = db.get_db().execute(
                'SELECT * FROM robot WHERE id=? LIMIT 1',
                (robot_setup[0]["id"],)
            ).fetchone()
        except Exception as error:
            raise error
        return robot

    @staticmethod
    def update_state(id, state):
        from robotr import db
        try:
            db_con = db.get_db()
            db_con.execute(
                'UPDATE robot SET state=(?) WHERE id=(?)',
                (state, id,)
            )
            db_con.commit()
        except db.get_db().DatabaseError as error:
            return error
        return True

    @staticmethod
    def create(data):
        from robotr import db
        identifier = data['id']
        name = data['name']
        charge = 0.0
        state = 'charging'
        db_connection = db.get_db()

        db_connection.execute(
            'INSERT INTO robot (id, name, charge, state)'
            'VALUES (?, ?, ?, ?)',
            (identifier, name, charge, state)
        )

        db_connection.commit()
        return data

    # set the ready state
    def set_ready(self):
        if self.charge > 50 and self.state not in ['stopping', 'recharging']:
            Robot.update_state(self.id, 'ready')
            return self
        else:
            self.recharge()
            return False

    # set the recharging state
    def set_recharging(self):
        if self.charge < 100:
            Robot.update_state('recharging')
            self.recharge()

    def recharging(self):
        while self.charge <= 100:
            sleep(1)
            self.charge += 1
        self.set_ready()
        return self

    def starting(self):
        if self.state is not 'charging':
            self.state = 'starting'
            Robot.update_state(self.id, 'starting')
            self.started()
            return self.state

        return False

    def started(self):
        if self.state in ['starting']:
            self.state = 'started'
            Robot.update_state(self.id, 'started')
        return self.state

    def stopping(self):
        return self

    def start(self):
        if self.state not in ['charging', 'started']:
            self.starting()
        else:
            return False

    def handle_discharge(self):
        return self