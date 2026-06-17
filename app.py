"""
HeartCare AI Flask Application
Main application file containing all routes, configuration loading, database initialization, 
and machine learning model integration for predicting cardiovascular risk.
"""
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from forms import RegistrationForm, LoginForm, ChangePasswordForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, bcrypt, User, PredictionHistory
from config import Config
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import numpy as np
import pandas as pd
import pickle
import os
import warnings
from datetime import datetime
from functools import wraps

def create_app():
    """
    Application factory function.
    Initializes the Flask application, loads configurations, and sets up extensions 
    including SQLAlchemy, Bcrypt, Flask-Migrate, and Flask-Login.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    CSRFProtect(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()

    return app


app = create_app()

# ─── Load ML Model ────────────────────────────────────────────────────────────
filename = os.path.join(os.path.dirname(__file__), 'models', 'heart_disease_model (1).pkl')
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    _model_data = pickle.load(open(filename, 'rb'))
    # The .pkl stores a dict {'model': classifier, 'features': [...], ...}
    model = _model_data['model'] if isinstance(_model_data, dict) else _model_data
    model_features = _model_data.get('features') if isinstance(_model_data, dict) else None


# ─── Helper ───────────────────────────────────────────────────────────────────
def get_risk_level(probability_float):
    """
    Determines the categorical risk level based on the percentage probability.
    
    Args:
        probability_float (float): The probability percentage (0-100) of heart disease.
        
    Returns:
        str: 'high', 'moderate', or 'low' risk category.
    """
    if probability_float >= 75:
        return 'high'
    elif probability_float >= 50:
        return 'moderate'
    else:
        return 'low'


# ─── Public Routes ────────────────────────────────────────────────────────────
@app.route("/")
def index():
    """Renders the landing page for the application."""
    return render_template('public/index.html')


@app.route("/about")
def about():
    """Renders the About page detailing project information."""
    return render_template('public/about.html')


@app.route("/termscondition")
def TermsCondition():
    """Renders the Terms and Conditions / Medical Disclaimer page."""
    return render_template('public/termscondition.html')


# ─── Auth Routes ──────────────────────────────────────────────────────────────
@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Handles new user registration.
    Validates form data, checks for existing users, and securely hashes the password.
    Redirects to login upon successful registration.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken. Please choose another.', 'danger')
            return render_template('auth/register.html', form=form)
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered. Please log in.', 'danger')
            return render_template('auth/register.html', form=form)
        User.create_user(
            fullname=form.fullname.data,
            username=form.username.data,
            email=form.email.data,
            mobile_number=form.mobile_number.data,
            password=form.password.data
        )
        db.session.commit()
        flash('Account created successfully! Welcome aboard.', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Handles user authentication.
    Verifies the submitted password against the Bcrypt hashed password stored in the database.
    If valid, logs the user in via Flask-Login and redirects to their dashboard.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.fullname.split()[0]}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('auth/login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    """Logs out the current authenticated user and clears the session."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


# ─── Protected Routes ─────────────────────────────────────────────────────────
@app.route("/main")
@login_required
def main():
    """Renders the main prediction dashboard form where users enter clinical parameters."""
    return render_template('dashboard/main.html', title='Predict')


