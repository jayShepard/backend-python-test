from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import backref, relationship
from database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }


class Todo(Base):
    __tablename__ = 'todo'

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey('user.id'), nullable=True)
    description: str = Column(String(255))

    user = relationship('User', backref=backref('todos', lazy=True))

    def __init__(self, user_id: int, description: str):
        self.user_id = user_id
        self.description = description

    def __repr__(self):
        return f'<Todo {self.description}>'
