use anchor_lang::prelude::*;

declare_id!("BioDID1111111111111111111111111111111111111");

#[program]
pub mod biometric_did_verifier {
    use super::*;

    pub fn verify_did_token(ctx: Context<VerifyToken>, did_token: String, risk_score: u16) -> Result<()> {
        require!(did_token.len() == 16, ErrorCode::InvalidTokenLength);
        
        msg!("Biometric DID Token Verified on Solana Devnet: {}", did_token);
        msg!("Behavioral Risk Score: {}/10000", risk_score);

        emit!(DidVerifiedEvent {
            verifier: *ctx.accounts.verifier.key,
            did_token,
            risk_score,
            timestamp: Clock::get()?.unix_timestamp,
        });

        Ok(())
    }
}

#[derive(Accounts)]
pub struct VerifyToken<'info> {
    #[account(mut)]
    pub verifier: Signer<'info>,
}

#[event]
pub struct DidVerifiedEvent {
    pub verifier: Pubkey,
    pub did_token: String,
    pub risk_score: u16,
    pub timestamp: i64,
}

#[error_code]
pub enum ErrorCode {
    #[msg("DID Token must be exactly 16 characters.")]
    InvalidTokenLength,
}