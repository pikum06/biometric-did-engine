# Conducting feature engineering on the cleaned dataset for the biometric DID system fraud detection project.

# importing libraries

import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def feature_engineering(data_path='../data/creditcard_cleaned.csv', target_col='Class', test_size=0.2, random_state=42):
    """
    Scales 'Amount' and 'Time' features, drops unscaled originals, 
    and returns stratified train/test split datasets.
    """
    print("Feature Engineering & Train/Test Split")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Cleaned dataset not found at: {data_path}")

    df = pd.read_csv(data_path)
    data = df.copy()

    # Scale 'Amount' and 'Time'

    scaler = StandardScaler()
    data['scaled_amount'] = scaler.fit_transform(data['Amount'].values.reshape(-1, 1))
    data['scaled_time'] = scaler.fit_transform(data['Time'].values.reshape(-1, 1))

    # Drop raw unscaled columns

    data = data.drop(['Amount', 'Time'], axis=1)

    # Separate features and target

    X = data.drop(target_col, axis=1)
    y = data[target_col]

    # Stratified train/test split

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    print(f"Feature set size: {X.shape[1]} columns")
    print(f"Training Samples: {X_train.shape[0]} | Testing Samples: {X_test.shape[0]}\n")

    return X_train, X_test, y_train, y_test

if __name__ == '__main__':
    feature_engineering()