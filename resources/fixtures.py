from typing import List
from database import db_session
from models import User, Todo


def _add_users(users: List[dict]):
    for user_dict in users:
        try:
            user = User(username=user_dict['username'],
                        password=user_dict['password'])
            db_session.add(user)
            db_session.commit()
        except:
            continue

def _add_todo(todos: List[dict]):
    for todo_dict in todos:
        try:
            todo = Todo(user_id=todo_dict['user_id'],
                        description=todo_dict['description'])
            db_session.add(todo)
            db_session.commit()
        except:
            continue

def populate_database():
    users = [
        {'username': 'user1', 'password': 'user1'},
        {'username': 'user2', 'password': 'user2'},
        {'username': 'user3', 'password': 'user3'}
    ]

    todos = [
        {'user_id': 1, 'description': 'Vivamus tempus'},
        {'user_id': 1, 'description': 'lorem ac odio'},
        {'user_id': 1, 'description': 'Ut congue odio'},
        {'user_id': 1, 'description': 'Sodales finibus'},
        {'user_id': 1, 'description': 'Accumsan nunc vitae'},
        {'user_id': 2, 'description': 'Lorem ipsum'},
        {'user_id': 2, 'description': 'In lacinia est'},
        {'user_id': 2, 'description': 'Odio varius gravida'}
    ]

    _add_users(users)
    _add_todo(todos)