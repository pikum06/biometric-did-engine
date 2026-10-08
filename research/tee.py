# Building the Hard bound HMAC-SHA26 for biometric salting and cross chain key derivation

#importing libraries
import hashlib
import hmac

def tee_enclave_key(emb_live, device_uid ="SECURE_ENCLAVE_SILICON_7789A"):
    """
    Step 1: Hardware-Bound HMAC-SHA256 Biometric Salting
    Step 2: Deterministic Cross-Chain Key Derivation (Ed25519 & SECP256k1)
    """
    # 1. Convert 512-D FaceNet embedding vector to raw byte message
    
    bio_bytes = emb_live.tobytes()
    uid_bytes = device_uid.encode('utf-8')
    
    # 2. Step 1: HMAC-SHA256 Enclave Master Salt
    
    master_salt = hmac.new(uid_bytes, bio_bytes, hashlib.sha256).digest()
    
    # 3. Step 2: Purpose-based derivation (Solana Ed25519 vs EVM SECP256k1)
    
    solana_seed = hmac.new(master_salt, b"solana_ed25519_purpose_0", hashlib.sha256).hexdigest()
    evm_seed = hmac.new(master_salt, b"evm_secp256k1_purpose_1", hashlib.sha256).hexdigest()
    
    return {
        "master_salt_hex": master_salt.hex()[:16],
        "solana_ed25519_seed": solana_seed[:32],
        "evm_secp256k1_seed": evm_seed[:32]
    }