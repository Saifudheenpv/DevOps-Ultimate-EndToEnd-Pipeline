from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# =========================
# Database Configuration
# =========================
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "notesdb")
DB_HOST = os.getenv("DB_HOST", "localhost")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================
# Database Models
# =========================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


# =========================
# Create Tables (IMPORTANT)
# =========================
with app.app_context():
    db.create_all()

# =========================
# Routes
# =========================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"}), 200


@app.route("/register", methods=["POST"])
def register():
    data = request.json

    if not data or "email" not in data or "password" not in data:
        return jsonify({"message": "Invalid request"}), 400

    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 409

    hashed_password = generate_password_hash(data["password"])
    user = User(email=data["email"], password=hashed_password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    if not data or "email" not in data or "password" not in data:
        return jsonify({"message": "Invalid request"}), 400

    user = User.query.filter_by(email=data["email"]).first()

    if user and check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Login successful", "user_id": user.id}), 200

    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/notes", methods=["POST"])
def create_note():
    data = request.json

    if not data or "content" not in data or "user_id" not in data:
        return jsonify({"message": "Invalid request"}), 400

    note = Note(content=data["content"], user_id=data["user_id"])
    db.session.add(note)
    db.session.commit()

    return jsonify({"message": "Note created"}), 201


@app.route("/notes/<int:user_id>", methods=["GET"])
def get_notes(user_id):
    notes = Note.query.filter_by(user_id=user_id).all()

    return jsonify([
        {"id": note.id, "content": note.content}
        for note in notes
    ]), 200


# =========================
# Application Entry Point
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
