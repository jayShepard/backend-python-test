from alayatodo.models import User
from database import db_session

users = User.query.all()

for user in users:
    password = user.password
    user.password(password)
    db_session.add(user)
    db_session.commit()