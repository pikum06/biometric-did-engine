use anchor_lang::prelude::*;
use groth16_solana::groth16::Groth16Verifier;

declare_id!("BioDID1111111111111111111111111111111111111");

#[program]
pub mod bio_did_verifier {
    use super::*;

    pub fn verify_zk_did(
        ctx: Context<VerifyZkDid>,
        proof_a: [u8; 64],
        proof_b: [u8; 128],
        proof_c: [u8; 64],
        public_inputs: [[u8; 32]; 2],
    ) -> Result<()> {
        // Load compiled Verifying Key generated from Noir/Barretenberg compile
        let vk = include_bytes!("../verifying_key.bin");

        let mut verifier = Groth16Verifier::new(
            &proof_a,
            &proof_b,
            &proof_c,
            &public_inputs,
            vk,
        ).map_err(|_| ErrorCode::InvalidProof)?;

        verifier.verify().map_err(|_| ErrorCode::ProofVerificationFailed)?;
        
        msg!("zk-SNARK Attestation Validated On-Chain.");
        Ok(())
    }
}

#[derive(Accounts)]
pub struct VerifyZkDid<'info> {
    #[account(mut)]
    pub verifier: Signer<'info>,
}

#[error_code]
pub enum ErrorCode {
    #[msg("Invalid Groth16 Proof Format")]
    InvalidProof,
    #[msg("Proof Verification Failed")]
    ProofVerificationFailed,
}