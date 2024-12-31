from flask_login import UserMixin
from app import mongo

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
