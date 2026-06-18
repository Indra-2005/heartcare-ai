"""
Model Evaluation Script for HeartCare AI
Loads the trained model artifact, predicts target values for the test split, 
generates performance metrics (classification report), and saves a confusion matrix plot.
"""

import sys
import os
# Add the project root directory to the python path to support direct script execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import yaml
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from ml.pipeline import load_and_validate_data, prepare_train_test_sets

def run_evaluation(config_path: str):
    """
    Loads the trained model artifact and evaluates its performance against the test dataset.
    
    Args:
        config_path (str): Path to the YAML configuration file.
        
    Raises:
        FileNotFoundError: If the configuration file or model artifact is missing.
    """
    # 1. Load Configuration
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    dataset_path = config['data']['dataset_path']
    target_column = config['data']['target_column']
    output_path = config['model']['output_path']
    plot_dir = config.get('evaluation', {}).get('plot_output_dir', 'notebooks/plots/')

    print("\n[1/3] Loading test datasets and model artifact...")
    # Re-verify and grab the exact same test split using the configured random state
    X, y = load_and_validate_data(dataset_path, target_column)
    _, X_test, _, y_test = prepare_train_test_sets(
        X, y, test_size=0.2, random_state=config['model']['hyperparameters'].get('random_state', 42)
    )

    # Load serialized model
    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Evaluation Error: Trained model not found at {output_path}. Run train.py first.")
    
    model_data = joblib.load(output_path)
    # Support both dictionary structure (which stores model + features) or raw classifier object
    model = model_data['model'] if isinstance(model_data, dict) else model_data

    # 2. Run Predictions & Generate Metrics
    print("[2/3] Generating performance evaluation metrics...")
    y_pred = model.predict(X_test)
    
    print("\n================== PRODUCTION CLASSIFICATION REPORT ==================")
    print(classification_report(y_test, y_pred))
    print("======================================================================\n")

    # 3. Generate and Save Plots
    print(f"[3/3] Generating confusion matrix plot...")
    os.makedirs(plot_dir, exist_ok=True)
    
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
    
    # Render plot without displaying an interactive window (essential for headless servers)
    fig, ax = plt.subplots(figsize=(6, 6))
    disp.plot(ax=ax, cmap=plt.cm.Blues, values_format='d')
    plt.title("Confusion Matrix - HeartCare AI Production Engine")
    
    plot_save_path = os.path.join(plot_dir, "confusion_matrix.png")
    plt.savefig(plot_save_path, bbox_inches='tight')
    plt.close()
    
    print(f"Success! Evaluation plot saved to: {plot_save_path}\n")

if __name__ == "__main__":
    run_evaluation("config/ml_config.yaml")