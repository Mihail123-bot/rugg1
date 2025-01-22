import streamlit as st
import secrets
import hashlib
from eth_account import Account

def generate_solana_keypair():
    private_key = secrets.token_bytes(32)
    public_key = hashlib.sha256(private_key).hexdigest()
    return {
        'address': public_key,
        'private_key': private_key.hex()
    }

def display_wallet_manager():
    st.markdown("<h1 style='text-align: center;'>Batch Wallet Generator 🔑</h1>", unsafe_allow_html=True)
    
    st.info("🔒 Wallet generation process is completed locally on your computer. We cannot access your mnemonic phrase or private key!", icon="🔒")
    
    st.markdown("### Blockchain for Batch Wallet Generation")
    blockchain = st.selectbox("", ["Solana"], disabled=True)
    
    st.markdown("### Number of Generated Wallet Addresses")
    num_wallets = st.number_input("", min_value=1, max_value=100, value=1)
    
    if st.button("Generate Now", use_container_width=True):
        wallets = [generate_solana_keypair() for _ in range(num_wallets)]
        
        st.markdown("### Generated Wallets 🎉")
        for i, wallet in enumerate(wallets, 1):
            st.markdown(f"""
                <div style='background-color: rgba(41, 55, 240, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
                    <h4>Wallet #{i}</h4>
                    <p><strong>Address:</strong> {wallet['address']}</p>
                    <p><strong>Private Key:</strong> {wallet['private_key']}</p>
                </div>
            """, unsafe_allow_html=True)
            
        if wallets:
            wallet_data = "\n\n".join([f"Wallet #{i+1}\nAddress: {w['address']}\nPrivate Key: {w['private_key']}" 
                                     for i, w in enumerate(wallets)])
            st.download_button(
                label="Download Wallet Info",
                data=wallet_data,
                file_name="solana_wallets.txt",
                mime="text/plain"
            )
