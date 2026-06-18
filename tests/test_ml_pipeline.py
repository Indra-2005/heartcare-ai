"""
ML Pipeline Integration and Unit Tests for HeartCare AI
Verifies configuration files, dataset shapes, and inference capabilities
for both Numpy array and Pandas DataFrame input representations.
"""

import os
import yaml
import pytest
import pandas as pd
import joblib
import numpy as np
from ml.pipeline import load_and_validate_data

@pytest.fixture
def ml_config():
    """Fixture to safely load and pass configuration parameters to tests."""
    config_path = "config/ml_config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def test_config_and_dataset_paths(ml_config):
    """CRITICAL: Verifies configuration entries match real filesystem paths."""
    dataset_path = ml_config['data']['dataset_path']
    model_path = ml_config['model']['output_path']
    
    assert os.path.exists(dataset_path), f"Configuration Error: Dataset missing at {dataset_path}"
    assert os.path.exists(os.path.dirname(model_path)), "Configuration Error: Output model directory missing"

def test_data_pipeline_dimensions(ml_config):
    """DATA INTEGRITY: Verifies dataset splits output exactly 13 input columns."""
    dataset_path = ml_config['data']['dataset_path']
    target_column = ml_config['data']['target_column']
    
    X, y = load_and_validate_data(dataset_path, target_column)
    
    # The processed Cleveland dataset has exactly 13 features + 1 target column
    assert X.shape[1] == 13, f"Pipeline Error: Expected 13 features, but detected {X.shape[1]}"
    assert len(X) == len(y), "Pipeline Error: Feature and target row counts mismatch"

def test_model_inference_numpy(ml_config):
    """INFERENCE GUARDRAIL: Verifies model can successfully accept a numpy row matrix and predict."""
    model_path = ml_config['model']['output_path']
    model_data = joblib.load(model_path)
    # Extract the model from the dictionary if it was saved as one
    model = model_data['model'] if isinstance(model_data, dict) else model_data
    
    # Mocking a single valid patient vector matching the 0-indexed layout
    # Features: age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
    mock_patient = np.array([[57.0, 1.0, 4.0, 140.0, 241.0, 0.0, 0.0, 123.0, 1.0, 0.2, 2.0, 0.0, 7.0]])
    
    prediction = model.predict(mock_patient)
    probabilities = model.predict_proba(mock_patient)
    
    assert len(prediction) == 1, "Inference Failure: Model failed to return a scalar prediction array"
    assert prediction[0] in [0, 1], "Inference Failure: Predicted target value out of binary boundaries"
    assert probabilities.shape == (1, 2), "Inference Failure: Model probability shapes are corrupted"

def test_model_inference_dataframe(ml_config):
    """INFERENCE GUARDRAIL: Verifies model can successfully accept a structured DataFrame and predict."""
    model_path = ml_config['model']['output_path']
    model_data = joblib.load(model_path)
    # Extract the model from the dictionary if it was saved as one
    model = model_data['model'] if isinstance(model_data, dict) else model_data
    
    # Dynamic Column Extraction: Grab the exact features used during training
    X, _ = load_and_validate_data(ml_config['data']['dataset_path'], ml_config['data']['target_column'])
    feature_names = X.columns.tolist()
    
    # Mocking a single valid patient vector matching the 0-indexed layout
    mock_values = [[57.0, 1.0, 4.0, 140.0, 241.0, 0.0, 0.0, 123.0, 1.0, 0.2, 2.0, 0.0, 7.0]]
    
    # Strict Engineering standard: Pass a DataFrame with matching column headers
    mock_patient_df = pd.DataFrame(mock_values, columns=feature_names)
    
    prediction = model.predict(mock_patient_df)
    probabilities = model.predict_proba(mock_patient_df)
    
    assert len(prediction) == 1, "Inference Failure: Model failed to return a scalar prediction array"
    assert prediction[0] in [0, 1], "Inference Failure: Predicted target value out of binary boundaries"
    assert probabilities.shape == (1, 2), "Inference Failure: Model probability shapes are corrupted"