# Sondage
Site de Sondage flask et mongoDB

## Instalation coté Dev

/!\ Il faut en amont installer mongoDB https://www.mongodb.com/try/download/community ou MongoDB Compass (interface graphique MongoDB + simple)

Pour installer les dépendances pour voir le site effectuez la commande  "pip install -r requirements.txt"

Pour installer la bdd effectuer la commande "python setup_db.py"

Pour lancer le projet effectuez la commande "python run.py"

# Tâches Restantes pour le Projet Sondage

## 1. Finaliser le Système de Gestion des Utilisateurs
- [ ] Implémenter les règles d'accès :
  - [ ] Les visiteurs peuvent voir les scrutins, mais **ne peuvent voter que s'ils sont connectés**.
  - [ ] Les utilisateurs connectés peuvent voter une seule fois par scrutin.
  - [ ] Les créateurs de scrutins peuvent **modifier et supprimer leurs propres scrutins uniquement**.
  - [ ] Les administrateurs peuvent **supprimer n'importe quel scrutin**.
- [ ] Validation des inscriptions :
  - [ ] Empêcher la création de plusieurs comptes avec le même email.

---

## 2. Gérer les Votes
- [ ] Ajouter la logique de vote :
  - [ ] Permettre de voter sur un scrutin et enregistrer les votes dans une collection `votes` ou dans un champ spécifique des scrutins.
  - [ ] Empêcher un utilisateur de voter plusieurs fois sur le même scrutin.
- [ ] Affichage des résultats :
  - [ ] Mettre à jour la page des détails du scrutin pour afficher le **nombre de votes** par option en temps réel (si possible).

---

## 3. Ajouter une Confirmation pour les Actions Importantes
- [ ] Ajouter un message de confirmation ou une boîte de dialogue :
  - [ ] Lors de la création d'un scrutin.
  - [ ] Lors de la suppression d'un scrutin.

---

## 4. Améliorer l'Interface Utilisateur
- [ ] Utiliser **Bootstrap** ou du CSS personnalisé pour rendre l'interface plus conviviale.
- [ ] Indiquer clairement le statut de l'utilisateur (visiteur, utilisateur connecté, administrateur).
- [ ] Ajouter des boutons clairs pour :
  - [ ] Voter sur un scrutin.
  - [ ] Afficher les résultats des scrutins.

---

## 5. Tester Toutes les Fonctionnalités
- [ ] Vérifier les routes et les règles d'accès :
  - [ ] Assurer que les visiteurs ne peuvent pas voter.
  - [ ] S'assurer que les créateurs ne peuvent modifier que leurs propres scrutins.
  - [ ] Vérifier que les administrateurs peuvent gérer tous les scrutins.
- [ ] Tester l'enregistrement des actions dans la base de données :
  - [ ] Création d'utilisateurs.
  - [ ] Création et suppression de scrutins.
  - [ ] Enregistrement des votes.

---

## 6. Ajouter un Dashboard pour l'Administrateur (Optionnel)
- [ ] Permettre à l'administrateur de :
  - [ ] Voir tous les utilisateurs.
  - [ ] Gérer les scrutins (supprimer ou modifier).
  - [ ] Voir les statistiques globales (nombre de votes, utilisateurs, scrutins).

---

## 7. Mise en Production
- [ ] **Héberger l'application** :
  - [ ] Configurer MongoDB sur un serveur cloud (par exemple : MongoDB Atlas).
  - [ ] Héberger l'application Flask sur un serveur web (Heroku, AWS, ou autre).
- [ ] Ajouter une **protection SSL** (HTTPS).
- [ ] Tester l'application en production pour valider toutes les fonctionnalités.

---

## Liste des Points à Vérifier
- [ ] Gestion des rôles : visiteur, utilisateur, administrateur.
- [ ] Système de vote et gestion des scrutins.
- [ ] Sécurité :
  - [ ] Empêcher les doublons d'inscription.
  - [ ] Protéger les données sensibles.
- [ ] Interface claire et ergonomique.
