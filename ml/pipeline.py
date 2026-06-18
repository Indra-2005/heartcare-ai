"""
Data Pipeline Module for HeartCare AI
Handles loading dataset, checking data integrity guardrails, and splitting into train/test sets.
"""

import pandas as pd
from sklearn.model_selection import train_test_split

def load_and_validate_data(csv_path: str, target_column: str):
    """
    Loads the preprocessed CSV dataset and executes production data integrity checks.
    
    Args:
        csv_path (str): File system path to the target CSV dataset.
        target_column (str): Name of the column representing the target variable.
        
    Returns:
        tuple (pd.DataFrame, pd.Series): Features (X) and Target labels (y).
        
    Raises:
        FileNotFoundError: If the specified dataset CSV file does not exist.
        ValueError: If the target column is missing from the dataset.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Critical Error: Dataset not found at {csv_path}")

    # Production Data Guardrails:
    # 1. Ensure target column exists
    if target_column not in df.columns:
        raise ValueError(f"Data Integrity Error: Target column '{target_column}' missing from dataset.")
        
    # 2. Check for unexpected missing values
    if df.isnull().sum().sum() > 0:
        # Since this is expected to be a clean preprocessed dataset, print warning and drop NaN rows
        print("[Warning]: Unexpected missing values found. Dropping NaN rows for safety.")
        df = df.dropna()

    print(f" Data loaded successfully. Shape: {df.shape}")
    
    # Separate independent features (X) and target/dependent variable (y)
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    return X, y

def prepare_train_test_sets(X, y, test_size=0.2, random_state=42):
    """
    Splits features and target datasets into train and test splits.
    Ensures reproducibility and maintains class balance through stratification.
    
    Args:
        X (pd.DataFrame): Features dataset.
        y (pd.Series): Target labels series.
        test_size (float): Proportion of dataset to include in the test split. Default is 0.2.
        random_state (int): Random seed for reproducibility. Default is 42.
        
    Returns:
        tuple: Splitted training and testing datasets (X_train, X_test, y_train, y_test).
    """
    # Use stratify=y to ensure training and testing splits maintain the same class proportions
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    print(f" Train shape: {X_train.shape} | Test shape: {X_test.shape}")
    return X_train, X_test, y_train, y_test