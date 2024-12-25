class Config:
    """
    Configuration de base pour l'application Flask.
    """
    DEBUG = True  # Mode debug pour le développement
    TESTING = False
    SECRET_KEY = "votre_clé_secrète"
    MONGO_URI = "mongodb://localhost:27017/testdb"  # Utilisation de la base de données testdb
