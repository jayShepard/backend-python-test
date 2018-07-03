PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

Alter table main.user RENAME TO main.temp_user;

CREATE TABLE main.user (
  id INTEGER PRIMARY KEY,
  username VARCHAR(20) NOT NULL UNIQUE,
  `_password` VARCHAR(64) NOT NULL
)
 INSERT INTO main.user (id, username, _password)
  SELECT id, username, password FROM main.temp_user;

DROP TABLE main.temp_user;

ALTER TABLE main.todo RENAME TO main.temp_todo;

CREATE TABLE main.todo (
  id INTEGER PRIMARY KEY,
  user_id INTEGER FOREIGN KEY main.user(id),
  description VARCHAR(255) NOT NULL,
  is_completed INTEGER NOT NULL DEFAULT '0'
)
CREATE INDEX idx_user_id ON main.todo(user_id)

DROP TABLE main.temp_todo

COMMIT;

PRAGMA foreign_keys=on;