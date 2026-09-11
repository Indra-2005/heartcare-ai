# HeartCare AI 🫀

> **Production-grade cardiovascular disease risk prediction web platform powered by machine learning.**

**Repository**: [https://github.com/Indra-2005/heartcare-ai](https://github.com/Indra-2005/heartcare-ai)

[![Live Demo](https://img.shields.io/badge/Render-Live%20Demo-46E3B7?style=flat-square&logo=render)](https://heartcare-ai-1.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4.2-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-22.0.0-499848?style=flat-square&logo=gunicorn&logoColor=white)](https://gunicorn.org/)
[![Pytest](https://img.shields.io/badge/Pytest-Passing-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://pytest.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

HeartCare AI is an end-to-end clinical decision-support web application that predicts cardiovascular disease risk from 13 clinical biomarkers using a scikit-learn Random Forest classifier. Built with a production-ready Flask architecture, PostgreSQL relational storage, and Gunicorn WSGI runtime, it delivers real-time risk stratification, probability scoring, patient prediction history, personalized recommendations, and exportable clinical reports.

---

## 🌐 Live Demo

The application is deployed and running live on **Render**:

**🌐 [Live Demo → https://heartcare-ai-1.onrender.com](https://heartcare-ai-1.onrender.com)**

- **Hosting Platform**: Render (Web Service)
- **Runtime**: Python 3.12
- **WSGI Server**: Gunicorn 22.0.0 (2 worker processes, 120s timeout)
- **Database**: Managed PostgreSQL
- **GitHub Repository**: [https://github.com/Indra-2005/heartcare-ai](https://github.com/Indra-2005/heartcare-ai)

---

## ✨ Features

- **Heart Disease Risk Prediction**: Binary classification determining the presence or absence of cardiovascular risk based on 13 patient clinical indicators.
- **Random Forest Classification**: Production ensemble model trained with cost-sensitive class weighting for robust decision boundaries.
- **Risk Probability**: Quantitative probability scoring (0–100%) coupled with categorical risk stratification (`Low`, `Moderate`, `High`).
- **User Authentication**: Secure user registration, login, and password management powered by Flask-Login and Bcrypt password hashing.
- **Prediction History**: Per-user audit trail tracking all past clinical submissions, results, and probabilities with record deletion support.
- **PostgreSQL Database**: Relational schema managed via Flask-SQLAlchemy with Alembic / Flask-Migrate database migrations.
- **Personalized Recommendations**: Context-aware clinical follow-up guidance and lifestyle modifications dynamically tailored to the computed risk tier.
- **PDF Report**: Browser-native print-to-PDF functionality for patient summaries and clinical consultation records.
- **Visual Analytics**: Interactive SVG risk gauge visualizer and dashboard profile analytics summarizing patient history.
- **Modular ML Pipeline**: Decoupled, production-grade scripts for data validation, training orchestration, and automated evaluation.
- **Automated Tests**: Automated Pytest suite validating configuration paths, pipeline dimensions, feature alignment, and inference behavior.

---

## 🛠️ Tech Stack

| Layer | Technology | Details |
|---|---|---|
| **Language** | **Python** | Version 3.12 (pinned via `.python-version`) |
| **Web Framework** | **Flask** | Lightweight, modular WSGI application framework (v3.0.3) |
| **Machine Learning** | **Scikit-learn** | Ensemble `RandomForestClassifier` with balanced class weights (v1.4.2) |
| **Data Processing** | **Pandas & NumPy** | Structured tabular validation, feature ordering, and numerical arrays |
| **Database & ORM** | **PostgreSQL & SQLAlchemy** | Relational persistence with Flask-SQLAlchemy (v3.1.1) and Flask-Migrate (v4.0.7) |
| **Security & Forms** | **Flask-Login & Bcrypt** | Session management, Bcrypt password hashing, and CSRF-protected WTForms |
| **WSGI Server** | **Gunicorn** | Production HTTP server with multi-worker concurrency (v22.0.0) |
| **Testing** | **Pytest** | Automated unit and pipeline validation test suite |
| **Frontend** | **HTML5, CSS3, JS** | Responsive layout, modern CSS design system, dynamic SVG risk gauge |
| **Deployment** | **Render** | Cloud deployment with automated builds and PostgreSQL service |

---

## 🏗️ Project Architecture

```text
User (Web Browser)
       │
       ▼
Flask Web Application (Gunicorn WSGI / Render)
       │
       ├── Authentication & Session Management (Flask-Login, Bcrypt)
       │
       ▼
Input Validation & Feature Alignment (WTForms, Pandas)
       │
       ▼
ML Pipeline (ml/pipeline.py)
       │
       ▼
Random Forest Classifier (models/heart_disease_model.pkl)
       │
       ▼
Prediction + Risk Probability (Binary Classification & Risk Stratification)
       │
       ▼
PostgreSQL Database (User & PredictionHistory Records)
       │
       ▼
Dashboard / Prediction History / Printable PDF Report
```

---

## 🗂️ Project Structure

```text
heartcare-ai/
├── app.py                     # Flask application factory, routes, and model integration
├── config.py                  # Environment-driven configuration (DB URL, secret keys)
├── models.py                  # SQLAlchemy models (User, PredictionHistory)
├── forms.py                   # WTForms form definitions with validation rules
├── requirements.txt           # Production pinned Python dependencies
├── Procfile                   # Gunicorn WSGI startup configuration for Render
├── .python-version            # Python 3.12 runtime pin for Render deployment
├── .env.example               # Template for environment variables (safe for version control)
├── .gitignore                 # Excludes .env, virtual environments, and cache files
├── LICENSE                    # MIT open-source license
├── config/
│   └── ml_config.yaml         # ML pipeline configuration (hyperparameters, paths)
├── ml/
│   ├── __init__.py
│   ├── pipeline.py            # Data loading, schema validation, and train/test splitting
│   ├── train.py               # Model training orchestrator and artifact serialization
│   └── evaluate.py            # Evaluation script (classification report, ROC-AUC, plots)
├── models/
│   └── heart_disease_model.pkl# Serialized production model artifact with feature schema
├── data/
│   └── Heart_disease_cleveland_new.csv # Cleveland Heart Disease dataset (303 records, 14 cols)
├── tests/
│   ├── __init__.py
│   └── test_ml_pipeline.py    # Pytest suite covering ML pipeline integrity and inference
├── migrations/                # Alembic / Flask-Migrate database migration scripts
├── notebooks/
│   ├── Heart_disease_prediction.ipynb # Exploratory EDA & SMOTE experimentation notebook
│   └── plots/                 # Visual evaluation outputs and diagnostic charts
├── static/
│   ├── css/style.css          # Application stylesheet
│   ├── js/main.js             # Client-side form interactions and dynamic UI logic
│   └── favicon.svg            # Application icon
└── templates/
    ├── base.html              # Base Jinja2 layout template
    ├── auth/                  # login.html, register.html, change_password.html
    ├── dashboard/             # main.html (input form), result.html, profile.html
    ├── public/                # index.html, about.html, termscondition.html
    └── errors/                # 404.html, 500.html custom error pages
```

---

## 🧠 Machine Learning

### Dataset
- **Source**: [Cleveland Heart Disease Dataset (UCI Machine Learning Repository)](https://archive.ics.uci.edu/dataset/45/heart+disease)
- **Instances**: 303 patient records
- **Target**: Binary classification — `0` (Healthy / Absence of disease) vs. `1` (Diseased / Presence of disease)
- **Class Balance**: 164 healthy (54.1%), 139 diseased (45.9%)

### Input Clinical Features (13 Features)

| # | Feature | Clinical Description | Range / Values |
|---|---|---|---|
| 1 | `age` | Patient age | Years (29–77) |
| 2 | `sex` | Biological sex | `1` = Male, `0` = Female |
| 3 | `cp` | Chest pain type | `0` = Typical Angina, `1` = Atypical Angina, `2` = Non-anginal, `3` = Asymptomatic |
| 4 | `trestbps` | Resting blood pressure | mmHg on admission (94–200) |
| 5 | `chol` | Serum cholesterol | mg/dl (126–564) |
| 6 | `fbs` | Fasting blood sugar > 120 mg/dl | `1` = True, `0` = False |
| 7 | `restecg` | Resting electrocardiographic results | `0` = Normal, `1` = ST-T wave abnormality, `2` = Left ventricular hypertrophy |
| 8 | `thalach` | Maximum heart rate achieved | Beats per minute (71–202) |
| 9 | `exang` | Exercise-induced angina | `1` = Yes, `0` = No |
| 10 | `oldpeak` | ST depression induced by exercise | Numeric depression relative to rest (0.0–6.2) |
| 11 | `slope` | Slope of peak exercise ST segment | `0` = Upsloping, `1` = Flat, `2` = Downsloping |
| 12 | `ca` | Major vessels colored by fluoroscopy | Count (0–3) |
| 13 | `thal` | Thalassemia cardiac scan status | `1` = Normal, `2` = Fixed defect, `3` = Reversible defect |

### Model & Hyperparameters
- **Algorithm**: `RandomForestClassifier` (`scikit-learn==1.4.2`)
- **Hyperparameters** (configured via `config/ml_config.yaml`):
  - `n_estimators`: 200
  - `max_depth`: 8
  - `min_samples_split`: 10
  - `min_samples_leaf`: 4
  - `max_features`: "sqrt"
  - `class_weight`: "balanced"
  - `random_state`: 42
- **Data Split**: 80% Training (242 samples), 20% Test (61 samples), stratified by target label (`random_state=42`).

### Class Imbalance Handling
- **Production Pipeline**: The production model handles class weighting directly via `class_weight='balanced'` in `RandomForestClassifier`. This weights samples inversely proportional to class frequencies during tree splits without altering the feature distribution.
- **Notebook Experimentation**: SMOTE (Synthetic Minority Over-sampling Technique via `imbalanced-learn`) was investigated during the exploratory phase (`notebooks/Heart_disease_prediction.ipynb`). SMOTE is strictly confined to the offline experimental notebook and is **not** part of the production training or inference pipeline.

### Model Evaluation Results

Evaluation metrics verified against the held-out test split (61 samples) using `python -m ml.evaluate`:

| Metric | Score | Note |
|---|---|---|
| **Train Accuracy** | **90.5%** | Evaluated on training split (242 samples) |
| **Test Accuracy** | **88.5%** | Evaluated on held-out test split (54 / 61 correct) |
| **Test ROC-AUC** | **96.21%** | Area under ROC curve on test split |
| **5-Fold CV ROC-AUC** | **88.7%** | Stratified 5-Fold cross-validation on training data |
| **Diseased Recall** | **92.9%** | Sensitivity (26 of 28 diseased cases correctly identified) |
| **Healthy Precision** | **93.3%** | Positive predictive value for healthy predictions |

#### Verified Classification Report (`python -m ml.evaluate`)
```text
================== CLASSIFICATION REPORT ==================
              precision    recall  f1-score   support

     Healthy       0.93      0.85      0.89        33
    Diseased       0.84      0.93      0.88        28

    accuracy                           0.89        61
   macro avg       0.89      0.89      0.89        61
weighted avg       0.89      0.89      0.89        61

  Test ROC-AUC Score : 0.9621 (96.21%)
===========================================================
```

> **Clinical Significance of Recall**: In clinical screening, false negatives (classifying a diseased patient as healthy) carry the highest clinical risk. The model achieves **93% recall on the diseased class**, demonstrating high sensitivity for identifying patients requiring cardiological follow-up.

### Visual Diagnostic Charts

#### Confusion Matrix (Test Set)
![Confusion Matrix](notebooks/plots/confusion_matrix.png)

#### Model Evaluation & Feature Importance
![Model Evaluation](notebooks/plots/model_evaluation.png)

#### Exploratory Data Analysis Overview
![EDA Overview](notebooks/plots/eda_overview.png)

#### Feature Correlation Heatmap
![Correlation Heatmap](notebooks/plots/correlation_heatmap.png)

#### Feature Distributions
![Feature Distributions](notebooks/plots/feature_distributions.png)

---

## ⚙️ ML Evaluation & Training

### Evaluate Model
Run model evaluation to generate the classification report, ROC-AUC score, and confusion matrix plot:
```bash
python -m ml.evaluate
```
*Outputs are saved directly to `notebooks/plots/confusion_matrix.png`.*

### Train Model
Retrain the model using the configuration defined in `config/ml_config.yaml`:
```bash
python -m ml.train
# Or pass a custom configuration:
python -m ml.train --config config/ml_config.yaml
```
*Saves the serialized dictionary artifact (`model` + `features`) to `models/heart_disease_model.pkl`.*

---

## 🧪 Testing

The repository contains automated unit and integration tests powered by **Pytest**:

```bash
python -m pytest tests/ -v
```

### Verified Test Status
```text
============================= test session starts =============================
platform win32 -- Python 3.10+, pytest-9.x, pluggy-1.x
collected 6 items

tests/test_ml_pipeline.py::test_config_and_dataset_paths PASSED          [ 16%]
tests/test_ml_pipeline.py::test_data_pipeline_dimensions PASSED          [ 33%]
tests/test_ml_pipeline.py::test_feature_names_match_model PASSED         [ 50%]
tests/test_ml_pipeline.py::test_model_inference_dataframe PASSED         [ 66%]
tests/test_ml_pipeline.py::test_model_inference_numpy_with_feature_names PASSED [ 83%]
tests/test_ml_pipeline.py::test_probability_output_range PASSED          [100%]

============================== 6 passed, 0 warnings ==============================
```

### Test Coverage
- `test_config_and_dataset_paths`: Asserts dataset and model directory paths exist.
- `test_data_pipeline_dimensions`: Validates 13 input features and row parity after cleaning.
- `test_feature_names_match_model`: Ensures training columns match model feature schema.
- `test_model_inference_dataframe`: Verifies inference with named Pandas DataFrame.
- `test_model_inference_numpy_with_feature_names`: Verifies inference when NumPy arrays are wrapped with feature names.
- `test_probability_output_range`: Asserts all output probabilities fall strictly between 0 and 1.

---

## 💻 Installation & Local Setup

### Prerequisites
- Python 3.10, 3.11, or 3.12
- PostgreSQL (local instance or remote connection URI)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Indra-2005/heartcare-ai.git
cd heartcare-ai
```

### 2. Create and Activate Virtual Environment
```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the environment template and provide your local credentials:
```bash
cp .env.example .env
```
Edit `.env` with your values:
```ini
SECRET_KEY=generate_a_secure_random_hex_string
DATABASE_URL=postgresql://postgres:password@localhost:5432/heartcare_db
PORT=8080
```
> Generate a secure `SECRET_KEY`:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

### 5. Database Setup
Apply migrations to create database tables:
```bash
flask db upgrade
```

### 6. Run Application
```bash
python app.py
```
Open your browser and navigate to: `http://localhost:8080`

---

## ☁️ Deployment

HeartCare AI is configured for continuous cloud deployment on **Render**.

### Render Configuration
- **Environment**: Python 3.12 (pinned via `.python-version`)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --workers 2 --timeout 120` (specified in `Procfile`)
- **Public URL**: `https://heartcare-ai-1.onrender.com`

### Required Environment Variables on Render
Configure the following in the **Render Dashboard > Environment**:

| Variable | Description | Example / Notes |
|---|---|---|
| `SECRET_KEY` | Flask session secret | 64-character random hex string |
| `DATABASE_URL` | PostgreSQL connection string | Automatically populated when linking a Render PostgreSQL database |
| `PORT` | Web server listening port | Set automatically by Render's runtime environment |

> **SQLAlchemy Compatibility**: `config.py` automatically normalizes legacy `postgres://` URLs to `postgresql://` to maintain full compatibility with SQLAlchemy 2.x.

---

## 📡 API Endpoints

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/` | Public | Landing page with platform overview |
| `GET` | `/about` | Public | Project mission, architecture, and medical details |
| `GET` | `/termscondition` | Public | Terms of service and medical disclaimer |
| `GET`, `POST` | `/register` | Public | User registration with input validation |
| `GET`, `POST` | `/login` | Public | User authentication with open-redirect protection |
| `GET` | `/logout` | Authenticated | Session termination |
| `GET` | `/main` | Authenticated | Clinical parameter submission form |
| `POST` | `/predict` | Authenticated | Model inference, risk calculation, and history storage |
| `GET` | `/profile` | Authenticated | User dashboard, prediction history, and statistics |
| `GET`, `POST` | `/change-password` | Authenticated | Secure in-app password update |
| `POST` | `/delete-history/<id>` | Authenticated | Delete individual prediction history entry |
| `GET` | `/api/stats` | Authenticated | JSON statistics endpoint for dashboard visualization |

---

## ⚠️ Limitations

- **Dataset Sample Size**: Trained on the Cleveland dataset containing 303 patient records. While standard for academic benchmarking, clinical deployment requires validation across tens of thousands of diverse patients.
- **Single-Center Cohort**: The data originates from a single clinical center (Cleveland Clinic Foundation) collected in the 1980s. Modern diagnostic criteria, laboratory assays, and population demographics have evolved.
- **Lack of External Clinical Validation**: The model has not undergone prospective multi-center clinical trials or cross-hospital external validation.
- **Uncalibrated Probabilities**: Random Forest `predict_proba()` computes the proportion of decision trees voting for each class. These percentages represent tree consensus rather than formally calibrated Bayesian posterior probabilities.
- **Screening Tool Only**: Outputs represent statistical risk estimates, not definitive medical diagnoses or anatomical confirmations.

---

## 🔮 Future Improvements

- **Probability Calibration**: Implement Platt scaling or Isotonic Regression via `CalibratedClassifierCV` for reliable probabilistic risk estimates.
- **Explainable AI (XAI)**: Integrate SHAP (SHapley Additive exPlanations) waterfall plots to provide patient-specific feature attribution in the UI.
- **External Multi-Dataset Validation**: Benchmark generalization against the Hungarian, Swiss, and Long Beach VA heart disease datasets.
- **Model Benchmarking**: Systematically compare Random Forest against gradient boosting frameworks (XGBoost, LightGBM, CatBoost).
- **Experiment Tracking**: Integrate MLflow for hyperparameter logging, metric tracking, and model versioning.
- **CI/CD Automation**: Implement GitHub Actions workflows for automated testing, linting, and continuous deployment triggers.
- **Containerization**: Provide `Dockerfile` and `docker-compose.yml` for fully reproducible local and multi-cloud container deployments.

---

## ⚕️ Medical Disclaimer

**HeartCare AI is an educational and machine learning portfolio project.**

This application is **NOT** a certified medical device and has not been reviewed, evaluated, or approved by the FDA or any other healthcare regulatory authority. It is designed solely for informational, screening, and educational purposes and must **NEVER** be used as a substitute for professional medical diagnosis, clinical advice, or treatment. Always seek the advice of a board-certified cardiologist or qualified healthcare professional with any questions regarding cardiovascular health.

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
