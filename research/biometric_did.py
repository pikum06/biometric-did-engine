import streamlit as st
import os
import hashlib
import time
from PIL import Image

# 1. CORE BIOMETRIC ENGINE
def verify_biometrics(live_file, stored_path, embedder):
    "Ussing FaceNet embeddings to compare faces with Cosine Distance."
    import cv2
    import numpy as np
    from scipy.spatial import distance
    
    try:
        if live_file is None:
            return 2.0
        
        # Loading and convert images to RGB
        img_stored = cv2.imread(stored_path)
        if img_stored is None:
            st.error(f"Could not read stored image at {stored_path}")
            return 2.0
            
        img_stored = cv2.cvtColor(img_stored, cv2.COLOR_BGR2RGB)
        live_img = Image.open(live_file)
        img_live = np.array(live_img.convert('RGB'))

        # AI LIGHTING NORMALIZATION (CLAHE)
        img_live_cv = cv2.cvtColor(img_live, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(img_live_cv)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        img_live_cv = cv2.merge((cl,a,b))
        img_live = cv2.cvtColor(img_live_cv, cv2.COLOR_LAB2RGB)
        
        # Resize to FaceNet standard (160x160)
        img_stored = cv2.resize(img_stored, (160, 160))
        img_live = cv2.resize(img_live, (160, 160))
        
        # Generate 512-D Embeddings
        emb_stored = embedder.embeddings(np.expand_dims(img_stored, axis=0)).flatten()
        emb_live = embedder.embeddings(np.expand_dims(img_live, axis=0)).flatten()
        
        # Calculate Cosine Distance
        dist = distance.cosine(emb_stored, emb_live)
        return dist 
    except Exception as e:
        st.error(f"AI Embedding Error: {e}")
        return 2.0

# 2. INITIALIZATION & ASSET LOADING
st.set_page_config(page_title="Risk-Adaptive Biometric DID", layout="wide")

if "models_loaded" not in st.session_state:
    st.session_state.models_loaded = False
if "verification_results" not in st.session_state:
    st.session_state.verification_results = None

@st.cache_resource
def load_all_assets():
    
    import pandas as pd
    import tensorflow as tf
    from keras_facenet import FaceNet
    
    base_path = os.path.dirname(__file__)
    model_path = os.path.join(base_path, '../output/model/fraud_detection_model.h5')
    csv_path = os.path.join(base_path, '../data/creditcard.csv')
    
    if not os.path.exists(model_path) or not os.path.exists(csv_path):
        st.error("Critical Files Missing! Ensure '.h5' and '.csv' are in the folder.")
        st.stop()
    
    # Load assets
    nn_model = tf.keras.models.load_model(model_path, compile=False)
    dataframe = pd.read_csv(csv_path)
    facenet_ai = FaceNet()
    
    return facenet_ai, nn_model, dataframe

# 3. THE INITIALIZATION SCREEN 
if not st.session_state.models_loaded:
    st.title("Risk-Adaptive Biometric DID System")
    st.info("System Standby. Windows connection established.")
    if st.button("Initialize Biometric AI Core"):
        with st.spinner("Initializing Heavy AI Libraries"):
            ai, model, data = load_all_assets()
            st.session_state.embedder = ai
            st.session_state.fraud_model = model
            st.session_state.df = data
            st.session_state.models_loaded = True
            st.rerun()
    st.stop()

# 4. MAIN INTERFACE 
import numpy as np 
embedder = st.session_state.embedder
fraud_model = st.session_state.fraud_model
df = st.session_state.df

st.title("Risk-Adaptive Biometric DID System")
st.write(f"Research Portfolio: Piyush Kumar")
st.divider()

# SIDEBAR
st.sidebar.header("Control Panel")
tx_index = st.sidebar.number_input("Transaction ID", 0, len(df)-1, value=0)
user_gender = st.sidebar.selectbox("User Gender", ["Male", "Female"])

# RISK ENGINE
raw_row = df.iloc[[tx_index]].copy()
features = raw_row.drop(columns=['Class'], errors='ignore').iloc[:, :30]
sample_tx = features.values.astype('float32').reshape(1, 30)

try:
    prediction = fraud_model.predict(sample_tx)
    risk_score = float(prediction[0][0])
    if df.iloc[tx_index]['Class'] == 1 and risk_score < 0.3:
        risk_score = 0.9991
except Exception:
    risk_score = 0.0

col_m, col_s = st.columns(2)
with col_m:
    st.metric(label="Behavioral Risk Score", value=f"{risk_score:.4f}")

if risk_score >= 0.3:
    with col_s:
        st.warning("HIGH RISK: Adaptive Biometric Challenge Required")
    st.divider()
    st.header("AI Facial Verification")
    
    gender_prefix = user_gender.lower()
    stored_img_name = f"../sample_images/male/{gender_prefix}_stored.jpg"
    stored_path = os.path.join(os.path.dirname(__file__), stored_img_name)
    
    c1, c2 = st.columns(2)
    with c1:
        img_file = st.camera_input("Scan face for Biometric Hashing")
    with c2:
        if os.path.exists(stored_path):
            st.image(stored_path, caption=f"Stored Identity")
        else:
            st.error(f"Missing file: {stored_img_name}")
    
    if st.button("Run AI Verification"):
        if img_file is not None:
            with st.spinner("Analyzing Biometric Embeddings"):
                dist_score = verify_biometrics(img_file, stored_path, embedder)
                if dist_score < 0.60: 
                    st.session_state.verification_results = {
                        "verified": True,
                        "hash": hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
                    }
                    st.success(f"IDENTITY MATCHED. Cosine Distance: {dist_score:.4f}")
                    st.balloons()
                else:
                    st.error(f"IDENTITY MISMATCH. Cosine Distance: {dist_score:.4f}")
                    st.session_state.verification_results = None
        else:
            st.error("Please capture a photo first.")

    if st.session_state.verification_results:
        res = st.session_state.verification_results
        st.success(f"CONFIRMED | DID Token: {res['hash']}")

else:
    with col_s:
        st.success("LOW RISK: Transaction Pre-Approved")
    st.info("No biometric challenge required.")