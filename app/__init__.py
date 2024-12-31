from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = "votre_cle_secrete"

# Configuration de MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/Sondage1"
mongo = PyMongo(app)

# Configuration Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "connexion"

from app import routes
