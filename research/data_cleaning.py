# Data cleaning code for the credit card fraud detection.

#importing libraries

import os
import pandas as pd

def data_cleaning(input_path='../data/creditcard.csv', output_path='../data/creditcard_cleaned.csv'):
    """
    Loads raw dataset, identifies and removes null values and duplicates,
    and saves the cleaned dataset to disk.
    """
    print("Data Cleaning")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Dataset not found at path: {input_path}")

    # Loading raw data

    data = pd.read_csv(input_path)
    print(f"Raw Dataset Shape: {data.shape}")

    # Checking for missing values

    null_count = data.isnull().sum().sum()
    print(f"Total Null Values Found: {null_count}")

    # Checking for duplicate rows
    duplicate_count = data.duplicated().sum()
    print(f"Total Duplicate Rows Found: {duplicate_count}")

    # Cleaning data
    data_clean = data.copy()
    if null_count > 0:
        data_clean = data_clean.dropna()
        print(f"Removed {null_count} rows containing null values.")

    if duplicate_count > 0:
        data_clean = data_clean.drop_duplicates()
        print(f"Removed {duplicate_count} duplicate rows.")

    print(f"Cleaned Dataset Shape: {data_clean.shape}")

    # Saving cleaned CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data_clean.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved successfully to: {output_path}\n")

    return data_clean

if __name__ == '__main__':
    data_cleaning()