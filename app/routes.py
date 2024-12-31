from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, mongo
from app.models import User

@app.route("/")
def index():
    scrutins = mongo.db.scrutins.find().limit(10)
    return render_template("index.html", scrutins=scrutins)

@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        infos_personnelles = request.form["infos_personnelles"]

        if mongo.db.utilisateurs.find_one({"_id": pseudo}):
            flash("Ce pseudonyme est déjà pris !", "danger")
            return redirect(url_for("inscription"))

        mongo.db.utilisateurs.insert_one({
            "_id": pseudo,
            "infos_personnelles": infos_personnelles,
            "ferme": False
        })
        flash("Inscription réussie !", "success")
        return redirect(url_for("connexion"))
    
    return render_template("inscription.html")

@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        utilisateur = mongo.db.utilisateurs.find_one({"_id": pseudo})

        if utilisateur and not utilisateur["ferme"]:
            user = User(pseudo)
            login_user(user)
            flash("Connexion réussie !", "success")
            return redirect(url_for("index"))
        flash("Pseudo invalide ou compte fermé.", "danger")
    
    return render_template("connexion.html")

@app.route("/deconnexion")
@login_required
def deconnexion():
    logout_user()
    flash("Vous êtes déconnecté.", "info")
    return redirect(url_for("index"))

@app.route("/scrutin/creer", methods=["GET", "POST"])
@login_required
def creer_scrutin():
    if request.method == "POST":
        question = request.form["question"]
        options = request.form.getlist("options")
        date_debut = request.form["date_debut"]
        date_fin = request.form["date_fin"]

        if len(options) < 2:
            flash("Un scrutin doit avoir au moins deux options.", "danger")
            return redirect(url_for("creer_scrutin"))

        mongo.db.scrutins.insert_one({
            "organisateur": current_user.id,
            "question": question,
            "options": options,
            "date_debut": date_debut,
            "date_fin": date_fin,
            "votes": []
        })
        flash("Scrutin créé avec succès !", "success")
        return redirect(url_for("index"))

    return render_template("scrutin.html")
