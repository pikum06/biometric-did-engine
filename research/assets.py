# 2. Model and dataset loader with Streamlit resource caching

# importing libraries

import os
import pandas as pd
import tensorflow as tf
from keras_facenet import FaceNet
import streamlit as st

# Initializing and asset loading

@st.cache_resource
def load_all_assets():
    """
    Loads Keras fraud detection model (.h5), credit card dataset (.csv),
    and FaceNet computer vision embedder.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Path resolution for output model
    model_path = os.path.join(base_path, '../output/model/fraud_detection_model.h5')
    if not os.path.exists(model_path):
        model_path = os.path.join(base_path, 'output/model/fraud_detection_model.h5')

    # Path resolution for transaction dataset
    csv_path = os.path.join(base_path, '../data/creditcard_cleaned.csv')
    if not os.path.exists(csv_path):
        csv_path = os.path.join(base_path, 'data/creditcard_cleaned.csv')

    if not os.path.exists(model_path) or not os.path.exists(csv_path):
        st.error("Files Missing! Ensure '.h5' model and '.csv' dataset are present in the output/ and data/ folders.")
        st.stop()
    
    # Load AI models and dataset
    nn_model = tf.keras.models.load_model(model_path, compile=False)
    dataframe = pd.read_csv(csv_path)
    facenet_ai = FaceNet()
    
    return facenet_ai, nn_model, dataframe
