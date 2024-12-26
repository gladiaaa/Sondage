from bson.objectid import ObjectId
from flask_login import UserMixin
from app import mongo

# Modèle pour les utilisateurs
class User(UserMixin):
    def __init__(self, data):
        self.id = str(data.get("_id"))
        self.username = data.get("username")
        self.email = data.get("email")
        self.password = data.get("password")
        self.is_admin = data.get("is_admin", False)

    @staticmethod
    def get(user_id):
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return User(user) if user else None

    @staticmethod
    def get_by_email(email):
        user = mongo.db.users.find_one({"email": email})
        return User(user) if user else None

    @staticmethod
    def create(username, email, password, is_admin=False):
        mongo.db.users.insert_one({
            "username": username,
            "email": email,
            "password": password,
            "is_admin": is_admin
        })

# Modèle pour les scrutins
class Scrutin:
    @staticmethod
    def create(question, options, start_date, end_date, creator_id):
        mongo.db.scrutins.insert_one({
            "question": question,
            "options": options,
            "start_date": start_date,
            "end_date": end_date,
            "creator_id": creator_id
        })

    @staticmethod
    def get_all():
        return list(mongo.db.scrutins.find())

    @staticmethod
    def get(scrutin_id):
        return mongo.db.scrutins.find_one({"_id": ObjectId(scrutin_id)})

    @staticmethod
    def delete(scrutin_id):
        mongo.db.scrutins.delete_one({"_id": ObjectId(scrutin_id)})
