from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])  # Convertir ObjectId en chaîne
        self.pseudo = user_data["pseudo"]
        self.email = user_data["email"]
        self.role = user_data["role"]
        self.status = user_data["status"]

    # Ajouter des propriétés personnalisées si nécessaire
    def is_admin(self):
        return self.role == "admin"

    def is_creator(self):
        return self.role == "creator"

def get_scrutin_model(question, options, start_date, end_date):
    return {
        "question": question,
        "options": options,  # Liste des options possibles
        "start_date": start_date,
        "end_date": end_date,
        "votes": [],  # Liste des votes effectués
        "status": "pending"  # pending, open, closed
    }

def get_user_model(pseudo, personal_info):
    return {
        "pseudo": pseudo,
        "personal_info": personal_info,
        "status": "active"  # active, closed
    }
