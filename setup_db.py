from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")


db_name = "sondage"
db = client[db_name]


collections = {
    "users": [
        {"username": "admin", "email": "admin@example.com", "password": "hashed_password", "is_admin": True},
        {"username": "user1", "email": "user1@example.com", "password": "hashed_password", "is_admin": False},
    ],
    "scrutins": [
        {
            "question": "Quelle est votre couleur préférée ?",
            "options": ["Rouge", "Bleu", "Vert"],
            "start_date": "2024-12-25",
            "end_date": "2024-12-30",
            "creator_id": "user1_id",
        }
    ]
}


for collection_name, data in collections.items():
    collection = db[collection_name]
    if collection_name == "users":
        for user in data:
            if not collection.find_one({"email": user["email"]}):
                collection.insert_one(user)
    else:

        collection.insert_many(data)

print(f"Base de données '{db_name}' et collections créées avec succès !")

# faire la commande "python setup_db.py" pour créer la bdd
