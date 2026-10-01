# Building model using tensorflow and keras for the biometric DID system fraud detection project.

# importing libraries

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.metrics import classification_report, confusion_matrix

def model_building(input_dim):

    """Constructing and compiling the Keras Sequential neural network model."""

    model = Sequential([
        Dense(32, activation='relu', input_shape=(input_dim,)),
        Dropout(0.2),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    return model

def model_training_and_evaluation(X_train, X_test, y_train, y_test, csv_dir = '../output/csv', graph_dir = '../output/graphs', model_dir = '../output/model')  :
    """
    Trains the neural network, saves classification report table,
    confusion matrix heatmap, and the full trained .h5 model.
    """
    print("Model Training & Evaluation")
    os.makedirs(csv_dir, exist_ok=True)
    os.makedirs(graph_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)
    
    # Building model

    model = model_building(input_dim=X_train.shape[1])

    # Training model

    history = model.fit(
        X_train, y_train,
        epochs=10,
        batch_size=2048,
        validation_split=0.2,
        verbose=1
    )

    # Predicting test probabilities and labels

    y_pred = (model.predict(X_test) > 0.35).astype("int32")

    # Generating & Saving Classification Report

    print("\nGenerating Tabular Classification Report")
    report_dict = classification_report(y_test, y_pred, output_dict=True)
    report_df = pd.DataFrame(report_dict).transpose()
    report_df.loc['accuracy', 'support'] = len(y_test)

    report_df['precision'] = report_df['precision'].round(4)
    report_df['recall'] = report_df['recall'].round(4)
    report_df['f1-score'] = report_df['f1-score'].round(4)
    report_df['support'] = report_df['support'].astype(int)
    report_df.index.name = 'Class / Metric'

    report_csv_path = os.path.join(csv_dir, 'classification_report.csv')
    report_df.to_csv(report_csv_path, index=True)
    print(f"Classification Report saved as '{report_csv_path}'")

    # Generating & Saving Confusion Matrix Plot

    plt.figure(figsize=(6, 4))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix', fontsize=12, pad=15)
    plt.xlabel('Predicted', fontsize=10, labelpad=10)
    plt.ylabel('Actual', fontsize=10, labelpad=10)

    cm_path = os.path.join(graph_dir, 'confusion_matrix.png')
    plt.tight_layout()
    plt.savefig(cm_path, bbox_inches='tight', pad_inches=0.3, dpi=300)
    plt.close()
    print(f"Confusion Matrix plot saved as '{cm_path}'")

    # Save Trained Keras Model

    model_save_path = os.path.join(model_dir, 'fraud_detection_model.h5')
    model.save(model_save_path)
    print(f"Trained Model saved as '{model_save_path}'\n")

    return model, history