@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    """
    Core prediction endpoint.
    Retrieves the 13 clinical features from the HTML form submission, formats them
    into a structured NumPy array, and feeds them into the trained Random Forest model.
    Saves the output result to the user's prediction history in the database.
    """
    if request.method == 'POST':
        try:
            age       = int(request.form['age'])
            sex       = int(request.form.get('sex'))
            cp        = int(request.form.get('cp'))
            trestbps  = int(request.form['trestbps'])
            chol      = int(request.form['chol'])
            fbs       = int(request.form.get('fbs'))
            restecg   = int(request.form['restecg'])
            thalach   = int(request.form['thalach'])
            exang     = int(request.form.get('exang'))
            oldpeak   = float(request.form['oldpeak'])
            slope     = int(request.form.get('slope'))
            ca        = int(request.form['ca'])
            thal      = int(request.form.get('thal'))
        except (ValueError, TypeError):
            flash('Invalid input. Please fill in all fields correctly.', 'danger')
            return redirect(url_for('main'))

        data_dict = {
            'age': [age], 'sex': [sex], 'cp': [cp], 'trestbps': [trestbps],
            'chol': [chol], 'fbs': [fbs], 'restecg': [restecg], 'thalach': [thalach],
            'exang': [exang], 'oldpeak': [oldpeak], 'slope': [slope], 'ca': [ca], 'thal': [thal]
        }
        if model_features:
            data = pd.DataFrame(data_dict, columns=model_features)
        else:
            data = pd.DataFrame(data_dict)

        my_prediction = model.predict(data)
        prediction_proba = model.predict_proba(data)
        heart_disease_probability = float(prediction_proba[0][1] * 100)
        formatted_probability = f"{int(heart_disease_probability)}%"
        risk_level = get_risk_level(heart_disease_probability)

        # Determine readable result
        if my_prediction[0] == 1:
            prediction_label = "Heart Disease Detected"
        else:
            prediction_label = "No Heart Disease Detected"

        # Save to history
        history_entry = PredictionHistory(
            user_id=current_user.id,
            age=age, sex=sex, cp=cp, trestbps=trestbps, chol=chol,
            fbs=fbs, restecg=restecg, thalach=thalach, exang=exang,
            oldpeak=oldpeak, slope=slope, ca=ca, thal=thal,
            prediction_result=prediction_label,
            probability=heart_disease_probability,
            risk_level=risk_level
        )
        db.session.add(history_entry)
        db.session.commit()

        return render_template(
            'dashboard/result.html',
            prediction=prediction_label,
            probability=formatted_probability,
            probability_value=int(heart_disease_probability),
            risk_level=risk_level,
            entry=history_entry
        )
    return redirect(url_for('main'))


@app.route("/profile")
@login_required
def profile():
    """
    Renders the user profile page.
    Displays user information, aggregate statistics of their predictions, 
    and a tabular history of past risk assessments.
    """
    history = PredictionHistory.query.filter_by(user_id=current_user.id)\
                .order_by(PredictionHistory.created_at.desc()).all()
    total = len(history)
    high_risk = sum(1 for h in history if h.risk_level == 'high')
    moderate_risk = sum(1 for h in history if h.risk_level == 'moderate')
    low_risk = sum(1 for h in history if h.risk_level == 'low')
    return render_template('dashboard/profile.html', history=history, total=total,
                           high_risk=high_risk, moderate_risk=moderate_risk, low_risk=low_risk)


@app.route("/change-password", methods=['GET', 'POST'])
@login_required
def change_password():
    """
    Handles secure password changes.
    Verifies the user's current password before hashing and saving the new one.
    """
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.current_password.data):
            current_user.password = bcrypt.generate_password_hash(
                form.new_password.data).decode('utf-8')
            db.session.commit()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Current password is incorrect.', 'danger')
    return render_template('auth/change_password.html', form=form)


@app.route("/delete-history/<int:entry_id>", methods=['POST'])
@login_required
def delete_history(entry_id):
    """
    Deletes a specific prediction history entry.
    Ensures that the entry exists and belongs to the currently authenticated user.
    """
    entry = db.get_or_404(PredictionHistory, entry_id)
    if entry.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('profile'))
    db.session.delete(entry)
    db.session.commit()
    flash('Prediction record deleted.', 'info')
    return redirect(url_for('profile'))


@app.route("/api/stats")
@login_required
def api_stats():
    """JSON endpoint for dashboard stats."""
    history = PredictionHistory.query.filter_by(user_id=current_user.id).all()
    data = {
        'total': len(history),
        'high': sum(1 for h in history if h.risk_level == 'high'),
        'moderate': sum(1 for h in history if h.risk_level == 'moderate'),
        'low': sum(1 for h in history if h.risk_level == 'low'),
        'recent': [
            {
                'date': h.created_at.strftime('%Y-%m-%d'),
                'result': h.prediction_result,
                'probability': h.probability,
                'risk': h.risk_level
            } for h in sorted(history, key=lambda x: x.created_at, reverse=True)[:5]
        ]
    }
    return jsonify(data)


# ─── Error Handlers ───────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    """Handles 404 Page Not Found errors."""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handles 500 Internal Server Error exceptions."""
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=False)