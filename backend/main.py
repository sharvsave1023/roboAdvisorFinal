from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Heroku provides the database URL as an environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///local.db')  # Fallback for local dev
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    riskQuestionnaire = db.Column(db.String, nullable=True)  # Example questionnaire data
    goalQuestionnaire = db.Column(db.String, nullable=True)

    def __init__(self, username, email, riskQuestionnaire, goalQuestionnaire):
        self.username = username
        self.email = email
        self.riskQuestionnaire = riskQuestionnaire
        self.goalQuestionnaire = goalQuestionnaire

# Initialize the database
with app.app_context():
    db.create_all()

# POST request to add user information
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    riskQuestionnaire = data.get('riskQuestionnaire')
    goalQuestionnaire = data.get('goalQuestionnaire')

    if not username or not email:
        return jsonify({'error': 'Username and email are required!'}), 400

    # Add user to database
    new_user = User(username=username, email=email, riskQuestionnaire=riskQuestionnaire, goalQuestionnaire=goalQuestionnaire)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully!'}), 201

if __name__ == '__main__':
    app.run(debug=True)
