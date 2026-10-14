# 1. Solana Devnet network broadcaster helper module

#importing libraries

import requests

def solana_devnet_broadcast(did_token: str):
    """
    Queries Solana Devnet RPC for latest blockhash and generates
    a valid Base58 Devnet Program Explorer link.
    """
    devnet_url = "https://api.devnet.solana.com"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getLatestBlockhash",
        "params": [{"commitment": "finalized"}]
    }
    
    try:
        response = requests.post(devnet_url, json=payload, headers=headers, timeout=5)
        res_data = response.json()
        blockhash = res_data["result"]["value"]["blockhash"]
        
        program_id = "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr"
        explorer_url = f"https://explorer.solana.com/address/{program_id}?cluster=devnet"
        
        return {
            "status": "Success",
            "blockhash": blockhash,
            "did_token": did_token,
            "explorer_url": explorer_url
        }
    except Exception as e:
        program_url = "https://explorer.solana.com/address/MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr?cluster=devnet"
        return {
            "status": "Devnet Failed",
            "error": str(e),
            "explorer_url": program_url
        }