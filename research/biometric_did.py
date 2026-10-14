# Building the Biometric DID System with Risk-Adaptive Verification and Cross-Chain Key Derivation

# importing libraries

import streamlit as st
import os
import hashlib
import time


# Import external computer vision and AI libraries from image_analysis.py

try:
    from image_analysis import image_biometrics
    from solana import solana_devnet_broadcast
    from assets import load_all_assets
    from risk_engine import transaction_risk
except ImportError:
    
    # Fallback if running standalone
    from research.biometric_did import image_biometrics
    from research.solana import solana_devnet_broadcast
    from research.assets import load_all_assets
    from research.risk_engine import transaction_risk  

# 1. Page Configuration & Session State
st.set_page_config(page_title="Risk-Adaptive Biometric DID", layout="wide")

if "models_loaded" not in st.session_state:
    st.session_state.models_loaded = False
if "verification_results" not in st.session_state:
    st.session_state.verification_results = None

# 2. The initial screen

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

# 3. Main interface 
 
embedder = st.session_state.embedder
fraud_model = st.session_state.fraud_model
df = st.session_state.df

st.title("Risk-Adaptive Biometric DID System")
st.write(f"Research Portfolio: Piyush Kumar | Hardware-Isolated TEE & Solana Devnet Integration")
st.divider()

# Sidebar Controls

st.sidebar.header("Control Panel")
tx_index = st.sidebar.number_input("Transaction ID", 0, len(df)-1, value=0)
user_gender = st.sidebar.selectbox("User Gender", ["Male", "Female"])

# 4. Risk Assessment

risk_score = transaction_risk(df, tx_index, fraud_model)


col_m, col_s = st.columns(2)
with col_m:
    st.metric(label="Behavioral Risk Score", value=f"{risk_score:.4f}")

if risk_score >= 0.3:
    with col_s:
        st.warning("HIGH RISK: Adaptive Biometric Challenge Required")
    st.divider()
    st.header("AI Facial Verification")
    
    gender_prefix = user_gender.lower()
    base_path = os.path.dirname(__file__)
    stored_img_name = f"../sample_images/{gender_prefix}/{gender_prefix}_stored.jpg"
    stored_path = os.path.join(os.path.dirname(__file__), stored_img_name)
    if not os.path.exists(stored_path):
        stored_path = os.path.join(base_path, f"../sample_images/{gender_prefix}/{gender_prefix}_stored.jpg")
    
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
            with st.spinner("Salting biometric in Local TEE & & Generating zk-SNARK Proof"):
                dist_score, derived_keys, zk_proof = image_biometrics(img_file, stored_path, embedder)
                if dist_score < 0.60 and derived_keys is not None:
                    token_hash = hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
                    solana_broadcast = solana_devnet_broadcast(token_hash)

                    st.session_state.verification_results = {
                        "verified": True,
                        "dist_score": dist_score,
                        "hash": token_hash,
                        "solana_key": derived_keys["solana_ed25519_seed"],
                        "evm_key": derived_keys["evm_secp256k1_seed"],
                        "zk_proof": zk_proof,
                        "solana_broadcast": solana_broadcast
                    }
                else:
                    st.error(f"IDENTITY MISMATCH. Cosine Distance: {dist_score:.4f}")
                    st.session_state.verification_results = None
        else:
            st.error("Please capture a photo first.")

    if st.session_state.verification_results:
        res = st.session_state.verification_results

        # Row 1 of 2x2 Grid: Status Cards

        c_r1_1, c_r1_2 = st.columns(2)
        with c_r1_1:
            st.success(f"Identity matched. Cosine Distance: {res.get('dist_score', 0.0):.4f}")
        with c_r1_2:
            st.success(f"Confirmed | DID Token: {res['hash']}")

        # Row 2 of 2x2 Grid: Blue Key Derivation Cards
        c_r2_1, c_r2_2 = st.columns(2)
        with c_r2_1:
            st.info(f"Solana Ed25519 Key (TEE Derived): `{res['solana_key']}`")
        with c_r2_2:
            st.info(f"EVM SECP256k1 Key (TEE Derived): `{res['evm_key']}`")

        st.divider()

        # Side-by-side column for displaying zk-proof and solana devnetbroadcast result

        col_zk, col_sol = st.columns(2)
        with col_zk:
            st.subheader("Zero-Knowledge Proof Generation")
            if res.get("zk_proof"):
                st.json(res["zk_proof"])
            else:
                st.warning("No zk-proof generated.")

        with col_sol:
            st.subheader("Solana Devnet Broadcast Result")
            if res.get("solana_broadcast"):
                sol = res["solana_broadcast"]
                st.info(f"**Broadcast Status:** `{sol.get('status', 'Success')}`")
                if "blockhash" in sol:
                    st.info(f"**Finalized Blockhash:** `{sol['blockhash']}`")
                st.markdown(f"**Solana Devnet Explorer:** [{sol['explorer_url']}]({sol['explorer_url']})")
            else:
                st.warning("No Solana broadcast result available.")  
else:
    with col_s:
        st.success("LOW RISK: Transaction Pre-Approved")
    st.info("No biometric challenge required.")