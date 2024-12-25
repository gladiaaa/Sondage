from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from bson.objectid import ObjectId
from .models import User

mongo = PyMongo()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "votre_clé_secrète"
    app.config["MONGO_URI"] = "mongodb://localhost:27017/sondage"

    mongo.init_app(app)
    login_manager.init_app(app)

    # Charger un utilisateur depuis l'ID
    @login_manager.user_loader
    def load_user(user_id):
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return User(user) if user else None

    # Importer et enregistrer les routes
    from .routes import routes
    app.register_blueprint(routes)

    return app
