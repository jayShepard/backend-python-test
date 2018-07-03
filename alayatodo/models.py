import hashlib
from typing import Dict

from database import Base

from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import backref, relationship
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property


class User(Base):
    __tablename__ = 'user'

    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(20), nullable=False, unique=True)
    _password: str = Column(String(64), nullable=False)

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext_password):
        self._password = hashlib.sha3_256(
            plaintext_password.encode('utf-8')).hexdigest()

    @hybrid_method
    def verify_password(self, plaintext_password):
        return (hashlib.sha3_256(
            plaintext_password.encode('utf-8')).hexdigest() == self._password)


class Todo(Base):
    __tablename__ = 'todo'

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey('user.id'), nullable=True)
    description: str = Column(String(255), nullable=False)
    is_completed: bool = Column(Boolean, nullable=False, default=False)

    user = relationship('User', backref=backref('todos', lazy=True))

    def __init__(self, user_id: int, description: str,
                 is_completed: bool=False):
        self.user_id = user_id
        self.description = description
        self.is_completed = is_completed

    def __repr__(self):
        return f'<Todo {self.description}>'

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'description': self.description,
            'is_completed': self.is_completed
        }
