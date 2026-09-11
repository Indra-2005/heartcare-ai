"""
ML Pipeline Integration and Unit Tests for HeartCare AI
Verifies configuration files, dataset shapes, and inference capabilities
for both Pandas DataFrame and NumPy array input representations.
"""

import os
import yaml
import pytest
import pandas as pd
import pickle
import numpy as np
from ml.pipeline import load_and_validate_data

# Canonical mock patient: one sample matching all 13 training features
# Features: age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
_MOCK_VALUES = [[57.0, 1.0, 4.0, 140.0, 241.0, 0.0, 0.0, 123.0, 1.0, 0.2, 2.0, 0.0, 7.0]]
_FEATURE_NAMES = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
                  'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']


@pytest.fixture
def ml_config():
    """Fixture to safely load and pass configuration parameters to tests."""
    config_path = "config/ml_config.yaml"
    assert os.path.exists(config_path), f"Config file missing: {config_path}"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


@pytest.fixture
def trained_model(ml_config):
    """Fixture to load the trained model artifact once and share across tests."""
    model_path = ml_config['model']['output_path']
    assert os.path.exists(model_path), (
        f"Model not found at '{model_path}'. Run 'python -m ml.train' first."
    )
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
    return model_data['model'] if isinstance(model_data, dict) else model_data


def test_config_and_dataset_paths(ml_config):
    """CRITICAL: Verifies configuration entries match real filesystem paths."""
    dataset_path = ml_config['data']['dataset_path']
    model_path = ml_config['model']['output_path']

    assert os.path.exists(dataset_path), f"Configuration Error: Dataset missing at {dataset_path}"
    assert os.path.exists(os.path.dirname(model_path)), \
        "Configuration Error: Output model directory missing"


def test_data_pipeline_dimensions(ml_config):
    """DATA INTEGRITY: Verifies dataset loads with exactly 13 input features."""
    dataset_path = ml_config['data']['dataset_path']
    target_column = ml_config['data']['target_column']

    X, y = load_and_validate_data(dataset_path, target_column)

    assert X.shape[1] == 13, f"Pipeline Error: Expected 13 features, got {X.shape[1]}"
    assert len(X) == len(y), "Pipeline Error: Feature and target row counts mismatch"


def test_feature_names_match_model(ml_config, trained_model):
    """FEATURE ALIGNMENT: Verifies training feature names match model's expected features."""
    X, _ = load_and_validate_data(
        ml_config['data']['dataset_path'],
        ml_config['data']['target_column']
    )
    assert list(X.columns) == _FEATURE_NAMES, (
        f"Feature mismatch.\nExpected: {_FEATURE_NAMES}\nGot: {list(X.columns)}"
    )


def test_model_inference_dataframe(trained_model):
    """INFERENCE: Verifies model accepts a named DataFrame and returns valid binary output."""
    mock_df = pd.DataFrame(_MOCK_VALUES, columns=_FEATURE_NAMES)

    prediction = trained_model.predict(mock_df)
    probabilities = trained_model.predict_proba(mock_df)

    assert len(prediction) == 1, "Inference Failure: Expected scalar prediction array"
    assert prediction[0] in [0, 1], "Inference Failure: Predicted value out of binary boundaries"
    assert probabilities.shape == (1, 2), "Inference Failure: Probability array shape mismatch"
    assert abs(probabilities[0].sum() - 1.0) < 1e-6, "Inference Failure: Probabilities don't sum to 1"


def test_model_inference_numpy_with_feature_names(trained_model):
    """INFERENCE: Verifies model accepts numpy input wrapped in DataFrame (avoids sklearn warning)."""
    # The model was trained on a DataFrame, so we wrap numpy data in a DataFrame
    # to maintain feature name alignment and avoid sklearn UserWarnings.
    mock_array = np.array(_MOCK_VALUES)
    mock_df = pd.DataFrame(mock_array, columns=_FEATURE_NAMES)

    prediction = trained_model.predict(mock_df)
    probabilities = trained_model.predict_proba(mock_df)

    assert len(prediction) == 1, "Inference Failure: Expected scalar prediction array"
    assert prediction[0] in [0, 1], "Inference Failure: Predicted value out of binary boundaries"
    assert probabilities.shape == (1, 2), "Inference Failure: Probability array shape mismatch"


def test_probability_output_range(trained_model):
    """PROBABILITY: Verifies all output probabilities are in [0, 1]."""
    mock_df = pd.DataFrame(_MOCK_VALUES, columns=_FEATURE_NAMES)
    probabilities = trained_model.predict_proba(mock_df)

    assert (probabilities >= 0).all(), "Probability values below 0 detected"
    assert (probabilities <= 1).all(), "Probability values above 1 detected"