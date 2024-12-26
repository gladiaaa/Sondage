from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager, AnonymousUserMixin

mongo = PyMongo()
login_manager = LoginManager()

# Classe pour gérer les visiteurs
class Visitor(AnonymousUserMixin):
    def __init__(self):
        self.id = None
        self.username = "Visiteur"
        self.is_admin = False

    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

# Initialisation de l'application Flask
def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "votre_clé_secrète"
    app.config["MONGO_URI"] = "mongodb://localhost:27017/sondage"

    # Initialisation des extensions
    mongo.init_app(app)
    login_manager.init_app(app)

    # Définir le gestionnaire pour les utilisateurs anonymes
    login_manager.anonymous_user = Visitor

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.get(user_id)

    # Enregistrement des blueprints
    from app.routes import routes
    app.register_blueprint(routes)

    return app
