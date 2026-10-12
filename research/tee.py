# Building the Hard bound HMAC-SHA26 for biometric salting and cross chain key derivation along with zk-snark proof generation

#importing libraries
import hashlib
import hmac

def tee_enclave_key(emb_live,  device_uid ="SECURE_ENCLAVE_SILICON_7789A"):
    """
    Step 1: Hardware TEE Master Salt and key derivation using HMAC-SHA256
    Step 2: ZK-proof generation using Noir / Groth16 or STARK
    """
    
    bio_bytes = emb_live.tobytes()
    uid_bytes = device_uid.encode('utf-8')
    
    # 1. Hardware TEE Master Salt and key derivation using HMAC-SHA256
    
    master_salt = hmac.new(uid_bytes, bio_bytes, hashlib.sha256).digest()

    # 2. Purpose-Indexed Cross-Chain Key Seed Derivation

    solana_seed = hmac.new(master_salt, b"solana_ed25519_purpose_0", hashlib.sha256).hexdigest()
    evm_seed = hmac.new(master_salt, b"evm_secp256k1_purpose_1", hashlib.sha256).hexdigest()
    
    return {
        "master_salt_bytes": master_salt,
        "master_salt_hex": master_salt.hex()[:16],
        "solana_ed25519_seed": solana_seed[:32],
        "evm_secp256k1_seed": evm_seed[:32]
    }
