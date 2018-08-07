DROP TABLE IF EXISTS robot;

CREATE TABLE robot (
  id VARCHAR PRIMARY KEY UNIQUE,
  name VARCHAR DEFAULT '',
  charge INTEGER NOT NULL DEFAULT 0.0,
  state VARCHAR DEFAULT 'stopped'
);


INSERT INTO robot (id, name, charge, state)
VALUES( '23fc1', 'c3po', 100, 'ready');

INSERT INTO robot (id, name, charge, state)
VALUES( '56fa12', 'r2d2', 50, 'ready');

INSERT INTO robot (id, name, charge, state)
VALUES( '11da23f', 'asimo', 100, 'ready');

INSERT INTO robot (id, name, charge, state)
VALUES( '99f1ab', 'aldebaran', 60, 'ready');

INSERT INTO robot (id, name, charge, state)
VALUES( '77f1122', 'robbie', 60, 'ready');

INSERT INTO robot (id, name, charge, state)
VALUES( '23fc111', 'optimus-prime', 80, 'ready');