# Main script to run the entire pipeline: data cleaning, data analysis, model building, training, and evaluation.

from data_cleaning import data_cleaning
from data_analysis import data_analysis
from feature_engineering import feature_engineering 
from model import model_training_and_evaluation

def run_pipeline():

    """Master entry point script to run the entire biometric fraud detection pipeline."""

    raw_csv_path = '../data/creditcard.csv'
    clean_csv_path = '../data/creditcard_cleaned.csv'

    # Cleaning raw data and save new CSV

    data_cleaning(input_path=raw_csv_path, output_path=clean_csv_path)

    # Running analysis and save plots
    data_analysis(data_path=clean_csv_path, output_dir='../output/graphs')

    # Feature engineering and train/test split
    X_train, X_test, y_train, y_test = feature_engineering(data_path=clean_csv_path)

    # Building, training, evaluating, and saving model artifacts
    model_training_and_evaluation(X_train, 
                                  X_test, 
                                  y_train, 
                                  y_test, 
                                  csv_dir='../output/csv', 
                                  graph_dir='../output/graphs', 
                                  model_dir='../output/model')

    print(" Pipeline execution completed successfully. All outputs saved in the 'output/model' directory.")

if __name__ == '__main__':
    run_pipeline()