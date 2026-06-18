# HeartCare AI 🫀

> **AI-powered cardiovascular risk prediction using machine learning**

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-black?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=flat-square&logo=postgresql)](https://postgresql.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?style=flat-square)](https://scikit-learn.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

HeartCare AI is a full-stack Flask web application that uses a **Random Forest classifier** to predict heart disease risk from 13 clinical parameters. It features a modern light UI, user authentication, prediction history tracking, and personalized health recommendations.

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
| 🌗 **Light UI** | Premium medical-teal glassmorphic light design system |
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
├── config/                   # Directory containing configuration files
│   └── ml_config.yaml        # Machine learning pipeline training configurations
├── ml/                       # Machine learning pipeline directory
│   ├── pipeline.py           # Preprocessing and validation utility functions
│   ├── train.py              # CLI orchestrator for classifier training
│   └── evaluate.py           # Classifier evaluation and metrics generator
├── models/                   # Directory containing serialized model pickles
│   └── heart_disease_model.pkl # Trained Random Forest model dictionary (V2)
├── data/                     # Subdirectory with training datasets
│   ├── Heart_disease_cleveland_new.csv  # 0-indexed processed Cleveland dataset      
├── tests/                    # Project test suite directory
│   └── test_ml_pipeline.py   # Unit & integration tests for the ML pipeline
├── requirements.txt          # Python dependencies
├── .env                      # Environment secrets (not committed)
├── .env.example              # Template for environment setup
├── migrations/               # Flask-Migrate database migrations
├── notebooks/
│   ├── heart_disease_prediction.ipynb # Fully documented end-to-end ML pipeline
│   └── plots/                # Subdirectory containing output evaluation plots
├── static/
│   ├── css/style.css         # Shared light design system
│   ├── js/main.js            # Shared JS (navbar, toasts, counters)
│   └── img/                  # Static images
└── templates/
    ├── base.html             # Base template (navbar, toasts, footer)
    ├── auth/                 # Authentication views
    │   ├── login.html        # Login page
    │   ├── register.html     # Registration page
    │   └── change_password.html # Password update form
    ├── dashboard/            # Dashboard views
    │   ├── main.html         # Multi-step prediction form
    │   ├── result.html       # Prediction results with gauge + recs
    │   └── profile.html      # User profile + prediction history
    ├── public/               # Public informative views
    │   ├── index.html        # Landing page (hero, features, CTA)
    │   ├── about.html        # About page
    │   └── termscondition.html # Terms & Conditions
    └── errors/               # Custom error pages
        ├── 404.html          # Custom 404 error page
        └── 500.html          # Custom 500 error page
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

## 🧠 Machine Learning Model

- **Algorithm**: Random Forest Classifier (with `class_weight='balanced'` for class imbalance handling)
- **Dataset**: [Cleveland Heart Disease Dataset (UCI ML Repository)](https://archive.ics.uci.edu/dataset/45/heart+disease)
- **Features**: 13 specific clinical parameters (including Age, Sex, Chest Pain Type, Resting BP, Cholesterol, Fasting Blood Sugar, Resting ECG, Max Heart Rate, Exercise Induced Angina, ST Depression, ST Slope, Number of Major Vessels, and Thalassemia).
- **Output**: Binary classification (Healthy/Diseased) + risk probability score
- **Model Storage**: Saved as `models/heart_disease_model.pkl` (serialized dictionary containing both the classifier and training features) and loaded directly by the Flask server.
- **Notebook**: See `notebooks/heart_disease_prediction.ipynb` for the fully documented, step-by-step training pipeline (including data preprocessing, SMOTE, hyperparameter tuning, cross-validation, and evaluation).

---

## ⚙️ Machine Learning Pipeline

The project features a modular, configuration-driven Machine Learning pipeline that automates data validation, model training, performance evaluation, and quality assurance testing.

### 1. Configuration (`config/ml_config.yaml`)
Pipeline parameters are controlled via a YAML configuration file:
* **Dataset Config**: Defines target labels and CSV paths.
* **Hyperparameters**: Explicitly tunes classifier options (e.g. tree depth limits) to prevent overfitting.
* **Artifact Path**: Directs where serialized model pickles are saved.

### 2. Execution Scripts (`ml/`)
* **Training (`ml/train.py`)**: Runs data parsing, feature extraction, model fitment, and exports a production-ready dictionary containing `{'model': classifier, 'features': list_of_features}` to ensure web app input feature alignment.
* **Evaluation (`ml/evaluate.py`)**: Loads the model to run predictions on the test set, output a classification metrics report, and update visual evaluation charts like the confusion matrix.

#### CLI Commands:
```bash
# Execute training pipeline
python -m ml.train

# Run model evaluation metrics and update plots
python -m ml.evaluate
```

### 3. Verification & Guardrail Tests (`tests/`)
We use `pytest` to enforce strict ML engineering guardrails:
* **Paths Verification**: Ensures config file paths align with the physical environment.
* **Data Dimensions Check**: Guards against feature drift by validating that exactly 13 input columns are prepared.
* **Inference Guardrails**: Validates classifier behavior with mock patients, testing both raw Numpy matrices and structured Pandas DataFrames.

#### Run Tests:
```bash
python -m pytest
```

### 📊 Model Performance Metrics

The model achieves exceptional accuracy and generalization, showing no signs of overfitting:

| Metric | Score | Note |
|---|---|---|
| **Train Accuracy** | **90.5%** | Robust fitting accuracy on balanced training set |
| **Test Accuracy** | **88.5%** | High model generalization on testing split |
| **5-Fold CV ROC-AUC** | **88.7%** | Consistent performance across stratified splits |
| **Test Split ROC-AUC** | **96.2%** | Outstanding class separation ability |

### 📈 Test Classification Report

```
              precision    recall  f1-score   support

     Healthy       0.93      0.85      0.89        33
    Diseased       0.84      0.93      0.88        28

    accuracy                           0.89        61
   macro avg       0.89      0.89      0.89        61
weighted avg       0.89      0.89      0.89        61
```


### 🖼️ Visual Model Evaluation & Insights

Here are the visual evaluation outputs generated by the machine learning pipeline:

#### 1. Confusion Matrix (Production Engine)
![Confusion Matrix](notebooks/plots/confusion_matrix.png)

*Generated dynamically by the evaluation script, showing the true vs. predicted classifications on the test split.*

#### 2. Model Evaluation Metrics (Confusion Matrix, ROC Curve, and Feature Importance - Training Phase)
![Model Evaluation](notebooks/plots/model_evaluation.png)

*The model displays exceptional performance on the test set, achieving a **95.3% ROC-AUC** and a balanced confusion matrix with very low false positive and false negative rates. The feature importance plot shows that **ca** (number of major vessels), **cp** (chest pain type), and **thalach** (max heart rate) are the strongest predictors.*

#### 2. Exploratory Data Analysis & Target Distributions
![EDA Overview](notebooks/plots/eda_overview.png)

#### 3. Feature Correlation Matrix
![Correlation Heatmap](notebooks/plots/correlation_heatmap.png)

#### 4. Numerical Feature Distributions
![Feature Distributions](notebooks/plots/feature_distributions.png)

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
