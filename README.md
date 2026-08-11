# Risk-Adaptive Biometric Decentralized Identity (DID) Engine

An interactive Web3 authentication gateway built with Streamlit. This application orchestrates an __AI Behavioral Fraud Engine with a FaceNet Biometric Verification Core__ to provide dynamic, risk-adapted authentication for Decentralized Identity (DID) token emission.

## Architecture Overview

The application executes a multi-stage risk-adaptive verification pipeline:

```text

[ Select Transaction ID & Demographics ]
                   │
                   ▼
[ 30-D Behavioral Feature Extraction ]
                   │
                   ▼
[ Deep Neural Network Fraud Prediction ]
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
 Risk Score < 0.30   Risk Score ≥ 0.30
 (Low Risk Path)     (High Risk Path)
         │                   │
         ▼                   ▼
 [ Auto-Pre-Approve ]  [ Step-Up AI Facial Verification ]
                             │
                             ▼
                       [ Optical Camera Scan / File Upload ]
                             │
                             ▼
                       [ LAB CLAHE Lighting Normalization ]
                             │
                             ▼
                       [ 512-D FaceNet Vector Embedding ]
                             │
                             ▼
                       [ Cosine Distance Verification ]
                             │
                   ┌─────────┴─────────┐
                   ▼                   ▼
            Distance < 0.60     Distance ≥ 0.60
            (Identity Match)   (Identity Mismatch)
                   │                   │
                   ▼                   ▼
          [ SHA-256 DID Token ] [ Block Transaction ]

```
## Key Features
1. **Lazy-Loaded Asset Core:** Heavy machine learning models (TensorFlow, Keras-FaceNet, Pandas) are deferred behind an interactive standby gate to prevent startup delays and Streamlit WebSocket timeouts.
2. **Behavioral Risk Engine:** Evaluates a 30-dimensional feature vector from transaction records using a pre-trained Deep Neural Network (fraud_detection_model.h5) to generate a continuous risk score between $0.0000$ and $1.0000$.
3. **CLAHE Computer Vision Enhancement:** Pre-processes optical images by converting RGB frames to the LAB color space and applying Contrast Limited Adaptive Histogram Equalization (CLAHE) to the Luminance ($L$) channel (clip limit 3.0, grid size $8 \times 8$) to normalize lighting variations.
4. **FaceNet Vector Embeddings:** Resizes live and reference images to $160 \times 160$ pixels and extracts 512-dimensional normalized feature embeddings via Keras-FaceNet.  Cosine Distance Identity Matching: Calculates spatial Cosine Distance between stored reference profiles and live optical captures:

$$D_{cosine}(u, v) = 1 - \frac{u \cdot v}{\Vert{}u\Vert{}_2 \Vert{}v\Vert{}_2}$$

An identity match is confirmed if $D_{cosine} < 0.60$. 

5. **Ephemeral DID Token Emission:** Generates a unique 16-character SHA-256 hash combined with a temporal timestamp upon successful identity verification.

## System Requirements & Dependencies
1. Python Version: Python 3.9 – 3.11

2. Hardware: Webcam access for live facial optical capture

## Dependencies 
1. streamlit
2. opencv-python / opencv-python-headless
3. numpy
4. pandas
5. pillow
6. scipy
7. tensorflow
8. keras-facenet


## Project Directory Structure
To run biometric_did.py successfully, organize your directory according to the relative file paths referenced in the code:
```
.
├── data/
│   └── creditcard.csv                 # Transaction dataset (30 PCA features)
├── output/
│   └── model/
│       └── fraud_detection_model.h5   # Pre-trained TensorFlow model
├── sample_images/
│   ├── male/
│   │   └── male_stored.jpg            # Reference male identity profile
│   └── female/
│       └── female_stored.jpg          # Reference female identity profile
└── src/
    └── biometric_did.py               # Main Streamlit application
```

## Installation & Setup

1. **Clone Repository**
git clone https://github.com/your-username/biometric-did-engine.git
cd biometric-did-engine

2. **Create and Activate a Virtual Environment:**
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. **Install Core Dependencies:**
pip install streamlit pandas numpy tensorflow keras-facenet opencv-python pillow scipy

4. **Verify Asset Placement:**
Ensure creditcard.csv, fraud_detection_model.h5, and profile images are in their respective relative directories.

5. **Running the Application**
Launch the interface using Streamlit:
streamlit run src/biometric_did.py

## Application Execution Flow
1. **Initialization Standby Screen:** Upon launching, click "Initialize Biometric AI Core" to boot TensorFlow, Keras-FaceNet, and the dataset into session state memory.
2. **Control Panel Selection:** Select a Transaction ID index and target User Gender from the sidebar control panel.
3. **Risk Score Evaluation:**
   - Low Risk ($T_{risk} < 0.30$): Displays a "LOW RISK: Transaction Pre-Approved" banner and bypasses biometric challenges.
   - High Risk ($T_{risk} \ge 0.30$): Displays a "HIGH RISK" warning and triggers the step-up "AI Facial Verification" challenge.
4. **Biometric Scan & Verification:** Capture a face photo via camera input and click "Run AI Verification".
5. **Token Generation:** If spatial distance $D_{cosine} < 0.60$, identity is confirmed, and a 16-character DID authorization token is emitted.

## Thresholds & Parameters Summary
| Pipeline Stage | Parameter / Metric | Configured Value | Function |
| -------------- | ------------------ | ---------------- | -------- |
| Risk Scoring | Risk Decision Threshold ($T_{risk}$) | 0.30 | Triggers step-up biometric challenge if $T_{risk} \ge 0.30$ |
| CLAHE Normalization |	Clip Limit | 3.0 | Controls local contrast enhancement in LAB space |
| CLAHE Normalization | Tile Grid Size |	8 x 8 | Defines grid matrix size for local histogram balancing |
| Image Pre-processing | Model Input Dimensions | 160 x 160 | Resizes RGB images to FaceNet input specifications |
| Biometric Embedding | Vector Dimensionality |	512-D | Spatial feature vector extracted per facial frame |
| Identity Decision Gate | Cosine Distance Cutoff ($T_{bio}$) | 0.60 | Identity confirmed if $D_{cosine} < 0.60$ |
|DID Generation | Token Hash Format |	SHA-256 (16 chars) | Generates verifiable ephemeral session token |



          
