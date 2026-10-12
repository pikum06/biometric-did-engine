# AI Facial Processing, CLAHE Normalization & Feature Extraction Engine for Biometric Hashing and zk-SNARK Proof Generation

# importiing libraries
import cv2
import numpy as np
from PIL import Image
from scipy.spatial import distance

# import TEE key derivation and zk-proof generation modules
try:
    from tee import tee_enclave_key
    from zk_prover import generate_zk_proof
except ImportError:
    
    # Fallback if running standalone

    from research.tee import tee_enclave_key  
    from research.zk_prover import generate_zk_proof  


# 1. CORE BIOMETRIC ENGINE
def image_biometrics(live_file, stored_path, embedder):
    
    "Using FaceNet embeddings to compare faces with Cosine Distance."
    
    
    if live_file is None:
        return 2.0, None, None
        
    # Loading and convert images to RGB

    img_stored = cv2.imread(stored_path)
    if img_stored is None:
        raise FileNotFoundError(f"Could not read stored image at {stored_path}")

            
    img_stored = cv2.cvtColor(img_stored, cv2.COLOR_BGR2RGB)
    live_img = Image.open(live_file)
    img_live = np.array(live_img.convert('RGB'))

    # Conducing CLAHE normalization for AI verificiation and feature extraction

    img_live_cv = cv2.cvtColor(img_live, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(img_live_cv)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    img_live_cv = cv2.merge((cl,a,b))
    img_live = cv2.cvtColor(img_live_cv, cv2.COLOR_LAB2RGB)
        
    # Resize to FaceNet standard (160x160)

    img_stored = cv2.resize(img_stored, (160, 160))
    img_live = cv2.resize(img_live, (160, 160))
        
    # Generating 512-D Embeddings

    emb_stored = embedder.embeddings(np.expand_dims(img_stored, axis=0)).flatten()
    emb_live = embedder.embeddings(np.expand_dims(img_live, axis=0)).flatten()

    # Calculate Cosine Distance
    
    dist = distance.cosine(emb_stored, emb_live)

    # Generate deterministic un-linkable key pairs inside local TEE simulation
        
    derived_keys = tee_enclave_key(emb_live)

    # Off-Chain Zero-Knowledge Proof Generation
    
    master_salt = derived_keys.get("master_salt_bytes")
    zk_proof = generate_zk_proof(emb_live, emb_stored, master_salt=master_salt)
        
   
    return dist, derived_keys, zk_proof 
    
