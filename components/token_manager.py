import streamlit as st
import pandas as pd

def display_token_manager():
    st.markdown("<h1 style='text-align: center;'>Solana Token Creator 🚀</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        token_name = st.text_input("Token Name", placeholder="Enter your token name")
        token_symbol = st.text_input("Token Symbol", placeholder="Enter token symbol")
        decimals = st.number_input("Decimals", min_value=0, max_value=9, value=9)
        supply = st.number_input("Supply", min_value=1, value=1000000)
        
        token_description = st.text_area("Token Description", placeholder="Describe your token")
        
        st.markdown("### Social Links")
        website = st.text_input("Website", placeholder="https://")
        twitter = st.text_input("Twitter", placeholder="https://twitter.com/")
        telegram = st.text_input("Telegram", placeholder="https://t.me/")
        
    with col2:
        st.markdown("### Token Logo")
        uploaded_file = st.file_uploader(
            "Click to Upload", 
            type=['png', 'gif', 'jpg', 'webp', 'jpeg'],
            help="Recommended size: 1000×1000 pixels"
        )
        
        if uploaded_file:
            st.image(uploaded_file, width=200)
            
        st.markdown("### Security Settings")
        revoke_update = st.checkbox("Revoke Update (Immutable)", 
            help="Renouncing ownership means you will not be able to modify the token metadata")
        
        revoke_freeze = st.checkbox("Revoke Freeze", 
            help="Revoking Freeze Authority removes control over specific account actions")
        
        revoke_mint = st.checkbox("Revoke Mint", 
            help="Relinquishing minting rights prevents further token supply creation")

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Create Token", use_container_width=True):
            with st.spinner("Creating your token..."):
                # Token creation logic here
                st.success(f"Token {token_symbol} created successfully! 🎉")
                st.info("Service fee: 0.1 SOL")

# Add this CSS for better styling
def token_manager_css():
    st.markdown("""
        <style>
        .stButton>button {
            background: linear-gradient(45deg, #2937f0, #9f1ae2);
            color: white;
            height: 60px;
            font-size: 20px;
        }
        .uploadedFile {
            border: 2px dashed #9f1ae2;
            border-radius: 10px;
            padding: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
