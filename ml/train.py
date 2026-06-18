"""
Model Training Script for HeartCare AI
Loads training configuration, runs the preprocessing pipeline, initializes and trains 
the RandomForestClassifier, and serializes the model artifact as a dictionary containing 
both the model object and training feature names.
"""

import sys
import os
# Add the project root directory to the python path to support direct script execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import yaml
import pickle
from sklearn.ensemble import RandomForestClassifier
from ml.pipeline import load_and_validate_data, prepare_train_test_sets

def run_training(config_path: str):
    """
    Orchestrates the entire training lifecycle using configurations.
    
    Args:
        config_path (str): Path to the YAML configuration file containing model hyperparameters
                           and dataset paths.
                           
    Raises:
        FileNotFoundError: If the configuration file or dataset file is missing.
    """
    # 1. Load YAML Configuration safely
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")
        
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    print("\n[1/4] Extracting configuration parameters...")
    dataset_path = config['data']['dataset_path']
    target_column = config['data']['target_column']
    model_params = config['model']['hyperparameters']
    output_path = config['model']['output_path']

    # 2. Run Data Pipeline
    print("[2/4] Triggering data preprocessing pipeline...")
    X, y = load_and_validate_data(dataset_path, target_column)
    X_train, X_test, y_train, y_test = prepare_train_test_sets(
        X, y, test_size=0.2, random_state=model_params.get('random_state', 42)
    )

    # 3. Initialize and Train Model
    print(f"[3/4] Initializing {config['model']['algorithm']} with configured hyperparameters...")
    model = RandomForestClassifier(**model_params)
    
    print("Training model... Please wait.")
    model.fit(X_train, y_train)

    # 4. Serialize and Save Model Artifact
    print("[4/4] Serializing model artifact...")
    # Ensure the models/ directory exists before saving
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save as a dictionary containing the model and the training feature names.
    # This structure is required by app.py for feature alignment during web inference.
    model_data = {
        'model': model,
        'features': list(X_train.columns)
    }
    with open(output_path, 'wb') as f:
        pickle.dump(model_data, f)
    print(f"Success! Production model saved directly to: {output_path}\n")

if __name__ == "__main__":
    # Using argparse allows passing a different config file path via the CLI
    parser = argparse.ArgumentParser(description="Production ML Training Orchestrator")
    parser.add_argument(
        "--config", 
        type=str, 
        default="config/ml_config.yaml", 
        help="Path to the YAML configuration file"
    )
    args = parser.parse_args()
    
    run_training(args.config)