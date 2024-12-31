from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret_key"

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# MongoDB setup
client = MongoClient("mongodb://127.0.0.1:27017")
db = client["sondage"]
users_collection = db["users"]
polls_collection = db["polls"]
votes_collection = db["votes"]

# Flask-Login User model
class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(str(user["_id"]), user["email"])
    return None

@app.route("/")
def home():
    polls = list(polls_collection.find())
    return render_template("index.html", polls=polls)

@app.route("/create_poll", methods=["GET", "POST"])
@login_required
def create_poll():
    if request.method == "POST":
        question = request.form["question"]
        options = request.form["options"].split(",")
        polls_collection.insert_one({
            "question": question,
            "options": options,
            "creator_id": current_user.id
        })
        return redirect(url_for("home"))
    return render_template("create_poll.html")

@app.route("/edit_poll/<poll_id>", methods=["GET", "POST"])
@login_required
def edit_poll(poll_id):
    poll = polls_collection.find_one({"_id": ObjectId(poll_id), "creator_id": current_user.id})
    if not poll:
        return "Unauthorized", 403

    if request.method == "POST":
        question = request.form["question"]
        options = request.form["options"].split(",")
        polls_collection.update_one(
            {"_id": ObjectId(poll_id)},
            {"$set": {"question": question, "options": options}}
        )
        return redirect(url_for("home"))

    return render_template("edit_poll.html", poll=poll)


@app.route("/poll/<poll_id>")
def poll_details(poll_id):
    poll = polls_collection.find_one({"_id": ObjectId(poll_id)})
    votes = list(votes_collection.find({"poll_id": poll_id}))
    results = {option: 0 for option in poll["options"]}
    for vote in votes:
        results[vote["option"]] += 1
    return render_template("poll_details.html", poll=poll, results=results)

@app.route("/vote/<poll_id>", methods=["POST"])
@login_required
def vote(poll_id):
    option = request.form["option"]
    if votes_collection.find_one({"poll_id": poll_id, "user_id": current_user.id}):
        return "Already voted", 400
    votes_collection.insert_one({
        "poll_id": poll_id,
        "user_id": current_user.id,
        "option": option
    })
    return redirect(url_for("poll_details", poll_id=poll_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = users_collection.find_one({"email": email})

        if user and check_password_hash(user["password"], password):
            user_obj = User(str(user["_id"]), user["email"])
            login_user(user_obj)
            return redirect(url_for("home"))
        return "Invalid credentials", 401

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if users_collection.find_one({"email": email}):
            return "Email already registered", 400

        hashed_password = generate_password_hash(password)
        users_collection.insert_one({"email": email, "password": hashed_password})
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
