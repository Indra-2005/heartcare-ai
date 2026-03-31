from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model, UserMixin):
    """
    Represents a registered user in the application.
    Inherits from db.Model (SQLAlchemy) and UserMixin (Flask-Login) for secure session management.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile_number = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    predictions = db.relationship('PredictionHistory', backref='user', lazy=True,
                                   cascade='all, delete-orphan')

    @classmethod
    def create_user(cls, fullname, username, email, mobile_number, password):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = cls(
            fullname=fullname,
            username=username,
            email=email,
            mobile_number=mobile_number,
            password=hashed_password
        )
        db.session.add(user)
        return user

    def get_id(self):
        return str(self.id)


class PredictionHistory(db.Model):
    """
    Stores historical heart disease predictions.
    Tracks all 13 clinical input parameters along with the AI-generated risk probability and category.
    Linked to the User model via a foreign key relationship.
    """
    __tablename__ = 'prediction_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    age = db.Column(db.Integer)
    sex = db.Column(db.Integer)
    cp = db.Column(db.Integer)
    trestbps = db.Column(db.Integer)
    chol = db.Column(db.Integer)
    fbs = db.Column(db.Integer)
    restecg = db.Column(db.Integer)
    thalach = db.Column(db.Integer)
    exang = db.Column(db.Integer)
    oldpeak = db.Column(db.Float)
    slope = db.Column(db.Integer)
    ca = db.Column(db.Integer)
    thal = db.Column(db.Integer)
    prediction_result = db.Column(db.String(200))
    probability = db.Column(db.Float)
    risk_level = db.Column(db.String(20))  # 'high', 'moderate', 'low'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)