from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, User, Scrutin
from bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt()
routes = Blueprint('routes', __name__)

# Page d'accueil
@routes.route('/')
def home():
    scrutins = Scrutin.query.all()
    return render_template('home.html', scrutins=scrutins)

# Page d'inscription
@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Vérification des mots de passe
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'error')
            return redirect(url_for('routes.register'))

        # Vérification si l'utilisateur existe déjà
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash('Nom d\'utilisateur ou email déjà utilisé.', 'error')
            return redirect(url_for('routes.register'))

        # Enregistrement de l'utilisateur
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Inscription réussie. Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html')

# Page de connexion
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash('Connexion réussie.', 'success')
            return redirect(url_for('routes.home'))
        else:
            flash('Identifiants incorrects.', 'error')
            return redirect(url_for('routes.login'))

    return render_template('login.html')

# Déconnexion
@routes.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('is_admin', None)
    flash('Déconnexion réussie.', 'success')
    return redirect(url_for('routes.home'))

# Page de gestion des scrutins
@routes.route('/scrutins', methods=['GET', 'POST'])
def scrutins():
    if 'user_id' not in session:
        flash('Vous devez être connecté pour accéder à cette page.', 'error')
        return redirect(url_for('routes.login'))

    if request.method == 'POST':
        question = request.form['question']
        options = request.form.getlist('options[]')
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Validation des données
        if not question or not options or not start_date or not end_date:
            flash('Tous les champs doivent être remplis.', 'error')
            return redirect(url_for('routes.scrutins'))

        # Vérification des dates
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            if start_date_obj >= end_date_obj:
                flash('La date de début doit être antérieure à la date de fin.', 'error')
                return redirect(url_for('routes.scrutins'))
        except ValueError:
            flash('Format de date invalide.', 'error')
            return redirect(url_for('routes.scrutins'))

        # Création d'un nouveau scrutin
        new_scrutin = Scrutin(
            question=question,
            options=options,
            start_date=start_date,
            end_date=end_date,
            creator_id=session['user_id']
        )
        db.session.add(new_scrutin)
        db.session.commit()
        flash('Scrutin créé avec succès.', 'success')
        return redirect(url_for('routes.scrutins'))

    user_scrutins = Scrutin.query.filter_by(creator_id=session['user_id']).all()
    return render_template('scrutins.html', scrutins=user_scrutins)

# Détails d'un scrutin
@routes.route('/scrutins/<int:scrutin_id>')
def scrutin_details(scrutin_id):
    scrutin = Scrutin.query.get_or_404(scrutin_id)
    return render_template('scrutins_details.html', scrutin=scrutin)

# Suppression d'un scrutin
@routes.route('/scrutins/delete/<int:scrutin_id>', methods=['POST'])
def delete_scrutin(scrutin_id):
    scrutin = Scrutin.query.get_or_404(scrutin_id)

    # Vérification des droits de suppression
    if scrutin.creator_id != session.get('user_id') and not session.get('is_admin'):
        flash('Vous n\'avez pas la permission de supprimer ce scrutin.', 'error')
        return redirect(url_for('routes.scrutins'))

    db.session.delete(scrutin)
    db.session.commit()
    flash('Scrutin supprimé avec succès.', 'success')
    return redirect(url_for('routes.scrutins'))
