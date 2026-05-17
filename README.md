# HeartCare AI 🫀

> **AI-powered cardiovascular risk prediction using machine learning**

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-black?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=flat-square&logo=postgresql)](https://postgresql.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?style=flat-square)](https://scikit-learn.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

HeartCare AI is a full-stack Flask web application that uses a **Random Forest classifier** to predict heart disease risk from 13 clinical parameters. It features a modern dark UI, user authentication, prediction history tracking, and personalized health recommendations.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **AI Prediction** | Random Forest model on Cleveland Heart Disease dataset |
| 🔐 **Authentication** | Secure registration/login with bcrypt hashing |
| 📊 **Prediction History** | Track and review past assessments per user |
| 📈 **Visual Analytics** | SVG risk gauge + metrics grid on result page |
| 📄 **Risk Reports** | Tiered recommendations + printable PDF report |
| 🔑 **Password Change** | Secure in-app password update with strength meter |
| 🗑️ **Delete Records** | Remove individual prediction entries |
| 🌗 **Dark UI** | Glassmorphic dark design system |
| 📱 **Responsive** | Works on desktop, tablet, and mobile |
| ⚠️ **Error Pages** | Custom 404 and 500 error pages |

---

## 🗂️ Project Structure

```
PostGre_Flask/
├── app.py                    # Main Flask application + all routes
├── models.py                 # SQLAlchemy models (User, PredictionHistory)
├── forms.py                  # WTForms (Registration, Login, ChangePassword)
├── config.py                 # App configuration from environment
├── models/                   # Directory containing the ML model
│   └── heart_disease_model_v2.pkl # Trained Random Forest model (V2)
├── Heart.csv                 # Original dataset (reference)
├── requirements.txt          # Python dependencies
├── .env                      # Environment secrets (not committed)
├── .env.example              # Template for environment setup
├── migrations/               # Flask-Migrate database migrations
├── notebooks/
│   └── heart_disease_prediction.ipynb # Fully documented end-to-end ML pipeline
├── static/
│   ├── css/style.css         # Shared dark design system
│   ├── js/main.js            # Shared JS (navbar, toasts, counters)
│   └── img/                  # Static images
└── templates/
    ├── base.html             # Base template (navbar, toasts, footer)
    ├── index.html            # Landing page (hero, features, CTA)
    ├── login.html            # Login page
    ├── register.html         # Registration page
    ├── main.html             # Multi-step prediction form
    ├── result.html           # Prediction results with gauge + recs
    ├── profile.html          # User profile + prediction history
    ├── about.html            # About page (no team section)
    ├── change_password.html  # Password update form
    ├── termscondition.html   # Terms & Conditions
    ├── 404.html              # Custom 404 error page
    └── 500.html              # Custom 500 error page
```

---

## 🔧 Setup & Installation

### Prerequisites
- Python 3.9+
- PostgreSQL database
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/heartcare-ai.git
cd heartcare-ai/PostGre_Flask
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your actual values
```

### 5. Set Up Database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the Application
```bash
python app.py
# App runs at http://localhost:8080
```

---

## ⚙️ Environment Variables

See `.env.example` for all required variables:

```env
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/heartcare_db
```

---

## 🧠 Machine Learning Model (V2)

- **Algorithm**: Random Forest Classifier (with SMOTE for class imbalance)
- **Dataset**: [Cleveland Heart Disease Dataset (UCI ML Repository)](https://archive.ics.uci.edu/dataset/45/heart+disease)
- **Features**: 13 specific clinical parameters (including Age, Sex, Chest Pain Type, Resting BP, Cholesterol, Fasting Blood Sugar, Resting ECG, Max Heart Rate, Exercise Induced Angina, ST Depression, ST Slope, Number of Major Vessels, and Thalassemia).
- **Output**: Binary classification (Healthy/Diseased) + risk probability score
- **Performance Metrics**: 
  - **Accuracy**: ~82.9% on stratified test split
  - **ROC-AUC Score**: ~91.8% (indicating excellent class separation)
- **Notebook**: See `notebooks/heart_disease_prediction.ipynb` for the fully documented, step-by-step training pipeline (including data preprocessing, SMOTE, hyperparameter tuning, cross-validation, and evaluation).


---

## 📡 API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/` | ❌ | Landing page |
| GET | `/register` | ❌ | Registration page |
| POST | `/register` | ❌ | Create account |
| GET | `/login` | ❌ | Login page |
| POST | `/login` | ❌ | Authenticate user |
| GET | `/logout` | ✅ | Logout |
| GET | `/main` | ✅ | Prediction form |
| POST | `/predict` | ✅ | Run prediction |
| GET | `/profile` | ✅ | User dashboard |
| GET/POST | `/change-password` | ✅ | Update password |
| POST | `/delete-history/<id>` | ✅ | Delete history entry |
| GET | `/api/stats` | ✅ | JSON stats endpoint |
| GET | `/about` | ❌ | About page |
| GET | `/termscondition` | ❌ | Terms page |

---

## ⚠️ Medical Disclaimer

HeartCare AI is **for educational purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified cardiologist for clinical decisions.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
