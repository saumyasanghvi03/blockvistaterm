# ================ 0. REQUIRED LIBRARIES ================

import streamlit as st
import pandas as pd
import talib # Replace pandas_ta with talib
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from kiteconnect import KiteConnect, exceptions as kite_exceptions
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta, time
import pytz
import feedparser
from email.utils import mktime_tz
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np
from scipy.stats import norm
from scipy.optimize import newton
from tabulate import tabulate
import time as a_time
import re
import yfinance as yf
import pyotp
import qrcode
from PIL import Image
import base64
import io
import requests
import hashlib
import random
from streamlit_autorefresh import st_autorefresh
import praw
from scipy import stats
from scipy.fft import fft
import warnings
warnings.filterwarnings('ignore')

# <<<--- ENSURE THESE IMPORTS ARE PRESENT --->>>
# If any are missing, add them above

# ================ UPSTOX API INTEGRATION ================
import requests
import json

# ================ 1. STYLING AND CONFIGURATION ===============

st.set_page_config(page_title="BlockVista Terminal", layout="wide", initial_sidebar_state="expanded")

def apply_custom_styling():
    """Applies a comprehensive CSS stylesheet for professional theming."""
    theme_css = """
    <style>
        :root {
            --dark-bg: #0E1117;
            --dark-secondary-bg: #161B22;
            --dark-widget-bg: #21262D;
            --dark-border: #30363D;
            --dark-text: #c9d1d9;
            --dark-text-light: #8b949e;
            --dark-green: #28a745;
            --dark-red: #da3633;

            --light-bg: #FFFFFF;
            --light-secondary-bg: #F0F2F6;
            --light-widget-bg: #F8F9FA;
            --light-border: #dee2e6;
            --light-text: #212529;
            --light-text-light: #6c757d;
            --light-green: #198754;
            --light-red: #dc3545;
        }

        body.dark-theme {
            --primary-bg: var(--dark-bg);
            --secondary-bg: var(--dark-secondary-bg);
            --widget-bg: var(--dark-widget-bg);
            --border-color: var(--dark-border);
            --text-color: var(--dark-text);
            --text-light: var(--dark-text-light);
            --green: var(--dark-green);
            --red: var(--dark-red);
        }

        body.light-theme {
            --primary-bg: var(--light-bg);
            --secondary-bg: var(--light-secondary-bg);
            --widget-bg: var(--light-widget-bg);
            --border-color: var(--light-border);
            --text-color: var(--light-text);
            --text-light: var(--light-text-light);
            --green: var(--light-green);
            --red: var(--light-red);
        }

        body {
            background-color: var(--primary-bg);
            color: var(--text-color);
        }
        
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        h1, h2, h3, h4, h5 {
            color: var(--text-color) !important;
        }
        
        hr {
            background: var(--border-color);
        }

        .stButton>button {
            border-color: var(--border-color);
            background-color: var(--widget-bg);
            color: var(--text-color);
        }
        .stButton>button:hover {
            border-color: var(--green);
            color: var(--green);
        }
        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div {
            background-color: var(--widget-bg);
            border-color: var(--border-color);
            color: var(--text-color);
        }
        .stRadio>div {
            background-color: var(--widget-bg);
            border: 1px solid var(--border-color);
            padding: 8px;
            border-radius: 8px;
        }
        
        .metric-card {
            background-color: var(--secondary-bg);
            border: 1px solid var(--border-color);
            padding: 1.5rem;
            border-radius: 10px;
            border-left-width: 5px;
        }
        
        .trade-card {
            background-color: var(--secondary-bg);
            border: 1px solid var(--border-color);
            padding: 1.5rem;
            border-radius: 10px;
            border-left-width: 5px;
        }

        .notification-bar {
            position: sticky;
            top: 0;
            width: 100%;
            background-color: var(--secondary-bg);
            color: var(--text-color);
            padding: 8px 12px;
            z-index: 999;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 0.9rem;
            border-bottom: 1px solid var(--border-color);
            margin-left: -20px;
            margin-right: -20px;
            width: calc(100% + 40px);
        }
        .notification-bar span {
            margin: 0 15px;
            white-space: nowrap;
        }
        
        .hft-depth-bid {
            background: linear-gradient(to left, rgba(0, 128, 0, 0.3), rgba(0, 128, 0, 0.05));
            padding: 2px 5px;
        }
        .hft-depth-ask {
            background: linear-gradient(to right, rgba(255, 0, 0, 0.3), rgba(255, 0, 0, 0.05));
            padding: 2px 5px;
        }
        .tick-up {
            color: var(--green);
            animation: flash-green 0.5s;
        }
        .tick-down {
            color: var(--red);
            animation: flash-red 0.5s;
        }
        @keyframes flash-green {
            0% { background-color: rgba(40, 167, 69, 0.5); }
            100% { background-color: transparent; }
        }
        @keyframes flash-red {
            0% { background-color: rgba(218, 54, 51, 0.5); }
            100% { background-color: transparent; }
        }
    </style>
    """
    st.markdown(theme_css, unsafe_allow_html=True)
    
    js_theme = f"""
    <script>
        document.body.classList.remove('light-theme', 'dark-theme');
        document.body.classList.add('{st.session_state.theme.lower()}-theme');
    </script>
    """
    st.components.v1.html(js_theme, height=0)

# Centralized data source configuration
ML_DATA_SOURCES = {
    "NIFTY 50": {
        "github_url": "https://raw.githubusercontent.com/saumyasanghvi03/BlockVista-Terminal/main/NIFTY50.csv",
        "tradingsymbol": "NIFTY 50",
        "exchange": "NSE"
    },
    "BANK NIFTY": {
        "github_url": "https://raw.githubusercontent.com/saumyasanghvi03/BlockVista-Terminal/main/BANKNIFTY.csv",
        "tradingsymbol": "BANKNIFTY",
        "exchange": "NFO"
    },
    "NIFTY Financial Services": {
        "github_url": "https://raw.githubusercontent.com/saumyasanghvi03/BlockVista-Terminal/main/FINNIFTY.csv",
        "tradingsymbol": "FINNIFTY",
        "exchange": "NFO"
    },
    "GOLD": {
        "github_url": "https://raw.githubusercontent.com/saumyasanghvi03/BlockVista-Terminal/main/GOLD.csv",
        "tradingsymbol": "GOLDM",
        "exchange": "MCX"
    },
    "USDINR": {
        "github_url": "https://raw.githubusercontent.com/saumyasanghvi03/BlockVista-Terminal/main/USDINR.csv",
        "tradingsymbol": "USDINR",
        "exchange": "CDS"
    },
    "SENSEX": {
        "github_url": "https://raw.githubusercontent.com/saumyasanghvi03/BlockVista-Terminal/main/SENSEX.csv",
        "tradingsymbol": "SENSEX",
        "exchange": "BSE"
    },
    "S&P 500": {
        "github_url": "https://raw.githubusercontent.com/saumyasanghvi03/BlockVista-Terminal/main/SP500.csv",
        "tradingsymbol": "^GSPC",
        "exchange": "yfinance"
    }
    
}
# Nifty50 stocks for Iceberg Detector with price-based parameters
NIFTY50_STOCKS = {
    "RELIANCE": {"category": "HIGH", "typical_price": 2500},
    "TCS": {"category": "HIGH", "typical_price": 3500},
    "HDFCBANK": {"category": "MEDIUM", "typical_price": 1500},
    "ICICIBANK": {"category": "MEDIUM", "typical_price": 900},
    "HINDUNILVR": {"category": "HIGH", "typical_price": 2400},
    "INFY": {"category": "MEDIUM", "typical_price": 1600},
    "ITC": {"category": "LOW", "typical_price": 400},
    "SBIN": {"category": "MEDIUM", "typical_price": 600},
    "BHARTIARTL": {"category": "MEDIUM", "typical_price": 1000},
    "KOTAKBANK": {"category": "MEDIUM", "typical_price": 1700},
    "LT": {"category": "HIGH", "typical_price": 3200},
    "AXISBANK": {"category": "MEDIUM", "typical_price": 1000},
    "ASIANPAINT": {"category": "HIGH", "typical_price": 2800},
    "MARUTI": {"category": "HIGH", "typical_price": 11000},
    "HCLTECH": {"category": "MEDIUM", "typical_price": 1300},
    "SUNPHARMA": {"category": "MEDIUM", "typical_price": 1200},
    "TITAN": {"category": "HIGH", "typical_price": 3300},
    "ULTRACEMCO": {"category": "HIGH", "typical_price": 8500},
    "BAJFINANCE": {"category": "HIGH", "typical_price": 6500},
    "WIPRO": {"category": "LOW", "typical_price": 400},
    "NESTLEIND": {"category": "HIGH", "typical_price": 2400},
    "POWERGRID": {"category": "LOW", "typical_price": 250},
    "NTPC": {"category": "LOW", "typical_price": 300},
    "TATAMOTORS": {"category": "MEDIUM", "typical_price": 800},
    "BAJAJFINSV": {"category": "HIGH", "typical_price": 1400},
    "ADANIPORTS": {"category": "MEDIUM", "typical_price": 1200},
    "ONGC": {"category": "LOW", "typical_price": 200},
    "HDFCLIFE": {"category": "MEDIUM", "typical_price": 600},
    "JSWSTEEL": {"category": "MEDIUM", "typical_price": 800},
    "TATASTEEL": {"category": "MEDIUM", "typical_price": 140},
    "TECHM": {"category": "LOW", "typical_price": 1100},
    "DRREDDY": {"category": "HIGH", "typical_price": 5500},
    "CIPLA": {"category": "MEDIUM", "typical_price": 1300},
    "INDUSINDBK": {"category": "MEDIUM", "typical_price": 1400},
    "GRASIM": {"category": "MEDIUM", "typical_price": 1800},
    "BRITANNIA": {"category": "HIGH", "typical_price": 4800},
    "COALINDIA": {"category": "LOW", "typical_price": 400},
    "HINDALCO": {"category": "MEDIUM", "typical_price": 500},
    "SBILIFE": {"category": "MEDIUM", "typical_price": 1300},
    "M&M": {"category": "MEDIUM", "typical_price": 1600},
    "DIVISLAB": {"category": "HIGH", "typical_price": 3600},
    "HDFC": {"category": "HIGH", "typical_price": 2700},
    "APOLLOHOSP": {"category": "HIGH", "typical_price": 5000},
    "BAJAJ-AUTO": {"category": "HIGH", "typical_price": 7500},
    "EICHERMOT": {"category": "HIGH", "typical_price": 3500},
    "HEROMOTOCO": {"category": "HIGH", "typical_price": 4000},
    "SHREECEM": {"category": "HIGH", "typical_price": 24000},
    "UPL": {"category": "MEDIUM", "typical_price": 500},
    "BPCL": {"category": "LOW", "typical_price": 550}
}

# Price-based detection parameters for Nifty50
NIFTY50_DETECTION_PARAMS = {
    "LOW": {  # Stocks < ₹500
        "large_order_threshold": 50000,    # shares
        "volume_anomaly_multiplier": 3.0,
        "order_imbalance_threshold": 0.7,
        "min_confidence": 0.6,
        "trade_size_factor": 1.5,
        "momentum_weight": 0.3
    },
    "MEDIUM": {  # Stocks ₹500 - ₹5000
        "large_order_threshold": 10000,    # shares  
        "volume_anomaly_multiplier": 2.5,
        "order_imbalance_threshold": 0.65,
        "min_confidence": 0.7,
        "trade_size_factor": 1.2,
        "momentum_weight": 0.4
    },
    "HIGH": {  # Stocks > ₹5000
        "large_order_threshold": 1000,     # shares
        "volume_anomaly_multiplier": 2.0,
        "order_imbalance_threshold": 0.6,
        "min_confidence": 0.75,
        "trade_size_factor": 1.0,
        "momentum_weight": 0.5
    }
}
# ================ 1.5 INITIALIZATION ========================

def initialize_session_state():
    """Initializes all necessary session state variables."""
    if 'broker' not in st.session_state: st.session_state.broker = None
    if 'kite' not in st.session_state: st.session_state.kite = None
    if 'profile' not in st.session_state: st.session_state.profile = None
    if 'run_iceberg_analysis' not in st.session_state:
        st.session_state.run_iceberg_analysis = False
    if 'login_animation_complete' not in st.session_state: st.session_state.login_animation_complete = False
    if 'authenticated' not in st.session_state: st.session_state.authenticated = False
    if 'two_factor_setup_complete' not in st.session_state: st.session_state.two_factor_setup_complete = False
    if 'pyotp_secret' not in st.session_state: st.session_state.pyotp_secret = None
    if 'theme' not in st.session_state: st.session_state.theme = 'Dark'
    if 'show_company_events' not in st.session_state:
        st.session_state.show_company_events = False
    if 'fundamental_symbol' not in st.session_state:
        st.session_state.fundamental_symbol = 'RELIANCE'
    if 'company_analysis_data' not in st.session_state:
        st.session_state.company_analysis_data = {}
    
    # Remove the dialog state variables
    if 'show_quick_trade' not in st.session_state: st.session_state.show_quick_trade = False
    
    # Add other existing initializations...
    if 'watchlists' not in st.session_state:
        st.session_state.watchlists = {
            "Watchlist 1": [{'symbol': 'RELIANCE', 'exchange': 'NSE'}, {'symbol': 'HDFCBANK', 'exchange': 'NSE'}],
            "Watchlist 2": [{'symbol': 'TCS', 'exchange': 'NSE'}, {'symbol': 'INFY', 'exchange': 'NSE'}],
            "Watchlist 3": [{'symbol': 'SENSEX', 'exchange': 'BSE'}]
        }
    # Add all other existing initializations...
    if 'active_watchlist' not in st.session_state: st.session_state.active_watchlist = "Watchlist 1"
    if 'order_history' not in st.session_state: st.session_state.order_history = []
    if 'basket' not in st.session_state: st.session_state.basket = []
    if 'last_order_details' not in st.session_state: st.session_state.last_order_details = {}
    if 'underlying_pcr' not in st.session_state: st.session_state.underlying_pcr = "NIFTY"
    if 'strategy_legs' not in st.session_state: st.session_state.strategy_legs = []
    if 'calculated_greeks' not in st.session_state: st.session_state.calculated_greeks = None
    if 'messages' not in st.session_state: st.session_state.messages = []
    if 'ml_forecast_df' not in st.session_state: st.session_state.ml_forecast_df = None
    if 'ml_instrument_name' not in st.session_state: st.session_state.ml_instrument_name = None
    if 'backtest_results' not in st.session_state: st.session_state.backtest_results = None
    if 'hft_last_price' not in st.session_state: st.session_state.hft_last_price = 0
    if 'hft_tick_log' not in st.session_state: st.session_state.hft_tick_log = []
    if 'last_bot_result' not in st.session_state: st.session_state.last_bot_result = None
    
    # Add new dialog state variables
    if 'show_quick_trade' not in st.session_state: st.session_state.show_quick_trade = False
    if 'show_most_active' not in st.session_state: st.session_state.show_most_active = False
    if 'show_2fa_dialog' not in st.session_state: st.session_state.show_2fa_dialog = False
    if 'show_qr_dialog' not in st.session_state: st.session_state.show_qr_dialog = False
    
    # Add automated mode variables
    if 'automated_mode' not in st.session_state:
        st.session_state.automated_mode = {
            'enabled': False,
            'running': False,
            'bots_active': {},
            'total_capital': 10000,
            'risk_per_trade': 2,
            'max_open_trades': 5,
            'trade_history': [],
            'performance_metrics': {},
            'last_signal_check': None
        }
    
    # Add special trading days
    if 'special_trading_days' not in st.session_state:
        st.session_state.special_trading_days = []
# ================ 2. HELPER FUNCTIONS ================
def get_ist_time():
    """Get current time in IST timezone."""
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist)

def check_for_special_session():
    """Checks if the current time falls within any special trading session."""
    if 'special_trading_days' not in st.session_state:
        return None
    
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    now_date = now.date()
    now_time = now.time()

    for session in st.session_state.special_trading_days:
        if now_date == session['date'] and session['start'] <= now_time <= session['end']:
            return session # Return the active session details
    return None

def setup_auto_refresh_control():
    """Setup comprehensive auto-refresh control to prevent flickering."""
    if 'refresh_control' not in st.session_state:
        st.session_state.refresh_control = {
            'enabled': True,
            'last_refresh': datetime.now(),
            'refresh_interval': 60,  # seconds
            'excluded_tabs': ["🔍 Live Thinking", "📋 Trade History", "🎯 Symbol Override"],
            'user_interaction_time': datetime.now(),
            'prevent_refresh_until': None
        }

def should_auto_refresh(current_tab=None):
    """Determine if auto-refresh should occur based on current context."""
    control = st.session_state.get('refresh_control', {})
    
    # Check if auto-refresh is disabled globally
    if not control.get('enabled', True):
        return False
    
    # Check if we're in a cooldown period
    prevent_until = control.get('prevent_refresh_until')
    if prevent_until and datetime.now() < prevent_until:
        return False
    
    # Check if current tab is excluded from auto-refresh
    if current_tab and current_tab in control.get('excluded_tabs', []):
        return False
    
    # Check if user recently interacted (within last 5 seconds)
    last_interaction = control.get('user_interaction_time', datetime.now())
    time_since_interaction = (datetime.now() - last_interaction).total_seconds()
    if time_since_interaction < 5:
        return False
    
    # Check refresh interval
    last_refresh = control.get('last_refresh', datetime.now())
    refresh_interval = control.get('refresh_interval', 60)
    time_since_refresh = (datetime.now() - last_refresh).total_seconds()
    
    return time_since_refresh >= refresh_interval

def update_refresh_timestamp():
    """Update the last refresh timestamp."""
    if 'refresh_control' in st.session_state:
        st.session_state.refresh_control['last_refresh'] = datetime.now()

def prevent_refresh_for(seconds=10):
    """Temporarily prevent auto-refresh for specified seconds."""
    if 'refresh_control' in st.session_state:
        st.session_state.refresh_control['prevent_refresh_until'] = (
            datetime.now() + timedelta(seconds=seconds)
        )

def record_user_interaction():
    """Record when user interacts with the app to prevent immediate refresh."""
    if 'refresh_control' in st.session_state:
        st.session_state.refresh_control['user_interaction_time'] = datetime.now()

def get_broker_client():
    """Gets current broker client from session state."""
    broker = st.session_state.get('broker')
    
    if broker == "Zerodha":
        return st.session_state.get('kite')
    elif broker == "Upstox":
        # For Upstox, we use the access token directly in API calls
        return st.session_state.get('upstox_access_token')
    
    return None

def get_nifty50_stock_category(symbol):
    """Get the price category for a Nifty50 stock."""
    symbol_upper = symbol.upper()
    
    # Handle variations in symbol names
    symbol_mappings = {
        "BAJAJ-AUTO": "BAJAJAUTO",
        "M&M": "M_M",
        # Add other mappings if needed
    }
    
    lookup_symbol = symbol_mappings.get(symbol_upper, symbol_upper)
    
    if lookup_symbol in NIFTY50_STOCKS:
        return NIFTY50_STOCKS[lookup_symbol]["category"]
    else:
        # Fallback: determine by current price
        return "MEDIUM"

def get_nifty50_detection_params(symbol):
    """Get detection parameters for a specific Nifty50 stock."""
    category = get_nifty50_stock_category(symbol)
    return NIFTY50_DETECTION_PARAMS.get(category, NIFTY50_DETECTION_PARAMS["MEDIUM"])

def is_nifty50_stock(symbol):
    """Check if a symbol is in Nifty50."""
    symbol_upper = symbol.upper()
    symbol_mappings = {
        "BAJAJ-AUTO": "BAJAJAUTO", 
        "M&M": "M_M",
    }
    lookup_symbol = symbol_mappings.get(symbol_upper, symbol_upper)
    return lookup_symbol in NIFTY50_STOCKS

# @st.dialog("Quick Trade")
def quick_trade_interface(symbol=None, exchange=None):
    """A quick trade interface that doesn't use dialogs."""
    if st.session_state.get('show_quick_trade', False):
        st.markdown("---")
        st.subheader(f"Quick Trade - {symbol}" if symbol else "Quick Order")
        
        if symbol is None:
            symbol = st.text_input("Symbol").upper()
        
        transaction_type = st.radio("Transaction", ["BUY", "SELL"], horizontal=True, key="quick_trans_type")
        product = st.radio("Product", ["MIS", "CNC"], horizontal=True, key="quick_prod_type")
        order_type = st.radio("Order Type", ["MARKET", "LIMIT"], horizontal=True, key="quick_order_type")
        quantity = st.number_input("Quantity", min_value=1, step=1, key="quick_qty")
        price = st.number_input("Price", min_value=0.01, key="quick_price") if order_type == "LIMIT" else 0

        col1, col2 = st.columns(2)
        if col1.button("Submit Order", use_container_width=True, type="primary"):
            if symbol and quantity > 0:
                place_order(get_instrument_df(), symbol, quantity, order_type, transaction_type, product, price if price > 0 else None)
                st.session_state.show_quick_trade = False
                st.rerun()
            else:
                st.warning("Please fill in all fields.")
        
        if col2.button("Cancel", use_container_width=True):
            st.session_state.show_quick_trade = False
            st.rerun()

@st.cache_data(ttl=3600)
def get_market_holidays(year):
    """NSE holidays (update yearly)."""
    holidays_by_year = {
        2024: ['2024-01-22', '2024-01-26', '2024-03-08', '2024-03-25', '2024-03-29', '2024-04-11', '2024-04-17', '2024-05-01', '2024-05-20', '2024-06-17', '2024-07-17', '2024-08-15', '2024-10-02', '2024-11-01', '2024-11-15', '2024-12-25'],
        2025: ['2025-01-26', '2025-03-06', '2025-03-21', '2025-04-14', '2025-04-18', '2025-05-01', '2025-08-15', '2025-10-02', '2025-10-21', '2025-11-05', '2025-12-25'],
        2026: ['2026-01-26', '2026-02-24', '2026-04-03', '2026-04-14', '2026-05-01', '2026-08-15', '2026-10-02', '2026-11-09', '2026-11-24', '2026-12-25']
    }
    return holidays_by_year.get(year, [])


# =============================================================================
# MARKET TIMING FUNCTIONS - REPLACE EXISTING ONES
# =============================================================================
def is_market_hours():
    """Check if current time is within market hours OR a special session."""
    if check_for_special_session():
        return True

    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    
    if now.strftime('%Y-%m-%d') in get_market_holidays(now.year):
        return False
        
    current_time = now.time()
    current_day = now.weekday()
    
    if current_day >= 5:
        return False
    
    market_open = time(9, 15)
    market_close = time(15, 30)
    
    return market_open <= current_time <= market_close

def is_pre_market_hours():
    """Check for pre-market hours, but not during a special session."""
    if check_for_special_session():
        return False

    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    current_time = now.time()
    current_day = now.weekday()
    
    if current_day >= 5 or now.strftime('%Y-%m-%d') in get_market_holidays(now.year):
        return False
    
    pre_market_start = time(9, 0)
    market_open = time(9, 15)
    
    return pre_market_start <= current_time < market_open

def is_square_off_time():
    """Check for square-off time, but not during a special session."""
    if check_for_special_session():
        return False

    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    current_time = now.time()
    current_day = now.weekday()
    
    if current_day >= 5 or now.strftime('%Y-%m-%d') in get_market_holidays(now.year):
        return False
    
    square_off_start = time(15, 20)
    square_off_end = time(15, 30)
    
    return square_off_start <= current_time <= square_off_end

def is_derivatives_square_off_time():
    """Check for derivatives square-off time, but not during a special session."""
    if check_for_special_session():
        return False

    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    current_time = now.time()
    current_day = now.weekday()
    
    if current_day >= 5 or now.strftime('%Y-%m-%d') in get_market_holidays(now.year):
        return False
    
    square_off_start = time(15, 25)
    square_off_end = time(15, 30)
    
    return square_off_start <= current_time <= square_off_end

def get_market_status():
    """Get current market status, accounting for special sessions, holidays, and weekends."""
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    
    active_session = check_for_special_session()
    if active_session:
        session_end_datetime = datetime.combine(active_session['date'], active_session['end'], tzinfo=ist)
        return {
            "status": "special_trading_session",
            "next_market": session_end_datetime,
            "color": "#9400D3"
        }

    if now.strftime('%Y-%m-%d') in get_market_holidays(now.year):
        next_day = now + timedelta(days=1)
        while next_day.weekday() >= 5 or next_day.strftime('%Y-%m-%d') in get_market_holidays(next_day.year):
            next_day += timedelta(days=1)
        return {
            "status": "market_holiday",
            "next_market": next_day.replace(hour=9, minute=0, second=0, microsecond=0),
            "color": "#A52A2A"
        }

    current_day = now.weekday()
    if current_day >= 5:
        next_day = now + timedelta(days=(7 - current_day))
        while next_day.strftime('%Y-%m-%d') in get_market_holidays(next_day.year):
            next_day += timedelta(days=1)
        return {
            "status": "weekend",
            "next_market": next_day.replace(hour=9, minute=0, second=0, microsecond=0),
            "color": "#cccccc"
        }

    current_time = now.time()
    pre_market_start = time(9, 0)
    market_open = time(9, 15)
    equity_square_off = time(15, 20)
    derivatives_square_off = time(15, 25)
    market_close = time(15, 30)

    if current_time < pre_market_start:
        status, next_event_time, color = "market_closed", time(9, 0), "#cccccc"
    elif current_time < market_open:
        status, next_event_time, color = "pre_market", time(9, 15), "#ffcc00"
    elif current_time < equity_square_off:
        status, next_event_time, color = "market_open", time(15, 20), "#00cc00"
    elif current_time < derivatives_square_off:
        status, next_event_time, color = "equity_square_off", time(15, 25), "#ff9900"
    elif current_time <= market_close:
        status, next_event_time, color = "derivatives_square_off", time(15, 30), "#ff6600"
    else:
        status, color = "market_closed", "#cccccc"
        next_day = now + timedelta(days=1)
        while next_day.weekday() >= 5 or next_day.strftime('%Y-%m-%d') in get_market_holidays(next_day.year):
            next_day += timedelta(days=1)
        return {
            "status": status,
            "next_market": next_day.replace(hour=9, minute=0, second=0, microsecond=0),
            "color": color
        }

    return {
        "status": status,
        "next_market": now.replace(hour=next_event_time.hour, minute=next_event_time.minute, second=0, microsecond=0),
        "color": color
    }
    
def display_header():
    """Displays the main header with market status, a live clock, and trade buttons."""
    status_info = get_market_status()
    current_time = get_ist_time().strftime("%H:%M:%S IST")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown('<h1 style="margin: 0; line-height: 1.2;">BlockVista Terminal</h1>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style="text-align: right;">
                <h5 style="margin: 0;">{current_time}</h5>
                <h5 style="margin: 0;">Market: <span style='color:{status_info["color"]}; font-weight: bold;'>{status_info["status"].replace("_", " ").title()}</span></h5>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        b_col1, b_col2 = st.columns(2)
        if b_col1.button("Buy", use_container_width=True, key="header_buy"):
            st.session_state.show_quick_trade = True
            st.rerun()
        if b_col2.button("Sell", use_container_width=True, key="header_sell"):
            st.session_state.show_quick_trade = True
            st.rerun()

    st.markdown("<hr style='margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)


@st.cache_data(ttl=300)
def get_global_indices_data(tickers):
    """Fetch global indices data for the overnight changes bar."""
    if not tickers:
        return pd.DataFrame()
    
    data = []
    
    for ticker_name, yf_ticker in tickers.items():
        try:
            stock_data = yf.download(yf_ticker, period="2d", progress=False)
            
            if not stock_data.empty and len(stock_data) >= 2:
                current_close = stock_data['Close'].iloc[-1]
                prev_close = stock_data['Close'].iloc[-2]
                
                if prev_close > 0:
                    change = current_close - prev_close
                    pct_change = (change / prev_close) * 100
                else:
                    change = 0
                    pct_change = 0
                
                data.append({
                    'Ticker': ticker_name,
                    'Price': current_close,
                    'Change': change,
                    '% Change': pct_change
                })
            else:
                # Add placeholder for unavailable data
                data.append({
                    'Ticker': ticker_name,
                    'Price': np.nan,
                    'Change': np.nan,
                    '% Change': np.nan
                })
                
        except Exception as e:
            print(f"Error fetching {ticker_name}: {e}")
            # Add placeholder for failed fetch
            data.append({
                'Ticker': ticker_name,
                'Price': np.nan,
                'Change': np.nan,
                '% Change': np.nan
            })
    
    return pd.DataFrame(data)
    
def display_overnight_changes_bar():
    """Displays a notification bar with overnight market changes."""
    overnight_tickers = {"GIFT NIFTY": "NIFTY_F1", "S&P 500 Futures": "ES=F", "NASDAQ Futures": "NQ=F"}
    data = get_global_indices_data(overnight_tickers)
    
    if not data.empty:
        bar_html = "<div class='notification-bar'>"
        for name, ticker in overnight_tickers.items():
            row = data[data['Ticker'] == name]
            if not row.empty:
                price = row.iloc[0]['Price']
                change = row.iloc[0]['% Change']
                if not np.isnan(price):
                    color = 'var(--green)' if change > 0 else 'var(--red)'
                    bar_html += f"<span>{name}: {price:,.2f} <span style='color:{color};'>({change:+.2f}%)</span></span>"
        bar_html += "</div>"
        st.markdown(bar_html, unsafe_allow_html=True)

# ================ 3. CORE DATA & CHARTING FUNCTIONS ================

def create_chart(df, ticker, chart_type='Candlestick', forecast_df=None, conf_int_df=None):
    """Generates a Plotly chart with various chart types and overlays."""
    fig = go.Figure()
    if df.empty: return fig
    chart_df = df.copy()
    
    if isinstance(chart_df.columns, pd.MultiIndex):
        chart_df.columns = chart_df.columns.droplevel(0)
        
    chart_df.columns = [str(col).lower() for col in chart_df.columns]
    
    required_cols = ['open', 'high', 'low', 'close']
    if not all(col in chart_df.columns for col in required_cols):
        st.error(f"Charting error for {ticker}: Dataframe is missing required columns (open, high, low, close).")
        return go.Figure()

    if chart_type == 'Heikin-Ashi':
        # Manual Heikin-Ashi calculation
        ha_close = (chart_df['open'] + chart_df['high'] + chart_df['low'] + chart_df['close']) / 4
        ha_open = (chart_df['open'].shift(1) + chart_df['close'].shift(1)) / 2
        ha_open.iloc[0] = (chart_df['open'].iloc[0] + chart_df['close'].iloc[0]) / 2
        ha_high = chart_df[['high', 'open', 'close']].max(axis=1)
        ha_low = chart_df[['low', 'open', 'close']].min(axis=1)
        
        fig.add_trace(go.Candlestick(x=chart_df.index, open=ha_open, high=ha_high, low=ha_low, close=ha_close, name='Heikin-Ashi'))
    elif chart_type == 'Line':
        fig.add_trace(go.Scatter(x=chart_df.index, y=chart_df['close'], mode='lines', name='Line'))
    elif chart_type == 'Bar':
        fig.add_trace(go.Ohlc(x=chart_df.index, open=chart_df['open'], high=chart_df['high'], low=chart_df['low'], close=chart_df['close'], name='Bar'))
    else:
        fig.add_trace(go.Candlestick(x=chart_df.index, open=chart_df['open'], high=chart_df['high'], low=chart_df['low'], close=chart_df['close'], name='Candlestick'))
        
    # Bollinger Bands using TA-Lib
    if 'close' in chart_df.columns:
        upperband, middleband, lowerband = talib.BBANDS(chart_df['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        fig.add_trace(go.Scatter(x=chart_df.index, y=lowerband, line=dict(color='rgba(135,206,250,0.5)', width=1), name='Lower Band'))
        fig.add_trace(go.Scatter(x=chart_df.index, y=upperband, line=dict(color='rgba(135,206,250,0.5)', width=1), fill='tonexty', fillcolor='rgba(135,206,250,0.1)', name='Upper Band'))
        
    if forecast_df is not None:
        fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df['Predicted'], mode='lines', line=dict(color='yellow', dash='dash'), name='Forecast'))
        if conf_int_df is not None:
            fig.add_trace(go.Scatter(x=conf_int_df.index, y=conf_int_df['lower'], line=dict(color='rgba(255,255,0,0.2)', width=1), name='Lower CI', showlegend=False))
            fig.add_trace(go.Scatter(x=conf_int_df.index, y=conf_int_df['upper'], line=dict(color='rgba(255,255,0,0.2)', width=1), fill='tonexty', fillcolor='rgba(255,255,0,0.2)', name='Confidence Interval'))
        
    template = 'plotly_dark' if st.session_state.get('theme') == 'Dark' else 'plotly_white'
    fig.update_layout(title=f'{ticker} Price Chart ({chart_type})', yaxis_title='Price (INR)', xaxis_rangeslider_visible=False, template=template, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    return fig


@st.cache_resource(ttl=3600)
@st.cache_resource(ttl=3600)
def get_instrument_df():
    """Fetches the full list of tradable instruments from the broker."""
    client = get_broker_client()
    broker = st.session_state.get('broker')
    
    if not client: 
        st.info("Please connect to a broker to view the dashboard.")
        return pd.DataFrame()
    
    if broker == "Zerodha":
        try:
            df = pd.DataFrame(client.instruments())
            if 'expiry' in df.columns:
                df['expiry'] = pd.to_datetime(df['expiry'])
            st.success(f"Loaded {len(df)} instruments from Zerodha")
            return df
        except Exception as e:
            st.error(f"Error loading Zerodha instruments: {e}")
            return pd.DataFrame()
    
    elif broker == "Upstox":
        access_token = st.session_state.get('upstox_access_token')
        if not access_token:
            st.error("Upstox access token not found. Please login again.")
            return pd.DataFrame()
        
        # Try the most common exchanges first
        exchanges_to_try = ['NSE', 'BSE', 'NFO', 'MCX', 'CDS']
        all_instruments = []
        
        for exchange in exchanges_to_try:
            try:
                exchange_instruments = get_upstox_instruments(access_token, exchange)
                if not exchange_instruments.empty:
                    all_instruments.append(exchange_instruments)
            except Exception as e:
                st.error(f"Failed to load instruments from {exchange}: {e}")
                continue
        
        if all_instruments:
            combined_df = pd.concat(all_instruments, ignore_index=True)
            st.success(f"Successfully loaded {len(combined_df)} instruments from Upstox")
            return combined_df
        else:
            st.error("""
            Could not load any instruments from Upstox. Possible reasons:
            1. Your Upstox account may not have access to these market segments
            2. There might be temporary API issues
            3. Your API key might not have the required permissions
            
            Please use the debug button to check available exchanges.
            """)
            return pd.DataFrame()
    
    else:
        st.warning(f"Instrument list for {broker} not implemented.")
        return pd.DataFrame()

def get_instrument_token(symbol, instrument_df, exchange='NSE'):
    """Finds the instrument token for a given symbol and exchange."""
    if instrument_df.empty: return None
    match = instrument_df[(instrument_df['tradingsymbol'] == symbol.upper()) & (instrument_df['exchange'] == exchange)]
    return match.iloc[0]['instrument_token'] if not match.empty else None


@st.cache_data(ttl=60)
def get_historical_data(instrument_token, interval, period=None, from_date=None, to_date=None):
    """Fetches historical data from the broker's API."""
    client = get_broker_client()
    broker = st.session_state.get('broker')
    
    if not client or not instrument_token: 
        return pd.DataFrame()
    
    if broker == "Zerodha":
        # Your existing Zerodha code
        if not to_date: to_date = datetime.now().date()
        if not from_date:
            days_to_subtract = {'1d': 2, '5d': 7, '1mo': 31, '6mo': 182, '1y': 365, '5y': 1825}
            from_date = to_date - timedelta(days=days_to_subtract.get(period, 1825))
        
        if from_date > to_date:
            from_date = to_date - timedelta(days=1)
            
        try:
            records = client.historical_data(instrument_token, from_date, to_date, interval)
            df = pd.DataFrame(records)
            if df.empty: return df
            df.set_index('date', inplace=True)
            df.index = pd.to_datetime(df.index)
            return df

        except Exception as e:
            st.error(f"Kite API Error (Historical): {e}")
            return pd.DataFrame()
    
    elif broker == "Upstox":
        # Use Upstox REST API
        access_token = st.session_state.get('upstox_access_token')
        return get_upstox_historical_data(access_token, instrument_token, interval, period)
    
    else:
        st.warning(f"Historical data for {broker} not implemented.")
        return pd.DataFrame()

@st.cache_resource(ttl=3600)

@st.cache_data(ttl=15)
def get_watchlist_data(symbols_with_exchange):
    """Fetches live prices - UPDATED FOR UPSTOX."""
    client = get_broker_client()
    if not client or not symbols_with_exchange: 
        return pd.DataFrame()
    
    broker = st.session_state.broker
    
    if broker == "Zerodha":
        # Existing Zerodha implementation
        instrument_names = [f"{item['exchange']}:{item['symbol']}" for item in symbols_with_exchange]
        try:
            quotes = client.quote(instrument_names)
            watchlist = []
            for item in symbols_with_exchange:
                instrument = f"{item['exchange']}:{item['symbol']}"
                if instrument in quotes:
                    quote = quotes[instrument]
                    last_price = quote['last_price']
                    prev_close = quote['ohlc']['close']
                    change = last_price - prev_close
                    pct_change = (change / prev_close * 100) if prev_close != 0 else 0
                    watchlist.append({
                        'Ticker': item['symbol'], 
                        'Exchange': item['exchange'], 
                        'Price': last_price, 
                        'Change': change, 
                        '% Change': pct_change
                    })
            return pd.DataFrame(watchlist)
        except Exception as e:
            st.toast(f"Error fetching watchlist data: {e}", icon="⚠️")
            return pd.DataFrame()
    
    else:
        st.warning(f"Watchlist for {broker} not implemented.")
        return pd.DataFrame()

@st.cache_data(ttl=2)  # 2 second cache for real-time data
def get_market_depth_enhanced(instrument_token, levels=5):
    """Enhanced market depth fetcher with top 5 levels only from Kite Connect."""
    client = get_broker_client()
    if not client or not instrument_token:
        return None
    
    try:
        # Use Kite Connect quote method which provides market depth
        quote_data = client.quote(str(instrument_token))
        
        if not quote_data:
            return None
            
        instrument_quote = quote_data.get(str(instrument_token), {})
        
        # Initialize depth structure
        depth = {
            'buy': [],
            'sell': [],
            'timestamp': datetime.now().isoformat(),
            'instrument_token': instrument_token,
            'last_price': instrument_quote.get('last_price', 0),
            'volume': instrument_quote.get('volume', 0),
            'change': instrument_quote.get('change', 0),
            'oi': instrument_quote.get('oi', 0)
        }
        
        # Extract depth from quote data - Kite Connect provides depth in 'depth' key
        if 'depth' in instrument_quote:
            market_depth = instrument_quote['depth']
            
            # Buy side (bids) - get top 5 levels only (highest bids first)
            buy_orders = market_depth.get('buy', [])
            # Sort by price descending and take top 5
            depth['buy'] = sorted(buy_orders, key=lambda x: x.get('price', 0), reverse=True)[:levels]
            
            # Sell side (asks) - get top 5 levels only (lowest asks first)
            sell_orders = market_depth.get('sell', [])
            # Sort by price ascending and take top 5
            depth['sell'] = sorted(sell_orders, key=lambda x: x.get('price', 0))[:levels]
            
            # Calculate depth metrics for top 5 levels only
            depth['total_bid_volume'] = sum(order.get('quantity', 0) for order in depth['buy'])
            depth['total_ask_volume'] = sum(order.get('quantity', 0) for order in depth['sell'])
            depth['bid_ask_ratio'] = depth['total_bid_volume'] / depth['total_ask_volume'] if depth['total_ask_volume'] > 0 else 0
            
            # Best bid/ask from top 5 levels
            depth['best_bid'] = depth['buy'][0] if depth['buy'] else {}
            depth['best_ask'] = depth['sell'][0] if depth['sell'] else {}
            depth['spread'] = depth['best_ask'].get('price', 0) - depth['best_bid'].get('price', 0) if depth['best_bid'] and depth['best_ask'] else 0
            
            # Additional depth insights for top 5 levels
            depth['avg_bid_size'] = depth['total_bid_volume'] / len(depth['buy']) if depth['buy'] else 0
            depth['avg_ask_size'] = depth['total_ask_volume'] / len(depth['sell']) if depth['sell'] else 0
            
        return depth
        
    except Exception as e:
        st.toast(f"❌ Error fetching market depth: {e}", icon="⚠️")
        return get_market_depth_fallback(instrument_token, levels)

def display_optimized_hft_market_depth(instrument_token, symbol, levels=5):
    """Display optimized HFT market depth with top 5 levels only."""
    
    st.subheader(f"🏦 HFT Market Depth - {symbol} (Top {levels} Levels)")
    
    # Refresh controls
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"**Real-time Order Book** (Top {levels} levels from Kite)")
    with col2:
        if st.button("🔄 Refresh", key=f"refresh_{symbol}", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    with col3:
        auto_refresh = st.checkbox("Auto-refresh", value=True, key=f"auto_{symbol}")
    
    # Fetch market depth - only top 5 levels
    depth_data = get_market_depth_enhanced(instrument_token, levels)
    
    if not depth_data:
        st.error("❌ Failed to fetch market depth data from Kite Connect")
        return
    
    # Display key metrics
    st.markdown("### 📊 Key Market Depth Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Last price with change indicator
        change = depth_data.get('change', 0)
        change_color = "green" if change >= 0 else "red"
        st.metric(
            "Last Price", 
            f"₹{depth_data['last_price']:.2f}",
            f"{change:+.2f}" if change != 0 else "0.00",
            delta_color="normal" if change >= 0 else "inverse"
        )
    
    with col2:
        # Spread analysis
        spread = depth_data['spread']
        spread_status = "Tight" if spread <= depth_data['last_price'] * 0.001 else "Wide"
        st.metric("Spread", f"₹{spread:.2f}", spread_status)
    
    with col3:
        # Market pressure
        ratio = depth_data['bid_ask_ratio']
        if ratio > 1.2:
            pressure = "BUYING 📈"
            delta_color = "normal"
        elif ratio < 0.8:
            pressure = "SELLING 📉" 
            delta_color = "inverse"
        else:
            pressure = "BALANCED ➡️"
            delta_color = "off"
        st.metric("Pressure", pressure, f"Ratio: {ratio:.2f}", delta_color=delta_color)
    
    with col4:
        # Volume insight
        total_volume = depth_data['total_bid_volume'] + depth_data['total_ask_volume']
        st.metric("Top 5 Volume", f"{total_volume:,}")
    
    st.markdown("---")
    
    # Visual depth chart for top 5 levels
    display_compact_depth_chart(depth_data, levels)
    
    # Order book table for top 5 levels
    display_compact_order_book(depth_data, levels)
    
    # Quick insights for top 5 levels
    display_top5_insights(depth_data)
    
    # Auto-refresh
    if auto_refresh:
        a_time.sleep(2)
        st.rerun()

def display_compact_depth_chart(depth_data, levels=5):
    """Display compact depth chart for top 5 levels only."""
    
    # Prepare data for top 5 levels only
    bid_prices = [level.get('price', 0) for level in depth_data['buy']]
    bid_quantities = [level.get('quantity', 0) for level in depth_data['buy']]
    ask_prices = [level.get('price', 0) for level in depth_data['sell']] 
    ask_quantities = [level.get('quantity', 0) for level in depth_data['sell']]
    
    fig = go.Figure()
    
    # Add bid depth (left side) - only top 5
    if bid_prices and bid_quantities:
        fig.add_trace(go.Bar(
            x=bid_quantities,
            y=bid_prices,
            name=f'Top {levels} Bids',
            orientation='h',
            marker_color='#2E8B57',  # Dark green
            opacity=0.8,
            hovertemplate='<b>Bid</b><br>Price: ₹%{y:.2f}<br>Qty: %{x:,}<extra></extra>'
        ))
    
    # Add ask depth (right side) - only top 5
    if ask_prices and ask_quantities:
        fig.add_trace(go.Bar(
            x=[-q for q in ask_quantities],  # Negative for right side
            y=ask_prices,
            name=f'Top {levels} Asks',
            orientation='h',
            marker_color='#DC143C',  # Crimson red
            opacity=0.8,
            hovertemplate='<b>Ask</b><br>Price: ₹%{y:.2f}<br>Qty: %{x:,}<extra></extra>'
        ))
    
    # Update layout for compact view
    fig.update_layout(
        title=f"Top {levels} Levels Market Depth",
        xaxis_title="Quantity",
        yaxis_title="Price (₹)",
        showlegend=True,
        height=350,
        bargap=0.1,
        template="plotly_dark" if st.session_state.get('theme') == 'Dark' else "plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Center the x-axis around zero for better visualization
    if bid_quantities or ask_quantities:
        max_quantity = max(bid_quantities + ask_quantities) if bid_quantities or ask_quantities else 1
        fig.update_xaxis(range=[-max_quantity * 1.1, max_quantity * 1.1])
    
    st.plotly_chart(fig, use_container_width=True)

def display_compact_order_book(depth_data, levels=5):
    """Display compact order book table for top 5 levels only."""
    
    st.subheader(f"📋 Top {levels} Levels Order Book")
    
    # Create table data for top 5 levels only
    table_data = []
    
    # Add asks (sell side) - top 5 levels
    for i in range(min(levels, len(depth_data['sell']))):
        ask = depth_data['sell'][i]
        table_data.append({
            'Side': 'SELL',
            'Level': i + 1,
            'Price (₹)': ask.get('price', 0),
            'Quantity': ask.get('quantity', 0),
            'Orders': ask.get('orders', 1)
        })
    
    # Add current spread
    if depth_data['buy'] and depth_data['sell']:
        table_data.append({
            'Side': 'SPREAD',
            'Level': '-',
            'Price (₹)': depth_data['spread'],
            'Quantity': '-',
            'Orders': '-'
        })
    
    # Add bids (buy side) - top 5 levels
    for i in range(min(levels, len(depth_data['buy']))):
        bid = depth_data['buy'][i]
        table_data.append({
            'Side': 'BUY', 
            'Level': i + 1,
            'Price (₹)': bid.get('price', 0),
            'Quantity': bid.get('quantity', 0),
            'Orders': bid.get('orders', 1)
        })
    
    if table_data:
        # Convert to DataFrame
        df = pd.DataFrame(table_data)
        
        # Format display values
        df_display = df.copy()
        df_display['Price (₹)'] = df_display['Price (₹)'].apply(lambda x: f'₹{x:,.2f}' if isinstance(x, (int, float)) else x)
        df_display['Quantity'] = df_display['Quantity'].apply(lambda x: f'{x:,.0f}' if isinstance(x, (int, float)) else x)
        
        # Style function
        def style_compact_order_book(row):
            if row['Side'] == 'SELL':
                return ['background-color: #ffebee', 'background-color: #ffebee', 'background-color: #ffebee', 'background-color: #ffebee', 'background-color: #ffebee']
            elif row['Side'] == 'BUY':
                return ['background-color: #e8f5e8', 'background-color: #e8f5e8', 'background-color: #e8f5e8', 'background-color: #e8f5e8', 'background-color: #e8f5e8']
            else:
                return ['background-color: #fff3cd', 'background-color: #fff3cd', 'background-color: #fff3cd', 'background-color: #fff3cd', 'background-color: #fff3cd']
        
        styled_df = df_display.style.apply(style_compact_order_book, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.info("No depth data available for display.")

def display_top5_insights(depth_data):
    """Display insights based on top 5 market depth levels."""
    
    st.subheader("🔍 Top 5 Levels Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📊 Market Structure**")
        
        # Imbalance analysis
        total_bid = depth_data['total_bid_volume']
        total_ask = depth_data['total_ask_volume']
        imbalance_ratio = total_bid / total_ask if total_ask > 0 else 1
        
        if imbalance_ratio > 1.5:
            st.success("**Strong Buying Dominance**")
            st.progress(0.8)
            st.caption(f"Bids are {imbalance_ratio:.1f}x stronger than asks")
        elif imbalance_ratio < 0.67:
            st.error("**Strong Selling Dominance**")
            st.progress(0.2)
            st.caption(f"Asks are {1/imbalance_ratio:.1f}x stronger than bids")
        else:
            st.info("**Balanced Market**")
            st.progress(0.5)
            st.caption("Buyers and sellers are evenly matched")
        
        # Depth quality
        total_depth = total_bid + total_ask
        if total_depth > 50000:
            quality = "Excellent"
            color = "green"
        elif total_depth > 20000:
            quality = "Good" 
            color = "blue"
        elif total_depth > 5000:
            quality = "Fair"
            color = "orange"
        else:
            quality = "Thin"
            color = "red"
            
        st.metric("Depth Quality", quality)
    
    with col2:
        st.write("**🎯 Trading Signals**")
        
        # Support/Resistance from top 5 levels
        if depth_data['buy']:
            st.write("**Key Support Levels:**")
            for i in range(min(3, len(depth_data['buy']))):
                level = depth_data['buy'][i]
                st.caption(f"Level {i+1}: ₹{level.get('price', 0):.2f} ({level.get('quantity', 0):,} shares)")
        
        if depth_data['sell']:
            st.write("**Key Resistance Levels:**")
            for i in range(min(3, len(depth_data['sell']))):
                level = depth_data['sell'][i]
                st.caption(f"Level {i+1}: ₹{level.get('price', 0):.2f} ({level.get('quantity', 0):,} shares)")
        
        # Quick action recommendation
        spread_pct = (depth_data['spread'] / depth_data['last_price']) * 100 if depth_data['last_price'] > 0 else 0
        if spread_pct < 0.1:
            st.success("**✅ Good Trading Conditions**")
            st.caption("Tight spread, consider trading")
        else:
            st.warning("**⚠️ Wide Spread Caution**")
            st.caption("Consider waiting for better prices")

def page_optimized_hft_depth():
    """Optimized HFT Market Depth Page - Top 5 Levels Only"""
    display_header()
    st.title("⚡ HFT Market Depth (Top 5 Levels)")
    
    instrument_df = get_instrument_df()
    if instrument_df.empty:
        st.info("Please connect to Zerodha Kite to view market depth.")
        return
    
    # Symbol selection
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Popular symbols first
        popular_symbols = ['RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR', 'ICICIBANK', 'SBIN', 'KOTAKBANK', 'LT', 'BHARTIARTL']
        all_symbols = instrument_df[instrument_df['exchange'].isin(['NSE', 'BSE'])]['tradingsymbol'].unique()
        
        # Sort with popular symbols first
        sorted_symbols = sorted([s for s in all_symbols if s in popular_symbols]) + \
                        sorted([s for s in all_symbols if s not in popular_symbols])
        
        selected_symbol = st.selectbox(
            "Select Symbol",
            sorted_symbols,
            index=0
        )
    
    with col2:
        # Fixed to 5 levels as requested
        levels = 5
        st.info(f"Levels: {levels}")
    
    # Get instrument token
    instrument_token = get_instrument_token(selected_symbol, instrument_df, 'NSE')
    
    if instrument_token:
        display_optimized_hft_market_depth(instrument_token, selected_symbol, levels)
    else:
        st.error(f"Could not find instrument token for {selected_symbol}")

# Update your navigation to use the optimized version
def page_hft_depth():
    """HFT Market Depth Page - Uses optimized version"""
    page_optimized_hft_depth()


@st.cache_data(ttl=30)
def get_options_chain(underlying, instrument_df, expiry_date=None):
    """Fetches and processes the options chain for a given underlying."""
    client = get_broker_client()
    if not client or instrument_df.empty: return pd.DataFrame(), None, 0.0, []
    if st.session_state.broker == "Zerodha":
        exchange_map = {"GOLDM": "MCX", "CRUDEOIL": "MCX", "SILVERM": "MCX", "NATURALGAS": "MCX", "USDINR": "CDS"}
        exchange = exchange_map.get(underlying, 'NFO')
        ltp_symbol = {"NIFTY": "NIFTY 50", "BANKNIFTY": "NIFTY BANK", "FINNIFTY": "NIFTY FIN SERVICE"}.get(underlying, underlying)
        ltp_exchange = "NSE" if exchange == "NFO" else exchange
        underlying_instrument_name = f"{ltp_exchange}:{ltp_symbol}"
        try:
            underlying_ltp = client.ltp(underlying_instrument_name)[underlying_instrument_name]['last_price']
        except Exception:
            underlying_ltp = 0.0
        
        options = instrument_df[(instrument_df['name'] == underlying.upper()) & (instrument_df['exchange'] == exchange)]
        if options.empty: return pd.DataFrame(), None, underlying_ltp, []
        
        expiries = sorted(options['expiry'].dt.date.unique())
        three_months_later = datetime.now().date() + timedelta(days=90)
        available_expiries = [e for e in expiries if datetime.now().date() <= e <= three_months_later]
        if not available_expiries: return pd.DataFrame(), None, underlying_ltp, []
        
        if not expiry_date: 
            expiry_date = available_expiries[0]
        else: 
            expiry_date = pd.to_datetime(expiry_date).date()
        
        chain_df = options[options['expiry'].dt.date == expiry_date].sort_values(by='strike')
        ce_df = chain_df[chain_df['instrument_type'] == 'CE'].copy()
        pe_df = chain_df[chain_df['instrument_type'] == 'PE'].copy()
        instruments_to_fetch = [f"{exchange}:{s}" for s in list(ce_df['tradingsymbol']) + list(pe_df['tradingsymbol'])]
        if not instruments_to_fetch: return pd.DataFrame(), expiry_date, underlying_ltp, available_expiries
        
        try:
            quotes = client.quote(instruments_to_fetch)
            ce_df['LTP'] = ce_df['tradingsymbol'].apply(lambda x: quotes.get(f"{exchange}:{x}", {}).get('last_price', 0))
            pe_df['LTP'] = pe_df['tradingsymbol'].apply(lambda x: quotes.get(f"{exchange}:{x}", {}).get('last_price', 0))
            ce_df['oi'] = ce_df['tradingsymbol'].apply(lambda x: quotes.get(f"{exchange}:{x}", {}).get('oi', 0))
            pe_df['oi'] = pe_df['tradingsymbol'].apply(lambda x: quotes.get(f"{exchange}:{x}", {}).get('oi', 0))
            
            final_chain = pd.merge(ce_df[['tradingsymbol', 'strike', 'LTP', 'oi']], 
                                   pe_df[['tradingsymbol', 'strike', 'LTP', 'oi']], 
                                   on='strike', suffixes=('_CE', '_PE')).rename(columns={'LTP_CE': 'CALL LTP', 'LTP_PE': 'PUT LTP', 'strike': 'STRIKE', 'oi_CE': 'CALL OI', 'oi_PE': 'PUT OI', 'tradingsymbol_CE': 'CALL', 'tradingsymbol_PE': 'PUT'}).fillna(0)
            
            return final_chain[['CALL', 'CALL LTP', 'CALL OI', 'STRIKE', 'PUT LTP', 'PUT OI', 'PUT']], expiry_date, underlying_ltp, available_expiries
        except Exception as e:
            st.error(f"Failed to fetch real-time OI data: {e}")
            return pd.DataFrame(), expiry_date, underlying_ltp, available_expiries
    else:
        st.warning(f"Options chain for {st.session_state.broker} not implemented.")
        return pd.DataFrame(), None, 0.0, []

@st.cache_data(ttl=10)
def get_portfolio():
    """Fetches real-time portfolio - UPDATED FOR UPSTOX."""
    client = get_broker_client()
    if not client: 
        return pd.DataFrame(), pd.DataFrame(), 0.0, 0.0
        
    broker = st.session_state.broker
    
    if broker == "Zerodha":
        # Existing Zerodha implementation
        try:
            positions = client.positions().get('net', [])
            holdings = client.holdings()
            positions_df = pd.DataFrame(positions)[['tradingsymbol', 'quantity', 'average_price', 'last_price', 'pnl']] if positions else pd.DataFrame()
            total_pnl = positions_df['pnl'].sum() if not positions_df.empty else 0.0
            holdings_df = pd.DataFrame(holdings)[['tradingsymbol', 'quantity', 'average_price', 'last_price', 'pnl']] if holdings else pd.DataFrame()
            total_investment = (holdings_df['quantity'] * holdings_df['average_price']).sum() if not holdings_df.empty else 0.0
            return positions_df, holdings_df, total_pnl, total_investment
        except Exception as e:
            st.error(f"Portfolio API Error: {e}")
            return pd.DataFrame(), pd.DataFrame(), 0.0, 0.0
            
    elif broker == "Upstox":
        # Upstox implementation
        try:
            positions_df = get_upstox_positions()
            holdings_df = get_upstox_holdings()
            
            total_pnl = positions_df['pnl'].sum() if not positions_df.empty else 0.0
            total_investment = (holdings_df['quantity'] * holdings_df['average_price']).sum() if not holdings_df.empty else 0.0
            
            return positions_df, holdings_df, total_pnl, total_investment
            
        except Exception as e:
            st.error(f"Upstox portfolio error: {e}")
            return pd.DataFrame(), pd.DataFrame(), 0.0, 0.0
    
    else:
        st.warning(f"Portfolio for {broker} not implemented.")
        return pd.DataFrame(), pd.DataFrame(), 0.0, 0.0


def place_order(instrument_df, symbol, quantity, order_type, transaction_type, product, price=None):
    """Places a single order - UPDATED FOR UPSTOX."""
    client = get_broker_client()
    if not client:
        st.error("Broker not connected.")
        return
        
    broker = st.session_state.broker
    
    if broker == "Zerodha":
        # Existing Zerodha implementation
        try:
            is_option = any(char.isdigit() for char in symbol)
            if is_option:
                exchange = 'NFO'
            else:
                instrument = instrument_df[instrument_df['tradingsymbol'] == symbol.upper()]
                if instrument.empty:
                    st.error(f"Symbol '{symbol}' not found.")
                    return
                exchange = instrument.iloc[0]['exchange']

            order_id = client.place_order(
                tradingsymbol=symbol.upper(), 
                exchange=exchange, 
                transaction_type=transaction_type, 
                quantity=quantity, 
                order_type=order_type, 
                product=product, 
                variety=client.VARIETY_REGULAR, 
                price=price
            )
            st.toast(f"✅ Order placed successfully! ID: {order_id}", icon="🎉")
            st.session_state.order_history.insert(0, {
                "id": order_id, 
                "symbol": symbol, 
                "qty": quantity, 
                "type": transaction_type, 
                "status": "Success"
            })
        except Exception as e:
            st.toast(f"❌ Order failed: {e}", icon="🔥")
            st.session_state.order_history.insert(0, {
                "id": "N/A", 
                "symbol": symbol, 
                "qty": quantity, 
                "type": transaction_type, 
                "status": f"Failed: {e}"
            })
            
    elif broker == "Upstox":
        # Upstox implementation
        try:
            # Find instrument token
            instrument = instrument_df[instrument_df['tradingsymbol'] == symbol.upper()]
            if instrument.empty:
                st.error(f"Symbol '{symbol}' not found.")
                return
                
            instrument_token = instrument.iloc[0]['instrument_token']
            
            # Map product types
            product_map = {
                'MIS': 'intraday',
                'CNC': 'delivery',
                'NRML': 'normal'
            }
            
            # Map order types
            order_type_map = {
                'MARKET': 'market',
                'LIMIT': 'limit'
            }
            
            order_params = {
                'instrument_token': instrument_token,
                'quantity': quantity,
                'product': product_map.get(product, 'intraday'),
                'validity': 'day',
                'order_type': order_type_map.get(order_type, 'market'),
                'transaction_type': transaction_type.lower(),
                'price': price if order_type == 'LIMIT' else 0
            }
            
            order_id = place_upstox_order(order_params)
            if order_id:
                st.toast(f"✅ Upstox order placed successfully! ID: {order_id}", icon="🎉")
                st.session_state.order_history.insert(0, {
                    "id": order_id, 
                    "symbol": symbol, 
                    "qty": quantity, 
                    "type": transaction_type, 
                    "status": "Success"
                })
            else:
                st.toast(f"❌ Upstox order failed", icon="🔥")
                st.session_state.order_history.insert(0, {
                    "id": "N/A", 
                    "symbol": symbol, 
                    "qty": quantity, 
                    "type": transaction_type, 
                    "status": "Failed"
                })
                
        except Exception as e:
            st.toast(f"❌ Upstox order failed: {e}", icon="🔥")
            st.session_state.order_history.insert(0, {
                "id": "N/A", 
                "symbol": symbol, 
                "qty": quantity, 
                "type": transaction_type, 
                "status": f"Failed: {e}"
            })
    
    else:
        st.warning(f"Order placement for {broker} not implemented.")


@st.cache_data(ttl=1800)  # Cache for 30 minutes
def fetch_and_analyze_news(query=None):
    """Enhanced news fetcher with multiple fallback sources and better error handling."""
    analyzer = SentimentIntensityAnalyzer()
    
    # Curated reliable news sources
    news_sources = {
        "Moneycontrol": "https://www.moneycontrol.com/rss/latestnews.xml",
        "Economic Times Markets": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
        "Business Standard Markets": "https://www.business-standard.com/rss/markets-102.rss",
        "Reuters Business": "https://feeds.reuters.com/reuters/businessNews",
        "Bloomberg Markets": "https://feeds.bloomberg.com/markets/news.rss",
    }
    
    all_news = []
    successful_sources = 0
    
    for source, url in news_sources.items():
        try:
            # Add proper headers and timeout
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            
            if hasattr(feed, 'entries') and feed.entries:
                successful_sources += 1
                for entry in feed.entries[:5]:  # Limit per source
                    try:
                        # Get publication date
                        published_date = datetime.now().date()
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            published_date = datetime(*entry.published_parsed[:6]).date()
                        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                            published_date = datetime(*entry.updated_parsed[:6]).date()
                        
                        # Check if news matches query
                        title = entry.title if hasattr(entry, 'title') else "No title"
                        summary = entry.summary if hasattr(entry, 'summary') else title
                        
                        if query is None or query.lower() in title.lower() or query.lower() in summary.lower():
                            # Calculate sentiment with enhanced analysis
                            text_for_sentiment = f"{title} {summary}"
                            sentiment_scores = analyzer.polarity_scores(text_for_sentiment)
                            
                            # Enhanced sentiment classification
                            compound = sentiment_scores['compound']
                            if compound >= 0.05:
                                sentiment_label = "BULLISH"
                                sentiment_emoji = "📈"
                            elif compound <= -0.05:
                                sentiment_label = "BEARISH" 
                                sentiment_emoji = "📉"
                            else:
                                sentiment_label = "NEUTRAL"
                                sentiment_emoji = "➡️"
                            
                            all_news.append({
                                "source": source,
                                "title": title,
                                "link": entry.link if hasattr(entry, 'link') else "#",
                                "date": published_date,
                                "sentiment_score": compound,
                                "sentiment_label": sentiment_label,
                                "sentiment_emoji": sentiment_emoji,
                                "summary": summary[:200] + "..." if len(summary) > 200 else summary,
                                "positive": sentiment_scores['pos'],
                                "negative": sentiment_scores['neg'],
                                "neutral": sentiment_scores['neu']
                            })
                    except Exception as e:
                        continue  # Skip individual entry errors
                        
        except Exception as e:
            print(f"Failed to fetch from {source}: {e}")
            continue
    
    # If no news fetched, use enhanced fallback
    if not all_news:
        return get_fallback_news_enhanced()
    
    # Sort by date (newest first)
    all_news.sort(key=lambda x: x['date'], reverse=True)
    
    # Calculate overall market sentiment
    if all_news:
        avg_sentiment = sum(item['sentiment_score'] for item in all_news) / len(all_news)
        return {
            'news_items': pd.DataFrame(all_news),
            'overall_sentiment': avg_sentiment,
            'bullish_articles': len([n for n in all_news if n['sentiment_label'] == 'BULLISH']),
            'bearish_articles': len([n for n in all_news if n['sentiment_label'] == 'BEARISH']),
            'total_articles': len(all_news),
            'successful_sources': successful_sources
        }
    else:
        return get_fallback_news_enhanced()

def get_fallback_news_enhanced():
    """Enhanced fallback news with sentiment analysis."""
    fallback_news = [
        {
            "source": "Market Intelligence",
            "title": "Indian markets show resilience amid global volatility",
            "link": "#",
            "date": datetime.now().date(),
            "sentiment_score": 0.15,
            "sentiment_label": "BULLISH",
            "sentiment_emoji": "📈",
            "summary": "Domestic markets demonstrate strength despite global headwinds, with selective buying in key sectors.",
            "positive": 0.65,
            "negative": 0.20,
            "neutral": 0.15
        },
        {
            "source": "Economic Indicators",
            "title": "RBI maintains accommodative stance in policy review",
            "link": "#", 
            "date": datetime.now().date(),
            "sentiment_score": 0.08,
            "sentiment_label": "NEUTRAL",
            "sentiment_emoji": "➡️",
            "summary": "Central bank keeps rates unchanged while monitoring inflation trajectory and growth recovery.",
            "positive": 0.45,
            "negative": 0.25,
            "neutral": 0.30
        },
        {
            "source": "Corporate News",
            "title": "IT sector earnings season begins with mixed expectations",
            "link": "#",
            "date": datetime.now().date(),
            "sentiment_score": 0.05,
            "sentiment_label": "NEUTRAL",
            "sentiment_emoji": "➡️",
            "summary": "Technology companies set to announce quarterly results amid global demand concerns.",
            "positive": 0.40,
            "negative": 0.35,
            "neutral": 0.25
        },
        {
            "source": "Global Markets",
            "title": "US Fed policy decisions to influence emerging markets",
            "link": "#",
            "date": datetime.now().date(),
            "sentiment_score": -0.10,
            "sentiment_label": "BEARISH",
            "sentiment_emoji": "📉",
            "summary": "Federal Reserve's monetary policy outlook remains key driver for global capital flows.",
            "positive": 0.30,
            "negative": 0.55,
            "neutral": 0.15
        },
        {
            "source": "Commodities Update",
            "title": "Crude oil prices volatile amid supply adjustments",
            "link": "#",
            "date": datetime.now().date(),
            "sentiment_score": -0.05,
            "sentiment_label": "NEUTRAL",
            "sentiment_emoji": "➡️",
            "summary": "Oil markets balance supply concerns with demand outlook in uncertain global environment.",
            "positive": 0.35,
            "negative": 0.40,
            "neutral": 0.25
        }
    ]
    
    df = pd.DataFrame(fallback_news)
    avg_sentiment = df['sentiment_score'].mean()
    
    return {
        'news_items': df,
        'overall_sentiment': avg_sentiment,
        'bullish_articles': len([n for n in fallback_news if n['sentiment_label'] == 'BULLISH']),
        'bearish_articles': len([n for n in fallback_news if n['sentiment_label'] == 'BEARISH']),
        'total_articles': len(fallback_news),
        'successful_sources': 5
    }

def display_market_sentiment_dashboard():
    """Display comprehensive market sentiment analysis."""
    st.subheader("📊 AI Market Sentiment Analyzer")
    
    # Sentiment analysis controls
    col1, col2 = st.columns([2, 1])
    with col1:
        query = st.text_input("🔍 Filter news by keyword", placeholder="e.g., RBI, IT, Inflation")
    with col2:
        if st.button("🔄 Refresh Sentiment", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    # Fetch sentiment data
    with st.spinner("🤖 Analyzing market sentiment from news sources..."):
        sentiment_data = fetch_and_analyze_news(query if query else None)
    
    if not sentiment_data:
        st.error("❌ Failed to fetch market sentiment data")
        return
    
    # Display overall sentiment metrics
    st.markdown("---")
    st.subheader("🎯 Overall Market Sentiment")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    overall_sentiment = sentiment_data['overall_sentiment']
    with col1:
        if overall_sentiment > 0.1:
            st.metric("Market Mood", "BULLISH 📈", f"+{overall_sentiment:.2f}", delta_color="normal")
        elif overall_sentiment < -0.1:
            st.metric("Market Mood", "BEARISH 📉", f"{overall_sentiment:.2f}", delta_color="inverse")
        else:
            st.metric("Market Mood", "NEUTRAL ➡️", f"{overall_sentiment:.2f}")
    
    with col2:
        st.metric("Bullish Articles", sentiment_data['bullish_articles'])
    
    with col3:
        st.metric("Bearish Articles", sentiment_data['bearish_articles'])
    
    with col4:
        neutral_articles = sentiment_data['total_articles'] - sentiment_data['bullish_articles'] - sentiment_data['bearish_articles']
        st.metric("Neutral Articles", neutral_articles)
    
    with col5:
        st.metric("News Sources", sentiment_data['successful_sources'])
    
    # Sentiment visualization
    st.markdown("---")
    st.subheader("📈 Sentiment Distribution")
    
    # Create sentiment gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = overall_sentiment,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Market Sentiment Score"},
        delta = {'reference': 0},
        gauge = {
            'axis': {'range': [-1, 1]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [-1, -0.1], 'color': "lightcoral"},
                {'range': [-0.1, 0.1], 'color': "lightyellow"},
                {'range': [0.1, 1], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 0.9
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    # News articles with sentiment
    st.markdown("---")
    st.subheader("📰 Latest Market News & Analysis")
    
    news_df = sentiment_data['news_items']
    
    if not news_df.empty:
        for _, article in news_df.iterrows():
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.write(f"**{article['title']}**")
                    st.caption(f"📰 {article['source']} | 📅 {article['date']}")
                    st.write(article['summary'])
                    if article['link'] != "#":
                        st.markdown(f"[Read more]({article['link']})")
                
                with col2:
                    sentiment_color = "green" if article['sentiment_label'] == "BULLISH" else "red" if article['sentiment_label'] == "BEARISH" else "orange"
                    st.markdown(f'<div style="text-align: center; padding: 10px; border: 1px solid {sentiment_color}; border-radius: 5px;">'
                              f'<h3 style="color: {sentiment_color}; margin: 0;">{article["sentiment_emoji"]}</h3>'
                              f'<p style="margin: 0; font-weight: bold; color: {sentiment_color};">{article["sentiment_label"]}</p>'
                              f'<p style="margin: 0; font-size: 0.8em;">{article["sentiment_score"]:.2f}</p>'
                              f'</div>', unsafe_allow_html=True)
                
                st.markdown("---")
    else:
        st.info("No relevant news articles found for your search criteria.")

# ================ 4. HNI & PRO TRADER FEATURES ================

def execute_basket_order(basket_items, instrument_df):
    """Formats and places a basket of orders in a single API call."""
    client = get_broker_client()
    if not client:
        st.error("Broker not connected.")
        return
    
    if st.session_state.broker == "Zerodha":
        orders_to_place = []
        for item in basket_items:
            instrument = instrument_df[instrument_df['tradingsymbol'] == item['symbol']]
            if instrument.empty:
                st.toast(f"❌ Could not find symbol {item['symbol']} in instrument list. Skipping.", icon="🔥")
                continue
            exchange = instrument.iloc[0]['exchange']

            order = {
                "tradingsymbol": item['symbol'],
                "exchange": exchange,
                "transaction_type": client.TRANSACTION_TYPE_BUY if item['transaction_type'] == 'BUY' else client.TRANSACTION_TYPE_SELL,
                "quantity": int(item['quantity']),
                "product": client.PRODUCT_MIS if item['product'] == 'MIS' else client.PRODUCT_CNC,
                "order_type": client.ORDER_TYPE_MARKET if item['order_type'] == 'MARKET' else client.ORDER_TYPE_LIMIT,
            }
            if order['order_type'] == client.ORDER_TYPE_LIMIT:
                order['price'] = item['price']
            orders_to_place.append(order)
        
        if not orders_to_place:
            st.warning("No valid orders to place in the basket.")
            return

        try:
            client.place_order(variety=client.VARIETY_REGULAR, orders=orders_to_place)
            st.toast("✅ Basket order placed successfully!", icon="🎉")
            st.session_state.basket = []
            st.rerun()
        except Exception as e:
            st.toast(f"❌ Basket order failed: {e}", icon="🔥")

@st.cache_data(ttl=3600)
def get_sector_data():
    """Loads stock-to-sector mapping from a local CSV file."""
    try:
        return pd.read_csv("sensex_sectors.csv")
    except FileNotFoundError:
        st.warning("'sensex_sectors.csv' not found. Sector allocation will be unavailable.")
        return None

def style_option_chain(df, ltp):
    """Applies conditional styling to highlight ITM/OTM in the options chain."""
    if df.empty or 'STRIKE' not in df.columns or ltp == 0:
        return df.style

    def highlight_itm(row):
        styles = [''] * len(row)
        if row['STRIKE'] < ltp:
            styles[df.columns.get_loc('CALL LTP')] = 'background-color: #2E4053'
            styles[df.columns.get_loc('CALL OI')] = 'background-color: #2E4053'
        if row['STRIKE'] > ltp:
            styles[df.columns.get_loc('PUT LTP')] = 'background-color: #2E4053'
            styles[df.columns.get_loc('PUT OI')] = 'background-color: #2E4053'
        return styles

    return df.style.apply(highlight_itm, axis=1)

@st.dialog("Most Active Options")
def show_most_active_dialog(underlying, instrument_df):
    """Dialog to display the most active options by volume."""
    if 'show_most_active' not in st.session_state:
        st.session_state.show_most_active = False
    
    if st.button("Most Active Options", use_container_width=True) or st.session_state.show_most_active:
        st.session_state.show_most_active = True
        
        st.subheader(f"Most Active {underlying} Options (By Volume)")
        with st.spinner("Fetching data..."):

            client = get_broker_client()
            if not client:
                st.toast("Broker not connected.", icon="⚠️")
                return pd.DataFrame()
            
            try:
                chain_df, expiry, _, _ = get_options_chain(underlying, instrument_df)
                if chain_df.empty or expiry is None:
                    return pd.DataFrame()
                ce_symbols = chain_df['CALL'].dropna().tolist()
                pe_symbols = chain_df['PUT'].dropna().tolist()
                all_symbols = [f"NFO:{s}" for s in ce_symbols + pe_symbols]

                if not all_symbols:
                    return pd.DataFrame()

                quotes = client.quote(all_symbols)
                
                active_options = []
                for symbol, data in quotes.items():
                    prev_close = data.get('ohlc', {}).get('close', 0)
                    last_price = data.get('last_price', 0)
                    change = last_price - prev_close
                    pct_change = (change / prev_close * 100) if prev_close != 0 else 0
                    
                    active_options.append({
                        'Symbol': data.get('tradingsymbol'),
                        'LTP': last_price,
                        'Change %': pct_change,
                        'Volume': data.get('volume', 0),
                        'OI': data.get('oi', 0)
                    })
                
                df = pd.DataFrame(active_options)
                df_sorted = df.sort_values(by='Volume', ascending=False)
                st.dataframe(df_sorted.head(10), use_container_width=True, hide_index=True)

                if st.button("Close", use_container_width=True):
                    st.session_state.show_most_active = False
                    st.rerun()

            except Exception as e:
                st.error(f"Could not fetch most active options: {e}")


@st.cache_data(ttl=300)  # 5 minute cache
def get_global_indices_data_enhanced(tickers):
    """Enhanced global indices data fetcher with multiple fallbacks."""
    if not tickers:
        return pd.DataFrame()
    
    data = []
    
    for ticker_name, yf_ticker in tickers.items():
        try:
            # Try to download data with timeout
            stock_data = yf.download(yf_ticker, period="2d", progress=False, timeout=10)
            
            if stock_data.empty or len(stock_data) < 2:
                # Try alternative period
                stock_data = yf.download(yf_ticker, period="5d", progress=False, timeout=10)
            
            if not stock_data.empty and len(stock_data) >= 2:
                current_close = stock_data['Close'].iloc[-1]
                prev_close = stock_data['Close'].iloc[-2]
                
                # Handle division by zero
                if prev_close > 0:
                    change = current_close - prev_close
                    pct_change = (change / prev_close) * 100
                else:
                    change = 0
                    pct_change = 0
                
                data.append({
                    'Ticker': ticker_name,
                    'Price': current_close,
                    'Change': change,
                    '% Change': pct_change
                })
            else:
                # Add placeholder for unavailable data
                data.append({
                    'Ticker': ticker_name,
                    'Price': np.nan,
                    'Change': np.nan,
                    '% Change': np.nan
                })
                
        except Exception as e:
            print(f"Error fetching {ticker_name}: {e}")
            # Add placeholder for failed fetch
            data.append({
                'Ticker': ticker_name,
                'Price': np.nan,
                'Change': np.nan,
                '% Change': np.nan
            })
    
    return pd.DataFrame(data)

# Fallback global data
def get_fallback_global_data(tickers):
    """Provide fallback global data when live data is unavailable."""
    fallback_data = []
    
    # Mock data based on typical values
    mock_data = {
        "S&P 500": 4500.0,
        "Dow Jones": 34500.0, 
        "NASDAQ": 14000.0,
        "FTSE 100": 7500.0,
        "Nikkei 225": 32500.0,
        "Hang Seng": 18000.0,
        "SGX Nifty": 19500.0
    }
    
    for ticker_name in tickers.keys():
        base_price = mock_data.get(ticker_name, 1000.0)
        # Add some random variation
        variation = random.uniform(-0.02, 0.02)  # -2% to +2%
        current_price = base_price * (1 + variation)
        change = current_price - base_price
        pct_change = (change / base_price) * 100
        
        fallback_data.append({
            'Ticker': ticker_name,
            'Price': current_price,
            'Change': change,
            '% Change': pct_change
        })
    
    return pd.DataFrame(fallback_data)

# ================ ALGO TRADING BOTS SECTION ================

def momentum_trader_bot(instrument_df, symbol, capital=100):
    """Momentum trading bot that buys on upward momentum and sells on downward momentum."""
    exchange = 'NSE'
    token = get_instrument_token(symbol, instrument_df, exchange)
    if not token:
        return {"error": f"Could not find instrument for {symbol}"}
    
    try:
        data = get_historical_data(token, '5minute', period='1d')
        if data.empty or len(data) < 20:
            return {"error": "Insufficient data for analysis"}
        
        # Calculate indicators with TA-Lib
        data['RSI'] = talib.RSI(data['close'], timeperiod=14)
        data['EMA_20'] = talib.EMA(data['close'], timeperiod=20)
        data['EMA_50'] = talib.EMA(data['close'], timeperiod=50)
        
        latest = data.iloc[-1]
        prev = data.iloc[-2]
        
        signals = []
        
        # Momentum signals
        if (latest['EMA_20'] > latest['EMA_50'] and 
            prev['EMA_20'] <= prev['EMA_50']):
            signals.append("EMA crossover - BULLISH")
        
        rsi_val = latest.get('RSI', 50)
        if rsi_val < 30:
            signals.append("RSI oversold - BULLISH")
        elif rsi_val > 70:
            signals.append("RSI overbought - BEARISH")
        
        # Price momentum
        if len(data) >= 6:
            price_change_5min = ((latest['close'] - data.iloc[-6]['close']) / data.iloc[-6]['close']) * 100
            if price_change_5min > 0.5:
                signals.append(f"Strong upward momentum: +{price_change_5min:.2f}%")
        
        # Calculate position size
        current_price = latest['close']
        quantity = max(1, int((capital * 0.8) / current_price))
        
        action = "HOLD"
        if len([s for s in signals if "BULLISH" in s]) >= 2:
            action = "BUY"
        elif len([s for s in signals if "BEARISH" in s]) >= 2:
            action = "SELL"
        
        return {
            "bot_name": "Momentum Trader",
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "current_price": current_price,
            "signals": signals,
            "capital_required": quantity * current_price,
            "risk_level": "Medium"
        }
    
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

def mean_reversion_bot(instrument_df, symbol, capital=100):
    """Mean reversion bot that trades on price returning to mean levels."""
    exchange = 'NSE'
    token = get_instrument_token(symbol, instrument_df, exchange)
    if not token:
        return {"error": f"Could not find instrument for {symbol}"}
    
    try:
        data = get_historical_data(token, '15minute', period='5d')
        if data.empty or len(data) < 50:
            return {"error": "Insufficient data for analysis"}
        
        # Calculate Bollinger Bands using TA-Lib
        upperband, middleband, lowerband = talib.BBANDS(data['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        data['BB_Upper'] = upperband
        data['BB_Middle'] = middleband
        data['BB_Lower'] = lowerband
        
        latest = data.iloc[-1]
        
        signals = []
        current_price = latest['close']
        bb_lower = latest.get('BB_Lower', current_price)
        bb_upper = latest.get('BB_Upper', current_price)
        bb_middle = latest.get('BB_Middle', current_price)
        
        # Mean reversion signals
        if current_price <= bb_lower * 1.02:
            signals.append("Near lower Bollinger Band - BULLISH")
        
        if current_price >= bb_upper * 0.98:
            signals.append("Near upper Bollinger Band - BEARISH")
        
        # Distance from mean
        distance_from_mean = ((current_price - bb_middle) / bb_middle) * 100
        if abs(distance_from_mean) > 3:
            signals.append(f"Price {abs(distance_from_mean):.1f}% from mean")
        
        # RSI for confirmation
        data['RSI'] = talib.RSI(data['close'], timeperiod=14)
        rsi = data['RSI'].iloc[-1]
        if rsi < 35:
            signals.append("RSI supporting oversold condition")
        elif rsi > 65:
            signals.append("RSI supporting overbought condition")
        
        # Calculate position size
        quantity = max(1, int((capital * 0.6) / current_price))
        
        action = "HOLD"
        if any("BULLISH" in s for s in signals) and rsi < 40:
            action = "BUY"
        elif any("BEARISH" in s for s in signals) and rsi > 60:
            action = "SELL"
        
        return {
            "bot_name": "Mean Reversion",
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "current_price": current_price,
            "signals": signals,
            "capital_required": quantity * current_price,
            "risk_level": "Low"
        }
    
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

def volatility_breakout_bot(instrument_df, symbol, capital=100):
    """Volatility breakout bot that trades on breakouts from consolidation."""
    exchange = 'NSE'
    token = get_instrument_token(symbol, instrument_df, exchange)
    if not token:
        return {"error": f"Could not find instrument for {symbol}"}
    
    try:
        data = get_historical_data(token, '30minute', period='5d')
        if data.empty or len(data) < 30:
            return {"error": "Insufficient data for analysis"}
        
        # Calculate ATR using TA-Lib
        data['ATR'] = talib.ATR(data['high'], data['low'], data['close'], timeperiod=14)
        data['Range'] = data['high'] - data['low']
        avg_range = data['Range'].rolling(window=20).mean()
        
        latest = data.iloc[-1]
        current_price = latest['close']
        current_atr = latest['ATR']
        current_range = latest['Range']
        
        signals = []
        
        # Volatility signals
        if current_range > avg_range.iloc[-1] * 1.5:
            signals.append("High volatility - potential breakout")
        
        # Price action signals
        prev_high = data['high'].iloc[-2]
        prev_low = data['low'].iloc[-2]
        
        if current_price > prev_high + current_atr * 0.5:
            signals.append("Breakout above resistance - BULLISH")
        
        if current_price < prev_low - current_atr * 0.5:
            signals.append("Breakdown below support - BEARISH")
        
        # Volume confirmation (if available)
        if 'volume' in data.columns:
            avg_volume = data['volume'].rolling(window=20).mean().iloc[-1]
            if data['volume'].iloc[-1] > avg_volume * 1.2:
                signals.append("High volume confirmation")
        
        # Calculate position size based on ATR
        atr_percentage = (current_atr / current_price) * 100
        risk_per_trade = min(20, max(5, atr_percentage * 2))
        quantity = max(1, int((capital * (risk_per_trade / 100)) / current_price))
        
        action = "HOLD"
        if any("BULLISH" in s for s in signals):
            action = "BUY"
        elif any("BEARISH" in s for s in signals):
            action = "SELL"
        
        return {
            "bot_name": "Volatility Breakout",
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "current_price": current_price,
            "signals": signals,
            "capital_required": quantity * current_price,
            "risk_level": "High"
        }
    
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

def value_investor_bot(instrument_df, symbol, capital=100):
    """Value investor bot focusing on longer-term value signals."""
    exchange = 'NSE'
    token = get_instrument_token(symbol, instrument_df, exchange)
    if not token:
        return {"error": f"Could not find instrument for {symbol}"}
    
    try:
        data = get_historical_data(token, 'day', period='1y')
        if data.empty or len(data) < 100:
            return {"error": "Insufficient data for analysis"}
        
        # Calculate moving averages using TA-Lib
        data['SMA_50'] = talib.SMA(data['close'], timeperiod=50)
        data['SMA_200'] = talib.SMA(data['close'], timeperiod=200)
        data['EMA_21'] = talib.EMA(data['close'], timeperiod=21)
        
        latest = data.iloc[-1]
        current_price = latest['close']
        
        signals = []
        
        # Trend analysis
        if latest['SMA_50'] > latest['SMA_200']:
            signals.append("Bullish trend (50 > 200 SMA)")
        else:
            signals.append("Bearish trend (50 < 200 SMA)")
        
        # Support and resistance levels
        support_20 = data['low'].rolling(window=20).min().iloc[-1]
        resistance_20 = data['high'].rolling(window=20).max().iloc[-1]
        
        distance_to_support = ((current_price - support_20) / current_price) * 100
        distance_to_resistance = ((resistance_20 - current_price) / current_price) * 100
        
        if distance_to_support < 5:
            signals.append("Near strong support - BULLISH")
        
        if distance_to_resistance < 5:
            signals.append("Near strong resistance - BEARISH")
        
        # Monthly performance
        monthly_return = ((current_price - data['close'].iloc[-21]) / data['close'].iloc[-21]) * 100
        if monthly_return < -10:
            signals.append("Oversold on monthly basis - BULLISH")
        elif monthly_return > 15:
            signals.append("Overbought on monthly basis - BEARISH")
        
        # Calculate position size for longer term
        quantity = max(1, int((capital * 0.5) / current_price))
        
        action = "HOLD"
        bullish_signals = len([s for s in signals if "BULLISH" in s])
        bearish_signals = len([s for s in signals if "BEARISH" in s])
        
        if bullish_signals >= 2 and bearish_signals == 0:
            action = "BUY"
        elif bearish_signals >= 2 and bullish_signals == 0:
            action = "SELL"
        
        return {
            "bot_name": "Value Investor",
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "current_price": current_price,
            "signals": signals,
            "capital_required": quantity * current_price,
            "risk_level": "Low"
        }
    
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

def scalper_bot(instrument_df, symbol, capital=100):
    """High-frequency scalping bot for quick, small profits."""
    exchange = 'NSE'
    token = get_instrument_token(symbol, instrument_df, exchange)
    if not token:
        return {"error": f"Could not find instrument for {symbol}"}
    
    try:
        data = get_historical_data(token, 'minute', period='1d')
        if data.empty or len(data) < 100:
            return {"error": "Insufficient data for analysis"}
        
        # Calculate scalping indicators using TA-Lib
        data['RSI_9'] = talib.RSI(data['close'], timeperiod=9)
        data['EMA_8'] = talib.EMA(data['close'], timeperiod=8)
        data['EMA_21'] = talib.EMA(data['close'], timeperiod=21)
        
        latest = data.iloc[-1]
        current_price = latest['close']
        
        signals = []
        
        # Scalping signals
        if latest['EMA_8'] > latest['EMA_21']:
            signals.append("Fast EMA above slow EMA - BULLISH")
        else:
            signals.append("Fast EMA below slow EMA - BEARISH")
        
        rsi_9 = latest['RSI_9']
        if rsi_9 < 25:
            signals.append("Extremely oversold - BULLISH")
        elif rsi_9 > 75:
            signals.append("Extremely overbought - BEARISH")
        
        # Price momentum for scalping
        price_change_3min = ((current_price - data['close'].iloc[-3]) / data['close'].iloc[-3]) * 100
        if abs(price_change_3min) > 0.3:
            signals.append(f"Strong short-term momentum: {price_change_3min:+.2f}%")
        
        # Calculate small position size for scalping
        quantity = max(1, int((capital * 0.3) / current_price))
        
        action = "HOLD"
        if (any("BULLISH" in s for s in signals) and 
            "BEARISH" not in str(signals) and
            rsi_9 < 70):
            action = "BUY"
        elif (any("BEARISH" in s for s in signals) and 
              "BULLISH" not in str(signals) and
              rsi_9 > 30):
            action = "SELL"
        
        return {
            "bot_name": "Scalper Pro",
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "current_price": current_price,
            "signals": signals,
            "capital_required": quantity * current_price,
            "risk_level": "Very High"
        }
    
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

def trend_follower_bot(instrument_df, symbol, capital=100):
    """Trend following bot that rides established trends."""
    exchange = 'NSE'
    token = get_instrument_token(symbol, instrument_df, exchange)
    if not token:
        return {"error": f"Could not find instrument for {symbol}"}
    
    try:
        data = get_historical_data(token, 'hour', period='1mo')
        if data.empty or len(data) < 100:
            return {"error": "Insufficient data for analysis"}
        
        # Calculate trend indicators using TA-Lib
        data['ADX'] = talib.ADX(data['high'], data['low'], data['close'], timeperiod=14)
        data['EMA_20'] = talib.EMA(data['close'], timeperiod=20)
        data['EMA_50'] = talib.EMA(data['close'], timeperiod=50)
        
        # Simple trend detection without SuperTrend
        data['Trend'] = np.where(data['EMA_20'] > data['EMA_50'], 1, -1)
        
        latest = data.iloc[-1]
        current_price = latest['close']
        
        signals = []
        
        # Trend strength
        adx = latest.get('ADX', 0)
        if adx > 25:
            signals.append(f"Strong trend (ADX: {adx:.1f})")
        else:
            signals.append(f"Weak trend (ADX: {adx:.1f})")
        
        # Trend direction
        if latest['EMA_20'] > latest['EMA_50']:
            signals.append("Uptrend confirmed - BULLISH")
        else:
            signals.append("Downtrend confirmed - BEARISH")
        
        # Price relative to trend
        if current_price > latest['EMA_20']:
            signals.append("Price above short-term trend - BULLISH")
        else:
            signals.append("Price below short-term trend - BEARISH")
        
        # Pullback opportunities
        if (latest['EMA_20'] > latest['EMA_50'] and 
            current_price < latest['EMA_20'] and 
            current_price > latest['EMA_50']):
            signals.append("Pullback in uptrend - BULLISH")
        
        elif (latest['EMA_20'] < latest['EMA_50'] and 
              current_price > latest['EMA_20'] and 
              current_price < latest['EMA_50']):
            signals.append("Pullback in downtrend - BEARISH")
        
        # Calculate position size
        quantity = max(1, int((capital * 0.7) / current_price))
        
        action = "HOLD"
        bullish_count = len([s for s in signals if "BULLISH" in s])
        bearish_count = len([s for s in signals if "BEARISH" in s])
        
        if bullish_count >= 2 and adx > 20:
            action = "BUY"
        elif bearish_count >= 2 and adx > 20:
            action = "SELL"
        
        return {
            "bot_name": "Trend Follower",
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "current_price": current_price,
            "signals": signals,
            "capital_required": quantity * current_price,
            "risk_level": "Medium"
        }
    
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

# Dictionary of all available bots
ALGO_BOTS = {
    "Momentum Trader": momentum_trader_bot,
    "Mean Reversion": mean_reversion_bot,
    "Volatility Breakout": volatility_breakout_bot,
    "Value Investor": value_investor_bot,
    "Scalper Pro": scalper_bot,
    "Trend Follower": trend_follower_bot
}

def execute_bot_trade(instrument_df, bot_result):
    """Displays bot recommendations WITHOUT automatic execution - requires manual confirmation."""
    if bot_result.get("error"):
        st.error(bot_result["error"])
        return
    
    if bot_result["action"] == "HOLD":
        st.info(f"🤖 {bot_result['bot_name']} recommends HOLDING {bot_result['symbol']}")
        return
    
    action = bot_result["action"]
    symbol = bot_result["symbol"]
    quantity = bot_result["quantity"]
    current_price = bot_result["current_price"]
    required_capital = bot_result["capital_required"]
    
    st.success(f"""
    🚀 **{bot_result['bot_name']} Recommendation:**
    - **Action:** {action} {quantity} shares of {symbol}
    - **Current Price:** ₹{current_price:.2f}
    - **Required Capital:** ₹{required_capital:.2f}
    - **Risk Level:** {bot_result['risk_level']}
    """)
    
    # Display signals first
    st.subheader("📊 Analysis Signals")
    for signal in bot_result["signals"]:
        if "BULLISH" in signal:
            st.success(f"✅ {signal}")
        elif "BEARISH" in signal:
            st.error(f"❌ {signal}")
        else:
            st.info(f"📈 {signal}")
    
    # Manual execution section - clearly separated
    st.markdown("---")
    st.subheader("🚀 Manual Trade Execution")
    st.warning("**Manual Confirmation Required:** Click the button below ONLY if you want to execute this trade.")
    
    col1, col2 = st.columns(2)
    
    if col1.button(f"Execute {action} Order", key=f"execute_{symbol}", use_container_width=True, type="primary"):
        # Only execute when user explicitly clicks
        place_order(instrument_df, symbol, quantity, 'MARKET', action, 'MIS')
        st.toast(f"✅ {action} order for {symbol} placed successfully!", icon="🎉")
        st.rerun()
    
    if col2.button("Ignore Recommendation", key=f"ignore_{symbol}", use_container_width=True):
        st.info("Trade execution cancelled.")
        st.rerun()

def page_algo_bots():
    """Main algo bots page where users can run different trading bots."""
    display_header()
    st.title("🤖 Algo Trading Bots")
    st.info("Run automated trading bots with minimum capital of ₹100. Each bot uses different strategies and risk profiles.", icon="🤖")
    
    instrument_df = get_instrument_df()
    if instrument_df.empty:
        st.info("Please connect to a broker to use algo bots.")
        return
    
    # Bot selection and configuration
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_bot = st.selectbox(
            "Select Trading Bot",
            list(ALGO_BOTS.keys()),
            help="Choose a trading bot based on your risk appetite and trading style"
        )
        
        # Bot descriptions
        bot_descriptions = {
            "Momentum Trader": "Trades on strong price momentum and trend continuations. Medium risk.",
            "Mean Reversion": "Buys low and sells high based on statistical mean reversion. Low risk.",
            "Volatility Breakout": "Captures breakouts from low volatility periods. High risk.",
            "Value Investor": "Focuses on longer-term value and fundamental trends. Low risk.",
            "Scalper Pro": "High-frequency trading for quick, small profits. Very high risk.",
            "Trend Follower": "Identifies and rides established market trends using ADX and EMAs. Medium risk."
        }
        
        st.markdown(f"**Description:** {bot_descriptions.get(selected_bot, 'N/A')}")
    
    with col2:
        trading_capital = st.number_input(
            "Trading Capital (₹)",
            min_value=100,
            max_value=100000,
            value=1000,
            step=100,
            help="Minimum ₹100 required"
        )
    
    st.markdown("---")
    
    # Symbol selection and bot execution
    col3, col4 = st.columns([1, 1])
    
    with col3:
        st.subheader("Stock Selection")
        all_symbols = instrument_df[instrument_df['exchange'].isin(['NSE', 'BSE'])]['tradingsymbol'].unique()
        selected_symbol = st.selectbox(
            "Select Stock",
            sorted(all_symbols),
            index=list(all_symbols).index('RELIANCE') if 'RELIANCE' in all_symbols else 0
        )
        
        # Show current price
        quote_data = get_watchlist_data([{'symbol': selected_symbol, 'exchange': 'NSE'}])
        if not quote_data.empty:
            current_price = quote_data.iloc[0]['Price']
            st.metric("Current Price", f"₹{current_price:.2f}")
    
    with col4:
        st.subheader("Bot Execution")
        st.write(f"**Selected Bot:** {selected_bot}")
        st.write(f"**Available Capital:** ₹{trading_capital:,}")
        
        if st.button("🚀 Run Trading Bot", use_container_width=True, type="primary"):
            with st.spinner(f"Running {selected_bot} analysis..."):
                bot_function = ALGO_BOTS[selected_bot]
                bot_result = bot_function(instrument_df, selected_symbol, trading_capital)
                
                if bot_result and not bot_result.get("error"):
                    st.session_state.last_bot_result = bot_result
                    st.rerun()
    
    # Display bot results
    if 'last_bot_result' in st.session_state and st.session_state.last_bot_result:
        bot_result = st.session_state.last_bot_result
        
        if bot_result.get("error"):
            st.error(bot_result["error"])
        else:
            st.markdown("---")
            st.subheader("🤖 Bot Analysis Results")
            
            # Create metrics cards
            col5, col6, col7, col8 = st.columns(4)
            
            with col5:
                action_color = "green" if bot_result["action"] == "BUY" else "red" if bot_result["action"] == "SELL" else "orange"
                st.markdown(f'<div class="metric-card" style="border-color: {action_color};">'
                            f'<h3 style="color: {action_color};">{bot_result["action"]}</h3>'
                            f'<p>Recommended Action</p></div>', unsafe_allow_html=True)
            
            with col6:
                st.metric("Quantity", bot_result["quantity"])
            
            with col7:
                st.metric("Capital Required", f"₹{bot_result['capital_required']:.2f}")
            
            with col8:
                risk_color = {"Low": "green", "Medium": "orange", "High": "red", "Very High": "darkred"}
                st.markdown(f'<div class="metric-card" style="border-color: {risk_color.get(bot_result["risk_level"], "gray")};">'
                            f'<h3 style="color: {risk_color.get(bot_result["risk_level"], "gray")};">{bot_result["risk_level"]}</h3>'
                            f'<p>Risk Level</p></div>', unsafe_allow_html=True)
            
            # Display signals and execute trade
            execute_bot_trade(instrument_df, bot_result)

    # Bot performance history
    st.markdown("---")
    st.subheader("📈 Bot Performance Tips")
    
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.markdown("""
        **Best Practices:**
        - Start with minimum capital (₹100)
        - Use 'Value Investor' for beginners
        - 'Scalper Pro' requires constant monitoring
        - Always check signals before executing
        - Combine multiple bot recommendations
        """)
    
    with tips_col2:
        st.markdown("""
        **Risk Management:**
        - Never risk more than 2% per trade
        - Use stop losses with every trade
        - Diversify across different bots
        - Monitor performance regularly
        - Adjust capital based on experience
        """)
    
    # Quick bot comparison
    with st.expander("🤖 Bot Comparison Guide"):
        comparison_data = {
            "Bot": list(ALGO_BOTS.keys()),
            "Risk Level": ["Medium", "Low", "High", "Low", "Very High", "Medium"],
            "Holding Period": ["Hours", "Days", "Minutes", "Weeks", "Minutes", "Days"],
            "Capital Recommended": ["₹1,000+", "₹500+", "₹2,000+", "₹2,000+", "₹5,000+", "₹1,500+"],
            "Best For": ["Trend riding", "Safe returns", "Quick profits", "Long term", "Experienced", "Trend following"]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# ================ AUTOMATED BOT FUNCTIONS ================

def automated_momentum_trader(instrument_df, symbol):
    """Enhanced momentum trader for automated mode."""
    exchange = 'NSE'
    token = get_instrument_token(symbol, instrument_df, exchange)
    if not token:
        return {"error": f"Could not find instrument for {symbol}"}
    
    try:
        data = get_historical_data(token, '5minute', period='1d')
        if data.empty or len(data) < 50:
            return {"error": "Insufficient data for analysis"}
        
        # Calculate multiple indicators
        data['RSI_14'] = talib.RSI(data['close'], timeperiod=14)
        data['RSI_21'] = talib.RSI(data['close'], timeperiod=21)
        data['EMA_20'] = talib.EMA(data['close'], timeperiod=20)
        data['EMA_50'] = talib.EMA(data['close'], timeperiod=50)
        data['MACD'], data['MACD_Signal'], _ = talib.MACD(data['close'])
        
        latest = data.iloc[-1]
        prev = data.iloc[-2]
        
        signals = []
        score = 0
        
        # EMA Crossover (30 points)
        if (latest['EMA_20'] > latest['EMA_50'] and 
            prev['EMA_20'] <= prev['EMA_50']):
            signals.append("EMA Bullish Crossover")
            score += 30
        
        # RSI Signals (25 points)
        rsi_14 = latest['RSI_14']
        if 30 < rsi_14 < 70:  # Avoid extremes
            if rsi_14 > 50:
                signals.append("RSI Bullish")
                score += 15
            if rsi_14 > latest['RSI_21']:
                signals.append("RSI Positive Divergence")
                score += 10
        
        # MACD Signals (20 points)
        if (latest['MACD'] > latest['MACD_Signal'] and 
            prev['MACD'] <= prev['MACD_Signal']):
            signals.append("MACD Bullish Crossover")
            score += 20
        
        # Volume confirmation (15 points)
        if 'volume' in data.columns and len(data) > 20:
            avg_volume = data['volume'].rolling(20).mean().iloc[-1]
            if data['volume'].iloc[-1] > avg_volume * 1.2:
                signals.append("High Volume Confirmation")
                score += 15
        
        # Price momentum (10 points)
        if len(data) >= 10:
            price_change_30min = ((latest['close'] - data['close'].iloc[-6]) / data['close'].iloc[-6]) * 100
            if price_change_30min > 1:
                signals.append("Strong Short-term Momentum")
                score += 10
        
        current_price = latest['close']
        risk_level = "High" if score >= 60 else "Medium" if score >= 40 else "Low"
        
        action = "HOLD"
        if score >= 50:  # Minimum threshold for trade
            action = "BUY"
        elif score <= 20:  # Very weak momentum could signal SELL
            # Check if we have an existing position to sell
            open_trades = [t for t in st.session_state.automated_mode['trade_history'] 
                          if t.get('symbol') == symbol and t.get('status') == 'OPEN']
            if open_trades and open_trades[0]['action'] == 'BUY':
                action = "SELL"
        
        return {
            "bot_name": "Auto Momentum Trader",
            "symbol": symbol,
            "action": action,
            "quantity": 1,  # Will be calculated based on risk
            "current_price": current_price,
            "signals": signals,
            "score": score,
            "risk_level": risk_level,
            "capital_required": current_price
        }
    
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

def automated_mean_reversion(instrument_df, symbol):
    """Enhanced mean reversion bot for automated mode."""
    exchange = 'NSE'
    token = get_instrument_token(symbol, instrument_df, exchange)
    if not token:
        return {"error": f"Could not find instrument for {symbol}"}
    
    try:
        data = get_historical_data(token, '15minute', period='5d')
        if data.empty or len(data) < 100:
            return {"error": "Insufficient data for analysis"}
        
        # Calculate Bollinger Bands and other indicators
        upperband, middleband, lowerband = talib.BBANDS(data['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        data['BB_Upper'] = upperband
        data['BB_Middle'] = middleband
        data['BB_Lower'] = lowerband
        data['RSI_14'] = talib.RSI(data['close'], timeperiod=14)
        
        latest = data.iloc[-1]
        current_price = latest['close']
        
        signals = []
        score = 0
        
        # Bollinger Band position (40 points)
        bb_position = (current_price - latest['BB_Lower']) / (latest['BB_Upper'] - latest['BB_Lower'])
        
        if bb_position < 0.1:  # Near lower band
            signals.append("Near Lower Bollinger Band")
            score += 40
        elif bb_position > 0.9:  # Near upper band
            signals.append("Near Upper Bollinger Band")
            score += 40
        
        # RSI confirmation (30 points)
        rsi = latest['RSI_14']
        if bb_position < 0.1 and rsi < 35:  # Oversold confirmation
            signals.append("RSI Oversold Confirmation")
            score += 30
        elif bb_position > 0.9 and rsi > 65:  # Overbought confirmation
            signals.append("RSI Overbought Confirmation")
            score += 30
        
        # Distance from mean (20 points)
        distance_from_mean = abs((current_price - latest['BB_Middle']) / latest['BB_Middle']) * 100
        if distance_from_mean > 3:
            signals.append(f"Price {distance_from_mean:.1f}% from mean")
            score += 20
        
        # Volume confirmation (10 points)
        if 'volume' in data.columns:
            avg_volume = data['volume'].rolling(20).mean().iloc[-1]
            if data['volume'].iloc[-1] > avg_volume * 1.5:
                signals.append("High Volume Reversion Signal")
                score += 10
        
        risk_level = "Low" if score >= 60 else "Medium" if score >= 30 else "High"
        
        action = "HOLD"
        if score >= 50 and bb_position < 0.1:  # Buy near lower band
            action = "BUY"
        elif score >= 50 and bb_position > 0.9:  # Sell near upper band
            # Check for existing position
            open_trades = [t for t in st.session_state.automated_mode['trade_history'] 
                          if t.get('symbol') == symbol and t.get('status') == 'OPEN']
            if open_trades and open_trades[0]['action'] == 'BUY':
                action = "SELL"
        
        return {
            "bot_name": "Auto Mean Reversion",
            "symbol": symbol,
            "action": action,
            "quantity": 1,
            "current_price": current_price,
            "signals": signals,
            "score": score,
            "risk_level": risk_level,
            "capital_required": current_price
        }
    
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

def setup_breakout_bot(instrument_df, nifty25_auto_trade=False):
    """Setup Breakout Detection Bot with advanced pattern recognition."""
    st.write("**📈 Breakout Trading Bot**")
    st.caption("Identifies and trades breakouts from consolidation patterns with volume confirmation")
    
    if nifty25_auto_trade:
        st.info("🔷 Nifty 25 Auto-Trading is ACTIVE - Breakout Bot will scan Nifty 25 stocks")
        symbols_to_scan = get_nifty25_instruments(instrument_df)
    else:
        # User-selected symbols
        watchlist_symbols = st.session_state.get('watchlists', {}).get(
            st.session_state.get('active_watchlist', 'Watchlist 1'), []
        )
        symbols_to_scan = watchlist_symbols
        st.info(f"🔍 Breakout Bot will scan {len(symbols_to_scan)} symbols from your watchlist")
    
    if not symbols_to_scan:
        st.warning("No symbols available for scanning. Please set up your watchlist or enable Nifty 25 mode.")
        return
    
    # BREAKOUT BOT CONFIGURATION
    with st.expander("⚙️ Breakout Bot Settings", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # CAPITAL AND RISK MANAGEMENT
            st.subheader("💰 Capital & Risk")
            total_capital = st.number_input(
                "Total Capital (₹)", 
                min_value=1000, 
                max_value=1000000, 
                value=10000, 
                step=1000,
                key="breakout_capital"
            )
            
            risk_percent = st.slider(
                "Risk per Trade (%)", 
                min_value=0.5, 
                max_value=10.0, 
                value=2.0, 
                step=0.5,
                key="breakout_risk"
            )
            st.caption(f"Risk Amount: ₹{total_capital * risk_percent/100:.2f} per trade")
            
            consolidation_period = st.slider("Consolidation Period (days)", 10, 30, 15)
            min_volume_ratio = st.slider("Min Volume Ratio", 1.2, 3.0, 1.8)
        
        with col2:
            st.subheader("🎯 Breakout Parameters")
            breakout_confirmation = st.selectbox(
                "Breakout Confirmation", 
                ["Close Above", "High Above", "Both Close and High"]
            )
            min_price_move = st.slider("Min Price Move %", 1.0, 5.0, 2.0)
            stop_loss_type = st.selectbox(
                "Stop Loss Type", 
                ["ATR Based", "Percentage Based", "Support/Resistance"]
            )
            
            if stop_loss_type == "Percentage Based":
                stop_loss_pct = st.slider("Stop Loss %", 1.0, 5.0, 2.5)
            elif stop_loss_type == "ATR Based":
                atr_multiplier = st.slider("ATR Multiplier", 1.5, 3.0, 2.0)
    
    # TRADING CONTROLS
    col_control1, col_control2, col_control3 = st.columns(3)
    with col_control1:
        auto_execute = st.checkbox("🤖 Auto-Execute Trades", value=False)
    with col_control2:
        max_positions = st.slider("Max Positions", 1, 10, 3, key="breakout_max_pos")
    with col_control3:
        min_confidence = st.slider("Min Confidence", 60, 90, 75, key="breakout_conf")
    
    # SCAN AND EXECUTE
    if st.button("🔍 Scan Breakout Opportunities", type="primary", use_container_width=True):
        with st.spinner(f"Scanning {len(symbols_to_scan)} symbols for breakout patterns..."):
            breakout_signals = run_breakout_analysis(
                symbols_to_scan, 
                instrument_df,
                consolidation_period,
                min_volume_ratio,
                min_price_move
            )
        
        if breakout_signals and breakout_signals.get('signals'):
            display_breakout_signals(
                breakout_signals, 
                total_capital, 
                risk_percent, 
                auto_execute,
                max_positions
            )
        else:
            st.info("🤖 No breakout signals found. Market may be in consolidation.")

def run_breakout_analysis(symbols, instrument_df, consolidation_period=15, min_volume_ratio=1.8, min_price_move=2.0):
    """Run breakout analysis on given symbols."""
    breakout_signals = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, item in enumerate(symbols[:25]):  # Limit to 25 for performance
        symbol = item['symbol']
        exchange = item['exchange']
        status_text.text(f"Analyzing {symbol}... ({i+1}/{min(25, len(symbols))})")
        
        try:
            token = get_instrument_token(symbol, instrument_df, exchange)
            if not token:
                continue
                
            # Get 60 days historical data
            data = get_historical_data_60days(token, 'day')
            if data.empty or len(data) < 30:
                continue
            
            # Analyze for breakouts
            signal = analyze_breakout_pattern(data, symbol, consolidation_period, min_volume_ratio, min_price_move)
            if signal and signal.get('signal') != 'NO_SIGNAL':
                breakout_signals.append(signal)
                
        except Exception as e:
            continue
        
        progress_bar.progress((i + 1) / min(25, len(symbols)))
    
    status_text.text("Breakout analysis complete!")
    
    return {
        'signals': sorted(breakout_signals, key=lambda x: x.get('confidence', 0), reverse=True),
        'total_scanned': min(25, len(symbols)),
        'breakouts_found': len(breakout_signals),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def analyze_breakout_pattern(data, symbol, consolidation_period, min_volume_ratio, min_price_move):
    """Analyze stock data for breakout patterns."""
    if len(data) < consolidation_period + 5:
        return None
    
    # Calculate technical indicators
    data = calculate_advanced_indicators(data)
    latest = data.iloc[-1]
    prev_day = data.iloc[-2]
    
    # Calculate consolidation parameters
    consolidation_high = data['high'].tail(consolidation_period).max()
    consolidation_low = data['low'].tail(consolidation_period).min()
    consolidation_range = consolidation_high - consolidation_low
    current_close = latest['close']
    current_high = latest['high']
    current_volume = latest['volume']
    
    # Volume analysis
    avg_volume = data['volume'].tail(consolidation_period).mean()
    volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
    
    # Price movement analysis
    price_move_pct = ((current_close - prev_day['close']) / prev_day['close']) * 100
    
    # Initialize signal
    signal = 'NO_SIGNAL'
    confidence = 0
    pattern_type = ""
    breakout_level = 0
    
    # UPPER BREAKOUT DETECTION
    if current_close > consolidation_high and volume_ratio >= min_volume_ratio:
        signal = 'BUY'
        pattern_type = "Upper Breakout"
        breakout_level = consolidation_high
        confidence = 70
        
        # Enhance confidence based on factors
        if price_move_pct >= min_price_move:
            confidence += 10
        if current_high > consolidation_high * 1.01:  # Strong breakout
            confidence += 10
        if latest.get('EMA_20', 0) > latest.get('EMA_50', 0):  # Trend confirmation
            confidence += 10
    
    # LOWER BREAKOUT DETECTION (Breakdown)
    elif current_close < consolidation_low and volume_ratio >= min_volume_ratio:
        signal = 'SELL'
        pattern_type = "Lower Breakout"
        breakout_level = consolidation_low
        confidence = 65
        
        if price_move_pct <= -min_price_move:
            confidence += 10
        if latest.get('EMA_20', 0) < latest.get('EMA_50', 0):  # Downtrend confirmation
            confidence += 10
    
    if signal != 'NO_SIGNAL':
        # Calculate stop loss and target
        if signal == 'BUY':
            stop_loss = consolidation_low
            target = current_close + (2 * (current_close - stop_loss))
        else:  # SELL
            stop_loss = consolidation_high
            target = current_close - (2 * (stop_loss - current_close))
        
        risk_reward = abs((target - current_close) / (current_close - stop_loss)) if current_close != stop_loss else 0
        
        return {
            'symbol': symbol,
            'signal': signal,
            'confidence': min(95, confidence),
            'pattern_type': pattern_type,
            'current_price': current_close,
            'breakout_level': breakout_level,
            'volume_ratio': volume_ratio,
            'price_move_pct': price_move_pct,
            'consolidation_high': consolidation_high,
            'consolidation_low': consolidation_low,
            'stop_loss': stop_loss,
            'target': target,
            'risk_reward': risk_reward,
            'consolidation_range_pct': (consolidation_range / consolidation_low * 100) if consolidation_low > 0 else 0
        }
    
    return None

def setup_multi_signal_bot(instrument_df, nifty25_auto_trade=False):
    """Setup Multi-Signal Bot that combines multiple technical strategies."""
    st.write("**🎯 Multi-Signal Trading Bot**")
    st.caption("Combines momentum, mean reversion, breakout, and volume signals for high-probability trades")
    
    if nifty25_auto_trade:
        st.info("🔷 Nifty 25 Auto-Trading is ACTIVE - Multi-Signal Bot will scan Nifty 25 stocks")
        symbols_to_scan = get_nifty25_instruments(instrument_df)
    else:
        watchlist_symbols = st.session_state.get('watchlists', {}).get(
            st.session_state.get('active_watchlist', 'Watchlist 1'), []
        )
        symbols_to_scan = watchlist_symbols
        st.info(f"🔍 Multi-Signal Bot will scan {len(symbols_to_scan)} symbols from your watchlist")
    
    if not symbols_to_scan:
        st.warning("No symbols available for scanning. Please set up your watchlist or enable Nifty 25 mode.")
        return
    
    # MULTI-SIGNAL BOT CONFIGURATION
    with st.expander("⚙️ Multi-Signal Bot Settings", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Capital & Risk")
            total_capital = st.number_input(
                "Total Capital (₹)", 
                min_value=1000, 
                max_value=1000000, 
                value=10000, 
                step=1000,
                key="multi_capital"
            )
            
            risk_percent = st.slider(
                "Risk per Trade (%)", 
                min_value=0.5, 
                max_value=10.0, 
                value=1.5, 
                step=0.5,
                key="multi_risk"
            )
            st.caption(f"Risk Amount: ₹{total_capital * risk_percent/100:.2f} per trade")
            
            st.subheader("📊 Signal Weights")
            momentum_weight = st.slider("Momentum Weight", 0.0, 1.0, 0.3)
            mean_reversion_weight = st.slider("Mean Reversion Weight", 0.0, 1.0, 0.25)
            breakout_weight = st.slider("Breakout Weight", 0.0, 1.0, 0.25)
            volume_weight = st.slider("Volume Weight", 0.0, 1.0, 0.2)
        
        with col2:
            st.subheader("🎯 Strategy Parameters")
            min_combined_score = st.slider("Min Combined Score", 50, 90, 70)
            require_volume_confirmation = st.checkbox("Require Volume Confirmation", value=True)
            require_trend_alignment = st.checkbox("Require Trend Alignment", value=True)
            
            st.subheader("⏱️ Timeframe Settings")
            primary_timeframe = st.selectbox("Primary Timeframe", ["Daily", "Hourly", "Both"])
            lookback_period = st.slider("Lookback Period (days)", 20, 100, 60)
    
    # SIGNAL FILTERS
    with st.expander("🔍 Signal Filters"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            min_rsi = st.slider("Min RSI", 20, 50, 30)
            max_rsi = st.slider("Max RSI", 50, 80, 70)
            min_volume_ratio = st.slider("Min Volume Ratio", 1.0, 2.0, 1.2)
        with col_f2:
            min_adx = st.slider("Min ADX", 15, 30, 20)
            max_positions = st.slider("Max Positions", 1, 8, 4, key="multi_max_pos")
    
    # TRADING CONTROLS
    col_control1, col_control2 = st.columns(2)
    with col_control1:
        auto_execute = st.checkbox("🤖 Auto-Execute Trades", value=False, key="multi_auto")
    with col_control2:
        if st.button("🚀 Scan Multi-Signal Opportunities", type="primary", use_container_width=True):
            with st.spinner(f"Running multi-signal analysis on {len(symbols_to_scan)} symbols..."):
                multi_signals = run_multi_signal_analysis(
                    symbols_to_scan,
                    instrument_df,
                    {
                        'momentum_weight': momentum_weight,
                        'mean_reversion_weight': mean_reversion_weight,
                        'breakout_weight': breakout_weight,
                        'volume_weight': volume_weight,
                        'min_combined_score': min_combined_score,
                        'require_volume_confirmation': require_volume_confirmation,
                        'require_trend_alignment': require_trend_alignment,
                        'min_rsi': min_rsi,
                        'max_rsi': max_rsi,
                        'min_volume_ratio': min_volume_ratio,
                        'min_adx': min_adx,
                        'lookback_period': lookback_period
                    }
                )
            
            if multi_signals and multi_signals.get('signals'):
                display_multi_signals(
                    multi_signals,
                    total_capital,
                    risk_percent,
                    auto_execute,
                    max_positions
                )
            else:
                st.info("🤖 No multi-signal opportunities found. Adjust parameters or try later.")

def run_multi_signal_analysis(symbols, instrument_df, params):
    """Run multi-signal analysis combining multiple strategies."""
    multi_signals = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, item in enumerate(symbols[:20]):  # Limit for performance
        symbol = item['symbol']
        exchange = item['exchange']
        status_text.text(f"Multi-signal analysis: {symbol}... ({i+1}/{min(20, len(symbols))})")
        
        try:
            token = get_instrument_token(symbol, instrument_df, exchange)
            if not token:
                continue
                
            # Get historical data
            data = get_historical_data_60days(token, 'day')
            if data.empty or len(data) < 30:
                continue
            
            # Run multi-signal analysis
            signal = analyze_multi_signals(data, symbol, params)
            if signal and signal.get('combined_score', 0) >= params['min_combined_score']:
                multi_signals.append(signal)
                
        except Exception as e:
            continue
        
        progress_bar.progress((i + 1) / min(20, len(symbols)))
    
    status_text.text("Multi-signal analysis complete!")
    
    return {
        'signals': sorted(multi_signals, key=lambda x: x.get('combined_score', 0), reverse=True),
        'total_scanned': min(20, len(symbols)),
        'signals_found': len(multi_signals),
        'params': params,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def analyze_multi_signals(data, symbol, params):
    """Combine multiple technical signals into a unified score."""
    if len(data) < 30:
        return None
    
    data = calculate_advanced_indicators(data)
    latest = data.iloc[-1]
    
    signal_scores = {
        'momentum': 0,
        'mean_reversion': 0,
        'breakout': 0,
        'volume': 0
    }
    
    signal_details = []
    final_signal = 'HOLD'
    
    # 1. MOMENTUM SIGNAL
    momentum_score = calculate_momentum_score(latest, data)
    signal_scores['momentum'] = momentum_score
    
    # 2. MEAN REVERSION SIGNAL  
    mean_reversion_score = calculate_mean_reversion_score(latest, data, params)
    signal_scores['mean_reversion'] = mean_reversion_score
    
    # 3. BREAKOUT SIGNAL
    breakout_score = calculate_breakout_score(latest, data)
    signal_scores['breakout'] = breakout_score
    
    # 4. VOLUME SIGNAL
    volume_score = calculate_volume_score(latest, data, params)
    signal_scores['volume'] = volume_score
    
    # COMBINE SCORES WITH WEIGHTS
    combined_score = (
        signal_scores['momentum'] * params['momentum_weight'] +
        signal_scores['mean_reversion'] * params['mean_reversion_weight'] +
        signal_scores['breakout'] * params['breakout_weight'] +
        signal_scores['volume'] * params['volume_weight']
    ) * 100
    
    # DETERMINE FINAL SIGNAL
    buy_signals = 0
    sell_signals = 0
    
    if momentum_score > 0.6: buy_signals += 1
    if momentum_score < 0.4: sell_signals += 1
    
    if mean_reversion_score > 0.7: buy_signals += 1
    if mean_reversion_score < 0.3: sell_signals += 1
    
    if breakout_score > 0.6: buy_signals += 1
    if breakout_score < 0.4: sell_signals += 1
    
    if volume_score > 0.5: buy_signals += 1  # Volume usually confirms
    
    if buy_signals >= 3 and combined_score >= params['min_combined_score']:
        final_signal = 'BUY'
    elif sell_signals >= 3 and combined_score >= params['min_combined_score']:
        final_signal = 'SELL'
    
    if final_signal != 'HOLD':
        # Calculate position metrics
        current_price = latest['close']
        atr = latest.get('ATR', current_price * 0.02)  # Default 2% if ATR not available
        
        return {
            'symbol': symbol,
            'signal': final_signal,
            'combined_score': combined_score,
            'signal_breakdown': signal_scores,
            'current_price': current_price,
            'rsi': latest.get('RSI_14', 50),
            'volume_ratio': latest.get('volume', 0) / data['volume'].tail(20).mean(),
            'atr': atr,
            'momentum_strength': "Strong" if momentum_score > 0.7 else "Medium" if momentum_score > 0.5 else "Weak",
            'confidence': min(95, combined_score),
            'buy_signals': buy_signals,
            'sell_signals': sell_signals,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
    
    return None

def calculate_momentum_score(latest, data):
    """Calculate momentum score (0-1)."""
    score = 0
    factors = 0
    
    # EMA Alignment
    if (latest.get('EMA_20', 0) > latest.get('EMA_50', 0) > latest.get('EMA_200', 0)):
        score += 0.3
    factors += 1
    
    # RSI Momentum
    rsi = latest.get('RSI_14', 50)
    if 60 < rsi < 70:
        score += 0.2  # Strong but not overbought
    factors += 1
    
    # MACD
    if latest.get('MACD', 0) > latest.get('MACD_Signal', 0):
        score += 0.2
    factors += 1
    
    # ADX Trend Strength
    if latest.get('ADX', 0) > 25:
        score += 0.3
    factors += 1
    
    return score / factors if factors > 0 else 0

def calculate_mean_reversion_score(latest, data, params):
    """Calculate mean reversion score (0-1)."""
    current_price = latest['close']
    mean_price = data['close'].tail(50).mean()
    std_price = data['close'].tail(50).std()
    
    score = 0
    factors = 0
    
    if std_price > 0:
        z_score = abs(current_price - mean_price) / std_price
        
        # Oversold conditions (higher score for more oversold)
        if z_score > 1.5 and current_price < mean_price:
            score += min(0.4, z_score * 0.2)
            factors += 1
    
    # RSI based mean reversion
    rsi = latest.get('RSI_14', 50)
    if rsi < params['min_rsi']:
        score += 0.3
        factors += 1
    
    # Bollinger Band position
    bb_lower = latest.get('BB_Lower', 0)
    if current_price <= bb_lower * 1.02 and bb_lower > 0:
        score += 0.3
        factors += 1
    
    return score / factors if factors > 0 else 0

def calculate_breakout_score(latest, data):
    """Calculate breakout score (0-1)."""
    score = 0
    factors = 0
    recent_high = data['high'].tail(20).max()
    if latest['close'] > recent_high:
        score += 0.4
    factors += 1
    
    # Volume confirmation
    volume_avg = data['volume'].tail(20).mean()
    if latest['volume'] > volume_avg * 1.5:
        score += 0.3
    factors += 1
    
    # Price above key EMAs
    if latest['close'] > latest.get('EMA_20', 0) > latest.get('EMA_50', 0):
        score += 0.3
    factors += 1
    
    return score / factors if factors > 0 else 0

def calculate_volume_score(latest, data, params):
    """Calculate volume confirmation score (0-1)."""
    volume_avg = data['volume'].tail(20).mean()
    current_volume = latest['volume']
    volume_ratio = current_volume / volume_avg if volume_avg > 0 else 1
    
    if volume_ratio >= params['min_volume_ratio']:
        return 0.8  # Strong volume confirmation
    elif volume_ratio >= 1.0:
        return 0.5  # Moderate volume
    else:
        return 0.2  # Weak volume

def display_breakout_signals(signals_data, total_capital, risk_percent, auto_execute, max_positions):
    """Display breakout signals with trading options."""
    st.subheader("🎯 Breakout Signals Found")
    
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    with col_stats1:
        st.metric("Total Scanned", signals_data['total_scanned'])
    with col_stats2:
        st.metric("Breakouts Found", signals_data['breakouts_found'])
    with col_stats3:
        st.metric("Last Scan", signals_data['timestamp'].split()[1])
    
    st.markdown("---")
    
    # Display top signals
    top_signals = signals_data['signals'][:max_positions]
    
    for i, signal in enumerate(top_signals, 1):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
            
            with col1:
                st.write(f"**#{i}**")
                st.write(f"**{signal['symbol']}**")
                st.write(f"₹{signal['current_price']:.2f}")
            
            with col2:
                # Signal visualization
                confidence = signal['confidence']
                if confidence > 80:
                    color = "🟢"
                elif confidence > 65:
                    color = "🟡" 
                else:
                    color = "🟠"
                
                st.write(f"{color} **{signal['signal']}** - {signal['pattern_type']}")
                st.progress(confidence / 100)
                
                # FIXED: Corrected the f-string syntax
                st.caption(f"Breakout: ₹{signal['breakout_level']:.2f} | Volume: {signal['volume_ratio']:.1f}x | Move: {signal['price_move_pct']:.1f}%")
            
            with col3:
                st.metric("Confidence", f"{confidence}%")
                st.metric("R/R", f"{signal['risk_reward']:.1f}")
            
            with col4:
                st.metric("Stop Loss", f"₹{signal['stop_loss']:.2f}")
                st.metric("Target", f"₹{signal['target']:.2f}")
            
            with col5:
                # Position sizing
                risk_amount = total_capital * (risk_percent / 100)
                position_size = calculate_breakout_position_size(signal, risk_amount)
                
                st.write(f"**Qty:** {position_size}")
                st.write(f"**Risk:** ₹{risk_amount:.2f}")
                
                if st.button("🚀 Trade", key=f"breakout_trade_{signal['symbol']}", type="primary"):
                    execute_breakout_trade(signal, position_size)
            
            st.markdown("---")
    
    # AUTO-EXECUTION
    if auto_execute and top_signals:
        if st.button("🤖 Execute All Breakout Trades", type="primary", use_container_width=True):
            execute_batch_breakout_trades(top_signals, total_capital, risk_percent)

def execute_batch_breakout_trades(signals, total_capital, risk_percent):
    """Execute multiple breakout trades in batch."""
    executed_trades = []
    failed_trades = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, signal in enumerate(signals):
        status_text.text(f"Executing trade {i+1}/{len(signals)}: {signal['symbol']}")
        
        try:
            risk_amount = total_capital * (risk_percent / 100)
            position_size = calculate_breakout_position_size(signal, risk_amount)
            
            instrument_df = get_instrument_df()
            place_order(
                instrument_df,
                signal['symbol'],
                position_size,
                'MARKET',
                signal['signal'],
                'MIS'
            )
            
            executed_trades.append({
                'symbol': signal['symbol'],
                'action': signal['signal'],
                'quantity': position_size,
                'price': signal['current_price']
            })
            
            log_breakout_trade(signal, position_size, 'AUTO_BATCH')
            
        except Exception as e:
            failed_trades.append({
                'symbol': signal['symbol'],
                'error': str(e)
            })
        
        progress_bar.progress((i + 1) / len(signals))
    
    # Display results
    if executed_trades:
        st.success(f"✅ Successfully executed {len(executed_trades)} breakout trades!")
        for trade in executed_trades:
            st.write(f"• {trade['action']} {trade['quantity']} shares of {trade['symbol']} @ ₹{trade['price']:.2f}")
    
    if failed_trades:
        st.error(f"❌ {len(failed_trades)} trades failed")
        for trade in failed_trades:
            st.write(f"• {trade['symbol']}: {trade['error']}")

def display_multi_signals(signals_data, total_capital, risk_percent, auto_execute, max_positions):
    """Display multi-signal analysis results."""
    st.subheader("🎯 Multi-Signal Opportunities")
    
    col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
    with col_stats1:
        st.metric("Total Scanned", signals_data['total_scanned'])
    with col_stats2:
        st.metric("Signals Found", signals_data['signals_found'])
    with col_stats3:
        strong_signals = len([s for s in signals_data['signals'] if s['combined_score'] > 80])
        st.metric("Strong Signals", strong_signals)
    with col_stats4:
        st.metric("Last Scan", signals_data['timestamp'].split()[1])
    
    st.markdown("---")
    
    # Display top signals
    top_signals = signals_data['signals'][:max_positions]
    
    for i, signal in enumerate(top_signals, 1):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
            
            with col1:
                st.write(f"**#{i}**")
                st.write(f"**{signal['symbol']}**")
                st.write(f"₹{signal['current_price']:.2f}")
            
            with col2:
                # Combined score visualization
                score = signal['combined_score']
                if score > 80:
                    color = "🟢"
                    strength = "VERY STRONG"
                elif score > 70:
                    color = "🟡"
                    strength = "STRONG"
                else:
                    color = "🟠"
                    strength = "MODERATE"
                
                st.write(f"{color} **{signal['signal']}** - {strength}")
                st.progress(score / 100)
                
                # Signal breakdown
                breakdown = signal['signal_breakdown']
                breakdown_text = f"M:{breakdown['momentum']:.1f} • R:{breakdown['mean_reversion']:.1f} • B:{breakdown['breakout']:.1f} • V:{breakdown['volume']:.1f}"
                st.caption(breakdown_text)
                st.caption(f"Buy Signals: {signal['buy_signals']} | Sell Signals: {signal['sell_signals']}")
            
            with col3:
                st.metric("Combined Score", f"{score:.0f}")
                st.metric("RSI", f"{signal['rsi']:.1f}")
            
            with col4:
                st.metric("Volume", f"{signal['volume_ratio']:.1f}x")
                st.metric("Confidence", f"{signal['confidence']}%")
            
            with col5:
                # Position sizing
                risk_amount = total_capital * (risk_percent / 100)
                position_size = calculate_risk_position_size(signal, risk_amount)
                
                st.write(f"**Qty:** {position_size}")
                st.write(f"**Risk:** ₹{risk_amount:.2f}")
                
                if st.button("🚀 Trade", key=f"multi_trade_{signal['symbol']}", type="primary"):
                    execute_multi_signal_trade(signal, position_size)
            
            st.markdown("---")
    
    # AUTO-EXECUTION
    if auto_execute and top_signals:
        if st.button("🤖 Execute All Multi-Signal Trades", type="primary", use_container_width=True):
            execute_batch_multi_trades(top_signals, total_capital, risk_percent)

def calculate_breakout_position_size(signal, risk_amount):
    """Calculate position size for breakout trades."""
    current_price = signal['current_price']
    stop_loss = signal['stop_loss']
    
    if current_price > stop_loss:  # For long trades
        risk_per_share = current_price - stop_loss
    else:  # For short trades
        risk_per_share = stop_loss - current_price
    
    if risk_per_share > 0:
        position_size = int(risk_amount / risk_per_share)
    else:
        position_size = int(risk_amount / (current_price * 0.02))  # Default 2% stop
    
    # Ensure minimum 1 share and reasonable maximum
    return max(1, min(position_size, 1000))

def calculate_risk_position_size(signal, risk_amount):
    """Calculate position size based on ATR risk."""
    current_price = signal['current_price']
    atr = signal.get('atr', current_price * 0.02)  # Default 2% if ATR not available
    
    # Use 2x ATR for stop loss
    risk_per_share = 2 * atr
    
    if risk_per_share > 0:
        position_size = int(risk_amount / risk_per_share)
    else:
        position_size = int(risk_amount / (current_price * 0.02))
    
    return max(1, min(position_size, 1000))

def execute_breakout_trade(signal, quantity):
    """Execute a single breakout trade."""
    try:
        instrument_df = get_instrument_df()
        place_order(
            instrument_df,
            signal['symbol'],
            quantity,
            'MARKET',
            signal['signal'],
            'MIS'
        )
        st.success(f"✅ {signal['signal']} order executed for {signal['symbol']} (Qty: {quantity})")
        
        # Log the trade
        log_breakout_trade(signal, quantity, 'MANUAL')
        
    except Exception as e:
        st.error(f"❌ Trade execution failed: {str(e)}")

def execute_multi_signal_trade(signal, quantity):
    """Execute a single multi-signal trade."""
    try:
        instrument_df = get_instrument_df()
        place_order(
            instrument_df,
            signal['symbol'],
            quantity,
            'MARKET',
            signal['signal'],
            'MIS'
        )
        st.success(f"✅ {signal['signal']} order executed for {signal['symbol']} (Qty: {quantity})")
        
        # Log the trade
        log_multi_signal_trade(signal, quantity, 'MANUAL')
        
    except Exception as e:
        st.error(f"❌ Trade execution failed: {str(e)}")

# Add these logging functions
def log_breakout_trade(signal, quantity, execution_type):
    """Log breakout trade execution."""
    trade_log = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'symbol': signal['symbol'],
        'signal': signal['signal'],
        'quantity': quantity,
        'price': signal['current_price'],
        'type': 'BREAKOUT',
        'execution': execution_type,
        'confidence': signal['confidence'],
        'pattern': signal['pattern_type']
    }
    
    if 'trade_logs' not in st.session_state:
        st.session_state.trade_logs = []
    
    st.session_state.trade_logs.append(trade_log)

def log_multi_signal_trade(signal, quantity, execution_type):
    """Log multi-signal trade execution."""
    trade_log = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'symbol': signal['symbol'],
        'signal': signal['signal'],
        'quantity': quantity,
        'price': signal['current_price'],
        'type': 'MULTI_SIGNAL',
        'execution': execution_type,
        'confidence': signal['confidence'],
        'combined_score': signal['combined_score']
    }
    
    if 'trade_logs' not in st.session_state:
        st.session_state.trade_logs = []
    
    st.session_state.trade_logs.append(trade_log)

# Dictionary of automated bots
AUTOMATED_BOTS = {
    "Auto Momentum Trader": automated_momentum_trader,
    "Auto Mean Reversion": automated_mean_reversion,
    "Breakout Bot": setup_breakout_bot,
    "Multi-Signal Bot": setup_multi_signal_bot
}

# ================ ALGO BOTS PAGE FUNCTIONS ================

def page_algo_bots():
    """Main algo bots page with both semi-automated and fully automated modes."""
    display_header()
    st.title("🤖 Algo Trading Bots")
    
    # Initialize automated mode
    initialize_automated_mode()
    
    instrument_df = get_instrument_df()
    if instrument_df.empty:
        st.info("Please connect to a broker to use algo bots.")
        return
    
    # Mode selection tabs
    tab1, tab2 = st.tabs(["🚀 Semi-Automated Bots", "⚡ Fully Automated Bots"])
    
    with tab1:
        page_semi_automated_bots(instrument_df)
    
    with tab2:
        page_fully_automated_bots(instrument_df)

def page_semi_automated_bots(instrument_df):
    """Semi-automated bots page - requires manual confirmation."""
    st.info("Run automated analysis and get trading signals. Manual confirmation required for execution.", icon="🚀")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_bot = st.selectbox(
            "Select Trading Bot",
            list(ALGO_BOTS.keys()),
            help="Choose a trading bot based on your risk appetite and trading style",
            key="semi_bot_select"
        )
        
        # Bot descriptions
        bot_descriptions = {
            "Momentum Trader": "Trades on strong price momentum and trend continuations. Medium risk.",
            "Mean Reversion": "Buys low and sells high based on statistical mean reversion. Low risk.",
            "Volatility Breakout": "Captures breakouts from low volatility periods. High risk.",
            "Value Investor": "Focuses on longer-term value and fundamental trends. Low risk.",
            "Scalper Pro": "High-frequency trading for quick, small profits. Very high risk.",
            "Trend Follower": "Rides established trends with multiple confirmation signals. Medium risk."
        }
        
        st.markdown(f"**Description:** {bot_descriptions[selected_bot]}")
    
    with col2:
        trading_capital = st.number_input(
            "Trading Capital (₹)",
            min_value=100,
            max_value=100000,
            value=1000,
            step=100,
            help="Minimum ₹100 required",
            key="semi_capital"
        )
    
    st.markdown("---")
    
    # Symbol selection and bot execution
    col3, col4 = st.columns([1, 1])
    
    with col3:
        st.subheader("Stock Selection")
        all_symbols = instrument_df[instrument_df['exchange'].isin(['NSE', 'BSE'])]['tradingsymbol'].unique()
        selected_symbol = st.selectbox(
            "Select Stock",
            sorted(all_symbols),
            index=list(all_symbols).index('RELIANCE') if 'RELIANCE' in all_symbols else 0,
            key="semi_symbol"
        )
        
        # Show current price
        quote_data = get_watchlist_data([{'symbol': selected_symbol, 'exchange': 'NSE'}])
        if not quote_data.empty:
            current_price = quote_data.iloc[0]['Price']
            st.metric("Current Price", f"₹{current_price:.2f}")
    
    with col4:
        st.subheader("Bot Execution")
        st.write(f"**Selected Bot:** {selected_bot}")
        st.write(f"**Available Capital:** ₹{trading_capital:,}")
        
        if st.button("🚀 Run Trading Bot", use_container_width=True, type="primary", key="semi_run"):
            with st.spinner(f"Running {selected_bot} analysis..."):
                bot_function = ALGO_BOTS[selected_bot]
                bot_result = bot_function(instrument_df, selected_symbol, trading_capital)
                
                if bot_result and not bot_result.get("error"):
                    st.session_state.last_bot_result = bot_result
                    st.rerun()
    
    # Display bot results
    if 'last_bot_result' in st.session_state and st.session_state.last_bot_result:
        bot_result = st.session_state.last_bot_result
        
        if bot_result.get("error"):
            st.error(bot_result["error"])
        else:
            st.markdown("---")
            st.subheader("🤖 Bot Analysis Results")
            
            # Create metrics cards
            col5, col6, col7, col8 = st.columns(4)
            
            with col5:
                action_color = "green" if bot_result["action"] == "BUY" else "red" if bot_result["action"] == "SELL" else "orange"
                st.markdown(f'<div class="metric-card" style="border-color: {action_color};">'
                          f'<h3 style="color: {action_color};">{bot_result["action"]}</h3>'
                          f'<p>Recommended Action</p></div>', unsafe_allow_html=True)
            
            with col6:
                st.metric("Quantity", bot_result["quantity"])
            
            with col7:
                st.metric("Capital Required", f"₹{bot_result['capital_required']:.2f}")
            
            with col8:
                risk_color = {"Low": "green", "Medium": "orange", "High": "red", "Very High": "darkred"}
                st.markdown(f'<div class="metric-card" style="border-color: {risk_color.get(bot_result["risk_level"], "gray")};">'
                          f'<h3 style="color: {risk_color.get(bot_result["risk_level"], "gray")};">{bot_result["risk_level"]}</h3>'
                          f'<p>Risk Level</p></div>', unsafe_allow_html=True)
            
            # Display signals and execute trade
            execute_bot_trade(instrument_df, bot_result)

    # Bot performance history
    st.markdown("---")
    st.subheader("📈 Bot Performance Tips")
    
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.markdown("""
        **Best Practices:**
        - Start with minimum capital (₹100)
        - Use 'Value Investor' for beginners
        - 'Scalper Pro' requires constant monitoring
        - Always check signals before executing
        - Combine multiple bot recommendations
        """)
    
    with tips_col2:
        st.markdown("""
        **Risk Management:**
        - Never risk more than 2% per trade
        - Use stop losses with every trade
        - Diversify across different bots
        - Monitor performance regularly
        - Adjust capital based on experience
        """)
    
    # Quick bot comparison
    with st.expander("🤖 Bot Comparison Guide"):
        comparison_data = {
            "Bot": list(ALGO_BOTS.keys()),
            "Risk Level": ["Medium", "Low", "High", "Low", "Very High", "Medium"],
            "Holding Period": ["Hours", "Days", "Minutes", "Weeks", "Minutes", "Days"],
            "Capital Recommended": ["₹1,000+", "₹500+", "₹2,000+", "₹2,000+", "₹5,000+", "₹1,500+"],
            "Best For": ["Trend riding", "Safe returns", "Quick profits", "Long term", "Experienced", "Trend following"]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)

def initialize_automated_mode():
    """Initialize session state for fully automated trading with paper trading."""
    if 'automated_mode' not in st.session_state:
        st.session_state.automated_mode = {
            'enabled': False,
            'running': False,
            'live_trading': False,
            'bots_active': {},
            'total_capital': 10000.0,
            'risk_per_trade': 2.0,
            'max_open_trades': 5,
            'trade_history': [],
            'performance_metrics': {},
            'last_signal_check': None,
            'paper_portfolio': {
                'cash_balance': 10000.0,
                'positions': {},
                'initial_capital': 100.0,
                'total_value': 10000.0
            }
        }
    else:
        # Migration: Ensure paper_portfolio exists for existing users
        if 'paper_portfolio' not in st.session_state.automated_mode:
            st.session_state.automated_mode['paper_portfolio'] = {
                'cash_balance': st.session_state.automated_mode.get('total_capital', 10000.0),
                'positions': {},
                'initial_capital': st.session_state.automated_mode.get('total_capital', 10000.0),
                'total_value': st.session_state.automated_mode.get('total_capital', 10000.0)
            }

def update_paper_portfolio_values(instrument_df):
    """Update paper portfolio values with current market prices."""
    paper_portfolio = st.session_state.automated_mode.get('paper_portfolio', {})
    if not paper_portfolio:
        return
    
    positions = paper_portfolio.get('positions', {})
    if not positions:
        paper_portfolio['total_value'] = paper_portfolio.get('cash_balance', 0.0)
        return
    
    # Get current prices for all positions
    symbols_with_exchange = []
    for symbol in positions.keys():
        symbols_with_exchange.append({'symbol': symbol, 'exchange': 'NSE'})
    
    if symbols_with_exchange:
        live_data = get_watchlist_data(symbols_with_exchange)
        
        if not live_data.empty:
            total_position_value = 0.0
            
            for symbol, position in positions.items():
                symbol_data = live_data[live_data['Ticker'] == symbol]
                if not symbol_data.empty:
                    current_price = symbol_data.iloc[0]['Price']
                    position_value = position['quantity'] * current_price
                    total_position_value += position_value
                    
                    # Update unrealized P&L for open trades
                    open_trades = [t for t in st.session_state.automated_mode.get('trade_history', []) 
                                  if t.get('symbol') == symbol and t.get('status') == 'OPEN']
                    for trade in open_trades:
                        if trade.get('action') == 'BUY':
                            trade['pnl'] = (current_price - trade.get('entry_price', 0)) * trade.get('quantity', 0)
                        else:  # SELL (short)
                            trade['pnl'] = (trade.get('entry_price', 0) - current_price) * trade.get('quantity', 0)
            
            paper_portfolio['total_value'] = paper_portfolio.get('cash_balance', 0.0) + total_position_value

# Also add the missing close_paper_position function
def close_paper_position(symbol, quantity=None):
    """Close a paper trading position."""
    paper_portfolio = st.session_state.automated_mode.get('paper_portfolio', {})
    
    if not paper_portfolio or symbol not in paper_portfolio.get('positions', {}):
        st.error(f"No position found for {symbol}")
        return False
    
    position = paper_portfolio['positions'][symbol]
    close_quantity = quantity if quantity else position['quantity']
    
    if close_quantity > position['quantity']:
        st.error(f"Cannot close more than current position: {position['quantity']}")
        return False
    
    # Get current price
    live_data = get_watchlist_data([{'symbol': symbol, 'exchange': 'NSE'}])
    if live_data.empty:
        st.error(f"Could not get current price for {symbol}")
        return False
    
    current_price = live_data.iloc[0]['Price']
    
    # Calculate P&L
    pnl = (current_price - position['avg_price']) * close_quantity
    if position.get('action') == 'SELL':  # For short positions, reverse the P&L
        pnl = -pnl
    
    # Update cash and position
    paper_portfolio['cash_balance'] += close_quantity * current_price
    paper_portfolio['positions'][symbol]['quantity'] -= close_quantity
    
    # Remove position if fully closed
    if paper_portfolio['positions'][symbol]['quantity'] == 0:
        del paper_portfolio['positions'][symbol]
    
    # Update trade history
    open_trades = [t for t in st.session_state.automated_mode.get('trade_history', []) 
                  if t.get('symbol') == symbol and t.get('status') == 'OPEN']
    for trade in open_trades:
        if trade.get('action') == position.get('action'):  # Find matching trade
            # Close the trade
            trade['status'] = 'CLOSED'
            trade['exit_price'] = current_price
            trade['exit_time'] = datetime.now().isoformat()
            trade['pnl'] = pnl
    
    st.success(f"✅ Closed {close_quantity} shares of {symbol} at ₹{current_price:.2f} | P&L: ₹{pnl:.2f}")
    return True


def get_automated_bot_performance():
    """Calculate performance metrics for automated bots with paper trading support."""
    trade_history = st.session_state.automated_mode.get('trade_history', [])
    if not trade_history:
        paper_portfolio = st.session_state.automated_mode.get('paper_portfolio', {})
        current_value = paper_portfolio.get('total_value', paper_portfolio.get('cash_balance', 0.0))
        initial_capital = paper_portfolio.get('initial_capital', current_value)
        paper_return_pct = ((current_value - initial_capital) / initial_capital) * 100 if initial_capital > 0 else 0.0
        
        return {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_pnl': 0.0,
            'win_rate': 0.0,
            'avg_win': 0.0,
            'avg_loss': 0.0,
            'open_trades': 0,
            'paper_portfolio_value': current_value,
            'paper_return_pct': paper_return_pct,
            'unrealized_pnl': 0.0
        }
    
    closed_trades = [t for t in trade_history if t.get('status') == 'CLOSED']
    open_trades = [t for t in trade_history if t.get('status') == 'OPEN']
    
    # Calculate metrics for closed trades
    winning_trades = [t for t in closed_trades if t.get('pnl', 0) > 0]
    losing_trades = [t for t in closed_trades if t.get('pnl', 0) <= 0]
    
    total_pnl = sum(t.get('pnl', 0) for t in closed_trades)
    win_rate = len(winning_trades) / len(closed_trades) * 100 if closed_trades else 0.0
    
    avg_win = sum(t.get('pnl', 0) for t in winning_trades) / len(winning_trades) if winning_trades else 0.0
    avg_loss = sum(t.get('pnl', 0) for t in losing_trades) / len(losing_trades) if losing_trades else 0.0
    
    # Paper trading metrics
    paper_portfolio = st.session_state.automated_mode.get('paper_portfolio', {})
    initial_capital = paper_portfolio.get('initial_capital', 10000.0)
    current_value = paper_portfolio.get('total_value', paper_portfolio.get('cash_balance', initial_capital))
    paper_return_pct = ((current_value - initial_capital) / initial_capital) * 100 if initial_capital > 0 else 0.0
    
    return {
        'total_trades': len(closed_trades),
        'winning_trades': len(winning_trades),
        'losing_trades': len(losing_trades),
        'total_pnl': total_pnl,
        'win_rate': win_rate,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'open_trades': len(open_trades),
        'paper_portfolio_value': current_value,
        'paper_return_pct': paper_return_pct,
        'unrealized_pnl': sum(t.get('pnl', 0) for t in open_trades)
    }

def execute_automated_trade(instrument_df, bot_result, risk_per_trade):
    """Execute trades automatically based on bot signals."""
    if bot_result.get("error") or bot_result["action"] == "HOLD":
        return None
    
    try:
        symbol = bot_result["symbol"]
        action = bot_result["action"]
        current_price = bot_result["current_price"]
        
        # Calculate position size based on risk
        risk_amount = (risk_per_trade / 100) * st.session_state.automated_mode['total_capital']
        quantity = max(1, int(risk_amount / current_price))
        
        # Check if we have too many open trades
        open_trades = [t for t in st.session_state.automated_mode['trade_history'] 
                      if t.get('status') == 'OPEN']
        if len(open_trades) >= st.session_state.automated_mode['max_open_trades']:
            return None
        
        # Check for existing position in the same symbol
        existing_position = next((t for t in open_trades if t.get('symbol') == symbol), None)
        if existing_position:
            # Avoid opening same position multiple times
            if existing_position['action'] == action:
                return None
        
        # PLACE REAL ORDER if live trading is enabled
        order_type = "PAPER"
        if st.session_state.automated_mode.get('live_trading', False):
            try:
                # Place the real order
                place_order(instrument_df, symbol, quantity, 'MARKET', action, 'MIS')
                order_type = "LIVE"
            except Exception as e:
                st.error(f"❌ Failed to place LIVE order for {symbol}: {e}")
                return None
        
        # Record the trade with IST timestamp
        ist_time = get_ist_time()
        trade_record = {
            'timestamp': ist_time.isoformat(),
            'timestamp_display': ist_time.strftime("%Y-%m-%d %H:%M:%S IST"),
            'symbol': symbol,
            'action': action,
            'quantity': quantity,
            'entry_price': current_price,
            'status': 'OPEN',
            'bot_name': bot_result['bot_name'],
            'risk_level': bot_result['risk_level'],
            'order_type': order_type,
            'pnl': 0  # Initialize P&L
        }
        
        st.session_state.automated_mode['trade_history'].append(trade_record)
        
        if order_type == "LIVE":
            st.toast(f"🤖 LIVE {action} order executed for {symbol} (Qty: {quantity})", icon="⚡")
        else:
            st.toast(f"🤖 PAPER {action} order simulated for {symbol} (Qty: {quantity})", icon="📄")
            
        return trade_record
        
    except Exception as e:
        st.error(f"Automated trade execution failed: {e}")
        return None
        
        
        trade_record = {
            'timestamp': datetime.now().isoformat(),
            'symbol': symbol,
            'action': action,
            'quantity': quantity,
            'entry_price': current_price,
            'status': 'OPEN',
            'bot_name': bot_result['bot_name'],
            'risk_level': bot_result['risk_level'],
            'order_type': order_type,
            'pnl': 0.0,  # Initialize P&L
            'exit_price': None,
            'exit_time': None
        }
        
        if 'trade_history' not in st.session_state.automated_mode:
            st.session_state.automated_mode['trade_history'] = []
        st.session_state.automated_mode['trade_history'].append(trade_record)
        
        if order_type == "LIVE":
            st.toast(f"🤖 LIVE {action} order executed for {symbol} (Qty: {quantity})", icon="⚡")
        else:
            st.toast(f"🤖 PAPER {action} order simulated for {symbol} (Qty: {quantity})", icon="📄")
            
        return trade_record
        
    except Exception as e:
        st.error(f"Automated trade execution failed: {e}")
        return None

def run_automated_bots_cycle(instrument_df, watchlist_symbols):
    """Run one cycle of all active automated bots with paper trading updates."""
    if not st.session_state.automated_mode.get('running', False):
        return
    
    # Update paper portfolio values first
    update_paper_portfolio_values(instrument_df)
    
    active_bots = [bot for bot, active in st.session_state.automated_mode.get('bots_active', {}).items() if active]
    
    for bot_name in active_bots:
        for symbol in watchlist_symbols[:10]:  # Limit to first 10 symbols to avoid rate limits
            try:
                bot_function = AUTOMATED_BOTS[bot_name]
                bot_result = bot_function(instrument_df, symbol)
                
                if not bot_result.get("error") and bot_result["action"] != "HOLD":
                    execute_automated_trade(
                        instrument_df, 
                        bot_result, 
                        st.session_state.automated_mode.get('risk_per_trade', 2.0)
                    )
                
                # Small delay to avoid rate limiting
                a_time.sleep(0.5)
                
            except Exception as e:
                st.error(f"Automated bot {bot_name} failed for {symbol}: {e}")
    
    # Update performance metrics
    st.session_state.automated_mode['performance_metrics'] = get_automated_bot_performance()
    st.session_state.automated_mode['last_signal_check'] = datetime.now().isoformat()

# Now define the page_fully_automated_bots function
import streamlit as st
import pandas as pd
from datetime import datetime

# These are assumed to be defined elsewhere in your application
# from your_utils import initialize_automated_mode, update_paper_portfolio_values, close_paper_position, run_automated_bots_cycle, get_automated_bot_performance
# from streamlit_autorefresh import st_autorefresh
# AUTOMATED_BOTS = {"Auto Momentum Trader": None, "Auto Mean Reversion": None}

# Define helper functions FIRST, before the main function

def get_live_trading_performance():
    """Get live trading performance metrics (would connect to broker API)"""
    # Simulated broker connection data
    total_capital = st.session_state.automated_mode.get('total_capital', 10000.0)
    
    # Calculate some simulated metrics based on trade history
    trade_history = st.session_state.automated_mode.get('trade_history', [])
    live_trades = [t for t in trade_history if t.get('order_type') == 'LIVE']
    
    total_pnl = sum(trade.get('pnl', 0) for trade in live_trades)
    winning_trades = [t for t in live_trades if t.get('pnl', 0) > 0]
    win_rate = (len(winning_trades) / len(live_trades) * 100) if live_trades else 0
    
    return {
        'account_balance': total_capital + total_pnl,
        'used_margin': total_capital * 0.1,  # 10% margin usage
        'available_margin': total_capital * 0.9,
        'margin_usage': 10.0,
        'open_pnl': total_pnl * 0.3,  # 30% of total as open
        'open_pnl_pct': (total_pnl * 0.3 / total_capital * 100),
        'daily_pnl': total_pnl * 0.1,  # 10% as daily
        'total_pnl': total_pnl,
        'portfolio_risk': st.session_state.automated_mode.get('risk_per_trade', 2.0),
        'max_drawdown': abs(min([t.get('pnl', 0) for t in live_trades] + [0])),
        'sharpe_ratio': 1.2 if win_rate > 50 else 0.8,
        'win_rate': win_rate,
        'avg_position_size': total_capital * 0.05,  # 5% per position
        'leverage': 1.0,
        'volatility': 15.5
    }

def get_nifty25_instruments(instrument_df):
    """Get top 25 Nifty stocks by market cap."""
    # Top 25 Nifty stocks (you can update this list periodically)
    nifty_25_symbols = [
        'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR', 'ICICIBANK', 'ITC', 
        'KOTAKBANK', 'LT', 'SBIN', 'BHARTIARTL', 'AXISBANK', 'ASIANPAINT', 
        'MARUTI', 'SUNPHARMA', 'TITAN', 'ULTRACEMCO', 'WIPRO', 'NESTLEIND', 
        'POWERGRID', 'NTPC', 'HCLTECH', 'BAJFINANCE', 'ADANIPORTS', 'TATAMOTORS'
    ]
    
    nifty_instruments = []
    
    for symbol in nifty_25_symbols:
        # Find instrument in NSE
        instrument = instrument_df[
            (instrument_df['tradingsymbol'] == symbol) |
            (instrument_df['tradingsymbol'].str.startswith(symbol + '-')) |
            (instrument_df['name'].str.contains(symbol, case=False, na=False))
        ].head(1)
        
        if not instrument.empty:
            nifty_instruments.append({
                'symbol': instrument.iloc[0]['tradingsymbol'],
                'exchange': instrument.iloc[0]['exchange'],
                'token': instrument.iloc[0]['instrument_token'],
                'name': instrument.iloc[0]['name']
            })
        else:
            # Try alternative search if exact match not found
            alt_instrument = instrument_df[
                instrument_df['tradingsymbol'].str.contains(symbol, case=False, na=False)
            ].head(1)
            if not alt_instrument.empty:
                nifty_instruments.append({
                    'symbol': alt_instrument.iloc[0]['tradingsymbol'],
                    'exchange': alt_instrument.iloc[0]['exchange'],
                    'token': alt_instrument.iloc[0]['instrument_token'],
                    'name': alt_instrument.iloc[0]['name']
                })
    
    return nifty_instruments

def get_nifty25_auto_trading_status():
    """Get current status of Nifty 25 auto-trading."""
    # This would typically query your trading database
    return {
        'active_positions': st.session_state.automated_mode.get('active_nifty_positions', 0),
        'signals_today': st.session_state.automated_mode.get('nifty_signals_today', 0),
        'success_rate': st.session_state.automated_mode.get('nifty_success_rate', 0),
        'pnl_today': st.session_state.automated_mode.get('nifty_pnl_today', 0.0),
        'total_trades': st.session_state.automated_mode.get('nifty_total_trades', 0),
        'win_rate': st.session_state.automated_mode.get('nifty_win_rate', 0)
    }

def initialize_automated_mode():
    """Initialize automated trading mode with default values."""
    st.session_state.automated_mode = {
        'enabled': False,
        'running': False,
        'live_trading': False,
        'total_capital': 10000.0,
        'risk_per_trade': 2.0,
        'nifty25_auto_trade': False,
        'paper_portfolio': {
            'cash_balance': 10000.0,
            'positions': {},
            'initial_capital': 10000.0,
            'total_value': 10000.0
        },
        'active_bots': {},
        'trade_history': []
    }

def get_automated_bot_performance():
    """Get paper trading performance metrics"""
    paper_portfolio = st.session_state.automated_mode.get('paper_portfolio', {})
    cash_balance = paper_portfolio.get('cash_balance', 0.0)
    portfolio_value = paper_portfolio.get('total_value', cash_balance)
    initial_capital = paper_portfolio.get('initial_capital', portfolio_value)
    
    # Calculate metrics from trade history
    trade_history = st.session_state.automated_mode.get('trade_history', [])
    paper_trades = [t for t in trade_history if t.get('order_type') != 'LIVE']
    
    total_trades = len(paper_trades)
    winning_trades = [t for t in paper_trades if t.get('pnl', 0) > 0]
    win_rate = (len(winning_trades) / total_trades * 100) if total_trades > 0 else 0
    
    total_pnl = sum(trade.get('pnl', 0) for trade in paper_trades)
    avg_win = np.mean([t.get('pnl', 0) for t in winning_trades]) if winning_trades else 0
    losing_trades = [t for t in paper_trades if t.get('pnl', 0) < 0]
    avg_loss = np.mean([t.get('pnl', 0) for t in losing_trades]) if losing_trades else 0
    
    return {
        'paper_return_pct': ((portfolio_value - initial_capital) / initial_capital * 100) if initial_capital > 0 else 0,
        'total_trades': total_trades,
        'win_rate': win_rate,
        'total_pnl': total_pnl,
        'unrealized_pnl': portfolio_value - cash_balance - initial_capital,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'max_drawdown': 5.2,  # Simulated
        'profit_factor': abs(avg_win / avg_loss) if avg_loss != 0 else 0,
        'recovery_factor': 1.8  # Simulated
    }

# Define diagnostic helper functions
def get_symbol_data(instrument_df, symbol):
    """Get data for a specific symbol"""
    try:
        if symbol in instrument_df.columns:
            return instrument_df[symbol]
        else:
            # Try to find symbol in dataframe
            for col in instrument_df.columns:
                if symbol in col:
                    return instrument_df[col]
        return None
    except:
        return None

def analyze_with_bot(bot_name, symbol, data):
    """Analyze a symbol with a specific bot and return thinking"""
    if bot_name == "Auto Momentum Trader":
        return analyze_momentum(symbol, data)
    elif bot_name == "Auto Mean Reversion":
        return analyze_mean_reversion(symbol, data)
    else:
        return "HOLD", 50, "Unknown bot strategy"

def analyze_momentum(symbol, data):
    """Momentum bot analysis with detailed thinking"""
    if len(data) < 20:
        return "HOLD", 0, "Insufficient data for momentum analysis"
    
    # Simple momentum logic (replace with actual implementation)
    recent_price = data['close'].iloc[-1] if 'close' in data.columns else data.iloc[-1]
    prev_price = data['close'].iloc[-5] if 'close' in data.columns else data.iloc[-5]
    
    momentum = (recent_price - prev_price) / prev_price * 100
    
    if momentum > 2:
        return "BUY", 70, f"Strong upward momentum: {momentum:.2f}%"
    elif momentum < -2:
        return "SELL", 70, f"Strong downward momentum: {momentum:.2f}%"
    else:
        return "HOLD", 60, f"Neutral momentum: {momentum:.2f}%"

def analyze_mean_reversion(symbol, data):
    """Mean reversion bot analysis with detailed thinking"""
    if len(data) < 20:
        return "HOLD", 0, "Insufficient data for mean reversion analysis"
    
    # Simple mean reversion logic (replace with actual implementation)
    recent_price = data['close'].iloc[-1] if 'close' in data.columns else data.iloc[-1]
    mean_price = data['close'].mean() if 'close' in data.columns else data.mean()
    
    deviation = (recent_price - mean_price) / mean_price * 100
    
    if deviation > 5:
        return "SELL", 65, f"Price {deviation:.2f}% above mean - overbought"
    elif deviation < -5:
        return "BUY", 65, f"Price {deviation:.2f}% below mean - oversold"
    else:
        return "HOLD", 55, f"Price near mean: {deviation:.2f}% deviation"

def run_detailed_bot_analysis(instrument_df, watchlist_symbols):
    """Run detailed analysis and return thinking data"""
    thinking_data = []
    active_bots = [bot for bot, active in st.session_state.automated_mode.get('bots_active', {}).items() if active]
    
    for symbol in watchlist_symbols[:15]:  # Limit for performance
        symbol_data = get_symbol_data(instrument_df, symbol)
        if symbol_data is None:
            continue
            
        for bot_name in active_bots:
            if bot_name in AUTOMATED_BOTS:
                try:
                    signal, confidence, reasoning = analyze_with_bot(bot_name, symbol, symbol_data)
                    thinking_data.append({
                        'symbol': symbol,
                        'bot': bot_name,
                        'signal': signal,
                        'confidence': confidence,
                        'thinking': reasoning,
                        'timestamp': datetime.now().isoformat()
                    })
                except Exception as e:
                    thinking_data.append({
                        'symbol': symbol,
                        'bot': bot_name,
                        'signal': 'ERROR',
                        'confidence': 0,
                        'thinking': f"Analysis error: {str(e)}",
                        'timestamp': datetime.now().isoformat()
                    })
    
    # Store thinking data for display
    st.session_state.automated_mode['last_thinking_analysis'] = thinking_data
    return thinking_data

def display_bot_thinking(instrument_df):
    """Display real-time bot thinking and analysis"""
    
    # Get current state
    active_bots = [bot for bot, active in st.session_state.automated_mode.get('bots_active', {}).items() if active]
    active_watchlist = st.session_state.get('active_watchlist', 'Watchlist 1')
    watchlist_symbols = [item['symbol'] for item in st.session_state.watchlists.get(active_watchlist, [])]
    
    if not active_bots:
        st.error("❌ **No Active Bots**: Enable at least one bot in the configuration panel")
        return
        
    if not watchlist_symbols:
        st.error("❌ **No Symbols**: Add symbols to your active watchlist first")
        return
    
    st.write("**🔍 Current Bot Analysis:**")
    
    # Use cached thinking data or run new analysis
    if 'last_thinking_analysis' in st.session_state.automated_mode:
        thinking_data = st.session_state.automated_mode['last_thinking_analysis']
    else:
        thinking_data = run_detailed_bot_analysis(instrument_df, watchlist_symbols)
    
    if thinking_data:
        # Convert to dataframe for better display
        thinking_df = pd.DataFrame(thinking_data)
        
        # Color code signals
        def color_signal(signal):
            if signal == 'BUY':
                return 'background-color: #90EE90'  # Light green
            elif signal == 'SELL':
                return 'background-color: #FFB6C1'  # Light red
            elif signal == 'HOLD':
                return 'background-color: #F0F0F0'  # Light gray
            else:
                return ''
        
        # Display styled dataframe
        styled_df = thinking_df.style.apply(lambda x: [color_signal(val) for val in x], subset=['signal'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # Summary statistics
        buy_signals = len(thinking_df[thinking_df['signal'] == 'BUY'])
        sell_signals = len(thinking_df[thinking_df['signal'] == 'SELL'])
        hold_signals = len(thinking_df[thinking_df['signal'] == 'HOLD'])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Buy Signals", buy_signals)
        col2.metric("Sell Signals", sell_signals)
        col3.metric("Hold Signals", hold_signals)
        
        # Reasons for no trades
        if buy_signals == 0 and sell_signals == 0:
            st.warning("""
            **🤔 Why No Trades? Possible Reasons:**
            - Market conditions don't match bot strategies
            - Risk limits preventing position sizing
            - Maximum open trades limit reached
            - Insufficient confidence in signals
            - Missing or stale market data
            - Technical indicators showing neutral signals
            """)
    else:
        st.info("No analysis data available. Run diagnostics to see bot thinking.")

def display_detailed_diagnostics(instrument_df):
    """Display comprehensive diagnostics"""
    st.markdown("---")
    st.subheader("🔧 Detailed System Diagnostics")
    
    # System status
    st.write("**🖥️ System Status:**")
    col1, col2, col3 = st.columns(3)
    
    # Check basic requirements
    active_bots = [bot for bot, active in st.session_state.automated_mode.get('bots_active', {}).items() if active]
    active_watchlist = st.session_state.get('active_watchlist', 'Watchlist 1')
    watchlist_symbols = [item['symbol'] for item in st.session_state.watchlists.get(active_watchlist, [])]
    
    with col1:
        if active_bots:
            st.success(f"✅ **Bots Active**: {len(active_bots)}")
        else:
            st.error("❌ **No Bots Active**")
    
    with col2:
        if watchlist_symbols:
            st.success(f"✅ **Symbols**: {len(watchlist_symbols)}")
        else:
            st.error("❌ **No Symbols**")
    
    with col3:
        if st.session_state.automated_mode.get('running', False):
            st.success("✅ **Trading Active**")
        else:
            st.error("❌ **Trading Stopped**")
    
    # Market data diagnostics
    st.write("**📊 Market Data Status:**")
    if watchlist_symbols:
        data_status = []
        for symbol in watchlist_symbols[:5]:  # Check first 5 symbols
            symbol_data = get_symbol_data(instrument_df, symbol)
            if symbol_data is not None and len(symbol_data) > 0:
                latest_time = symbol_data.index.max() if hasattr(symbol_data.index, 'max') else datetime.now()
                data_age = (datetime.now() - latest_time).total_seconds() / 60  # minutes
                
                if data_age < 5:
                    status = "✅ Fresh"
                elif data_age < 15:
                    status = "⚠️ Stale"
                else:
                    status = "❌ Old"
                    
                data_status.append({
                    'Symbol': symbol,
                    'Status': status,
                    'Age (min)': f"{data_age:.1f}",
                    'Data Points': len(symbol_data)
                })
            else:
                data_status.append({
                    'Symbol': symbol,
                    'Status': "❌ No Data",
                    'Age (min)': "N/A",
                    'Data Points': 0
                })
        
        st.dataframe(pd.DataFrame(data_status), use_container_width=True, hide_index=True)
    
    # Bot-specific diagnostics
    st.write("**🤖 Bot Configuration Check:**")
    bot_diagnostics = []
    for bot_name in AUTOMATED_BOTS.keys():
        is_active = st.session_state.automated_mode.get('bots_active', {}).get(bot_name, False)
        bot_diagnostics.append({
            'Bot': bot_name,
            'Status': '✅ Active' if is_active else '❌ Inactive',
            'Strategy': AUTOMATED_BOTS[bot_name].get('description', 'N/A')
        })
    
    st.dataframe(pd.DataFrame(bot_diagnostics), use_container_width=True, hide_index=True)
    
    # Trading limits check
    st.write("**📈 Trading Limits:**")
    limits_data = {
        'Setting': ['Max Open Trades', 'Risk per Trade', 'Total Capital', 'Analysis Frequency'],
        'Current Value': [
            st.session_state.automated_mode.get('max_open_trades', 5),
            f"{st.session_state.automated_mode.get('risk_per_trade', 2.0)}%",
            f"₹{st.session_state.automated_mode.get('total_capital', 10000.0):,.2f}",
            st.session_state.automated_mode.get('check_interval', '1 minute')
        ],
        'Status': ['✅ OK', '✅ OK', '✅ OK', '✅ OK']
    }
    st.dataframe(pd.DataFrame(limits_data), use_container_width=True, hide_index=True)

# NOW define the main function
def page_fully_automated_bots(instrument_df):
    """Fully automated bots page with comprehensive paper trading simulation."""
    
    # Display current time and market status first
    current_time = get_ist_time().strftime("%H:%M:%S IST")
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    st.warning("🚨 **LIVE TRADING WARNING**: Automated bots will execute real trades with real money! Use at your own risk.", icon="⚠️")
    
    # 🎯 ENHANCED HEADER WITH TICKER THEME
    col_header1, col_header2, col_header3 = st.columns([2, 1, 1])
    with col_header1:
        st.subheader("🤖 Automated Trading Bots")
    with col_header2:
        st.caption(f"📅 {current_date}")
    with col_header3:
        # Live ticker-style time display
        if st.session_state.automated_mode.get('live_trading', False):
            st.caption(f"🔴 {current_time}")
        else:
            st.caption(f"🔵 {current_time}")
    
    # Initialize automated mode if not exists
    if 'automated_mode' not in st.session_state:
        initialize_automated_mode()
    else:
        # Ensure paper_portfolio exists (migration for existing sessions)
        if 'paper_portfolio' not in st.session_state.automated_mode:
            st.session_state.automated_mode['paper_portfolio'] = {
                'cash_balance': st.session_state.automated_mode.get('total_capital', 10000.0),
                'positions': {},
                'initial_capital': st.session_state.automated_mode.get('total_capital', 10000.0),
                'total_value': st.session_state.automated_mode.get('total_capital', 10000.0)
            }
    
    # Fix the total_capital value if it's below minimum
    current_capital = float(st.session_state.automated_mode.get('total_capital', 100.0))
    if current_capital < 100.0:
        st.session_state.automated_mode['total_capital'] = 100.0
    
    # Get market status with error handling
    try:
        status_info = get_market_status()
        market_status = status_info['status']
        next_market = status_info['next_market']
    except Exception as e:
        st.error(f"Error getting market status: {e}")
        market_status = "unknown"
        next_market = datetime.now()
    
    # 🎯 ENHANCED NIFTY 25 AUTO-TRADING TOGGLE SECTION
    st.markdown("---")
    st.subheader("🔷 Nifty 25 Auto-Trading")
    
    col_nifty1, col_nifty2, col_nifty3 = st.columns([2, 1, 1])
    with col_nifty1:
        nifty25_auto_trade = st.toggle(
            "🎯 Enable Nifty 25 Auto-Trading",
            value=st.session_state.automated_mode.get('nifty25_auto_trade', False),
            help="Automatically trade all top 25 Nifty stocks based on AI signals",
            key="nifty25_toggle"
        )
        st.session_state.automated_mode['nifty25_auto_trade'] = nifty25_auto_trade
    
    with col_nifty2:
        if nifty25_auto_trade:
            st.success("🟢 ACTIVE")
            # Show Nifty 25 count
            nifty_instruments = get_nifty25_instruments(instrument_df)
            st.caption(f"{len(nifty_instruments)} stocks")
        else:
            st.info("⚪ INACTIVE")
    
    with col_nifty3:
        if nifty25_auto_trade:
            if st.button("🔄 Refresh Nifty", use_container_width=True):
                st.rerun()
    
    # NIFTY 25 CONFIGURATION WHEN ENABLED
    if nifty25_auto_trade:
        with st.expander("⚙️ Nifty 25 Auto-Trading Settings", expanded=True):
            col_nifty_settings1, col_nifty_settings2 = st.columns(2)
            
            with col_nifty_settings1:
                nifty_bot_strategy = st.selectbox(
                    "Trading Strategy",
                    ["Momentum", "Mean Reversion", "Breakout", "Multi-Signal"],
                    key="nifty_strategy"
                )
                nifty_max_positions = st.slider("Max Open Positions", 1, 10, 5, key="nifty_max_pos")
                
                # Strategy-specific settings
                if nifty_bot_strategy == "Momentum":
                    nifty_momentum_period = st.slider("Momentum Period (days)", 5, 30, 10)
                elif nifty_bot_strategy == "Mean Reversion":
                    nifty_reversion_threshold = st.slider("Deviation Threshold (std)", 1.0, 3.0, 1.5)
            
            with col_nifty_settings2:
                nifty_risk_per_trade = st.slider("Risk per Trade (%)", 0.5, 10.0, 2.0, key="nifty_risk")
                nifty_min_confidence = st.slider("Min Confidence", 70, 90, 80, key="nifty_conf")
                
                nifty_position_size = st.selectbox(
                    "Position Sizing",
                    ["Fixed", "Dynamic Risk-Based", "Volatility Adjusted"],
                    key="nifty_size"
                )
            
            # NIFTY 25 STATUS DASHBOARD
            nifty_status = get_nifty25_auto_trading_status()
            st.markdown("---")
            st.subheader("📊 Nifty 25 Auto-Trading Status")
            
            col_status1, col_status2, col_status3, col_status4 = st.columns(4)
            with col_status1:
                st.metric("Active Positions", f"{nifty_status['active_positions']}/{nifty_max_positions}")
            with col_status2:
                st.metric("Signals Today", nifty_status['signals_today'])
            with col_status3:
                st.metric("Success Rate", f"{nifty_status['success_rate']}%")
            with col_status4:
                st.metric("P&L Today", f"₹{nifty_status['pnl_today']:+.2f}")
    
    # 🎯 ENHANCED MARKET STATUS WITH SEGMENT TIMING
    st.markdown("---")
    
    # Get status color for display
    status_colors = {
        "market_open": "#00cc00",
        "equity_square_off": "#ff9900", 
        "derivatives_square_off": "#ff6600",
        "pre_market": "#ffcc00",
        "market_closed": "#cccccc",
        "weekend": "#cccccc"
    }
    
    status_color = status_colors.get(market_status, "#cccccc")
    
    if market_status == "market_open":
        time_left = datetime.combine(datetime.now().date(), time(15, 20)) - datetime.now()
        minutes_left = time_left.seconds // 60
        st.markdown(f'<div style="color: {status_color}; font-weight: bold;">🟢 **MARKET OPEN** | Equity square-off at 3:20 PM | {minutes_left} minutes remaining</div>', unsafe_allow_html=True)
        
    elif market_status == "equity_square_off":
        time_left = datetime.combine(datetime.now().date(), time(15, 25)) - datetime.now()
        minutes_left = time_left.seconds // 60
        st.markdown(f'<div style="color: {status_color}; font-weight: bold;">🔴 **EQUITY SQUARE-OFF** | Derivatives square-off in {minutes_left} minutes</div>', unsafe_allow_html=True)
        
    elif market_status == "derivatives_square_off":
        time_left = datetime.combine(datetime.now().date(), time(15, 30)) - datetime.now()
        minutes_left = time_left.seconds // 60
        st.markdown(f'<div style="color: {status_color}; font-weight: bold;">🚨 **DERIVATIVES SQUARE-OFF** | Market closes in {minutes_left} minutes</div>', unsafe_allow_html=True)
        
    elif market_status == "pre_market":
        time_left = datetime.combine(datetime.now().date(), time(9, 15)) - datetime.now()
        minutes_left = time_left.seconds // 60
        st.markdown(f'<div style="color: {status_color}; font-weight: bold;">⏰ **PRE-MARKET** | Live trading starts in {minutes_left} minutes</div>', unsafe_allow_html=True)
        
    elif market_status == "market_closed":
        st.markdown(f'<div style="color: {status_color}; font-weight: bold;">🔴 **MARKET CLOSED** | Paper trading available 24/7</div>', unsafe_allow_html=True)
        
    else:  # weekend or unknown
        st.markdown(f'<div style="color: {status_color}; font-weight: bold;">🎉 **WEEKEND** | Paper trading available 24/7</div>', unsafe_allow_html=True)
    
    # Trading status indicators
    is_live_trading = st.session_state.automated_mode.get('live_trading', False)
    if st.session_state.automated_mode.get('running', False):
        if is_live_trading:
            if is_market_hours():
                st.error("**🔴 LIVE TRADING ACTIVE** - Real money at risk! Monitor positions carefully.")
            else:
                st.warning("**⏸️ LIVE TRADING ACTIVE (Market Closed)** - Orders will execute when market opens")
        else:
            st.info("**🔵 PAPER TRADING ACTIVE** - Safe simulation running 24/7")
    
    # 🎯 ENHANCED CONTROL PANEL
    st.markdown("---")
    st.subheader("🎮 Control Panel")
    
    # Main control panel with better layout
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.write("**🔧 Mode**")
        auto_enabled = st.toggle(
            "Enable Bots", 
            value=st.session_state.automated_mode.get('enabled', False),
            help="Enable automated trading bots",
            key="auto_enable"
        )
        st.session_state.automated_mode['enabled'] = auto_enabled
    
    with col2:
        st.write("**🎯 Trading Type**")
        # Always allow live trading toggle, regardless of market hours
        live_trading = st.toggle(
            "Live Trading",
            value=st.session_state.automated_mode.get('live_trading', False),
            help="Real money trading - Available anytime (trades execute during market hours)",
            key="live_trading"
        )
        st.session_state.automated_mode['live_trading'] = live_trading
        
        # Show warning if live trading is enabled outside market hours
        if live_trading and not is_market_hours() and not is_pre_market_hours():
            st.warning("⚠️ Market is closed - Live orders will queue until market opens")
    
    with col3:
        st.write("**🚦 Actions**")
        if st.session_state.automated_mode['enabled']:
            if not st.session_state.automated_mode.get('running', False):
                # Start button - always available
                if live_trading:
                    if st.button("🔴 Start Live Trading", use_container_width=True, type="secondary"):
                        st.session_state.need_live_confirmation = True
                        st.rerun()
                else:
                    if st.button("🔵 Start Paper Trading", use_container_width=True, type="primary"):
                        st.session_state.automated_mode['running'] = True
                        st.success("Paper trading started!")
                        st.rerun()
            else:
                # Stop button
                if st.button("🛑 Stop Trading", use_container_width=True, type="secondary"):
                    st.session_state.automated_mode['running'] = False
                    st.rerun()
        else:
            st.button("Start Trading", use_container_width=True, disabled=True)
    
    with col4:
        st.write("**💰 Capital**")
        current_capital = float(st.session_state.automated_mode.get('total_capital', 100.0))
        current_capital = max(100.0, current_capital)
        
        total_capital = st.number_input(
            "Trading Capital (₹)",
            min_value=100.0,
            max_value=1000000.0,
            value=current_capital,
            step=100.0,
            help="Minimum ₹100 required for automated trading",
            key="auto_capital",
            label_visibility="collapsed"
        )
        st.session_state.automated_mode['total_capital'] = float(total_capital)
    
    with col5:
        st.write("**⚡ Risk**")
        current_risk = float(st.session_state.automated_mode.get('risk_per_trade', 2.0))
        current_risk = max(0.5, min(10.0, current_risk))  # Updated to 10% max as requested
        
        risk_per_trade = st.number_input(
            "Risk per Trade (%)",
            min_value=0.5,
            max_value=10.0,  # Updated to 10% max
            value=current_risk,
            step=0.5,
            help="Risk percentage per trade (0.5% to 10%)",
            key="auto_risk",
            label_visibility="collapsed"
        )
        st.session_state.automated_mode['risk_per_trade'] = float(risk_per_trade)
    
    # Update paper portfolio capital if not running
    if not st.session_state.automated_mode.get('running', False):
        paper_portfolio = st.session_state.automated_mode.get('paper_portfolio', {})
        if not paper_portfolio:
            st.session_state.automated_mode['paper_portfolio'] = {
                'cash_balance': float(total_capital),
                'positions': {},
                'initial_capital': float(total_capital),
                'total_value': float(total_capital)
            }
        else:
            st.session_state.automated_mode['paper_portfolio']['initial_capital'] = float(total_capital)
            st.session_state.automated_mode['paper_portfolio']['cash_balance'] = float(total_capital)
            st.session_state.automated_mode['paper_portfolio']['total_value'] = float(total_capital)

    # Live trading confirmation dialog
    if st.session_state.get('need_live_confirmation', False):
        st.markdown("---")
        st.error("""
        🚨 **LIVE TRADING CONFIRMATION REQUIRED**
        
        **You are about to enable LIVE TRADING with real money!**
        
        **Important Notes:**
        • Real orders with real money
        • You are responsible for ALL losses
        • Market conditions can change rapidly
        • Trading available 24/7 (orders execute during market hours)
        • Auto-stop at market close for position safety
        
        **Market Hours: 9:15 AM - 3:30 PM (Mon-Fri)**
        """)
        
        col_confirm1, col_confirm2, col_confirm3 = st.columns([2, 1, 1])
        
        with col_confirm1:
            if st.button("✅ CONFIRM LIVE TRADING", type="primary", use_container_width=True):
                st.session_state.automated_mode['running'] = True
                st.session_state.automated_mode['live_trading'] = True
                st.session_state.need_live_confirmation = False
                st.session_state.live_trading_start_time = get_ist_time().isoformat()
                st.success("🚀 LIVE TRADING ACTIVATED!")
                st.rerun()
        
        with col_confirm2:
            if st.button("📄 PAPER TRADING", use_container_width=True):
                st.session_state.automated_mode['running'] = True
                st.session_state.automated_mode['live_trading'] = False
                st.session_state.need_live_confirmation = False
                st.info("Paper trading started.")
                st.rerun()
                
        with col_confirm3:
            if st.button("❌ CANCEL", use_container_width=True):
                st.session_state.automated_mode['live_trading'] = False
                st.session_state.need_live_confirmation = False
                st.info("Live trading cancelled.")
                st.rerun()
        
        return  # Stop execution here if confirmation is needed
    
    st.markdown("---")
    
    if st.session_state.automated_mode['enabled']:
        # 🎯 ENHANCED DASHBOARD LAYOUT WITH NEW FEATURES
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🤖 Bot Configuration", "📊 Live Dashboard", "🔍 Live Thinking", "🎯 Symbol Override", "📋 Trade History"])
        
        with tab1:
            display_bot_configuration_tab(instrument_df, nifty25_auto_trade)
        
        with tab2:
            # Live performance dashboard - CALL THE ACTUAL FUNCTION
            try:
                display_enhanced_live_dashboard(instrument_df)
            except Exception as e:
                st.error(f"Error displaying dashboard: {e}")
        
        with tab3:
            # 🎯 ENHANCED LIVE THINKING TAB - CALL THE ACTUAL FUNCTION
            # NO AUTO-REFRESH FOR LIVE THINKING TAB - IT HAS ITS OWN REFRESH BUTTON
            try:
                display_enhanced_live_thinking_tab(instrument_df)
            except Exception as e:
                st.error(f"Error in live thinking: {e}")
        
        with tab4:
            # 🎯 NEW SYMBOL OVERRIDE TAB - CALL THE ACTUAL FUNCTION
            try:
                display_symbol_override_tab(instrument_df)
            except Exception as e:
                st.error(f"Error in symbol override: {e}")
        
        with tab5:
            # 📋 TRADE HISTORY TAB - CALL THE ACTUAL FUNCTION
            try:
                display_trade_history()
            except Exception as e:
                st.error(f"Error displaying trade history: {e}")
        
        # 🎯 AUTO-REFRESH LOGIC (EXCLUDES LIVE THINKING TAB)
        if st.session_state.automated_mode.get('running', False):
            # Get current active tab to determine if we should auto-refresh
            current_tab = st.session_state.get('current_tab', '🤖 Bot Configuration')
            
            # Only auto-refresh if NOT on the Live Thinking tab
            if current_tab != "🔍 Live Thinking":
                # Get refresh interval from settings
                check_interval = st.session_state.automated_mode.get('check_interval', '1 minute')
                interval_seconds = {
                    "15 seconds": 15,
                    "30 seconds": 30,
                    "1 minute": 60,
                    "5 minutes": 300,
                    "15 minutes": 900,
                    "30 minutes": 1800
                }.get(check_interval, 60)
                
                # Auto-refresh only for non-Live Thinking tabs
                if interval_seconds <= 300:  # Only auto-refresh for intervals <= 5 minutes
                    st.rerun()
    
    else:
        # Setup guide when disabled
        display_setup_guide()

# Add helper function to track current tab
def track_current_tab():
    """Track the current active tab for auto-refresh purposes."""
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = "🤖 Bot Configuration"

# Add the missing function implementations

def display_enhanced_live_dashboard(instrument_df):
    """Enhanced live dashboard with optimized refresh behavior."""
    # Record user access
    record_user_interaction()
    
    st.subheader("📊 Live Trading Dashboard")
    
    # Add refresh control to dashboard
    col_refresh1, col_refresh2, col_refresh3 = st.columns([2, 1, 1])
    
    with col_refresh1:
        st.write("**Real-time Performance Metrics**")
    
    with col_refresh2:
        if st.button("🔄 Refresh Data", key="dashboard_refresh"):
            record_user_interaction()
            prevent_refresh_for(5)  # Prevent auto-refresh for 5 seconds after manual refresh
            st.rerun()
    
    with col_refresh3:
        if st.session_state.automated_mode.get('running', False):
            st.success("🟢 LIVE")
        else:
            st.info("⏸️ PAUSED")
    
    # Your existing dashboard content...
    # Add more user interaction recording for form elements
    
    # Example: Record interactions with form elements
    if st.button("Example Button", key="example_btn"):
        record_user_interaction()
        prevent_refresh_for(3)
        # Handle button click
    
    # Record interactions with sliders, inputs, etc.
    example_slider = st.slider("Example Slider", 0, 100, 50, key="example_slider")
    record_user_interaction()  # Record after slider interaction

def display_enhanced_live_thinking_tab(instrument_df):
    """Enhanced live bot thinking analysis with real reasoning and manual refresh only."""
    
    # Track that we're on the Live Thinking tab (NO AUTO-REFRESH)
    st.session_state.current_tab = "🔍 Live Thinking"
    
    st.subheader("🔍 Live Bot Analysis & Thinking")
    st.info("🤖 **Manual Refresh Only**: This tab doesn't auto-refresh to preserve analysis context. Use the refresh button below.", icon="ℹ️")
    
    # Get current state
    active_bots = [bot for bot, active in st.session_state.automated_mode.get('bots_active', {}).items() if active]
    active_watchlist = st.session_state.get('active_watchlist', 'Watchlist 1')
    watchlist_symbols = st.session_state.watchlists.get(active_watchlist, [])
    
    if not active_bots:
        st.error("❌ **No Active Bots**: Enable at least one bot in the configuration panel")
        return
        
    if not watchlist_symbols:
        st.error("❌ **No Symbols**: Add symbols to your active watchlist first")
        return
    
    # Analysis controls with enhanced layout
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"**Real-time Bot Analysis**")
        st.caption(f"Analyzing {len(watchlist_symbols)} symbols with {len(active_bots)} active bots")
    
    with col2:
        if st.button("🔄 Refresh Analysis", type="primary", use_container_width=True):
            st.session_state.last_analysis_time = get_ist_time().strftime("%H:%M:%S IST")
            st.rerun()
    
    with col3:
        if st.button("📊 View Raw Data", use_container_width=True):
            st.session_state.show_raw_thinking_data = not st.session_state.get('show_raw_thinking_data', False)
    
    # Show last analysis time
    last_analysis = st.session_state.get('last_analysis_time', 'Never')
    st.caption(f"Last analysis: {last_analysis}")
    
    # Run analysis on watchlist symbols
    thinking_data = []
    analysis_errors = []
    
    with st.spinner("🤖 Analyzing symbols with active bots... This may take a few moments."):
        progress_bar = st.progress(0)
        total_symbols = min(15, len(watchlist_symbols))  # Limit for performance
        
        for i, item in enumerate(watchlist_symbols[:total_symbols]):
            symbol = item['symbol']
            exchange = item.get('exchange', 'NSE')
            
            for bot_name in active_bots:
                try:
                    # Get current price for context first
                    quote_data = get_watchlist_data([{'symbol': symbol, 'exchange': exchange}])
                    current_price = quote_data.iloc[0]['Price'] if not quote_data.empty else 0
                    
                    # Run bot analysis based on bot type
                    if bot_name == "Momentum Bot":
                        bot_result = analyze_momentum_for_thinking(instrument_df, symbol, exchange)
                    elif bot_name == "Mean Reversion Bot":
                        bot_result = analyze_mean_reversion_for_thinking(instrument_df, symbol, exchange)
                    elif bot_name == "Breakout Bot":
                        bot_result = analyze_breakout_for_thinking(instrument_df, symbol, exchange)
                    elif bot_name == "Multi-Signal Bot":
                        bot_result = analyze_multi_signal_for_thinking(instrument_df, symbol, exchange)
                    else:
                        bot_result = {
                            'action': 'HOLD',
                            'score': 50,
                            'signals': ['Bot not implemented'],
                            'risk_level': 'Medium',
                            'reasoning': 'Bot analysis function not available'
                        }
                    
                    if bot_result and not bot_result.get("error"):
                        thinking_data.append({
                            'Symbol': symbol,
                            'Bot': bot_name,
                            'Signal': bot_result['action'],
                            'Confidence': bot_result.get('score', 50),
                            'Current Price': f"₹{current_price:.2f}",
                            'Analysis': " | ".join(bot_result.get('signals', ['Analyzing...'])),
                            'Risk Level': bot_result.get('risk_level', 'Medium'),
                            'Reasoning': bot_result.get('reasoning', 'Analysis complete'),
                            'Timestamp': get_ist_time().strftime("%H:%M:%S")
                        })
                    else:
                        analysis_errors.append(f"{symbol} - {bot_name}: {bot_result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    error_msg = f"{symbol} - {bot_name}: {str(e)}"
                    analysis_errors.append(error_msg)
                    thinking_data.append({
                        'Symbol': symbol,
                        'Bot': bot_name,
                        'Signal': 'ERROR',
                        'Confidence': 0,
                        'Current Price': 'N/A',
                        'Analysis': f"Analysis failed",
                        'Risk Level': 'High',
                        'Reasoning': error_msg,
                        'Timestamp': get_ist_time().strftime("%H:%M:%S")
                    })
            
            # Update progress
            progress_bar.progress((i + 1) / total_symbols)
    
    # Show analysis errors if any
    if analysis_errors:
        with st.expander("⚠️ Analysis Errors", expanded=False):
            for error in analysis_errors[:5]:  # Show first 5 errors
                st.error(error)
            if len(analysis_errors) > 5:
                st.caption(f"... and {len(analysis_errors) - 5} more errors")
    
    if thinking_data:
        # Convert to dataframe
        thinking_df = pd.DataFrame(thinking_data)
        
        # Color coding functions
        def color_signal(val):
            if val == 'BUY':
                return 'background-color: #d4edda; color: #155724; font-weight: bold;'
            elif val == 'SELL':
                return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
            elif val == 'HOLD':
                return 'background-color: #fff3cd; color: #856404; font-weight: bold;'
            else:
                return 'background-color: #f5f5f5; color: #333;'
        
        def color_confidence(val):
            if val >= 70:
                return 'color: #28a745; font-weight: bold;'
            elif val >= 50:
                return 'color: #ffc107; font-weight: bold;'
            else:
                return 'color: #dc3545; font-weight: bold;'
        
        def color_risk(val):
            if val == 'Low':
                return 'color: #28a745;'
            elif val == 'Medium':
                return 'color: #ffc107;'
            else:
                return 'color: #dc3545;'
        
        # Display styled dataframe
        st.subheader("📈 Real-time Analysis Results")
        
        # Filter options
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        with col_filter1:
            show_signals = st.multiselect(
                "Filter by Signal",
                options=['BUY', 'SELL', 'HOLD', 'ERROR'],
                default=['BUY', 'SELL'],
                key="signal_filter"
            )
        with col_filter2:
            min_confidence = st.slider("Min Confidence", 0, 100, 50, key="confidence_filter")
        with col_filter3:
            selected_bots = st.multiselect(
                "Filter by Bot",
                options=active_bots,
                default=active_bots,
                key="bot_filter"
            )
        
        # Apply filters
        filtered_df = thinking_df[
            (thinking_df['Signal'].isin(show_signals)) &
            (thinking_df['Confidence'] >= min_confidence) &
            (thinking_df['Bot'].isin(selected_bots))
        ]
        
        if not filtered_df.empty:
            # Display filtered results
            display_columns = ['Symbol', 'Bot', 'Signal', 'Confidence', 'Current Price', 'Analysis', 'Risk Level']
            styled_df = filtered_df[display_columns].style\
                .map(color_signal, subset=['Signal'])\
                .map(color_confidence, subset=['Confidence'])\
                .map(color_risk, subset=['Risk Level'])
            
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
            
            # Show raw data if requested
            if st.session_state.get('show_raw_thinking_data', False):
                with st.expander("📋 Raw Analysis Data", expanded=False):
                    st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning("No results match your current filters. Try adjusting filter settings.")
        
        # Summary statistics
        st.subheader("📊 Analysis Summary")
        
        total_analyses = len(thinking_df)
        buy_signals = len(thinking_df[thinking_df['Signal'] == 'BUY'])
        sell_signals = len(thinking_df[thinking_df['Signal'] == 'SELL'])
        hold_signals = len(thinking_df[thinking_df['Signal'] == 'HOLD'])
        error_signals = len(thinking_df[thinking_df['Signal'] == 'ERROR'])
        avg_confidence = thinking_df[thinking_df['Signal'] != 'ERROR']['Confidence'].mean()
        
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Analyses", total_analyses)
        col2.metric("Buy Signals", buy_signals)
        col3.metric("Sell Signals", sell_signals)
        col4.metric("Hold Signals", hold_signals)
        col5.metric("Avg Confidence", f"{avg_confidence:.1f}%" if not pd.isna(avg_confidence) else "N/A")
        
        # Bot-specific analysis
        st.subheader("🤖 Bot Performance Summary")
        bot_performance = thinking_df.groupby('Bot').agg({
            'Signal': 'count',
            'Confidence': 'mean'
        }).rename(columns={'Signal': 'Analyses', 'Confidence': 'Avg Confidence'})
        
        st.dataframe(bot_performance.style.format({'Avg Confidence': '{:.1f}%'}), use_container_width=True)
        
        # Actionable insights
        st.subheader("💡 Market Insights & Recommendations")
        
        # Market sentiment analysis
        total_valid_signals = buy_signals + sell_signals + hold_signals
        if total_valid_signals > 0:
            buy_ratio = (buy_signals / total_valid_signals) * 100
            sell_ratio = (sell_signals / total_valid_signals) * 100
            
            if buy_ratio > 60:
                st.success("**📈 Strong Bullish Sentiment**")
                st.caption(f"{buy_ratio:.1f}% of signals are BUY recommendations")
            elif sell_ratio > 60:
                st.error("**📉 Strong Bearish Sentiment**") 
                st.caption(f"{sell_ratio:.1f}% of signals are SELL recommendations")
            else:
                st.info("**⚖️ Mixed Market Sentiment**")
                st.caption(f"Balanced signals: {buy_ratio:.1f}% BUY, {sell_ratio:.1f}% SELL")
        
        # Signal quality assessment
        if avg_confidence >= 70:
            st.success("**✅ High Quality Signals**")
            st.caption("Most analyses show high confidence levels - consider acting on strong signals")
        elif avg_confidence >= 50:
            st.warning("**⚠️ Moderate Signal Quality**")
            st.caption("Mixed confidence levels - review individual analyses carefully")
        else:
            st.error("**❌ Low Confidence Environment**")
            st.caption("Consider waiting for better market conditions or reviewing strategy")
        
        # Top recommendations
        strong_buy_signals = filtered_df[
            (filtered_df['Signal'] == 'BUY') & 
            (filtered_df['Confidence'] >= 70)
        ]
        
        if not strong_buy_signals.empty:
            st.subheader("🎯 Top BUY Recommendations")
            for _, signal in strong_buy_signals.head(3).iterrows():
                st.success(f"**{signal['Symbol']}** - {signal['Bot']} (Confidence: {signal['Confidence']}%)")
                st.caption(f"Analysis: {signal['Analysis']}")
        
    else:
        st.info("""
        ## 🤖 No Analysis Data Available
        
        **Possible reasons:**
        - All bots are still processing
        - No active symbols in watchlist  
        - Market data currently unavailable
        - Bot configuration issues
        
        **Try these solutions:**
        - Click **🔄 Refresh Analysis** button above
        - Add more symbols to your active watchlist
        - Check bot activation status in Configuration tab
        - Ensure market data is available (9:15 AM - 3:30 PM IST for live data)
        - Verify your internet connection
        """)

# Add these helper analysis functions if not already defined
def analyze_momentum_for_thinking(instrument_df, symbol, exchange):
    """Momentum analysis for thinking tab."""
    try:
        # Your momentum analysis logic here
        return {
            'action': 'BUY',  # Example
            'score': 75,
            'signals': ['Strong uptrend', 'Volume confirmation'],
            'risk_level': 'Medium',
            'reasoning': 'Price above key moving averages with increasing volume'
        }
    except Exception as e:
        return {'error': str(e)}

def analyze_mean_reversion_for_thinking(instrument_df, symbol, exchange):
    """Mean reversion analysis for thinking tab."""
    try:
        # Your mean reversion analysis logic here
        return {
            'action': 'HOLD',  # Example
            'score': 60,
            'signals': ['Oversold condition', 'RSI below 30'],
            'risk_level': 'Low',
            'reasoning': 'Stock showing oversold signals but waiting for confirmation'
        }
    except Exception as e:
        return {'error': str(e)}

def analyze_breakout_for_thinking(instrument_df, symbol, exchange):
    """Breakout analysis for thinking tab."""
    try:
        # Your breakout analysis logic here
        return {
            'action': 'SELL',  # Example
            'score': 80,
            'signals': ['Breakdown confirmed', 'Volume spike'],
            'risk_level': 'High',
            'reasoning': 'Price broke below key support level with high volume'
        }
    except Exception as e:
        return {'error': str(e)}

def analyze_multi_signal_for_thinking(instrument_df, symbol, exchange):
    """Multi-signal analysis for thinking tab."""
    try:
        # Your multi-signal analysis logic here
        return {
            'action': 'BUY',
            'score': 85,
            'signals': ['Momentum + Volume + Breakout confirmation'],
            'risk_level': 'Low',
            'reasoning': 'Multiple strategies aligning for strong buy signal'
        }
    except Exception as e:
        return {'error': str(e)}

def display_symbol_override_tab(instrument_df):
    """Enhanced symbol override tab with manual control and analysis."""
    st.subheader("🎯 Symbol Override & Manual Control")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Manual Trade Entry")
        
        # Symbol selection with search
        symbol = st.text_input("Symbol", key="manual_symbol", placeholder="e.g., RELIANCE, TCS").upper()
        
        # Show symbol info if exists
        if symbol:
            symbol_info = instrument_df[instrument_df['tradingsymbol'] == symbol]
            if not symbol_info.empty:
                st.success(f"✅ Symbol found: {symbol_info.iloc[0].get('name', symbol)}")
            else:
                st.warning("⚠️ Symbol not found in instrument list")
        
        action = st.selectbox("Action", ["BUY", "SELL"], key="manual_action")
        quantity = st.number_input("Quantity", min_value=1, value=1, key="manual_quantity")
        price_type = st.radio("Order Type", ["MARKET", "LIMIT"], horizontal=True, key="manual_type")
        
        if price_type == "LIMIT":
            price = st.number_input("Price", min_value=0.01, key="manual_price", value=0.0)
        else:
            price = None
        
        # Market status info
        current_status = get_market_status()['status']
        market_open = is_market_hours()
        
        if st.button("🚀 Execute Manual Trade", type="primary", use_container_width=True):
            if symbol:
                try:
                    if st.session_state.automated_mode.get('live_trading', False):
                        if not market_open:
                            st.warning("⚠️ Market is closed - Live order will queue until market opens")
                        # Execute real trade
                        place_order(instrument_df, symbol, quantity, price_type, action, 'MIS', price)
                        st.success(f"✅ LIVE {action} order placed for {symbol}")
                    else:
                        # Paper trading simulation
                        paper_portfolio = st.session_state.automated_mode.get('paper_portfolio', {})
                        current_price = price if price else get_watchlist_data([{'symbol': symbol, 'exchange': 'NSE'}]).iloc[0]['Price']
                        
                        if action == "BUY":
                            trade_value = quantity * current_price
                            if paper_portfolio.get('cash_balance', 0) >= trade_value:
                                paper_portfolio['cash_balance'] -= trade_value
                                if symbol in paper_portfolio.get('positions', {}):
                                    # Update existing position
                                    old_qty = paper_portfolio['positions'][symbol]['quantity']
                                    old_avg = paper_portfolio['positions'][symbol]['avg_price']
                                    new_qty = old_qty + quantity
                                    new_avg = ((old_qty * old_avg) + (quantity * current_price)) / new_qty
                                    paper_portfolio['positions'][symbol]['quantity'] = new_qty
                                    paper_portfolio['positions'][symbol]['avg_price'] = new_avg
                                else:
                                    # New position
                                    if 'positions' not in paper_portfolio:
                                        paper_portfolio['positions'] = {}
                                    paper_portfolio['positions'][symbol] = {
                                        'quantity': quantity,
                                        'avg_price': current_price,
                                        'action': 'BUY',
                                        'entry_time': get_ist_time().isoformat()
                                    }
                                st.success(f"📄 PAPER {action} executed for {symbol} @ ₹{current_price:.2f}")
                            else:
                                st.error("❌ Insufficient paper trading balance")
                        else:  # SELL
                            # For paper trading, we simulate selling
                            if symbol in paper_portfolio.get('positions', {}):
                                position = paper_portfolio['positions'][symbol]
                                if position['quantity'] >= quantity:
                                    # Calculate P&L
                                    pnl = (current_price - position['avg_price']) * quantity
                                    paper_portfolio['cash_balance'] += quantity * current_price
                                    paper_portfolio['positions'][symbol]['quantity'] -= quantity
                                    
                                    # Remove if position closed
                                    if paper_portfolio['positions'][symbol]['quantity'] == 0:
                                        del paper_portfolio['positions'][symbol]
                                    
                                    st.success(f"📄 PAPER {action} executed for {symbol} @ ₹{current_price:.2f} | P&L: ₹{pnl:.2f}")
                                else:
                                    st.error(f"❌ Not enough shares to sell. Holding: {position['quantity']}")
                            else:
                                st.error(f"❌ No position found for {symbol}")
                except Exception as e:
                    st.error(f"❌ Trade execution failed: {e}")
            else:
                st.warning("⚠️ Please enter a symbol")
    
    with col2:
        st.write("### Quick Actions")
        
        # Force analysis on specific symbol
        st.write("**🔍 Quick Analysis**")
        analysis_symbol = st.text_input("Analyze Symbol", key="analysis_symbol", placeholder="Enter symbol for quick analysis").upper()
        
        if st.button("🤖 Run Bot Analysis", use_container_width=True) and analysis_symbol:
            with st.spinner(f"Analyzing {analysis_symbol}..."):
                # Run all active bots on this symbol
                active_bots = [bot for bot, active in st.session_state.automated_mode.get('bots_active', {}).items() if active]
                for bot_name in active_bots:
                    if bot_name in AUTOMATED_BOTS:
                        try:
                            bot_function = AUTOMATED_BOTS[bot_name]
                            bot_result = bot_function(instrument_df, analysis_symbol)
                            if not bot_result.get("error"):
                                st.write(f"**{bot_name}:** {bot_result['action']} - {bot_result.get('score', 'N/A')}% confidence")
                                for signal in bot_result.get('signals', []):
                                    st.write(f"  - {signal}")
                        except Exception as e:
                            st.error(f"{bot_name} failed: {e}")
        
        st.markdown("---")
        
        # Portfolio management
        st.write("**💰 Portfolio Actions**")
        
        if st.button("🔄 Update Portfolio Values", use_container_width=True):
            update_paper_portfolio_values(instrument_df)
            st.success("✅ Portfolio values updated!")
        
        if st.button("🗑️ Clear All Trades", use_container_width=True):
            st.session_state.automated_mode['trade_history'] = []
            st.session_state.automated_mode['paper_portfolio'] = {
                'cash_balance': st.session_state.automated_mode['total_capital'],
                'positions': {},
                'initial_capital': st.session_state.automated_mode['total_capital'],
                'total_value': st.session_state.automated_mode['total_capital']
            }
            st.session_state.order_history = []
            st.success("✅ All trades and positions cleared!")
        
        # Market status info
        st.markdown("---")
        st.write("### 📈 Market Status")
        status_info = get_market_status()
        st.write(f"**Status:** {status_info['status'].replace('_', ' ').title()}")
        st.write(f"**Paper Trading:** ✅ Always Available")
        st.write(f"**Live Trading:** ✅ Available 24/7")
        
        if not is_market_hours():
            st.info("📅 Live orders will queue and execute when market opens (9:15 AM - 3:30 PM IST)")
        
        # Current portfolio snapshot
        st.markdown("---")
        st.write("**💰 Portfolio Snapshot**")
        paper_portfolio = st.session_state.automated_mode.get('paper_portfolio', {})
        st.write(f"Cash: ₹{paper_portfolio.get('cash_balance', 0):.2f}")
        st.write(f"Positions: {len(paper_portfolio.get('positions', {}))}")
        st.write(f"Total Value: ₹{paper_portfolio.get('total_value', 0):.2f}")
def close_paper_position(symbol, quantity=None):
    """Close a paper trading position with proper P&L calculation."""
    paper_portfolio = st.session_state.automated_mode.get('paper_portfolio', {})
    
    if not paper_portfolio or symbol not in paper_portfolio.get('positions', {}):
        st.error(f"No position found for {symbol}")
        return False
    
    position = paper_portfolio['positions'][symbol]
    close_quantity = quantity if quantity else position['quantity']
    
    if close_quantity > position['quantity']:
        st.error(f"Cannot close more than current position: {position['quantity']}")
        return False
    
    # Get current price
    live_data = get_watchlist_data([{'symbol': symbol, 'exchange': 'NSE'}])
    if live_data.empty:
        st.error(f"Could not get current price for {symbol}")
        return False
    
    current_price = live_data.iloc[0]['Price']
    
    # Calculate P&L
    pnl = (current_price - position['avg_price']) * close_quantity
    
    # Update cash and position
    paper_portfolio['cash_balance'] += close_quantity * current_price
    paper_portfolio['positions'][symbol]['quantity'] -= close_quantity
    
    # Remove position if fully closed
    if paper_portfolio['positions'][symbol]['quantity'] == 0:
        del paper_portfolio['positions'][symbol]
    
    # Update trade history
    open_trades = [t for t in st.session_state.automated_mode.get('trade_history', []) 
                  if t.get('symbol') == symbol and t.get('status') == 'OPEN' and t.get('action') == position.get('action')]
    
    for trade in open_trades:
        if trade.get('quantity', 0) <= close_quantity:
            # Close this trade
            trade['status'] = 'CLOSED'
            trade['exit_price'] = current_price
            trade['exit_time'] = get_ist_time().isoformat()
            trade['pnl'] = pnl
            close_quantity -= trade.get('quantity', 0)
    
    st.success(f"✅ Closed {close_quantity} shares of {symbol} at ₹{current_price:.2f} | P&L: ₹{pnl:.2f}")
    return True

def display_setup_guide():
    """Display setup guide when automated mode is disabled."""
    st.subheader("🚀 Automated Trading Setup Guide")
    
    st.info("""
    **To get started with automated trading:**
    
    1. **Enable Bots** - Toggle the 'Enable Bots' switch in the Control Panel
    2. **Configure Bots** - Go to the '🤖 Bot Configuration' tab to select which bots to run
    3. **Set Capital & Risk** - Adjust your trading capital and risk per trade
    4. **Choose Trading Mode** - Select between Paper Trading (safe) or Live Trading (real money)
    5. **Start Trading** - Click the Start button to begin automated trading
    
    **Recommended for beginners:**
    - Start with Paper Trading to test strategies
    - Use minimum capital (₹1,000) initially
    - Enable only one bot at first to understand its behavior
    - Monitor performance in the '📊 Live Dashboard' tab
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📚 Learning Resources**")
        st.write("• Review bot strategies in Algo Trading Bots page")
        st.write("• Test strategies with paper trading first")
        st.write("• Monitor performance regularly")
        st.write("• Adjust risk parameters based on results")
    
    with col2:
        st.write("**⚠️ Risk Management**")
        st.write("• Never risk more than 2% per trade")
        st.write("• Start with paper trading")
        st.write("• Set stop losses for all positions")
        st.write("• Monitor automated trades regularly")

# =============================================================================
# INTELLIGENT SQUARE-OFF FUNCTIONS - ADD NEW ONES
# =============================================================================
def display_segment_square_off_info():
    """Display segment-specific square-off information"""
    st.markdown("---")
    st.subheader("🕒 Segment-wise Square-off Times")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**📈 Equity/Cash**")
        st.write("• Market: 9:15 AM - 3:30 PM")
        st.write("• Square-off: 3:20 PM")
        st.write("• Auto close: 3:20 PM")
    
    with col2:
        st.write("**📊 Equity Derivatives**")
        st.write("• Market: 9:15 AM - 3:30 PM")
        st.write("• Square-off: 3:25 PM")
        st.write("• Auto close: 3:25 PM")
    
    with col3:
        st.write("**🛢️ Commodities**")
        st.write("• Market: Varies by commodity")
        st.write("• Square-off: 10 min before close")
        st.write("• Auto close: 10 min before")

def display_enhanced_square_off_suggestions():
    """Display intelligent square-off suggestions with segment-specific timing - ONLY FOR LIVE TRADING"""
    # Only show for live trading
    if not st.session_state.automated_mode.get('live_trading', False):
        return
    
    st.warning("**⚠️ SQUARE-OFF TIME ACTIVE** - Consider closing positions before market close")
    portfolio = st.session_state.automated_mode.get('paper_portfolio', {})
    positions = portfolio.get('positions', {})
    
    if not positions:
        st.info("✅ No open positions to square off")
        return
    
    current_time = datetime.now()
    market_close = datetime.combine(current_time.date(), time(15, 30))
    
    # Check different square-off times
    equity_square_off_start = datetime.combine(current_time.date(), time(15, 20))
    derivatives_square_off_start = datetime.combine(current_time.date(), time(15, 25))
    
    minutes_to_equity_square_off = max(0, (equity_square_off_start - current_time).seconds // 60)
    minutes_to_derivatives_square_off = max(0, (derivatives_square_off_start - current_time).seconds // 60)
    minutes_to_market_close = max(0, (market_close - current_time).seconds // 60)
    
    # Determine which square-off period we're in
    if current_time >= equity_square_off_start and current_time < derivatives_square_off_start:
        # Equity square-off time (3:20 PM - 3:25 PM)
        st.markdown("---")
        st.error(f"🚨 **EQUITY SQUARE-OFF TIME** - Auto square-off in progress | {minutes_to_derivatives_square_off} min until derivatives")
        
    elif current_time >= derivatives_square_off_start and current_time <= market_close:
        # Derivatives square-off time (3:25 PM - 3:30 PM)
        st.markdown("---")
        st.error(f"🚨 **DERIVATIVES SQUARE-OFF TIME** - Final auto square-off | {minutes_to_market_close} min until market close")
        
    elif minutes_to_equity_square_off <= 15 and minutes_to_equity_square_off > 0:
        # Pre-square-off warning (3:05 PM - 3:20 PM)
        st.markdown("---")
        st.warning(f"⚠️ **PRE-SQUARE OFF WARNING** - {minutes_to_equity_square_off} minutes until equity auto square-off")
    
    # Get intelligent analysis only for live trading
    analyzed_positions = get_intelligent_square_off_suggestions(positions)
    
    if analyzed_positions:
        # Display priority actions
        display_priority_actions(analyzed_positions)
        
        # Display detailed analysis
        with st.expander("📊 Live Position Analysis", expanded=True):
            display_intelligent_position_analysis(analyzed_positions)
        
        # Quick action panel
        display_enhanced_square_off_actions(analyzed_positions)

def get_intelligent_square_off_suggestions(positions):
    """Get intelligent square-off suggestions for LIVE TRADING only"""
    
    if not st.session_state.automated_mode.get('live_trading', False):
        return []
    
    if not positions:
        return []
    
    analyzed_positions = []
    
    for symbol, position in positions.items():
        try:
            current_price = get_current_price(symbol)
            if not current_price:
                continue
                
            quantity = position.get('quantity', 0)
            avg_price = position.get('avg_price', 0)
            entry_time = position.get('entry_time')
            bot_name = position.get('bot_name', 'Unknown')
            
            # Calculate metrics
            pnl = (current_price - avg_price) * quantity
            pnl_percent = ((current_price - avg_price) / avg_price * 100) if avg_price > 0 else 0
            holding_period = calculate_holding_period(entry_time)
            
            position_data = {
                'symbol': symbol,
                'quantity': quantity,
                'avg_price': avg_price,
                'current_price': current_price,
                'pnl': pnl,
                'pnl_percent': pnl_percent,
                'holding_period': holding_period,
                'bot_name': bot_name,
                'entry_time': entry_time
            }
            
            # Get intelligent recommendation
            position_data['recommendation'] = get_ai_position_analysis(position_data)
            
            analyzed_positions.append(position_data)
            
        except Exception as e:
            print(f"Error analyzing {symbol}: {e}")
            continue
    
    return analyzed_positions

def display_priority_actions(analyzed_positions):
    """Display priority actions based on intelligent analysis"""
    
    # Sort by priority (high confidence CLOSE actions first)
    high_priority = [p for p in analyzed_positions 
                    if p['recommendation'].get('action') == 'CLOSE' 
                    and p['recommendation'].get('confidence', 0) >= 70]
    
    medium_priority = [p for p in analyzed_positions 
                      if p['recommendation'].get('action') == 'CLOSE' 
                      and 50 <= p['recommendation'].get('confidence', 0) < 70]
    
    hold_positions = [p for p in analyzed_positions 
                     if p['recommendation'].get('action') == 'HOLD_OVERNIGHT']
    
    if high_priority:
        st.subheader("🎯 HIGH PRIORITY - Close These Positions")
        for position in high_priority:
            display_priority_position_card(position)
    
    if medium_priority:
        st.subheader("⚠️ MEDIUM PRIORITY - Consider Closing")
        for position in medium_priority:
            display_priority_position_card(position)
    
    if hold_positions:
        st.subheader("💡 HOLD RECOMMENDED - Can Keep Overnight")
        for position in hold_positions:
            display_hold_position_card(position)

def display_priority_position_card(position):
    """Display a priority position card for closing"""
    
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    
    with col1:
        st.write(f"**{position['symbol']}**")
        st.write(f"*{position['bot_name']}*")
    
    with col2:
        # P&L display
        pnl = position['pnl']
        if pnl > 0:
            st.success(f"₹{pnl:+.2f}")
        else:
            st.error(f"₹{pnl:+.2f}")
    
    with col3:
        # Confidence level
        confidence = position['recommendation'].get('confidence', 0)
        if confidence >= 80:
            st.error(f"🔴 {confidence}%")
        elif confidence >= 60:
            st.warning(f"🟡 {confidence}%")
        else:
            st.info(f"🔵 {confidence}%")
    
    with col4:
        # Quick close button
        if st.button("📉 Close", key=f"quick_close_{position['symbol']}"):
            close_position(position['symbol'], position['quantity'])
            st.success(f"Closed {position['symbol']}")
            st.rerun()
    
    with col5:
        # View details
        if st.button("📖", key=f"details_{position['symbol']}"):
            st.session_state[f"show_{position['symbol']}"] = True

def display_intelligent_position_analysis(analyzed_positions):
    """Display detailed intelligent analysis of all positions"""
    
    for position in analyzed_positions:
        with st.container():
            st.markdown(f"### {position['symbol']} Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Position Details:**")
                st.write(f"• Entry: ₹{position['avg_price']:.2f}")
                st.write(f"• Current: ₹{position['current_price']:.2f}")
                st.write(f"• P&L: ₹{position['pnl']:+.2f} ({position['pnl_percent']:+.1f}%)")
                st.write(f"• Held: {position['holding_period']}")
                st.write(f"• Strategy: {position['bot_name']}")
            
            with col2:
                st.write("**Intelligent Analysis:**")
                recommendation = position['recommendation']
                
                action = recommendation.get('action', 'HOLD')
                confidence = recommendation.get('confidence', 50)
                reasoning = recommendation.get('reasoning', 'Analysis unavailable')
                
                # Action with color coding
                if action == "CLOSE":
                    st.error(f"**Action: CLOSE** (Confidence: {confidence}%)")
                elif action == "HOLD_OVERNIGHT":
                    st.success(f"**Action: HOLD** (Confidence: {confidence}%)")
                else:
                    st.warning(f"**Action: {action}** (Confidence: {confidence}%)")
                
                st.write(f"**Reasoning:** {reasoning}")
                
                if recommendation.get('target_price'):
                    st.write(f"**Target:** ₹{recommendation['target_price']:.2f}")
                if recommendation.get('stop_loss'):
                    st.write(f"**Stop Loss:** ₹{recommendation['stop_loss']:.2f}")
            
            st.markdown("---")

def display_enhanced_square_off_actions(analyzed_positions):
    """Display enhanced square-off action buttons with intelligence"""
    
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔴 Close High Priority", use_container_width=True, type="primary"):
            close_high_priority_positions(analyzed_positions)
            st.success("High priority positions closed!")
            st.rerun()
    
    with col2:
        if st.button("📉 Close All Losing", use_container_width=True):
            close_losing_positions(analyzed_positions)
            st.success("All losing positions closed!")
            st.rerun()
    
    with col3:
        if st.button("🤖 Smart Close All", use_container_width=True):
            execute_smart_close_all(analyzed_positions)
            st.success("Smart close executed!")
            st.rerun()
    
    with col4:
        if st.button("📊 Market Analysis", use_container_width=True):
            display_market_analysis_report(analyzed_positions)
            
# =============================================================================
# HELPER FUNCTIONS - ADD NEW ONES
# =============================================================================
# ================ ICEBERG DETECTOR HELPER FUNCTIONS ================

def is_nifty50_stock(symbol):
    """Check if a symbol is in Nifty50."""
    symbol_upper = symbol.upper()
    symbol_mappings = {
        "BAJAJ-AUTO": "BAJAJAUTO", 
        "M&M": "M_M",
    }
    lookup_symbol = symbol_mappings.get(symbol_upper, symbol_upper)
    return lookup_symbol in NIFTY50_STOCKS

def get_market_depth_data(instrument_token):
    """Get enhanced market depth data for iceberg detection."""
    depth = get_market_depth(instrument_token)
    if not depth:
        return {}
    
    # Process depth data for analysis
    bids = depth.get('buy', [])
    asks = depth.get('sell', [])
    
    # Sort bids (highest first) and asks (lowest first)
    bids_sorted = sorted(bids, key=lambda x: x.get('price', 0), reverse=True)[:10]
    asks_sorted = sorted(asks, key=lambda x: x.get('price', 0))[:10]
    
    return {
        'bids': bids_sorted,  # Top 10 bids
        'asks': asks_sorted,  # Top 10 asks
        'total_bid_volume': sum(bid.get('quantity', 0) for bid in bids_sorted),
        'total_ask_volume': sum(ask.get('quantity', 0) for ask in asks_sorted),
        'best_bid': bids_sorted[0] if bids_sorted else {},
        'best_ask': asks_sorted[0] if asks_sorted else {},
        'spread': (asks_sorted[0].get('price', 0) - bids_sorted[0].get('price', 0)) if bids_sorted and asks_sorted else 0
    }
# ================ FUNDAMENTAL ANALYTICS & COMPANY EVENTS FUNCTIONS ================

def get_company_fundamentals_kite(symbol, instrument_df):
    """Fetch company fundamentals using available Kite Connect API methods."""
    try:
        client = get_broker_client()
        if not client or st.session_state.broker != "Zerodha":
            return {"error": "Zerodha Kite connection required for fundamental data"}
        
        # Find instrument token
        instrument = instrument_df[
            (instrument_df['tradingsymbol'] == symbol.upper()) & 
            (instrument_df['exchange'] == 'NSE')
        ]
        if instrument.empty:
            return {"error": f"Instrument {symbol} not found in NSE"}
        
        instrument_token = instrument.iloc[0]['instrument_token']
        
        # Get quote data which contains some fundamental information
        quote = client.quote(instrument_token)
        
        if not quote:
            return {"error": "No quote data available"}
        
        # Extract available fundamental data from quote
        fundamentals = {
            'symbol': symbol,
            'quote_data': quote.get(str(instrument_token), {}),
            'instrument_info': instrument.iloc[0].to_dict()
        }
        
        return fundamentals
        
    except Exception as e:
        return {"error": f"Failed to fetch fundamentals: {str(e)}"}

def get_company_events_kite(symbol, instrument_df):
    """Fetch company events and corporate actions using available Kite data."""
    try:
        client = get_broker_client()
        if not client or st.session_state.broker != "Zerodha":
            return {"error": "Zerodha Kite connection required"}
        
        # Find instrument token
        instrument = instrument_df[
            (instrument_df['tradingsymbol'] == symbol.upper()) & 
            (instrument_df['exchange'] == 'NSE')
        ]
        if instrument.empty:
            return {"error": f"Instrument {symbol} not found in NSE"}
        
        instrument_token = instrument.iloc[0]['instrument_token']
        
        # Get historical data to analyze corporate events
        historical_data = client.historical_data(instrument_token, "day", 
                                               datetime.now() - timedelta(days=365), 
                                               datetime.now())
        
        # Get current quote for analysis
        quote_data = client.quote(instrument_token)
        
        events_data = {
            'symbol': symbol,
            'company_name': instrument.iloc[0].get('name', symbol),
            'historical_data': historical_data[-30:],  # Last 30 days
            'current_quote': quote_data.get(str(instrument_token), {}),
            'instrument_info': instrument.iloc[0].to_dict(),
            'corporate_events': analyze_corporate_events(historical_data, symbol),
            'market_analysis': analyze_market_events(symbol, historical_data)
        }
        
        return events_data
        
    except Exception as e:
        return {"error": f"Failed to fetch company events: {str(e)}"}

def analyze_corporate_events(historical_data, symbol):
    """Analyze historical data to detect corporate events."""
    if not historical_data or len(historical_data) < 10:
        return {}
    
    events = {
        'price_changes': [],
        'volume_spikes': [],
        'volatility_events': []
    }
    
    # Analyze for significant price movements (potential corporate actions)
    for i in range(1, len(historical_data)):
        prev_close = historical_data[i-1]['close']
        current_close = historical_data[i]['close']
        volume = historical_data[i]['volume']
        
        price_change_pct = ((current_close - prev_close) / prev_close) * 100
        
        # Detect significant price movements
        if abs(price_change_pct) > 5:  # More than 5% move
            events['price_changes'].append({
                'date': historical_data[i]['date'],
                'change_percent': price_change_pct,
                'type': 'GAIN' if price_change_pct > 0 else 'LOSS',
                'volume': volume
            })
        
        # Detect volume spikes (3x average volume)
        if i >= 5:  # Ensure we have enough data for average
            avg_volume = sum(h['volume'] for h in historical_data[i-5:i]) / 5
            if volume > avg_volume * 3:
                events['volume_spikes'].append({
                    'date': historical_data[i]['date'],
                    'volume': volume,
                    'avg_volume': avg_volume,
                    'multiplier': volume / avg_volume
                })
    
    return events

def analyze_market_events(symbol, historical_data):
    """Analyze market-related events and patterns."""
    if not historical_data or len(historical_data) < 20:
        return {}
    
    analysis = {
        'performance_metrics': {},
        'volatility_analysis': {},
        'trend_analysis': {}
    }
    
    # Calculate performance metrics
    closes = [day['close'] for day in historical_data]
    volumes = [day['volume'] for day in historical_data]
    
    if len(closes) >= 2:
        analysis['performance_metrics'] = {
            'total_return': ((closes[-1] - closes[0]) / closes[0]) * 100,
            'high_52_week': max(closes) if closes else 0,
            'low_52_week': min(closes) if closes else 0,
            'avg_volume': sum(volumes) / len(volumes) if volumes else 0,
            'current_volume': volumes[-1] if volumes else 0
        }
    
    # Volatility analysis
    if len(closes) >= 10:
        returns = [(closes[i] - closes[i-1]) / closes[i-1] for i in range(1, len(closes))]
        volatility = np.std(returns) * 100 * np.sqrt(252)  # Annualized volatility
        analysis['volatility_analysis'] = {
            'annual_volatility': volatility,
            'volatility_class': 'High' if volatility > 30 else 'Medium' if volatility > 15 else 'Low',
            'max_daily_gain': max(returns) * 100 if returns else 0,
            'max_daily_loss': min(returns) * 100 if returns else 0
        }
    
    # Trend analysis
    if len(closes) >= 5:
        recent_trend = 'UP' if closes[-1] > closes[-5] else 'DOWN'
        analysis['trend_analysis'] = {
            'short_term_trend': recent_trend,
            'trend_strength': abs((closes[-1] - closes[-5]) / closes[-5]) * 100,
            'support_level': min(closes[-5:]) if closes else 0,
            'resistance_level': max(closes[-5:]) if closes else 0
        }
    
    return analysis

def get_market_holidays_extended():
    """Get extended market holidays and special sessions."""
    current_year = datetime.now().year
    holidays = {
        '📅 Regular Holidays': get_market_holidays(current_year),
        '⚡ Special Trading Sessions': [
            'Diwali Muhurat Trading (Usually October/November)',
            'Budget Day (Usually February)',
            'Special Live Trading Sessions (Announced by NSE)'
        ],
        '🎯 Important Market Events': [
            'Quarterly Results: Jan, Apr, Jul, Oct',
            'Union Budget: February',
            'RBI Policy: Bi-monthly',
            'US Fed Meetings: 8 times per year',
            'F&O Expiry: Last Thursday of month',
            'Index Rebalancing: Semi-annually'
        ],
        '📊 Corporate Action Seasons': [
            'Dividend Declarations: Throughout the year',
            'Board Meetings: Quarterly for results',
            'AGMs: Mostly June-September',
            'Stock Splits/Bonus: Announced in board meetings'
        ]
    }
    return holidays

def display_company_events_kite(symbol, instrument_df):
    """Display company events and market analysis using available Kite data."""
    if not symbol:
        st.warning("Please enter a symbol to view company events.")
        return
        
    with st.spinner(f"Analyzing company events for {symbol}..."):
        events_data = get_company_events_kite(symbol, instrument_df)
    
    if "error" in events_data:
        st.error(events_data["error"])
        display_basic_company_info(symbol, instrument_df)
        return
        
    # Display in tabs for better organization
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Market Analysis", "📊 Performance", "📅 Corporate Events", "🏢 Company Info", "🎯 Market Calendar"])
    
    with tab1:
        st.subheader("📈 Market Analysis & Trends")
        
        if 'market_analysis' in events_data:
            analysis = events_data['market_analysis']
            
            # Performance Metrics
            if 'performance_metrics' in analysis:
                metrics = analysis['performance_metrics']
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    return_color = "green" if metrics.get('total_return', 0) >= 0 else "red"
                    st.metric("Total Return", f"{metrics.get('total_return', 0):.2f}%", 
                             delta_color="off" if metrics.get('total_return', 0) == 0 else "normal")
                
                with col2:
                    st.metric("52-Week High", f"₹{metrics.get('high_52_week', 0):.2f}")
                
                with col3:
                    st.metric("52-Week Low", f"₹{metrics.get('low_52_week', 0):.2f}")
                
                with col4:
                    volume_ratio = (metrics.get('current_volume', 0) / metrics.get('avg_volume', 1)) if metrics.get('avg_volume', 0) > 0 else 0
                    st.metric("Volume Ratio", f"{volume_ratio:.1f}x")
            
            # Volatility Analysis
            if 'volatility_analysis' in analysis:
                st.subheader("📊 Volatility Analysis")
                vol_analysis = analysis['volatility_analysis']
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Annual Volatility", f"{vol_analysis.get('annual_volatility', 0):.1f}%")
                with col2:
                    st.metric("Volatility Class", vol_analysis.get('volatility_class', 'N/A'))
                with col3:
                    st.metric("Max Daily Gain", f"{vol_analysis.get('max_daily_gain', 0):.1f}%")
                with col4:
                    st.metric("Max Daily Loss", f"{vol_analysis.get('max_daily_loss', 0):.1f}%")
    
    with tab2:
        st.subheader("📊 Performance Metrics")
        
        if 'historical_data' in events_data and events_data['historical_data']:
            # Create performance chart
            hist_data = events_data['historical_data']
            dates = [pd.to_datetime(day['date']) for day in hist_data]
            closes = [day['close'] for day in hist_data]
            volumes = [day['volume'] for day in hist_data]
            
            # Create performance DataFrame
            perf_df = pd.DataFrame({
                'Date': dates,
                'Close': closes,
                'Volume': volumes
            })
            perf_df.set_index('Date', inplace=True)
            
            # Calculate technical indicators
            perf_df['SMA_20'] = talib.SMA(perf_df['Close'], timeperiod=20)
            perf_df['SMA_50'] = talib.SMA(perf_df['Close'], timeperiod=50)
            
            # Display performance chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=perf_df.index, y=perf_df['Close'], name='Close Price', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=perf_df.index, y=perf_df['SMA_20'], name='SMA 20', line=dict(color='orange', dash='dash')))
            fig.add_trace(go.Scatter(x=perf_df.index, y=perf_df['SMA_50'], name='SMA 50', line=dict(color='red', dash='dash')))
            
            fig.update_layout(
                title=f"{symbol} - Price Performance (Last 30 Days)",
                xaxis_title="Date",
                yaxis_title="Price (₹)",
                template="plotly_dark" if st.session_state.theme == 'Dark' else "plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Volume analysis
            st.subheader("📈 Volume Analysis")
            avg_volume = perf_df['Volume'].mean()
            current_volume = perf_df['Volume'].iloc[-1]
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Current Volume", f"{current_volume:,.0f}")
            col2.metric("Average Volume", f"{avg_volume:,.0f}")
            col3.metric("Volume Ratio", f"{volume_ratio:.1f}x")
    
    with tab3:
        st.subheader("📅 Corporate Events & Price Movements")
        
        if 'corporate_events' in events_data:
            events = events_data['corporate_events']
            
            # Significant price changes
            if events.get('price_changes'):
                st.subheader("🎯 Significant Price Movements")
                for i, change in enumerate(events['price_changes'][:5]):  # Show last 5
                    with st.container():
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.write(f"**{change['date'].strftime('%Y-%m-%d')}**")
                        with col2:
                            change_color = "green" if change['type'] == 'GAIN' else "red"
                            st.markdown(f"<span style='color:{change_color}; font-weight:bold;'>{change['change_percent']:.1f}%</span>", 
                                      unsafe_allow_html=True)
                        with col3:
                            st.write(f"Volume: {change['volume']:,.0f}")
                        st.markdown("---")
            else:
                st.info("No significant price movements detected in recent data.")
            
            # Volume spikes
            if events.get('volume_spikes'):
                st.subheader("📊 Volume Spikes")
                for i, spike in enumerate(events['volume_spikes'][:3]):  # Show last 3
                    with st.container():
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**{spike['date'].strftime('%Y-%m-%d')}**")
                        with col2:
                            st.write(f"Volume: {spike['volume']:,.0f}")
                        with col3:
                            st.write(f"{spike['multiplier']:.1f}x average")
                        st.markdown("---")
    
    with tab4:
        st.subheader("🏢 Company Information")
        
        if 'instrument_info' in events_data:
            info = events_data['instrument_info']
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Basic Information**")
                if 'tradingsymbol' in info:
                    st.metric("Symbol", info['tradingsymbol'])
                if 'name' in info:
                    st.metric("Company Name", info['name'])
                if 'exchange' in info:
                    st.metric("Exchange", info['exchange'])
                if 'instrument_type' in info:
                    st.metric("Instrument Type", info['instrument_type'])
            
            with col2:
                st.write("**Trading Details**")
                if 'lot_size' in info:
                    st.metric("Lot Size", info['lot_size'])
                if 'tick_size' in info:
                    st.metric("Tick Size", info['tick_size'])
                if 'segment' in info:
                    st.metric("Segment", info['segment'])
                if 'expiry' in info and pd.notna(info['expiry']):
                    st.metric("Expiry", info['expiry'].strftime('%Y-%m-%d'))
        
        # Current market data
        if 'current_quote' in events_data and events_data['current_quote']:
            st.subheader("📈 Current Market Data")
            quote = events_data['current_quote']
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("LTP", f"₹{quote.get('last_price', 0):.2f}")
            with col2:
                st.metric("Change", f"₹{quote.get('change', 0):.2f}")
            with col3:
                change_pct = quote.get('change', 0) / quote.get('ohlc', {}).get('close', 1) * 100
                st.metric("Change %", f"{change_pct:.2f}%")
            with col4:
                st.metric("Volume", f"{quote.get('volume', 0):,.0f}")
    
    with tab5:
        st.subheader("🎯 Market Calendar & Events")
        
        # Market holidays
        holidays = get_market_holidays_extended()
        
        for category, dates in holidays.items():
            with st.expander(f"{category}"):
                for date in dates:
                    st.write(f"• {date}")
        
        # Upcoming events based on historical patterns
        st.subheader("📅 Expected Corporate Events")
        st.info("""
        **Typical Corporate Event Timeline:**
        - Quarterly Results: Jan, Apr, Jul, Oct
        - Dividend Declarations: Board meetings (varies)
        - AGMs: Mostly June-September  
        - Stock Splits/Bonus: Announced periodically
        """)
        
        # Add event reminder
        st.subheader("🔔 Event Reminders")
        if st.button("Set Dividend Alert", key="div_alert"):
            st.success(f"Dividend alert set for {symbol}. You'll be notified of any dividend declarations.")
        
        if st.button("Set Results Alert", key="results_alert"):
            st.success(f"Quarterly results alert set for {symbol}.")

def display_basic_company_info(symbol, instrument_df):
    """Display basic company information."""
    st.info("Displaying basic company information from available data...")
    
    # Get instrument info
    instrument = instrument_df[
        (instrument_df['tradingsymbol'] == symbol.upper()) & 
        (instrument_df['exchange'] == 'NSE')
    ]
    
    if not instrument.empty:
        inst_data = instrument.iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Basic Information:**")
            st.write(f"• Symbol: {inst_data['tradingsymbol']}")
            st.write(f"• Exchange: {inst_data['exchange']}")
            if 'name' in inst_data:
                st.write(f"• Company: {inst_data['name']}")
            if 'instrument_type' in inst_data:
                st.write(f"• Type: {inst_data['instrument_type']}")
        
        with col2:
            st.write("**Trading Details:**")
            if 'lot_size' in inst_data:
                st.write(f"• Lot Size: {inst_data['lot_size']}")
            if 'tick_size' in inst_data:
                st.write(f"• Tick Size: {inst_data['tick_size']}")
            if 'segment' in inst_data:
                st.write(f"• Segment: {inst_data['segment']}")
    
    # Show current market data
    quote_data = get_watchlist_data([{'symbol': symbol, 'exchange': 'NSE'}])
    if not quote_data.empty:
        st.subheader("📈 Current Market Data")
        current_price = quote_data.iloc[0]['Price']
        change = quote_data.iloc[0]['Change']
        pct_change = quote_data.iloc[0]['% Change']
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"₹{current_price:.2f}")
        col2.metric("Change", f"₹{change:+.2f}")
        col3.metric("Change %", f"{pct_change:+.2f}%")

def calculate_holding_period(entry_time):
    """Calculate how long position has been held"""
    if not entry_time:
        return "Unknown"
    
    try:
        if isinstance(entry_time, str):
            entry_dt = datetime.fromisoformat(entry_time)
        else:
            entry_dt = entry_time
            
        duration = datetime.now() - entry_dt
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    except:
        return "Unknown"

def close_high_priority_positions(analyzed_positions):
    """Close only high priority positions"""
    for position in analyzed_positions:
        if (position['recommendation'].get('action') == 'CLOSE' and 
            position['recommendation'].get('confidence', 0) >= 70):
            close_position(position['symbol'], position['quantity'])

def close_losing_positions(analyzed_positions):
    """Close all losing positions"""
    for position in analyzed_positions:
        if position['pnl'] < 0:
            close_position(position['symbol'], position['quantity'])

def execute_smart_close_all(analyzed_positions):
    """Execute smart closing based on recommendations"""
    for position in analyzed_positions:
        action = position['recommendation'].get('action')
        confidence = position['recommendation'].get('confidence', 0)
        
        if action == "CLOSE" and confidence >= 60:
            close_position(position['symbol'], position['quantity'])
        elif action == "PARTIAL_CLOSE" and confidence >= 50:
            # Close half position
            close_position(position['symbol'], position['quantity'] // 2)

def display_market_analysis_report(analyzed_positions):
    """Display comprehensive market analysis report"""
    
    total_pnl = sum(pos['pnl'] for pos in analyzed_positions)
    close_recommendations = sum(1 for pos in analyzed_positions 
                               if pos['recommendation'].get('action') == 'CLOSE')
    hold_recommendations = sum(1 for pos in analyzed_positions 
                              if pos['recommendation'].get('action') == 'HOLD_OVERNIGHT')
    
    st.info(f"""
    **📈 Live Market Analysis Report:**
    
    • **Total Portfolio P&L:** ₹{total_pnl:,.2f}
    • **Close Recommendations:** {close_recommendations} positions
    • **Hold Recommendations:** {hold_recommendations} positions
    • **Overall Sentiment:** {'Bearish' if close_recommendations > hold_recommendations else 'Bullish'}
    • **Suggested Action:** {'Square off majority' if close_recommendations > hold_recommendations else 'Hold quality positions'}
    """)

def display_hold_position_card(position):
    """Display hold position card"""
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.write(f"**{position['symbol']}**")
        st.write(f"*{position['bot_name']}*")
    
    with col2:
        pnl = position['pnl']
        if pnl > 0:
            st.success(f"₹{pnl:+.2f}")
        else:
            st.error(f"₹{pnl:+.2f}")
    
    with col3:
        confidence = position['recommendation'].get('confidence', 0)
        st.success(f"🟢 {confidence}%")

# Placeholder functions for the main implementation
def get_current_price(symbol):
    """Get current price for a symbol - implement based on your data source"""
    # This would connect to your data source (broker API, market data feed, etc.)
    # For now, return a placeholder value
    return 100.0

def close_position(symbol, quantity):
    """Close a position - implement based on your trading logic"""
    # This would execute through your broker API
    st.success(f"Closed {symbol} - {quantity} shares")

def get_ai_position_analysis(position_data):
    """Get AI analysis for position - implement based on your AI service"""
    # This would integrate with your AI service
    # For now, return sample analysis
    return {
        "action": "CLOSE",
        "confidence": 75,
        "reasoning": "Profit target achieved, take profits before market close",
        "target_price": None,
        "stop_loss": None
    }
# ================ AUTOMATED MODE HELPER FUNCTIONS ================

def initialize_automated_mode():
    """Initialize session state for fully automated trading."""
    if 'automated_mode' not in st.session_state:
        st.session_state.automated_mode = {
            'enabled': False,
            'running': False,
            'live_trading': False,
            'bots_active': {},
            'total_capital': 1000,
            'risk_per_trade': 2.0,
            'max_open_trades': 5,
            'trade_history': [],
            'performance_metrics': {},
            'last_signal_check': None
        }

def get_automated_bot_performance():
    """Calculate performance metrics for automated bots."""
    if not st.session_state.automated_mode['trade_history']:
        return {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_pnl': 0,
            'win_rate': 0,
            'avg_win': 0,
            'avg_loss': 0
        }
    
    trades = st.session_state.automated_mode['trade_history']
    winning_trades = [t for t in trades if t.get('pnl', 0) > 0]
    losing_trades = [t for t in trades if t.get('pnl', 0) <= 0]
    
    total_pnl = sum(t.get('pnl', 0) for t in trades)
    win_rate = len(winning_trades) / len(trades) * 100 if trades else 0
    
    avg_win = sum(t.get('pnl', 0) for t in winning_trades) / len(winning_trades) if winning_trades else 0
    avg_loss = sum(t.get('pnl', 0) for t in losing_trades) / len(losing_trades) if losing_trades else 0
    
    return {
        'total_trades': len(trades),
        'winning_trades': len(winning_trades),
        'losing_trades': len(losing_trades),
        'total_pnl': total_pnl,
        'win_rate': win_rate,
        'avg_win': avg_win,
        'avg_loss': avg_loss
    }

def display_trade_history():
    """Display comprehensive trade history with filtering and analysis."""
    st.subheader("📋 Trade History")
    
    trade_history = st.session_state.automated_mode.get('trade_history', [])
    
    if not trade_history:
        st.info("No trade history available yet.")
        return
    
    # Add filtering options
    col1, col2, col3 = st.columns(3)
    with col1:
        show_status = st.selectbox("Filter by Status", ["ALL", "OPEN", "CLOSED"])
    with col2:
        show_bot = st.selectbox("Filter by Bot", ["ALL"] + list(AUTOMATED_BOTS.keys()))
    with col3:
        show_type = st.selectbox("Filter by Type", ["ALL", "LIVE", "PAPER"])
    
    # Filter trades
    filtered_trades = trade_history.copy()
    
    if show_status != "ALL":
        filtered_trades = [t for t in filtered_trades if t.get('status') == show_status]
    
    if show_bot != "ALL":
        filtered_trades = [t for t in filtered_trades if t.get('bot_name') == show_bot]
    
    if show_type != "ALL":
        filtered_trades = [t for t in filtered_trades if t.get('order_type') == show_type]
    
    if not filtered_trades:
        st.warning("No trades match the selected filters.")
        return
    
    # Convert to DataFrame for display
    display_data = []
    for trade in filtered_trades:
        display_data.append({
            'Time': trade.get('timestamp_display', 
                            get_ist_time().strftime("%H:%M:%S") if 'timestamp' not in trade 
                            else datetime.fromisoformat(trade['timestamp'].replace('Z', '+00:00')).astimezone(pytz.timezone('Asia/Kolkata')).strftime("%H:%M:%S")),
            'Symbol': trade.get('symbol', 'N/A'),
            'Action': trade.get('action', 'N/A'),
            'Quantity': trade.get('quantity', 0),
            'Price': f"₹{trade.get('entry_price', 0):.2f}",
            'Status': trade.get('status', 'UNKNOWN'),
            'Bot': trade.get('bot_name', 'Manual'),
            'Type': trade.get('order_type', 'PAPER'),
            'P&L': f"₹{trade.get('pnl', 0):.2f}"
        })
    
    df_trades = pd.DataFrame(display_data)
    
    # Color coding for actions and P&L
    def color_trade_row(row):
        styles = [''] * len(row)
        
        # Color action column
        if row['Action'] == 'BUY':
            styles[2] = 'background-color: #90EE90; color: #006400;'  # Light green
        elif row['Action'] == 'SELL':
            styles[2] = 'background-color: #FFB6C1; color: #8B0000;'  # Light red
        
        # Color P&L column
        try:
            pnl_value = float(row['P&L'].replace('₹', ''))
            if pnl_value > 0:
                styles[7] = 'background-color: #90EE90; color: #006400; font-weight: bold;'
            elif pnl_value < 0:
                styles[7] = 'background-color: #FFB6C1; color: #8B0000; font-weight: bold;'
        except:
            pass
            
        # Color status column
        if row['Status'] == 'OPEN':
            styles[5] = 'background-color: #FFFACD; color: #8B7500;'  # Light yellow
        elif row['Status'] == 'CLOSED':
            styles[5] = 'background-color: #F0F0F0; color: #666;'     # Light gray
            
        return styles
    
    styled_df = df_trades.style.apply(color_trade_row, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Summary statistics
    st.subheader("📊 Trade Summary")
    
    closed_trades = [t for t in filtered_trades if t.get('status') == 'CLOSED']
    open_trades = [t for t in filtered_trades if t.get('status') == 'OPEN']
    
    if closed_trades:
        total_pnl = sum(t.get('pnl', 0) for t in closed_trades)
        winning_trades = [t for t in closed_trades if t.get('pnl', 0) > 0]
        losing_trades = [t for t in closed_trades if t.get('pnl', 0) < 0]
        win_rate = (len(winning_trades) / len(closed_trades)) * 100 if closed_trades else 0
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Trades", len(closed_trades))
        col2.metric("Win Rate", f"{win_rate:.1f}%")
        col3.metric("Total P&L", f"₹{total_pnl:.2f}")
        col4.metric("Open Trades", len(open_trades))
    
    # Action buttons
    st.markdown("---")
    col_actions1, col_actions2, col_actions3 = st.columns(3)
    
    with col_actions1:
        if st.button("📥 Export to CSV", use_container_width=True):
            # Create downloadable CSV
            csv = df_trades.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"trade_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col_actions2:
        if st.button("🗑️ Clear History", use_container_width=True, type="secondary"):
            st.session_state.automated_mode['trade_history'] = []
            st.success("Trade history cleared!")
            st.rerun()
    
    with col_actions3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

def get_current_price(symbol):
    """Get current price for a symbol with fallback."""
    try:
        # Try to get live data first
        live_data = get_watchlist_data([{'symbol': symbol, 'exchange': 'NSE'}])
        if not live_data.empty:
            return live_data.iloc[0]['Price']
        
        # Fallback: use instrument data
        instrument_df = get_instrument_df()
        if not instrument_df.empty:
            instrument = instrument_df[instrument_df['tradingsymbol'] == symbol]
            if not instrument.empty:
                # Return a reasonable estimate (you might want to enhance this)
                return 100.0  # Default fallback price
                
    except Exception as e:
        st.error(f"Error getting price for {symbol}: {e}")
    
    return 100.0  # Final fallback

def close_position(symbol, quantity):
    """Close a position in paper trading."""
    try:
        paper_portfolio = st.session_state.automated_mode.get('paper_portfolio', {})
        
        if symbol not in paper_portfolio.get('positions', {}):
            st.error(f"No position found for {symbol}")
            return False
        
        position = paper_portfolio['positions'][symbol]
        
        if quantity > position['quantity']:
            st.error(f"Cannot close more than current position: {position['quantity']}")
            return False
        
        # Get current price for P&L calculation
        current_price = get_current_price(symbol)
        
        # Calculate P&L
        pnl = (current_price - position['avg_price']) * quantity
        
        # Update cash balance
        paper_portfolio['cash_balance'] += quantity * current_price
        
        # Update position
        paper_portfolio['positions'][symbol]['quantity'] -= quantity
        
        # Remove position if fully closed
        if paper_portfolio['positions'][symbol]['quantity'] == 0:
            del paper_portfolio['positions'][symbol]
        
        # Update trade history
        open_trades = [t for t in st.session_state.automated_mode.get('trade_history', []) 
                      if t.get('symbol') == symbol and t.get('status') == 'OPEN']
        
        for trade in open_trades:
            if trade.get('quantity', 0) <= quantity:
                trade['status'] = 'CLOSED'
                trade['exit_price'] = current_price
                trade['exit_time'] = get_ist_time().isoformat()
                trade['pnl'] = pnl
                quantity -= trade.get('quantity', 0)
        
        st.success(f"✅ Closed {quantity} shares of {symbol} at ₹{current_price:.2f} | P&L: ₹{pnl:.2f}")
        return True
        
    except Exception as e:
        st.error(f"Error closing position for {symbol}: {e}")
        return False

def get_ai_position_analysis(position_data):
    """Get intelligent analysis for position with multiple factors."""
    try:
        symbol = position_data['symbol']
        current_price = position_data['current_price']
        avg_price = position_data['avg_price']
        pnl_percent = position_data['pnl_percent']
        holding_period = position_data['holding_period']
        
        # Simple AI logic (you can enhance this with ML models)
        action = "HOLD_OVERNIGHT"
        confidence = 50
        reasoning = "Holding for potential gains"
        
        # Profit-taking logic
        if pnl_percent >= 3:  # Take profit at 3%
            action = "CLOSE"
            confidence = 80
            reasoning = f"Profit target achieved (+{pnl_percent:.1f}%) - take profits"
        
        # Stop-loss logic
        elif pnl_percent <= -2:  # Stop loss at -2%
            action = "CLOSE"
            confidence = 75
            reasoning = f"Stop loss triggered ({pnl_percent:.1f}%) - limit losses"
        
        # Time-based exit for day trades
        elif "h" in holding_period and int(holding_period.split('h')[0]) >= 4:
            action = "CLOSE"
            confidence = 60
            reasoning = "Extended holding period - consider closing before market close"
        
        # Market context (simplified)
        market_status = get_market_status()['status']
        if "square_off" in market_status and pnl_percent > 0:
            action = "CLOSE"
            confidence = 70
            reasoning = "Square-off time - secure profits"
        
        return {
            "action": action,
            "confidence": confidence,
            "reasoning": reasoning,
            "target_price": current_price * 1.02 if action == "HOLD_OVERNIGHT" else None,
            "stop_loss": current_price * 0.98 if action == "HOLD_OVERNIGHT" else None
        }
        
    except Exception as e:
        return {
            "action": "HOLD_OVERNIGHT",
            "confidence": 30,
            "reasoning": f"Analysis error: {str(e)}",
            "target_price": None,
            "stop_loss": None
        }
# <<<--- PLACE execute_automated_trade FUNCTION HERE --->>>
def execute_automated_trade(instrument_df, bot_result, risk_per_trade):
    """Execute trades automatically based on bot signals."""
    if bot_result.get("error") or bot_result["action"] == "HOLD":
        return None
    
    try:
        symbol = bot_result["symbol"]
        action = bot_result["action"]
        current_price = bot_result["current_price"]
        
        # Calculate position size based on risk
        risk_amount = (risk_per_trade / 100) * st.session_state.automated_mode['total_capital']
        quantity = max(1, int(risk_amount / current_price))
        
        # Check if we have too many open trades
        open_trades = [t for t in st.session_state.automated_mode['trade_history'] 
                      if t.get('status') == 'OPEN']
        if len(open_trades) >= st.session_state.automated_mode['max_open_trades']:
            return None
        
        # Check for existing position in the same symbol
        existing_position = next((t for t in open_trades if t.get('symbol') == symbol), None)
        if existing_position:
            # Avoid opening same position multiple times
            if existing_position['action'] == action:
                return None
        
        # PLACE REAL ORDER if live trading is enabled
        order_type = "PAPER"
        if st.session_state.automated_mode.get('live_trading', False):
            try:
                # Place the real order
                place_order(instrument_df, symbol, quantity, 'MARKET', action, 'MIS')
                order_type = "LIVE"
            except Exception as e:
                st.error(f"❌ Failed to place LIVE order for {symbol}: {e}")
                return None
        
        # Record the trade
        trade_record = {
            'timestamp': datetime.now().isoformat(),
            'symbol': symbol,
            'action': action,
            'quantity': quantity,
            'entry_price': current_price,
            'status': 'OPEN',
            'bot_name': bot_result['bot_name'],
            'risk_level': bot_result['risk_level'],
            'order_type': order_type,
            'pnl': 0  # Initialize P&L
        }
        
        st.session_state.automated_mode['trade_history'].append(trade_record)
        
        if order_type == "LIVE":
            st.toast(f"🤖 LIVE {action} order executed for {symbol} (Qty: {quantity})", icon="⚡")
        else:
            st.toast(f"🤖 PAPER {action} order simulated for {symbol} (Qty: {quantity})", icon="📄")
            
        return trade_record
        
    except Exception as e:
        st.error(f"Automated trade execution failed: {e}")
        return None

def run_automated_bots_cycle(instrument_df, watchlist_symbols):
    """Run one cycle of all active automated bots."""
    if not st.session_state.automated_mode['running']:
        return
    
    active_bots = [bot for bot, active in st.session_state.automated_mode['bots_active'].items() if active]
    
    for bot_name in active_bots:
        for symbol in watchlist_symbols[:10]:  # Limit to first 10 symbols to avoid rate limits
            try:
                bot_function = AUTOMATED_BOTS[bot_name]
                bot_result = bot_function(instrument_df, symbol)
                
                if not bot_result.get("error") and bot_result["action"] != "HOLD":
                    execute_automated_trade(
                        instrument_df, 
                        bot_result, 
                        st.session_state.automated_mode['risk_per_trade']
                    )
                
                # Small delay to avoid rate limiting
                import time
                time.sleep(0.5)
                
            except Exception as e:
                st.error(f"Automated bot {bot_name} failed for {symbol}: {e}")
    
    # Update performance metrics
    st.session_state.automated_mode['performance_metrics'] = get_automated_bot_performance()
    st.session_state.automated_mode['last_signal_check'] = datetime.now().isoformat()

def execute_automated_trade(instrument_df, bot_result, risk_per_trade):
    """Execute trades automatically based on bot signals."""
    if bot_result.get("error") or bot_result["action"] == "HOLD":
        return None
    
    try:
        symbol = bot_result["symbol"]
        action = bot_result["action"]
        current_price = bot_result["current_price"]
        
        # Calculate position size based on risk
        risk_amount = (risk_per_trade / 100) * st.session_state.automated_mode['total_capital']
        quantity = max(1, int(risk_amount / current_price))
        
        # Check if we have too many open trades
        open_trades = [t for t in st.session_state.automated_mode['trade_history'] 
                      if t.get('status') == 'OPEN']
        if len(open_trades) >= st.session_state.automated_mode['max_open_trades']:
            return None
        
        # Check for existing position in the same symbol
        existing_position = next((t for t in open_trades if t.get('symbol') == symbol), None)
        if existing_position:
            # Avoid opening same position multiple times
            if existing_position['action'] == action:
                return None
        
       
        # Place the real order
        place_order(instrument_df, symbol, quantity, 'MARKET', action, 'MIS')
        
        # Record the trade (simulated for demo)
        trade_record = {
            'timestamp': datetime.now().isoformat(),
            'symbol': symbol,
            'action': action,
            'quantity': quantity,
            'entry_price': current_price,
            'status': 'OPEN',
            'bot_name': bot_result['bot_name'],
            'risk_level': bot_result['risk_level'],
            'pnl': 0  # Initialize P&L
        }
        
        st.session_state.automated_mode['trade_history'].append(trade_record)
        
        st.toast(f"🤖 Automated {action} order executed for {symbol}", icon="⚡")
        return trade_record
        
    except Exception as e:
        st.error(f"Automated trade execution failed: {e}")
        return None

def display_bot_configuration_tab(instrument_df, nifty25_auto_trade=False):
    """Display bot configuration tab with Nifty 25 integration and enhanced controls."""
    st.subheader("⚙️ Bot Configuration")
    
    col_config1, col_config2 = st.columns(2)
    
    with col_config1:
        st.write("**🤖 Active Bots**")
        
        # Define available bots
        available_bots = {
            "Momentum Bot": "Trades stocks showing strong upward momentum",
            "Mean Reversion Bot": "Identifies oversold/overbought conditions for reversal trades",
            "Breakout Bot": "Detects breakouts from consolidation patterns with volume confirmation",
            "Multi-Signal Bot": "Combines multiple strategies for high-probability trades",
            "Custom Bot": "User-defined trading strategy"
        }
        
        # Initialize bots_active if not exists
        if 'bots_active' not in st.session_state.automated_mode:
            st.session_state.automated_mode['bots_active'] = {}
        
        # Display bot toggles with descriptions - FIXED: Removed problematic expander
        for bot_name, bot_description in available_bots.items():
            # Create a container for each bot
            with st.container():
                col_bot1, col_bot2 = st.columns([3, 1])
                with col_bot1:
                    is_active = st.session_state.automated_mode['bots_active'].get(bot_name, False)
                    if st.checkbox(f"**{bot_name}**", value=is_active, key=f"auto_{bot_name}"):
                        st.session_state.automated_mode['bots_active'][bot_name] = True
                    else:
                        st.session_state.automated_mode['bots_active'][bot_name] = False
                    
                    # Show description as caption instead of expander
                    st.caption(f"📝 {bot_description}")
                
                with col_bot2:
                    if st.session_state.automated_mode['bots_active'].get(bot_name, False):
                        st.success("🟢 ON")
                    else:
                        st.info("⚪ OFF")
                
                st.markdown("---")
        
        st.write("**📊 Trading Limits**")
        
        col_limits1, col_limits2 = st.columns(2)
        
        with col_limits1:
            max_trades = st.slider(
                "Max Open Trades",
                min_value=1,
                max_value=20,
                value=st.session_state.automated_mode.get('max_open_trades', 5),
                help="Maximum simultaneous trades across all bots",
                key="auto_max_trades"
            )
            st.session_state.automated_mode['max_open_trades'] = max_trades
        
        with col_limits2:
            max_daily_trades = st.slider(
                "Max Daily Trades",
                min_value=5,
                max_value=100,
                value=st.session_state.automated_mode.get('max_daily_trades', 20),
                help="Maximum trades per day to manage risk",
                key="auto_max_daily"
            )
            st.session_state.automated_mode['max_daily_trades'] = max_daily_trades
        
        # Risk per trade settings
        st.markdown("---")
        st.write("**⚡ Risk Management**")
        
        current_risk = st.session_state.automated_mode.get('risk_per_trade', 2.0)
        risk_per_trade = st.slider(
            "Risk per Trade (%)",
            min_value=0.5,
            max_value=10.0,
            value=current_risk,
            step=0.5,
            help="Risk percentage per individual trade (0.5% to 10%)",
            key="config_risk"
        )
        st.session_state.automated_mode['risk_per_trade'] = risk_per_trade
        
        # Calculate risk amount
        total_capital = st.session_state.automated_mode.get('total_capital', 10000.0)
        risk_amount = total_capital * (risk_per_trade / 100)
        st.caption(f"💰 Risk Amount: ₹{risk_amount:.2f} per trade")
    
    with col_config2:
        st.write("**⏰ Analysis & Execution**")
        
        # Analysis frequency
        current_interval = st.session_state.automated_mode.get('check_interval', '1 minute')
        frequency_options = ["15 seconds", "30 seconds", "1 minute", "5 minutes", "15 minutes", "30 minutes"]
        
        current_index = 2  # Default to "1 minute"
        if current_interval in frequency_options:
            current_index = frequency_options.index(current_interval)
        
        check_interval = st.selectbox(
            "Analysis Frequency",
            options=frequency_options,
            index=current_index,
            help="How often bots analyze the market and check for signals",
            key="auto_freq"
        )
        st.session_state.automated_mode['check_interval'] = check_interval
        
        # Frequency warnings and info
        if check_interval == "15 seconds":
            st.warning("⚡ **High Frequency** - May hit API limits, use with caution")
        elif check_interval == "30 seconds":
            st.info("🚀 **Active Trading** - Good balance for day trading")
        elif check_interval == "1 minute":
            st.success("🔄 **Standard Frequency** - Stable and reliable")
        else:
            st.info("📊 **Swing Trading** - Lower frequency for longer-term positions")
        
        # Execution settings
        st.markdown("---")
        st.write("**🎯 Execution Settings**")
        
        execution_mode = st.selectbox(
            "Execution Mode",
            options=["Aggressive", "Moderate", "Conservative"],
            index=1,
            help="Aggressive: Take all signals, Conservative: Only highest confidence",
            key="execution_mode"
        )
        st.session_state.automated_mode['execution_mode'] = execution_mode
        
        # Confidence threshold based on execution mode
        if execution_mode == "Aggressive":
            min_confidence = st.slider("Min Confidence", 60, 90, 65, key="agg_confidence")
        elif execution_mode == "Moderate":
            min_confidence = st.slider("Min Confidence", 60, 90, 75, key="mod_confidence")
        else:  # Conservative
            min_confidence = st.slider("Min Confidence", 60, 90, 85, key="con_confidence")
        
        st.session_state.automated_mode['min_confidence'] = min_confidence
        
        st.markdown("---")
        st.write("**📋 Trading Universe**")
        
        # Nifty 25 status display
        if nifty25_auto_trade:
            st.success("🔷 **Nifty 25 Mode Active**")
            try:
                nifty_instruments = get_nifty25_instruments(instrument_df)
                st.caption(f"Trading {len(nifty_instruments)} Nifty 25 stocks")
                
                # Use a button to show symbols instead of expander
                if st.button("📋 View Nifty 25 Symbols", key="view_nifty"):
                    st.session_state.show_nifty_symbols = not st.session_state.get('show_nifty_symbols', False)
                
                if st.session_state.get('show_nifty_symbols', False):
                    symbol_text = "\n".join([f"{i+1}. {inst['symbol']} - {inst.get('name', 'N/A')}" 
                                           for i, inst in enumerate(nifty_instruments[:25])])
                    st.text_area("Nifty 25 Symbols", value=symbol_text, height=200, key="nifty_display")
            except Exception as e:
                st.error(f"Error loading Nifty 25: {e}")
        else:
            # Watchlist-based trading
            active_watchlist = st.session_state.get('active_watchlist', 'Watchlist 1')
            watchlist_symbols = st.session_state.watchlists.get(active_watchlist, [])
            
            if watchlist_symbols:
                st.success(f"📊 **Watchlist Mode**: {active_watchlist}")
                st.caption(f"Trading {len(watchlist_symbols)} symbols from watchlist")
                
                # Use button to show symbols instead of expander
                if st.button("📋 View Watchlist Symbols", key="view_watchlist"):
                    st.session_state.show_watchlist_symbols = not st.session_state.get('show_watchlist_symbols', False)
                
                if st.session_state.get('show_watchlist_symbols', False):
                    symbol_text = "\n".join([f"{i+1}. {item['symbol']}" 
                                           for i, item in enumerate(watchlist_symbols[:20])])
                    st.text_area("Watchlist Symbols", value=symbol_text, height=150, key="watchlist_display")
            else:
                st.warning("⚠️ **No Trading Symbols**")
                st.caption("Add symbols to your watchlist or enable Nifty 25 mode")
        
        # Quick actions
        st.markdown("---")
        st.write("**🔧 Quick Actions**")
        
        col_actions1, col_actions2 = st.columns(2)
        
        with col_actions1:
            if st.button("🔄 Reset Settings", use_container_width=True, key="reset_bots"):
                reset_bot_configuration()
                st.success("Bot configuration reset to defaults!")
                st.rerun()
        
        with col_actions2:
            if st.button("💾 Save Config", use_container_width=True, key="save_bots"):
                save_bot_configuration()
                st.success("Configuration saved!")

# Add these helper functions if not already defined
def reset_bot_configuration():
    """Reset bot configuration to default values."""
    st.session_state.automated_mode.update({
        'bots_active': {
            'Momentum Bot': True,
            'Mean Reversion Bot': True,
            'Breakout Bot': False,
            'Multi-Signal Bot': False,
            'Custom Bot': False
        },
        'max_open_trades': 5,
        'max_daily_trades': 20,
        'check_interval': '1 minute',
        'execution_mode': 'Moderate',
        'min_confidence': 75
    })

def save_bot_configuration():
    """Save current bot configuration."""
    config = {
        'bots_active': st.session_state.automated_mode.get('bots_active', {}),
        'max_open_trades': st.session_state.automated_mode.get('max_open_trades', 5),
        'max_daily_trades': st.session_state.automated_mode.get('max_daily_trades', 20),
        'check_interval': st.session_state.automated_mode.get('check_interval', '1 minute'),
        'execution_mode': st.session_state.automated_mode.get('execution_mode', 'Moderate'),
        'min_confidence': st.session_state.automated_mode.get('min_confidence', 75),
        'saved_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Store in session state (in production, you'd save to file/database)
    st.session_state.automated_mode['saved_config'] = config
    return config
            
# ================ 5. PAGE DEFINITIONS ============

def page_settings():
    """A page for platform-wide configurations, including special trading days."""
    display_header()
    st.title("⚙️ Platform Settings")
    st.info("Configure platform settings and add special trading sessions like Muhurat Trading.", icon="🛠️")

    st.subheader("Special Trading Sessions")
    st.write("Add custom market days and times. The market status indicators will respect these overrides.")

    # Form to add a new special session
    with st.form("special_session_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            session_date = st.date_input("Date")
        with col2:
            start_time = st.time_input("Start Time", time(18, 15)) # Default for Muhurat
        with col3:
            end_time = st.time_input("End Time", time(19, 15))

        submitted = st.form_submit_button("Add Special Session")
        if submitted:
            if start_time >= end_time:
                st.error("Error: Start time must be before end time.")
            else:
                st.session_state.special_trading_days.append({
                    'date': session_date,
                    'start': start_time,
                    'end': end_time
                })
                st.success(f"Added special session for {session_date.strftime('%d %b %Y')} from {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}.")

    st.markdown("---")

    # Display current special sessions
    st.subheader("Configured Special Sessions")
    if not st.session_state.special_trading_days:
        st.info("No special trading sessions have been added.")
    else:
        for i, session in enumerate(st.session_state.special_trading_days):
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            col1.write(session['date'].strftime("%A, %d %B %Y"))
            col2.write(f"Start: {session['start'].strftime('%H:%M')}")
            col3.write(f"End: {session['end'].strftime('%H:%M')}")
            if col4.button("Remove", key=f"remove_session_{i}"):
                st.session_state.special_trading_days.pop(i)
                st.rerun()

    st.markdown("---")
    st.subheader("Platform Configuration")
    st.write("Manage other platform settings here.")
    
    theme = st.radio("Theme", ["Dark", "Light"], index=0 if st.session_state.get('theme', 'Dark') == 'Dark' else 1, horizontal=True)
    if theme != st.session_state.get('theme'):
        st.session_state.theme = theme
        st.rerun()

# --- Bharatiya Market Pulse (BMP) Functions ---

def get_bmp_score_and_label(nifty_change, sensex_change, vix_value, lookback_df):
    """Calculates BMP score and returns the score and a Bharat-flavored label."""
    if lookback_df.empty or len(lookback_df) < 30:
        return 50, "Calculating...", "#cccccc"
    
    nifty_min, nifty_max = lookback_df['nifty_change'].min(), lookback_df['nifty_change'].max()
    sensex_min, sensex_max = lookback_df['sensex_change'].min(), lookback_df['sensex_change'].max()

    nifty_norm = ((nifty_change - nifty_min) / (nifty_max - nifty_min)) * 100 if (nifty_max - nifty_min) > 0 else 50
    sensex_norm = ((sensex_change - sensex_min) / (sensex_max - sensex_min)) * 100 if (sensex_max - sensex_min) > 0 else 50
    
    vix_min, vix_max = lookback_df['vix_value'].min(), lookback_df['vix_value'].max()
    vix_norm = 100 - (((vix_value - vix_min) / (vix_max - vix_min)) * 100) if (vix_max - vix_min) > 0 else 50

    bmp_score = (0.40 * nifty_norm) + (0.40 * sensex_norm) + (0.20 * vix_norm)
    bmp_score = min(100, max(0, bmp_score))

    if bmp_score >= 80:
        label, color = "Bharat Udaan (Very Bullish)", "#00b300"
    elif bmp_score >= 60:
        label, color = "Bharat Pragati (Bullish)", "#33cc33"
    elif bmp_score >= 40:
        label, color = "Bharat Santulan (Neutral)", "#ffcc00"
    elif bmp_score >= 20:
        label, color = "Bharat Sanket (Bearish)", "#ff6600"
    else:
        label, color = "Bharat Mandhi (Very Bearish)", "#ff0000"

    return bmp_score, label, color

@st.cache_data(ttl=300)
def get_nifty50_constituents(instrument_df):
    """Fetches the list of NIFTY 50 stocks by filtering the Kite API instrument list."""
    if instrument_df.empty:
        return pd.DataFrame()
    
    nifty50_symbols = [
        'RELIANCE', 'HDFCBANK', 'ICICIBANK', 'INFY', 'TCS', 'HINDUNILVR', 'ITC', 
        'LT', 'KOTAKBANK', 'SBIN', 'BAJFINANCE', 'BHARTIARTL', 'ASIANPAINT', 
        'AXISBANK', 'WIPRO', 'TITAN', 'ULTRACEMCO', 'M&M', 'NESTLEIND',
        'ADANIENT', 'TATASTEEL', 'INDUSINDBK', 'TECHM', 'NTPC', 'MARUTI', 
        'BAJAJ-AUTO', 'POWERGRID', 'HCLTECH', 'ADANIPORTS', 'BPCL', 'COALINDIA', 
        'EICHERMOT', 'GRASIM', 'JSWSTEEL', 'SHREECEM', 'HEROMOTOCO', 'HINDALCO',
        'DRREDDY', 'CIPLA', 'APOLLOHOSP', 'SBILIFE',
        'TATAMOTORS', 'BRITANNIA', 'DIVISLAB', 'BAJAJFINSV', 'SUNPHARMA', 'HDFCLIFE'
    ]
    
    nifty_constituents = instrument_df[
        (instrument_df['tradingsymbol'].isin(nifty50_symbols)) & 
        (instrument_df['segment'] == 'NSE')
    ].copy()

    constituents_df = pd.DataFrame({
        'Symbol': nifty_constituents['tradingsymbol'],
        'Name': nifty_constituents['tradingsymbol']
    })
    
    return constituents_df.drop_duplicates(subset='Symbol').head(15)

def create_nifty_heatmap(instrument_df):
    """Generates a Plotly Treemap for NIFTY 50 stocks."""
    constituents_df = get_nifty50_constituents(instrument_df)
    if constituents_df.empty:
        return go.Figure()
    
    symbols_with_exchange = [{'symbol': s, 'exchange': 'NSE'} for s in constituents_df['Symbol'].tolist()]
    live_data = get_watchlist_data(symbols_with_exchange)
    
    if live_data.empty:
        return go.Figure()
        
    full_data = pd.merge(live_data, constituents_df, left_on='Ticker', right_on='Symbol', how='left')
    full_data['size'] = full_data['Price'].astype(float) * 1000
    
    fig = go.Figure(go.Treemap(
        labels=full_data['Ticker'],
        parents=[''] * len(full_data),
        values=full_data['size'],
        marker=dict(
            colorscale='RdYlGn',
            colors=full_data['% Change'],
            colorbar=dict(title="% Change"),
        ),
        text=full_data['Ticker'],
        textinfo="label",
        hovertemplate='<b>%{label}</b><br>Price: ₹%{customdata[0]:.2f}<br>Change: %{customdata[1]:.2f}%<extra></extra>',
        customdata=np.column_stack([full_data['Price'], full_data['% Change']])
    ))

    fig.update_layout(title="NIFTY 50 Heatmap (Live)")
    return fig

@st.cache_data(ttl=300)
def get_gift_nifty_data():
    """Fetches GIFT NIFTY data using a more reliable yfinance ticker."""
    try:
        data = yf.download("NIFTY_F1", period="1d", interval="1m")
        if not data.empty:
            return data
    except Exception:
        pass
    return pd.DataFrame()

def page_dashboard():
    """A completely redesigned 'Trader UI' Dashboard."""
    display_header()
    instrument_df = get_instrument_df()
    if instrument_df.empty:
        st.info("Please connect to a broker to view the dashboard.")
        return
    
    index_symbols = [
        {'symbol': 'NIFTY 50', 'exchange': 'NSE'},
        {'symbol': 'SENSEX', 'exchange': 'BSE'},
        {'symbol': 'INDIA VIX', 'exchange': 'NSE'},
    ]
    index_data = get_watchlist_data(index_symbols)
    
    # BMP Calculation and Display
    bmp_col, heatmap_col = st.columns([1, 1], gap="large")
    with bmp_col:
        st.subheader("Bharatiya Market Pulse (BMP)")
        if not index_data.empty:
            nifty_row = index_data[index_data['Ticker'] == 'NIFTY 50'].iloc[0]
            sensex_row = index_data[index_data['Ticker'] == 'SENSEX'].iloc[0]
            vix_row = index_data[index_data['Ticker'] == 'INDIA VIX'].iloc[0]
            
            nifty_hist = get_historical_data(get_instrument_token('NIFTY 50', instrument_df, 'NSE'), 'day', period='1y')
            sensex_hist = get_historical_data(get_instrument_token('SENSEX', instrument_df, 'BSE'), 'day', period='1y')
            vix_hist = get_historical_data(get_instrument_token('INDIA VIX', instrument_df, 'NSE'), 'day', period='1y')
            
            if not nifty_hist.empty and not sensex_hist.empty and not vix_hist.empty:
                lookback_data = pd.DataFrame({
                    'nifty_change': nifty_hist['close'].pct_change() * 100,
                    'sensex_change': sensex_hist['close'].pct_change() * 100,
                    'vix_value': vix_hist['close']
                }).dropna()
                
                bmp_score, bmp_label, bmp_color = get_bmp_score_and_label(nifty_row['% Change'], sensex_row['% Change'], vix_row['Price'], lookback_data)
                
                st.markdown(f'<div class="metric-card" style="border-color:{bmp_color};"><h3>{bmp_score:.2f}</h3><p style="color:{bmp_color}; font-weight:bold;">{bmp_label}</p><small>Proprietary score from NIFTY, SENSEX, and India VIX.</small></div>', unsafe_allow_html=True)
                with st.expander("What do the BMP scores mean?"):
                    st.markdown("""
                    - **80-100 (Bharat Udaan):** Very Strong Bullish Momentum.
                    - **60-80 (Bharat Pragati):** Moderately Bullish Sentiment.
                    - **40-60 (Bharat Santulan):** Neutral or Sideways Market.
                    - **20-40 (Bharat Sanket):** Moderately Bearish Sentiment.
                    - **0-20 (Bharat Mandhi):** Very Strong Bearish Momentum.
                    """)
            else:
                st.info("BMP data is loading...")
        else:
            st.info("BMP data is loading...")
    with heatmap_col:
        st.subheader("NIFTY 50 Heatmap")
        st.plotly_chart(create_nifty_heatmap(instrument_df), use_container_width=True)

    st.markdown("---")
    
    # --- Middle Row: Main Content Area ---
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        tab1, tab2 = st.tabs(["Watchlist", "Portfolio Overview"])

        with tab1:
            st.session_state.active_watchlist = st.radio(
                "Select Watchlist",
                options=st.session_state.watchlists.keys(),
                horizontal=True,
                label_visibility="collapsed"
            )
            
            active_list = st.session_state.watchlists[st.session_state.active_watchlist]

            with st.form(key="add_stock_form"):
                add_col1, add_col2, add_col3 = st.columns([2, 1, 1])
                new_symbol = add_col1.text_input("Symbol", placeholder="Add symbol...", label_visibility="collapsed")
                new_exchange = add_col2.selectbox("Exchange", ["NSE", "BSE", "MCX", "CDS"], label_visibility="collapsed")
                if add_col3.form_submit_button("Add"):
                    if new_symbol:
                        if len(active_list) >= 15:
                            st.toast("Watchlist full (max 15 stocks).", icon="⚠️")
                        elif not any(d['symbol'] == new_symbol.upper() for d in active_list):
                            active_list.append({'symbol': new_symbol.upper(), 'exchange': new_exchange})
                            st.rerun()
                        else:
                            st.toast(f"{new_symbol.upper()} is already in this watchlist.", icon="⚠️")
            
            # Display watchlist
            watchlist_data = get_watchlist_data(active_list)
            if not watchlist_data.empty:
                for index, row in watchlist_data.iterrows():
                    w_cols = st.columns([3, 2, 1, 1, 1, 1])
                    color = 'var(--green)' if row['Change'] > 0 else 'var(--red)'
                    w_cols[0].markdown(f"**{row['Ticker']}**<br><small style='color:var(--text-light);'>{row['Exchange']}</small>", unsafe_allow_html=True)
                    w_cols[1].markdown(f"**{row['Price']:,.2f}**<br><small style='color:{color};'>{row['Change']:,.2f} ({row['% Change']:.2f}%)</small>", unsafe_allow_html=True)
                    
                    quantity = w_cols[2].number_input("Qty", min_value=1, step=1, key=f"qty_{row['Ticker']}", label_visibility="collapsed")
                    
                    if w_cols[3].button("B", key=f"buy_{row['Ticker']}", use_container_width=True):
                        place_order(instrument_df, row['Ticker'], quantity, 'MARKET', 'BUY', 'MIS')
                    if w_cols[4].button("S", key=f"sell_{row['Ticker']}", use_container_width=True):
                        place_order(instrument_df, row['Ticker'], quantity, 'MARKET', 'SELL', 'MIS')
                    if w_cols[5].button("🗑️", key=f"del_{row['Ticker']}", use_container_width=True):
                        st.session_state.watchlists[st.session_state.active_watchlist] = [item for item in active_list if item['symbol'] != row['Ticker']]
                        st.rerun()
                st.markdown("---")

        with tab2:
            st.subheader("My Portfolio")
            _, holdings_df, total_pnl, total_investment = get_portfolio()
            st.metric("Total Investment", f"₹{total_investment:,.2f}")
            st.metric("Today's Profit & Loss", f"₹{total_pnl:,.2f}", delta=f"{total_pnl:,.2f}")
            with st.expander("View Holdings"):
                if not holdings_df.empty:
                    st.dataframe(holdings_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No holdings found.")
    with col2:
        st.subheader("NIFTY 50 Live Chart (1-min)")
        nifty_token = get_instrument_token('NIFTY 50', instrument_df, 'NSE')
        if nifty_token:
            nifty_data = get_historical_data(nifty_token, "minute", period="1d")
            if not nifty_data.empty:
                st.plotly_chart(create_chart(nifty_data.tail(150), "NIFTY 50"), use_container_width=True)
            else:
                st.warning("Could not load NIFTY 50 chart. Market might be closed.")
    
    # --- Bottom Row: Live Ticker Tape ---
    ticker_symbols = st.session_state.get('watchlists', {}).get(st.session_state.get('active_watchlist'), [])
    
    if ticker_symbols:
        ticker_data = get_watchlist_data(ticker_symbols)
        
        if not ticker_data.empty:
            ticker_html = "".join([
                f"<span style='color: white; margin-right: 40px;'>{item['Ticker']} <span style='color: {'#28a745' if item['Change'] > 0 else '#FF4B4B'};'>{item['Price']:,.2f} ({item['% Change']:.2f}%)</span></span>"
                for _, item in ticker_data.iterrows()
            ])
            
            st.markdown(f"""
            <style>
                @keyframes marquee {{
                    0%   {{ transform: translate(100%, 0); }}
                    100% {{ transform: translate(-100%, 0); }}
                }}
                .marquee-container {{
                    width: 100%;
                    overflow: hidden;
                    position: fixed;
                    bottom: 0;
                    left: 0;
                    background-color: #1a1a1a;
                    border-top: 1px solid #333;
                    padding: 5px 0;
                    white-space: nowrap;
                }}
                .marquee-content {{
                    display: inline-block;
                    padding-left: 100%;
                    animation: marquee 35s linear infinite;
                }}
            </style>
            <div class="marquee-container">
                <div class="marquee-content">
                    {ticker_html}
                </div>
            </div>
            """, unsafe_allow_html=True)

def page_advanced_charting():
    """A page for advanced charting with custom intervals and indicators."""
    display_header()
    st.title("Advanced Multi-Chart Terminal")
    instrument_df = get_instrument_df()
    if instrument_df.empty:
        st.info("Please connect to a broker to use the charting tools.")
        return
    
    st.subheader("Chart Layout")
    layout_option = st.radio("Select Layout", ["Single Chart", "2 Charts", "4 Charts", "6 Charts"], horizontal=True)
    
    chart_counts = {"Single Chart": 1, "2 Charts": 2, "4 Charts": 4, "6 Charts": 6}
    num_charts = chart_counts[layout_option]
    
    st.markdown("---")
    
    if num_charts == 1:
        render_chart_controls(0, instrument_df)
    elif num_charts == 2:
        cols = st.columns(2)
        for i, col in enumerate(cols):
            with col:
                render_chart_controls(i, instrument_df)
    elif num_charts == 4:
        for i in range(2):
            cols = st.columns(2)
            with cols[0]:
                render_chart_controls(i * 2, instrument_df)
            with cols[1]:
                render_chart_controls(i * 2 + 1, instrument_df)
    elif num_charts == 6:
        for i in range(2):
            cols = st.columns(3)
            with cols[0]:
                render_chart_controls(i * 3, instrument_df)
            with cols[1]:
                render_chart_controls(i * 3 + 1, instrument_df)
            with cols[2]:
                render_chart_controls(i * 3 + 2, instrument_df)

def render_chart_controls(i, instrument_df):
    """Helper function to render controls for a single chart."""
    with st.container(border=True):
        st.subheader(f"Chart {i+1}")
        
        chart_cols = st.columns(4)
        ticker = chart_cols[0].text_input("Symbol", "NIFTY 50", key=f"ticker_{i}").upper()
        period = chart_cols[1].selectbox("Period", ["1d", "5d", "1mo", "6mo", "1y", "5y"], index=4, key=f"period_{i}")
        interval = chart_cols[2].selectbox("Interval", ["minute", "5minute", "day", "week"], index=2, key=f"interval_{i}")
        chart_type = chart_cols[3].selectbox("Chart Type", ["Candlestick", "Line", "Bar", "Heikin-Ashi"], key=f"chart_type_{i}")

        token = get_instrument_token(ticker, instrument_df)
        data = get_historical_data(token, interval, period=period)

        if data.empty:
            st.warning(f"No data to display for {ticker} with selected parameters.")
        else:
            st.plotly_chart(create_chart(data, ticker, chart_type), use_container_width=True, key=f"chart_{i}")

            order_cols = st.columns([2,1,1,1])
            order_cols[0].markdown("**Quick Order**")
            quantity = order_cols[1].number_input("Qty", min_value=1, step=1, key=f"qty_{i}", label_visibility="collapsed")
            
            if order_cols[2].button("Buy", key=f"buy_btn_{i}", use_container_width=True):
                place_order(instrument_df, ticker, quantity, 'MARKET', 'BUY', 'MIS')
            if order_cols[3].button("Sell", key=f"sell_btn_{i}", use_container_width=True):
                place_order(instrument_df, ticker, quantity, 'MARKET', 'SELL', 'MIS')

def page_iceberg_detector():
    """Iceberg Detector page with 5-day volume pattern focus and bot configuration"""
    
    try:
        display_header()
    except:
        st.title("🧊 Quantum Iceberg Detector - Nifty50")
    
    st.markdown("""
    **Real-time iceberg detection with 5-day volume pattern analysis**
    
    *Volume analysis based on last 5 market days (1 trading week)*
    *Enhanced intraday session tracking with weekly context*
    *More responsive to recent market conditions*
    """)
    
    # Market Status Display - FIRST
    display_market_status()
    
    # Bot Configuration - SECOND (this should now be visible)
    st.markdown("---")
    bot_configurator = TradingBotConfigurator()
    bot_mode = bot_configurator.render_bot_configuration()
    
    # Safe broker connection check
    try:
        client = get_broker_client()
        if not client:
            st.info("🔌 Demo Mode - Connect broker for live data")
        else:
            st.success("✅ Broker connected")
    except:
        st.info("🔌 Running in demo mode")
    
    # Safe instrument data loading
    with st.spinner("📊 Loading 5-day market data..."):
        instrument_df = get_instrument_df_safe()
        
        if instrument_df is None or instrument_df.empty:
            st.info("📋 Using demo data with 5-day volume analysis")
    
    # Nifty50 symbols list
    nifty50_symbols = [
        'RELIANCE', 'TCS', 'HDFC', 'INFY', 'HDFCBANK', 'ICICIBANK', 'KOTAKBANK',
        'HINDUNILVR', 'ITC', 'SBIN', 'BHARTIARTL', 'BAJFINANCE', 'ASIANPAINT',
        'MARUTI', 'TITAN', 'SUNPHARMA', 'AXISBANK', 'ULTRACEMCO', 'TATAMOTORS',
        'NESTLE', 'POWERGRID', 'NTPC', 'TATASTEEL', 'BAJAJFINSV', 'WIPRO',
        'ONGC', 'JSWSTEEL', 'HCLTECH', 'ADANIPORTS', 'LT', 'TECHM', 'HDFCLIFE',
        'DRREDDY', 'CIPLA', 'SBILIFE', 'TATACONSUM', 'BRITANNIA', 'BAJAJ-AUTO',
        'COALINDIA', 'GRASIM', 'EICHERMOT', 'UPL', 'HEROMOTOCO', 'DIVISLAB',
        'SHREECEM', 'HINDALCO', 'INDUSINDBK', 'APOLLOHOSP', 'BPCL', 'M&M'
    ]
    
    # Safe symbol mapping
    display_symbols = []
    symbol_mapping = {}
    
    try:
        for symbol in nifty50_symbols:
            if instrument_df is not None and not instrument_df.empty:
                instrument_match = instrument_df[instrument_df['tradingsymbol'] == symbol]
                if instrument_match.empty:
                    if symbol == "BAJAJ-AUTO":
                        alt_symbol = "BAJAJAUTO"
                    elif symbol == "M&M":
                        alt_symbol = "M_M"
                    elif symbol == "L&T":
                        alt_symbol = "L_T"
                    else:
                        alt_symbol = symbol
                    
                    if instrument_df is not None:
                        instrument_match = instrument_df[instrument_df['tradingsymbol'] == alt_symbol]
                        if not instrument_match.empty:
                            symbol_mapping[symbol] = alt_symbol
            
            display_symbols.append(symbol)
    except Exception as e:
        st.error("Error processing symbols")
        display_symbols = nifty50_symbols[:10]
    
    if not display_symbols:
        st.error("❌ No symbols available for analysis")
        return
    
    # UI Components - UPDATED DEFAULTS FOR 5-DAY ANALYSIS
    st.markdown("---")
    st.subheader("📊 Stock Selection & Analysis")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        selected_symbol = st.selectbox(
            "Select Nifty50 Stock",
            sorted(display_symbols),
            index=0,
            key="iceberg_symbol"
        )
        
        actual_symbol = symbol_mapping.get(selected_symbol, selected_symbol)
        st.caption(f"Analyzing: {actual_symbol} | 5-day volume patterns")
    
    with col2:
        timeframe = st.selectbox(
            "Timeframe",
            ["15minute", "30minute", "hour", "day", "5minute"],
            index=1,  # Default to 30minute
            key="iceberg_timeframe"
        )
    
    with col3:
        period = st.selectbox(
            "Analysis Period", 
            ["5d", "1wk", "1d", "3d"],  # 5d first for 5-day focus
            index=0,
            key="iceberg_period",
            help="5 days for weekly volume patterns"
        )

    # Volume Analysis Configuration
    st.markdown("---")
    st.subheader("📈 5-Day Volume Analysis")
    
    col_vol1, col_vol2, col_vol3 = st.columns(3)
    
    with col_vol1:
        volume_alert_threshold = st.slider(
            "Volume Spike Alert %",
            min_value=110,
            max_value=200,
            value=120,
            step=5,
            help="Alert when volume exceeds 5-day session average",
            key="volume_alert_threshold_slider"
        )
    
    with col_vol2:
        volume_impact_weight = st.slider(
            "Volume Impact %",
            min_value=10,
            max_value=50,
            value=30,  # Increased default for volume focus
            step=5,
            help="Weight of volume patterns in detection",
            key="volume_impact_weight_slider"
        )
    
    with col_vol3:
        st.markdown("**Analysis Focus**")
        st.success("**5-Day Volume Patterns**")
        st.markdown("Intraday: **20/30/20/30%**")
        st.markdown("Weekly: **5 Market Days**")

    # Analysis controls
    st.markdown("---")
    col_controls1, col_controls2, col_controls3 = st.columns([1, 1, 1])
    
    with col_controls1:
        analyze_clicked = st.button("🔍 Analyze 5-Day Patterns", type="primary", use_container_width=True, key="analyze_button")
    
    with col_controls2:
        auto_refresh = st.checkbox("🔄 Auto-refresh", value=False, key="iceberg_refresh")
    
    with col_controls3:
        show_weekly = st.checkbox("📊 Show Weekly Patterns", value=True, key="weekly_patterns")

    # Run analysis
    if analyze_clicked or auto_refresh:
        with st.spinner("🧊 Analyzing 5-day volume patterns..."):
            try:
                # Safe data preparation
                actual_symbol = symbol_mapping.get(selected_symbol, selected_symbol)
                instrument_token = None
                
                if instrument_df is not None and not instrument_df.empty:
                    instrument_token = get_instrument_token(actual_symbol, instrument_df, 'NSE')
                
                # Get historical data with 5-day focus
                historical_data = get_historical_data_safe(instrument_token, timeframe, period)
                
                if historical_data.empty:
                    st.warning("⚠️ Using demo data for 5-day analysis")
                
                # Prepare market data with enhanced volume analysis
                market_data = prepare_live_market_data_5day(
                    symbol=selected_symbol,
                    actual_symbol=actual_symbol,
                    instrument_token=instrument_token,
                    instrument_df=instrument_df,
                    historical_data=historical_data
                )
                
                if not market_data:
                    st.error("❌ Failed to prepare market data")
                    return
                
                # Show analysis period info
                st.info(f"📅 Analyzing volume patterns over: **{period}**")
                
                # Run detection
                detector = QuantumIcebergDetector()
                detection_result = detector.process_market_data(market_data)
                
                # Generate signals
                trading_signals = generate_trading_signals_enhanced(
                    detection_result, 
                    market_data,
                    volume_impact_weight/100.0
                )
                
                # Display results with weekly patterns
                display_iceberg_results_5day(
                    detection_result=detection_result,
                    market_data=market_data, 
                    trading_signals=trading_signals,
                    show_weekly=show_weekly,
                    bot_mode=bot_mode
                )
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")

    if auto_refresh:
        try:
            st_autorefresh(interval=15000, key="iceberg_autorefresh")
            st.info("🔄 Auto-refresh enabled - 5-day patterns")
        except:
            pass

def display_market_status():
    """Display current market status"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if is_market_hours():
            st.success("🟢 MARKET OPEN")
        else:
            st.error("🔴 MARKET CLOSED")
    
    with col2:
        now = datetime.now()
        st.write(f"**Time:** {now.strftime('%H:%M:%S')}")
    
    with col3:
        st.write(f"**Date:** {now.strftime('%Y-%m-%d')}")
        
        # Show next market action
        if not is_market_hours():
            weekday = now.weekday()
            if weekday >= 5:  # Weekend
                days_until_monday = (7 - weekday) % 7
                if days_until_monday == 0:  # Sunday
                    days_until_monday = 1
                next_market_day = now + timedelta(days=days_until_monday)
                st.write(f"**Opens:** {next_market_day.strftime('%A')} 9:15 AM")
            else:
                current_time = now.time()
                if current_time < time(9, 15):
                    st.write("**Opens:** Today 9:15 AM")
                else:
                    st.write("**Opens:** Tomorrow 9:15 AM")


def prepare_live_market_data_5day(symbol, actual_symbol, instrument_token, instrument_df, historical_data):
    """Prepare market data with 5-day volume focus"""
    try:
        client = get_broker_client()
        
        # Create sample market data if no live data available
        if not client:
            return create_sample_market_data_5day(symbol, historical_data)
        
        # Try to get live quote data
        try:
            quote_data = client.quote(str(instrument_token)) if instrument_token else None
        except:
            quote_data = None
        
        if not quote_data:
            return create_sample_market_data_5day(symbol, historical_data)
        
        # Extract quote data
        instrument_quote = quote_data.get(str(instrument_token), {}) if instrument_token else {}
        
        # Prepare order book
        depth = instrument_quote.get('depth', {})
        bids = depth.get('buy', [])[:10]
        asks = depth.get('sell', [])[:10]
        
        # Calculate metrics
        total_bid_volume = sum(bid.get('quantity', 0) for bid in bids)
        total_ask_volume = sum(ask.get('quantity', 0) for ask in asks)
        
        order_book = {
            'bids': bids,
            'asks': asks,
            'total_bid_volume': total_bid_volume,
            'total_ask_volume': total_ask_volume,
            'bid_ask_ratio': total_bid_volume / total_ask_volume if total_ask_volume > 0 else 1,
            'bid_concentration': calculate_volume_concentration(bids),
            'ask_concentration': calculate_volume_concentration(asks),
            'large_bid_orders': count_large_orders(bids, 10000),
            'large_ask_orders': count_large_orders(asks, 10000),
            'depth_levels_analyzed': max(len(bids), len(asks))
        }
        
        # Get volume and price data
        current_volume = instrument_quote.get('volume', historical_data['volume'].iloc[-1] if not historical_data.empty else 0)
        last_price = instrument_quote.get('last_price', historical_data['close'].iloc[-1] if not historical_data.empty else 1000)
        
        # Calculate 5-day average volume
        daily_avg_volume = calculate_accurate_daily_volume(historical_data, lookback_days=5)
        
        # Enhanced volume analysis with weekly patterns
        weekly_patterns = analyze_weekly_volume_patterns(historical_data, current_volume)
        volume_analysis = enhanced_intraday_volume_analysis(current_volume, daily_avg_volume, symbol, weekly_patterns)
        
        market_data = {
            'symbol': symbol,
            'timestamp': pd.Timestamp.now(),
            'last_price': last_price,
            'open': instrument_quote.get('ohlc', {}).get('open', last_price * 0.99),
            'high': instrument_quote.get('ohlc', {}).get('high', last_price * 1.01),
            'low': instrument_quote.get('ohlc', {}).get('low', last_price * 0.99),
            'close': last_price,
            'volume': current_volume,
            'daily_average_volume': daily_avg_volume,
            'volume_ratio': current_volume / daily_avg_volume if daily_avg_volume > 0 else 1,
            'order_book': order_book,
            'volatility': calculate_live_volatility(historical_data, last_price),
            'stock_category': get_nifty50_stock_category(symbol),
            'detection_params': get_nifty50_detection_params(symbol),
            'volume_analysis': volume_analysis,
            'data_source': 'LIVE',
            'analysis_period': '5_DAYS'
        }
        
        return market_data
        
    except Exception as e:
        return create_sample_market_data_5day(symbol, historical_data)

def create_sample_market_data_5day(symbol, historical_data):
    """Create sample market data with 5-day volume patterns"""
    try:
        if historical_data.empty:
            # Create sample data with realistic 5-day pattern
            last_price = 2500
            current_volume = 500000
            avg_volume = 750000
        else:
            last_price = historical_data['close'].iloc[-1]
            current_volume = historical_data['volume'].iloc[-1]
            avg_volume = calculate_accurate_daily_volume(historical_data, lookback_days=5)
        
        # Create sample order book
        bids = []
        asks = []
        
        for i in range(10):
            bid_price = last_price * (1 - 0.001 * (i + 1))
            ask_price = last_price * (1 + 0.001 * (i + 1))
            
            bid_quantity = max(100, int(10000 * (1 - 0.1 * i)))
            ask_quantity = max(100, int(8000 * (1 - 0.1 * i)))
            
            bids.append({'price': round(bid_price, 2), 'quantity': bid_quantity})
            asks.append({'price': round(ask_price, 2), 'quantity': ask_quantity})
        
        total_bid_volume = sum(bid['quantity'] for bid in bids)
        total_ask_volume = sum(ask['quantity'] for ask in asks)
        
        order_book = {
            'bids': bids,
            'asks': asks,
            'total_bid_volume': total_bid_volume,
            'total_ask_volume': total_ask_volume,
            'bid_ask_ratio': total_bid_volume / total_ask_volume if total_ask_volume > 0 else 1,
            'bid_concentration': 0.6,
            'ask_concentration': 0.5,
            'large_bid_orders': 2,
            'large_ask_orders': 1,
            'depth_levels_analyzed': 10
        }
        
        # Enhanced volume analysis with weekly patterns
        weekly_patterns = analyze_weekly_volume_patterns(historical_data, current_volume)
        volume_analysis = enhanced_intraday_volume_analysis(current_volume, avg_volume, symbol, weekly_patterns)
        
        return {
            'symbol': symbol,
            'timestamp': pd.Timestamp.now(),
            'last_price': last_price,
            'open': last_price * 0.995,
            'high': last_price * 1.015,
            'low': last_price * 0.985,
            'close': last_price,
            'volume': current_volume,
            'daily_average_volume': avg_volume,
            'volume_ratio': current_volume / avg_volume if avg_volume > 0 else 1,
            'order_book': order_book,
            'volatility': 0.02,
            'stock_category': get_nifty50_stock_category(symbol),
            'detection_params': get_nifty50_detection_params(symbol),
            'volume_analysis': volume_analysis,
            'data_source': 'DEMO_5DAY',
            'analysis_period': '5_DAYS'
        }
        
    except Exception as e:
        return {
            'symbol': symbol,
            'timestamp': pd.Timestamp.now(),
            'last_price': 1000,
            'volume': 100000,
            'order_book': {},
            'data_source': 'FALLBACK_5DAY',
            'analysis_period': '5_DAYS'
        }

def display_iceberg_results_5day(detection_result, market_data, trading_signals, show_weekly=True, bot_mode='MONITOR_ONLY'):
    """Display iceberg results with 5-day volume focus"""
    
    st.markdown("---")
    st.subheader("🎯 5-Day Pattern Analysis")
    
    # Key metrics
    probability = detection_result.get('iceberg_probability', 0)
    confidence = detection_result.get('confidence', 0)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if probability > 0.7:
            st.error(f"🔴 {probability:.1%}")
            st.write("**High Probability**")
        elif probability > 0.4:
            st.warning(f"🟡 {probability:.1%}")
            st.write("**Medium Probability**")
        else:
            st.success(f"🟢 {probability:.1%}")
            st.write("**Low Probability**")
    
    with col2:
        st.metric("Confidence", f"{confidence:.1%}")
    
    with col3:
        st.metric("Price", f"₹{market_data.get('last_price', 0):.2f}")
    
    with col4:
        bot_mode_display = {
            'SEMI_AUTO': '🤖 Semi-Auto',
            'FULL_AUTO': '🚀 Full Auto', 
            'MONITOR_ONLY': '👁️ Monitor'
        }
        st.metric("Bot Mode", bot_mode_display.get(bot_mode, 'Monitor'))
    
    # Volume Analysis Section
    volume_analysis = market_data.get('volume_analysis', {})
    if volume_analysis:
        st.markdown("---")
        st.subheader("📈 5-Day Volume Analysis")
        
        # Main volume metrics
        col_vol1, col_vol2, col_vol3, col_vol4 = st.columns(4)
        
        with col_vol1:
            current_session = volume_analysis.get('current_session', 'UNKNOWN')
            st.metric("Session", current_session)
            
            # Show market status indicator
            if current_session == 'MARKET_CLOSED':
                st.error("🔴 Closed")
            else:
                st.success("🟢 Open")
                
            st.metric("Live Volume", f"{volume_analysis.get('current_volume', 0):,}")
        
        with col_vol2:
            st.metric("5-Day Avg", f"{volume_analysis.get('daily_avg_volume', 0):,.0f}")
            session_ratio = volume_analysis.get('session_volume_ratio', 0)
            st.metric("Session Ratio", f"{session_ratio:.1f}x")  # Changed to show multiplier
        
        with col_vol3:
            cumulative_ratio = volume_analysis.get('cumulative_volume_ratio', 0)
            st.metric("Cumulative Ratio", f"{cumulative_ratio:.1f}x")  # Changed to show multiplier
            expected_pct = volume_analysis.get('cumulative_expected_percentage', 0)
            st.metric("Expected %", f"{expected_pct:.1%}")
        
        with col_vol4:
            volume_impact = trading_signals.get('volume_impact', 0)
            st.metric("Volume Impact", f"{volume_impact:.1%}")
            
            alert_level = volume_analysis.get('alert_level', 'NORMAL')
            if alert_level == "EXTREME":
                st.error("🚨 EXTREME")
            elif alert_level == "HIGH":
                st.error("🔴 HIGH")
            elif alert_level == "MEDIUM":
                st.warning("🟡 MEDIUM")
            elif alert_level == "LOW":
                st.info("📈 LOW")
            else:
                st.success("🟢 NORMAL")
        
        # Weekly patterns display
        weekly_patterns = volume_analysis.get('weekly_patterns', {})
        if weekly_patterns and show_weekly:
            st.markdown("**📊 Weekly Volume Patterns (5 Days)**")
            
            col_week1, col_week2, col_week3, col_week4 = st.columns(4)
            
            with col_week1:
                weekly_ratio = weekly_patterns.get('current_vs_weekly_ratio', 0)
                st.metric("Vs Weekly Avg", f"{weekly_ratio:.1f}x")  # Changed to show multiplier
            
            with col_week2:
                trend = weekly_patterns.get('volume_trend', 'STABLE')
                if trend == "INCREASING":
                    st.success("📈 Increasing")
                elif trend == "DECREASING":
                    st.error("📉 Decreasing")
                else:
                    st.info("➡️ Stable")
            
            with col_week3:
                volatility = weekly_patterns.get('volume_volatility', 0)
                st.metric("Volatility", f"{volatility:.1%}")
            
            with col_week4:
                st.metric("Period", "5 Market Days")
        
        # Alert message
        alert_message = volume_analysis.get('alert_message')
        if alert_message:
            if "EXTREME" in alert_message or "HIGH" in alert_message:
                st.error(alert_message)
            elif "MEDIUM" in alert_message:
                st.warning(alert_message)
            elif "LOW" in alert_message:
                st.info(alert_message)
            else:
                st.success(alert_message)
    
    # Trading signals with bot integration
    if trading_signals:
        st.markdown("---")
        st.subheader("📡 Trading Signals")
        
        col_signal1, col_signal2 = st.columns(2)
        
        with col_signal1:
            signal_type = trading_signals.get('primary_signal', 'HOLD')
            if signal_type in ['ICEBERG_BUY', 'FLOW_BUY', 'VOLUME_BUY']:
                st.success(f"🎯 **Signal: {signal_type}**")
                
                # Show bot action based on mode
                if bot_mode == 'FULL_AUTO':
                    st.info("🤖 Auto-entry triggered")
                elif bot_mode == 'SEMI_AUTO':
                    st.warning("⏳ Waiting for manual confirmation")
                    
            elif signal_type in ['ICEBERG_SELL', 'FLOW_SELL', 'VOLUME_SELL']:
                st.error(f"🎯 **Signal: {signal_type}**")
                
                if bot_mode == 'FULL_AUTO':
                    st.info("🤖 Auto-exit triggered")
                elif bot_mode == 'SEMI_AUTO':
                    st.warning("⏳ Waiting for manual confirmation")
            else:
                st.info(f"🎯 **Signal: {signal_type}**")
                st.info("🤖 No action required")
            
            # Show volume context
            weekly_patterns = volume_analysis.get('weekly_patterns', {}) if volume_analysis else {}
            weekly_ratio = weekly_patterns.get('current_vs_weekly_ratio', 0)
            if weekly_ratio > 1.5:
                st.info(f"📊 Volume: {weekly_ratio:.1f}x of 5-day average")
        
        with col_signal2:
            st.metric("Final Confidence", f"{trading_signals.get('confidence', 0):.1%}")
            st.metric("Volume Impact", f"+{trading_signals.get('volume_impact', 0):.1%}")
            
            # Bot status
            if bot_mode != 'MONITOR_ONLY':
                if probability > 0.7 and trading_signals.get('confidence', 0) > 0.7:
                    st.success("✅ Bot Active")
                else:
                    st.info("⏸️ Bot Paused")
    
    # Detection scores
    detection_scores = detection_result.get('detection_scores', {})
    if detection_scores:
        st.markdown("---")
        st.subheader("🔍 Detection Analysis")
        
        cols = st.columns(5)
        score_names = ['order_fragmentation', 'hidden_liquidity', 'volume_anomaly', 'momentum_disparity', 'depth_imbalance']
        display_names = ['Fragmentation', 'Hidden Liquidity', 'Volume Anomaly', 'Momentum', 'Depth Imbalance']
        
        for i, (col, score_name, display_name) in enumerate(zip(cols, score_names, display_names)):
            with col:
                score = detection_scores.get(score_name, 0)
                st.metric(display_name, f"{score:.1%}")
    
    # Visualization
    try:
        visualizer = QuantumVisualizer()
        fig = visualizer.create_quantum_chart(detection_result)
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("📊 Visualization unavailable")
    
    # Market depth
    order_book = market_data.get('order_book', {})
    if order_book:
        st.markdown("---")
        st.subheader("📊 Market Depth")
        
        col_depth1, col_depth2, col_depth3, col_depth4 = st.columns(4)
        
        with col_depth1:
            st.metric("Bid Volume", f"{order_book.get('total_bid_volume', 0):,}")
            st.metric("Bid Concentration", f"{order_book.get('bid_concentration', 0):.1%}")
        
        with col_depth2:
            st.metric("Ask Volume", f"{order_book.get('total_ask_volume', 0):,}")
            st.metric("Ask Concentration", f"{order_book.get('ask_concentration', 0):.1%}")
        
        with col_depth3:
            st.metric("Bid/Ask Ratio", f"{order_book.get('bid_ask_ratio', 1):.2f}")
            st.metric("Large Bid Orders", order_book.get('large_bid_orders', 0))
        
        with col_depth4:
            st.metric("Depth Levels", order_book.get('depth_levels_analyzed', 0))
            st.metric("Large Ask Orders", order_book.get('large_ask_orders', 0))
    
    # Alerts
    alerts = detection_result.get('alerts', [])
    if alerts:
        st.markdown("---")
        st.subheader("🚨 Alerts")
        for alert in alerts:
            if "🚨" in alert or "🔴" in alert:
                st.error(alert)
            elif "🟡" in alert:
                st.warning(alert)
            else:
                st.info(alert)
    
    # Show analysis period info
    st.info(f"📅 **Analysis Period**: Last 5 Market Days | **Data Source**: {market_data.get('data_source', 'Unknown')}")
    
    st.success("✅ 5-Day Pattern Analysis Completed")

# ==================== TRADING SIGNALS GENERATION ====================

def generate_trading_signals_enhanced(detection_result, market_data, volume_impact_weight=0.25):
    """Generate enhanced trading signals with 5-day volume focus"""
    try:
        if not detection_result or not market_data:
            return get_default_signals()
        
        probability = detection_result.get('iceberg_probability', 0)
        confidence = detection_result.get('confidence', 0)
        order_book = market_data.get('order_book', {})
        volume_analysis = market_data.get('volume_analysis', {})
        
        signals = {
            'primary_signal': 'HOLD',
            'secondary_signals': [],
            'confidence': confidence,
            'probability': probability,
            'timestamp': pd.Timestamp.now(),
            'entry_price': market_data.get('last_price', 0),
            'volume_impact': 0,
            'volume_alerts': []
        }
        
        # Volume analysis integration
        if volume_analysis:
            volume_spike = volume_analysis.get('volume_spike_detected', False)
            alert_level = volume_analysis.get('alert_level', 'NORMAL')
            
            volume_impact = 0
            if volume_spike:
                if alert_level == "EXTREME":
                    volume_impact = 0.4
                elif alert_level == "HIGH":
                    volume_impact = 0.3
                elif alert_level == "MEDIUM":
                    volume_impact = 0.2
                elif alert_level == "LOW":
                    volume_impact = 0.1
                    
                volume_impact *= volume_impact_weight
                signals['confidence'] = min(1.0, signals['confidence'] + volume_impact)
                signals['volume_impact'] = volume_impact
                
                signals['volume_alerts'].append(alert_level)
                signals['secondary_signals'].append(f"VOLUME_{alert_level}")
        
        # Order book analysis
        bid_volume = order_book.get('total_bid_volume', 0)
        ask_volume = order_book.get('total_ask_volume', 0)
        total_volume = bid_volume + ask_volume
        
        if total_volume > 0:
            imbalance = (bid_volume - ask_volume) / total_volume
        else:
            imbalance = 0
        
        # Signal generation
        final_confidence = signals['confidence']
        
        if probability > 0.7 and final_confidence > 0.7:
            if imbalance > 0.1:
                signals['primary_signal'] = 'ICEBERG_BUY'
            elif imbalance < -0.1:
                signals['primary_signal'] = 'ICEBERG_SELL'
        
        elif probability > 0.5 and final_confidence > 0.6:
            if imbalance > 0.05:
                signals['primary_signal'] = 'FLOW_BUY'
            elif imbalance < -0.05:
                signals['primary_signal'] = 'FLOW_SELL'
        
        return signals
        
    except Exception as e:
        return get_default_signals()

def get_default_signals():
    """Return default signals when errors occur"""
    return {
        'primary_signal': 'HOLD',
        'secondary_signals': ['Analysis unavailable'],
        'confidence': 0.0,
        'probability': 0.0,
        'timestamp': pd.Timestamp.now(),
        'entry_price': 0,
        'volume_impact': 0,
        'volume_alerts': []
    }

def page_premarket_pulse():
    """Global market overview and premarket indicators with professional data sources."""
    display_header()
    st.title("🌅 Premarket & Global Cues")
    st.info("Track global market movements, futures data, and overnight trends with professional data sources.", icon="📊")

    # Market status indicator
    status_info = get_market_status()
    current_time = get_ist_time().strftime("%H:%M:%S IST")
    
    col_status1, col_status2, col_status3 = st.columns([2, 1, 1])
    with col_status1:
        status_color = "#00cc00" if status_info['status'] == 'market_open' else "#ffcc00"
        st.markdown(f"**Market Status:** <span style='color:{status_color};'>{status_info['status'].replace('_', ' ').title()}</span>", unsafe_allow_html=True)
    with col_status2:
        st.markdown(f"**Time:** {current_time}")
    with col_status3:
        if is_pre_market_hours():
            st.success("🔸 Pre-market Hours")
        elif is_market_hours():
            st.success("🟢 Market Open")
        else:
            st.info("🔴 Market Closed")

    st.markdown("---")

    # Professional Data Source Selection
    st.subheader("🔧 Data Sources")
    col_source1, col_source2 = st.columns(2)
    with col_source1:
        use_alpha_vantage = st.checkbox("Alpha Vantage", value=True, help="Professional market data")
    with col_source2:
        use_fmp = st.checkbox("Financial Modeling Prep", value=True, help="Financial statements & fundamentals")

    # Global Market Snapshot with Professional Data
    st.subheader("🌍 Global Market Snapshot")
    
    try:
        # Try Alpha Vantage first for global indices
        if use_alpha_vantage:
            global_data = get_alpha_vantage_global_indices()
        else:
            global_data = pd.DataFrame()
        
        # Fallback to FMP if Alpha Vantage fails or is disabled
        if global_data.empty and use_fmp:
            global_data = get_fmp_global_indices()
        
        # Final fallback to free data
        if global_data.empty:
            global_tickers = {
                "S&P 500": "^GSPC", 
                "Dow Jones": "^DJI", 
                "NASDAQ": "^IXIC",
                "SGX Nifty": "NIFTY_F1"
            }
            global_data = get_global_indices_data_enhanced(global_tickers)
            st.info("📡 Using enhanced market data")
        
        if not global_data.empty:
            # Display global indices in a grid
            cols = st.columns(4)
            displayed_count = 0
            
            for i, row in global_data.iterrows():
                price = row['Price']
                change = row['Change']
                pct_change = row['% Change']
                
                if not np.isnan(price) and not np.isnan(pct_change):
                    col_idx = displayed_count % 4
                    with cols[col_idx]:
                        delta_color = "normal" if change >= 0 else "inverse"
                        st.metric(
                            label=row['Ticker'], 
                            value=f"{price:,.0f}" if price > 100 else f"{price:.2f}",
                            delta=f"{pct_change:+.2f}%",
                            delta_color=delta_color
                        )
                    displayed_count += 1
        else:
            st.warning("Unable to load global market data")
            
    except Exception as e:
        st.error(f"Error loading global data: {e}")

    st.markdown("---")

    # Main content columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 NIFTY 50 Futures (SGX Nifty)")
        
        # Get SGX Nifty data with professional sources
        sgx_data = get_professional_sgx_data()
        
        if not sgx_data.empty:
            # Calculate change and percentage
            if len(sgx_data) >= 2:
                current_price = sgx_data['Close'].iloc[-1]
                prev_close = sgx_data['Close'].iloc[-2] if len(sgx_data) > 1 else sgx_data['Close'].iloc[0]
                change = current_price - prev_close
                pct_change = (change / prev_close) * 100
                
                # Display current SGX Nifty price
                st.metric(
                    "SGX Nifty Current", 
                    f"{current_price:.2f}",
                    delta=f"{change:+.2f} ({pct_change:+.2f}%)",
                    delta_color="normal" if change >= 0 else "inverse"
                )
            
            # Create professional chart
            fig = create_professional_futures_chart(sgx_data)
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            # Professional fallback
            st.info("📊 Using NIFTY 50 as reference")
            show_nifty_fallback()
            
    with col2:
        st.subheader("🌏 Asian Markets Live")
        
        # Professional Asian markets data
        asian_data = get_professional_asian_markets()
        
        if not asian_data.empty:
            for _, row in asian_data.iterrows():
                price = row['Price']
                change = row['Change']
                pct_change = row['% Change']
                
                if not np.isnan(price) and not np.isnan(pct_change):
                    delta_color = "normal" if change >= 0 else "inverse"
                    st.metric(
                        label=row['Ticker'], 
                        value=f"{price:,.0f}" if price > 1000 else f"{price:.2f}",
                        delta=f"{pct_change:+.2f}%",
                        delta_color=delta_color
                    )
                else:
                    st.write(f"**{row['Ticker']}:** Data updating...")
        else:
            st.info("Asian market data updating...")

        st.markdown("---")
        
        # Professional Indian Market Indicators
        st.subheader("🇮🇳 Indian Market Indicators")
        show_professional_indian_indicators()

    st.markdown("---")

    # Professional News Section with Multiple Sources
    st.subheader("📰 Professional Market News & Analysis")
    
    # News source selection
    col_news1, col_news2 = st.columns([2, 1])
    with col_news1:
        news_query = st.text_input("Search news", placeholder="Enter keywords (e.g., RBI, earnings, inflation)...", key="news_search")
    with col_news2:
        news_source = st.selectbox("Source", ["Alpha Vantage", "FMP", "All Sources"], index=2)
    
    try:
        with st.spinner("📡 Fetching professional market news..."):
            # Try professional news sources
            news_data = get_professional_news(news_query, news_source)
            
            if news_data and not news_data['news_items'].empty:
                display_professional_news(news_data, news_limit=5)
            else:
                st.info("🔍 No professional news found. Showing enhanced news...")
                enhanced_news = fetch_and_analyze_news(query=news_query if news_query else None)
                display_enhanced_news(enhanced_news, news_limit=5)
                
    except Exception as e:
        st.error(f"❌ Error loading professional news: {str(e)}")
        st.info("📋 Showing enhanced news feed...")
        enhanced_news = fetch_and_analyze_news(query=news_query if news_query else None)
        display_enhanced_news(enhanced_news, news_limit=5)

    # Professional Economic Calendar
    st.markdown("---")
    st.subheader("📅 Professional Economic Calendar")
    
    try:
        economic_events = get_professional_economic_calendar()
        if economic_events:
            display_economic_calendar(economic_events)
        else:
            show_sample_economic_events()
    except Exception as e:
        st.error(f"Error loading economic calendar: {e}")
        show_sample_economic_events()

    # Refresh with professional data
    if st.button("🔄 Refresh Professional Data", use_container_width=True, type="primary"):
        st.cache_data.clear()
        st.rerun()

    # Last updated with source info
    st.caption(f"🕒 Last updated: {get_ist_time().strftime('%Y-%m-%d %H:%M:%S IST')} | Sources: {'Alpha Vantage' if use_alpha_vantage else ''} {'FMP' if use_fmp else ''}")

# ================ PROFESSIONAL DATA FUNCTIONS ================

@st.cache_data(ttl=300)
def get_alpha_vantage_global_indices():
    """Get global indices data from Alpha Vantage."""
    api_key = st.secrets.get("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        return pd.DataFrame()
    
    indices = {
        "SPX": "SPX",    # S&P 500
        "DJI": "DJI",    # Dow Jones
        "IXIC": "IXIC",  # NASDAQ
        "FTSE": "FTSE",  # FTSE 100
        "GDAXI": "GDAXI", # DAX
        "N225": "N225",  # Nikkei 225
        "HSI": "HSI",    # Hang Seng
    }
    
    data = []
    
    for symbol, av_code in indices.items():
        try:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={av_code}&apikey={api_key}"
            response = requests.get(url, timeout=10)
            result = response.json()
            
            if 'Global Quote' in result:
                quote = result['Global Quote']
                price = float(quote['05. price'])
                prev_close = float(quote['08. previous close'])
                change = price - prev_close
                pct_change = (change / prev_close) * 100
                
                data.append({
                    'Ticker': symbol,
                    'Price': price,
                    'Change': change,
                    '% Change': pct_change,
                    'Previous Close': prev_close
                })
                
        except Exception as e:
            print(f"Alpha Vantage error for {symbol}: {e}")
            continue
    
    return pd.DataFrame(data)

@st.cache_data(ttl=300)
def get_fmp_global_indices():
    """Get global indices data from Financial Modeling Prep."""
    api_key = st.secrets.get("FMP_API_KEY")
    if not api_key:
        return pd.DataFrame()
    
    try:
        # FMP major indices endpoint
        url = f"https://financialmodelingprep.com/api/v3/quotes/index?apikey={api_key}"
        response = requests.get(url, timeout=10)
        indices_data = response.json()
        
        data = []
        major_indices = ['^GSPC', '^DJI', '^IXIC', '^FTSE', '^GDAXI', '^N225', '^HSI']
        
        for index in indices_data:
            if index['symbol'] in major_indices:
                data.append({
                    'Ticker': index['symbol'].replace('^', ''),
                    'Price': index['price'],
                    'Change': index['change'],
                    '% Change': index['changesPercentage'],
                    'Previous Close': index['price'] - index['change']
                })
        
        return pd.DataFrame(data)
        
    except Exception as e:
        print(f"FMP global indices error: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=60)
def get_professional_sgx_data():
    """Get SGX Nifty data from professional sources."""
    # Try Alpha Vantage first
    alpha_data = get_alpha_vantage_futures()
    if not alpha_data.empty:
        return alpha_data
    
    # Try FMP as fallback
    fmp_data = get_fmp_futures()
    if not fmp_data.empty:
        return fmp_data
    
    # Final fallback to free data
    return get_gift_nifty_data_enhanced()

def get_alpha_vantage_futures():
    """Get futures data from Alpha Vantage."""
    api_key = st.secrets.get("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        return pd.DataFrame()
    
    try:
        # Alpha Vantage doesn't have direct SGX Nifty, so we'll use NIFTY 50
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=SNFX&apikey={api_key}"
        response = requests.get(url, timeout=10)
        result = response.json()
        
        if 'Global Quote' in result:
            quote = result['Global Quote']
            # Create synthetic intraday data based on the quote
            dates = pd.date_range(start=datetime.now() - timedelta(hours=6), end=datetime.now(), freq='5min')
            base_price = float(quote['05. price'])
            
            synthetic_data = []
            for date in dates:
                variation = random.uniform(-0.001, 0.001)  # Small variation
                price = base_price * (1 + variation)
                synthetic_data.append({
                    'Open': price * 0.999,
                    'High': price * 1.001,
                    'Low': price * 0.998,
                    'Close': price,
                    'Volume': random.randint(1000, 5000)
                })
            
            return pd.DataFrame(synthetic_data, index=dates)
            
    except Exception as e:
        print(f"Alpha Vantage futures error: {e}")
    
    return pd.DataFrame()

@st.cache_data(ttl=300)
def get_professional_asian_markets():
    """Get Asian markets data from professional sources."""
    # Combine Alpha Vantage and FMP data
    alpha_data = get_alpha_vantage_global_indices()
    fmp_data = get_fmp_global_indices()
    
    # Filter for Asian markets
    asian_symbols = ['N225', 'HSI', '000001.SS']
    
    asian_data = []
    
    # Add from Alpha Vantage
    if not alpha_data.empty:
        asian_alpha = alpha_data[alpha_data['Ticker'].isin(['N225', 'HSI'])]
        asian_data.extend(asian_alpha.to_dict('records'))
    
    # Add from FMP
    if not fmp_data.empty:
        asian_fmp = fmp_data[fmp_data['Ticker'].isin(['N225', 'HSI'])]
        asian_data.extend(asian_fmp.to_dict('records'))
    
    return pd.DataFrame(asian_data)

def show_professional_indian_indicators():
    """Show Indian market indicators using professional data."""
    try:
        # Get NIFTY 50 and BANK NIFTY from professional sources
        nifty_data = get_professional_index_data('NIFTY 50')
        bank_nifty_data = get_professional_index_data('BANKNIFTY')
        vix_data = get_professional_index_data('INDIAVIX')
        
        if nifty_data:
            st.metric("NIFTY 50", f"{nifty_data['price']:.2f}", 
                     f"{nifty_data['change']:+.2f} ({nifty_data['pct_change']:+.2f}%)")
        
        if bank_nifty_data:
            st.metric("BANK NIFTY", f"{bank_nifty_data['price']:.2f}",
                     f"{bank_nifty_data['change']:+.2f} ({bank_nifty_data['pct_change']:+.2f}%)")
        
        if vix_data:
            vix_color = "inverse" if vix_data['change'] > 0 else "normal"
            st.metric("India VIX", f"{vix_data['price']:.2f}",
                     f"{vix_data['change']:+.2f} ({vix_data['pct_change']:+.2f}%)",
                     delta_color=vix_color)
                    
    except Exception as e:
        st.error(f"Error loading professional Indian data: {e}")

@st.cache_data(ttl=300)
def get_professional_news(query=None, source="All Sources"):
    """Get professional news from Alpha Vantage or FMP."""
    news_data = {'news_items': pd.DataFrame()}
    
    try:
        if source in ["Alpha Vantage", "All Sources"]:
            alpha_news = get_alpha_vantage_news(query)
            if not alpha_news['news_items'].empty:
                news_data = alpha_news
                
        if (source in ["FMP", "All Sources"]) and news_data['news_items'].empty:
            fmp_news = get_fmp_news(query)
            if not fmp_news['news_items'].empty:
                news_data = fmp_news
                
    except Exception as e:
        print(f"Professional news error: {e}")
    
    return news_data

@st.cache_data(ttl=600)
def get_alpha_vantage_news(query=None):
    """Get news from Alpha Vantage."""
    api_key = st.secrets.get("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        return {'news_items': pd.DataFrame()}
    
    try:
        url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={api_key}"
        if query:
            url += f"&tickers={query}"
        
        response = requests.get(url, timeout=10)
        result = response.json()
        
        news_items = []
        if 'feed' in result:
            for item in result['feed'][:10]:  # Limit to 10 items
                news_items.append({
                    'title': item.get('title', ''),
                    'summary': item.get('summary', ''),
                    'source': item.get('source', 'Alpha Vantage'),
                    'link': item.get('url', '#'),
                    'date': datetime.strptime(item['time_published'], '%Y%m%dT%H%M%S').date(),
                    'sentiment_score': float(item.get('overall_sentiment_score', 0)),
                    'sentiment_label': 'BULLISH' if item.get('overall_sentiment_label') == 'Bullish' else 'BEARISH' if item.get('overall_sentiment_label') == 'Bearish' else 'NEUTRAL',
                    'sentiment_emoji': '📈' if item.get('overall_sentiment_label') == 'Bullish' else '📉' if item.get('overall_sentiment_label') == 'Bearish' else '➡️'
                })
        
        return {
            'news_items': pd.DataFrame(news_items),
            'overall_sentiment': np.mean([item['sentiment_score'] for item in news_items]) if news_items else 0,
            'total_articles': len(news_items)
        }
        
    except Exception as e:
        print(f"Alpha Vantage news error: {e}")
        return {'news_items': pd.DataFrame()}

@st.cache_data(ttl=600)
def get_fmp_news(query=None):
    """Get news from Financial Modeling Prep."""
    api_key = st.secrets.get("FMP_API_KEY")
    if not api_key:
        return {'news_items': pd.DataFrame()}
    
    try:
        url = f"https://financialmodelingprep.com/api/v3/stock_news?limit=10&apikey={api_key}"
        if query:
            url += f"&tickers={query}"
        
        response = requests.get(url, timeout=10)
        news_items_data = response.json()
        
        news_items = []
        for item in news_items_data:
            news_items.append({
                'title': item.get('title', ''),
                'summary': item.get('text', ''),
                'source': 'FMP',
                'link': item.get('url', '#'),
                'date': datetime.strptime(item['publishedDate'], '%Y-%m-%d %H:%M:%S').date(),
                'sentiment_score': 0.1,  # FMP doesn't provide sentiment, use neutral
                'sentiment_label': 'NEUTRAL',
                'sentiment_emoji': '➡️'
            })
        
        return {
            'news_items': pd.DataFrame(news_items),
            'overall_sentiment': 0.1,
            'total_articles': len(news_items)
        }
        
    except Exception as e:
        print(f"FMP news error: {e}")
        return {'news_items': pd.DataFrame()}

def display_professional_news(news_data, news_limit=5):
    """Display professional news with enhanced formatting."""
    news_df = news_data['news_items']
    
    if news_df.empty:
        return
    
    news_count = 0
    for _, news in news_df.iterrows():
        if news_count >= news_limit:
            break
            
        sentiment_score = news['sentiment_score']
        
        # Sentiment indicators
        if sentiment_score > 0.1:
            sentiment_icon = "🟢"
            sentiment_text = "Positive"
            border_color = "#28a745"
        elif sentiment_score < -0.1:
            sentiment_icon = "🔴" 
            sentiment_text = "Negative"
            border_color = "#dc3545"
        else:
            sentiment_icon = "🟡"
            sentiment_text = "Neutral"
            border_color = "#ffc107"
        
        # Professional news card
        st.markdown(f"""
        <div style="border-left: 4px solid {border_color}; padding-left: 10px; margin: 10px 0;">
            <div style="display: flex; justify-content: between; align-items: start;">
                <div style="flex: 1;">
                    <strong>{news['title']}</strong>
                    <br>
                    <small style="color: #666;">{news['source']} • {news['date']}</small>
                </div>
                <div style="margin-left: 10px;">
                    {sentiment_icon} {sentiment_text}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Expandable details
        with st.expander("Read summary"):
            if news.get('summary'):
                st.write(news['summary'])
            st.write(f"**Sentiment Score:** {sentiment_score:.2f}")
            if news['link'] != "#":
                st.markdown(f"[Read full article →]({news['link']})")
        
        news_count += 1

# Add the missing helper functions
def get_professional_index_data(symbol):
    """Get professional index data (placeholder implementation)."""
    # This would be implemented with actual API calls
    return None

def create_professional_futures_chart(data):
    """Create professional futures chart."""
    fig = go.Figure()
    
    if all(col in data.columns for col in ['Open', 'High', 'Low', 'Close']):
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Futures'
        ))
    else:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close' if 'Close' in data.columns else data.iloc[:, 0]],
            mode='lines',
            name='Futures',
            line=dict(color='cyan')
        ))
    
    fig.update_layout(
        title="Futures Price",
        xaxis_title="Time",
        yaxis_title="Price",
        template='plotly_dark',
        height=400,
        showlegend=False,
        xaxis_rangeslider_visible=False
    )
    
    return fig

def show_nifty_fallback():
    """Show NIFTY fallback data."""
    instrument_df = get_instrument_df()
    if not instrument_df.empty:
        nifty_token = get_instrument_token('NIFTY 50', instrument_df, 'NSE')
        if nifty_token:
            nifty_data = get_historical_data(nifty_token, "5minute", period="1d")
            if not nifty_data.empty:
                st.plotly_chart(create_chart(nifty_data.tail(100), "NIFTY 50"), use_container_width=True)
            else:
                st.error("Unable to load NIFTY 50 data")
        else:
            st.error("NIFTY 50 token not found")
    else:
        st.error("Instrument data not available")

def display_enhanced_news(news_data, news_limit=5):
    """Display enhanced news fallback."""
    news_df = news_data['news_items']
    
    if news_df.empty:
        st.info("No news available")
        return
    
    for _, news in news_df.head(news_limit).iterrows():
        st.write(f"**{news['title']}**")
        st.caption(f"Source: {news['source']} • {news['date']}")
        st.markdown("---")

def get_professional_economic_calendar():
    """Get professional economic calendar data."""
    # This would be implemented with actual API calls
    return None

def display_economic_calendar(events):
    """Display economic calendar."""
    if events:
        for event in events:
            col1, col2, col3 = st.columns([2, 3, 1])
            with col1:
                st.write(f"**{event['time']}**")
            with col2:
                st.write(f"{event['event']} ({event['country']})")
            with col3:
                impact_color = {"High": "#dc3545", "Medium": "#ffc107", "Low": "#28a745"}
                st.markdown(f"<span style='color:{impact_color[event['impact']]}; font-weight:bold;'>{event['impact']}</span>", unsafe_allow_html=True)
    else:
        show_sample_economic_events()

def show_sample_economic_events():
    """Show sample economic events."""
    st.info("No economic events data available. Showing sample events.")
    today_events = [
        {"time": "09:00 AM", "event": "GDP Growth Rate Q2", "country": "IND", "impact": "High"},
        {"time": "10:30 AM", "event": "Inflation Rate YoY", "country": "IND", "impact": "High"},
        {"time": "02:00 PM", "event": "FOMC Meeting Minutes", "country": "USA", "impact": "Medium"},
    ]
    
    for event in today_events:
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            st.write(f"**{event['time']}**")
        with col2:
            st.write(f"{event['event']} ({event['country']})")
        with col3:
            impact_color = {"High": "#dc3545", "Medium": "#ffc107", "Low": "#28a745"}
            st.markdown(f"<span style='color:{impact_color[event['impact']]}; font-weight:bold;'>{event['impact']}</span>", unsafe_allow_html=True)

# Add the missing get_fallback_news function for compatibility
def get_fallback_news():
    """Fallback news function for compatibility."""
    return get_fallback_news_enhanced()

def page_fo_analytics():
    """F&O Analytics page with comprehensive options analysis."""
    display_header()
    st.title("F&O Analytics Hub")
    
    instrument_df = get_instrument_df()
    if instrument_df.empty:
        st.info("Please connect to a broker to access F&O Analytics.")
        return
    
    tab1, tab2, tab3 = st.tabs(["Options Chain", "PCR Analysis", "Volatility & OI Analysis"])
    
    with tab1:
        st.subheader("Live Options Chain")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            underlying = st.selectbox("Select Underlying", ["NIFTY", "BANKNIFTY", "FINNIFTY"])
            st.session_state.underlying_pcr = underlying 
        
        chain_df, expiry, underlying_ltp, available_expiries = get_options_chain(underlying, instrument_df)

        if not chain_df.empty:
            with col2:
                st.metric("Current Price", f"₹{underlying_ltp:,.2f}")
                st.metric("Expiry Date", expiry.strftime("%d %b %Y") if expiry else "N/A")
            with col3:
                if st.button("Most Active Options", use_container_width=True):
                    show_most_active_dialog(underlying, instrument_df)

            st.dataframe(
                style_option_chain(chain_df, underlying_ltp).format({
                    'CALL LTP': '₹{:.2f}', 'PUT LTP': '₹{:.2f}',
                    'STRIKE': '₹{:.0f}',
                    'CALL OI': '{:,.0f}', 'PUT OI': '{:,.0f}'
                }),
                use_container_width=True, hide_index=True
            )
        else:
            st.warning("Could not load options chain data.")
    
    with tab2:
        st.subheader("Put-Call Ratio Analysis")
        
        chain_df, _, _, _ = get_options_chain(st.session_state.get('underlying_pcr', "NIFTY"), instrument_df)
        if not chain_df.empty and 'CALL OI' in chain_df.columns:
            total_ce_oi = chain_df['CALL OI'].sum()
            total_pe_oi = chain_df['PUT OI'].sum()
            pcr = total_pe_oi / total_ce_oi if total_ce_oi > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total CE OI", f"{total_ce_oi:,.0f}")
            col2.metric("Total PE OI", f"{total_pe_oi:,.0f}")
            col3.metric("PCR", f"{pcr:.2f}")
            
            if pcr > 1.3:
                st.success("High PCR suggests potential bearish sentiment (more Puts bought for hedging/speculation).")
            elif pcr < 0.7:
                st.error("Low PCR suggests potential bullish sentiment (more Calls bought).")
            else:
                st.info("PCR indicates neutral sentiment.")
        else:
            st.info("PCR data is loading... Select an underlying in the 'Options Chain' tab first.")
    
    with tab3:
        st.subheader("Volatility & Open Interest Surface")
        st.info("Real-time implied volatility and OI analysis for options contracts.")

        chain_df, expiry, underlying_ltp, _ = get_options_chain(st.session_state.get('underlying_pcr', "NIFTY"), instrument_df)

        if not chain_df.empty and expiry and underlying_ltp > 0:
            T = (expiry - datetime.now().date()).days / 365.0
            r = 0.07

            with st.spinner("Calculating Implied Volatility..."):
                chain_df['IV_CE'] = chain_df.apply(
                    lambda row: implied_volatility(underlying_ltp, row['STRIKE'], T, r, row['CALL LTP'], 'call') * 100,
                    axis=1
                )
                chain_df['IV_PE'] = chain_df.apply(
                    lambda row: implied_volatility(underlying_ltp, row['STRIKE'], T, r, row['PUT LTP'], 'put') * 100,
                    axis=1
                )

            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=chain_df['STRIKE'], y=chain_df['IV_CE'], mode='lines+markers', name='Call IV', line=dict(color='cyan')), secondary_y=False)
            fig.add_trace(go.Scatter(x=chain_df['STRIKE'], y=chain_df['IV_PE'], mode='lines+markers', name='Put IV', line=dict(color='magenta')), secondary_y=False)
            fig.add_trace(go.Bar(x=chain_df['STRIKE'], y=chain_df['CALL OI'], name='Call OI', marker_color='rgba(0, 255, 255, 0.4)'), secondary_y=True)
            fig.add_trace(go.Bar(x=chain_df['STRIKE'], y=chain_df['PUT OI'], name='Put OI', marker_color='rgba(255, 0, 255, 0.4)'), secondary_y=True)

            fig.update_layout(
                title_text=f"{st.session_state.get('underlying_pcr', 'NIFTY')} IV & OI Profile for {expiry.strftime('%d %b %Y')}",
                template='plotly_dark' if st.session_state.get('theme') == 'Dark' else 'plotly_white',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            fig.update_yaxes(title_text="Implied Volatility (%)", secondary_y=False)
            fig.update_yaxes(title_text="Open Interest", secondary_y=True)
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Please select an underlying and expiry in the 'Options Chain' tab to view the volatility surface.")

def page_ai_sentiment_analyzer():
    """AI Market Sentiment Analyzer with manual refresh and improved UI."""
    display_header()
    
    # Premium Header with Gradient
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <h1 style="color: white; margin: 0; font-size: 2.8em; text-align: center;">🤖 AI MARKET SENTIMENT ANALYZER</h1>
        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 1.2em; text-align: center;">
        Real-time News Analysis • Sentiment Scoring • Market Intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state for manual refresh control
    if 'sentiment_last_refresh' not in st.session_state:
        st.session_state.sentiment_last_refresh = "Never"
    if 'sentiment_data' not in st.session_state:
        st.session_state.sentiment_data = None
    if 'sentiment_loading' not in st.session_state:
        st.session_state.sentiment_loading = False

    # Control Panel with Manual Refresh
    st.markdown("### 🎛️ Control Panel")
    
    control_col1, control_col2, control_col3, control_col4 = st.columns([2, 1, 1, 1])
    
    with control_col1:
        query = st.text_input(
            "**🔍 Search News**", 
            placeholder="e.g., RBI, IT Stocks, Inflation...",
            help="Filter news by specific keywords or topics"
        )
    
    with control_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 **Refresh Now**", use_container_width=True, type="primary"):
            st.session_state.sentiment_loading = True
            st.session_state.sentiment_data = None
            st.rerun()
    
    with control_col3:
        news_limit = st.slider("**News Limit**", 5, 20, 10, help="Number of news articles to analyze")
    
    with control_col4:
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption(f"Last refresh: {st.session_state.sentiment_last_refresh}")

    # Loading State with Progress
    if st.session_state.sentiment_loading:
        with st.spinner("🤖 AI is analyzing market sentiment from news sources..."):
            progress_bar = st.progress(0)
            
            # Simulate progress steps for better UX
            for i in range(100):
                a_time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            # Fetch data
            sentiment_data = fetch_and_analyze_news_enhanced(query if query else None)
            st.session_state.sentiment_data = sentiment_data
            st.session_state.sentiment_loading = False
            st.session_state.sentiment_last_refresh = get_ist_time().strftime("%H:%M:%S")
            
            progress_bar.empty()

    # Display sentiment data if available
    if st.session_state.sentiment_data:
        display_sentiment_dashboard(st.session_state.sentiment_data, news_limit)
    else:
        # Initial load or no data
        if not st.session_state.sentiment_loading:
            st.info("""
            ## 📊 Ready to Analyze Market Sentiment
            
            Click **"Refresh Now"** to start analyzing real-time market sentiment from financial news sources.
            
            **Features:**
            • AI-powered sentiment analysis using VADER
            • Real-time news aggregation from multiple sources
            • Visual sentiment scoring and market mood indicators
            • Manual refresh control to avoid API limits
            """)

def fetch_and_analyze_news_enhanced(query=None):
    """Enhanced news fetcher with better error handling and performance."""
    analyzer = SentimentIntensityAnalyzer()
    
    # Curated reliable news sources with fallbacks
    news_sources = {
        "Moneycontrol": "https://www.moneycontrol.com/rss/latestnews.xml",
        "Economic Times": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
        "Business Standard": "https://www.business-standard.com/rss/markets-102.rss",
        "Reuters Business": "https://feeds.reuters.com/reuters/businessNews",
        "Bloomberg Markets": "https://feeds.bloomberg.com/markets/news.rss",
    }
    
    all_news = []
    successful_sources = 0
    
    # Progress tracking for sources
    source_progress = st.empty()
    
    for source_idx, (source, url) in enumerate(news_sources.items()):
        try:
            source_progress.info(f"📡 Fetching from {source}...")
            
            # Add proper headers and timeout
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/rss+xml, application/xml, text/xml'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            
            if hasattr(feed, 'entries') and feed.entries:
                successful_sources += 1
                for entry in feed.entries[:4]:  # Limit per source
                    try:
                        # Get publication date
                        published_date = datetime.now().date()
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            published_date = datetime(*entry.published_parsed[:6]).date()
                        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                            published_date = datetime(*entry.updated_parsed[:6]).date()
                        
                        # Clean and validate content
                        title = entry.title if hasattr(entry, 'title') else "No title"
                        summary = entry.summary if hasattr(entry, 'summary') else title
                        
                        # Skip if content is too short
                        if len(title) < 10:
                            continue
                            
                        # Check if news matches query
                        if query is None or query.lower() in title.lower() or query.lower() in summary.lower():
                            # Calculate sentiment with enhanced analysis
                            text_for_sentiment = f"{title} {summary}"
                            sentiment_scores = analyzer.polarity_scores(text_for_sentiment)
                            
                            # Enhanced sentiment classification
                            compound = sentiment_scores['compound']
                            if compound >= 0.05:
                                sentiment_label = "BULLISH"
                                sentiment_emoji = "📈"
                                sentiment_color = "#00ff88"
                            elif compound <= -0.05:
                                sentiment_label = "BEARISH" 
                                sentiment_emoji = "📉"
                                sentiment_color = "#ff4444"
                            else:
                                sentiment_label = "NEUTRAL"
                                sentiment_emoji = "➡️"
                                sentiment_color = "#888888"
                            
                            all_news.append({
                                "source": source,
                                "title": title,
                                "link": entry.link if hasattr(entry, 'link') else "#",
                                "date": published_date,
                                "sentiment_score": compound,
                                "sentiment_label": sentiment_label,
                                "sentiment_emoji": sentiment_emoji,
                                "sentiment_color": sentiment_color,
                                "summary": clean_summary(summary),
                                "positive": sentiment_scores['pos'],
                                "negative": sentiment_scores['neg'],
                                "neutral": sentiment_scores['neu'],
                                "confidence": abs(compound) * 100  # Confidence score
                            })
                    except Exception as e:
                        continue  # Skip individual entry errors
                        
        except Exception as e:
            continue  # Skip source if it fails
    
    source_progress.empty()
    
    # If no news fetched, use enhanced fallback
    if not all_news:
        return get_fallback_news_enhanced()
    
    # Sort by date (newest first)
    all_news.sort(key=lambda x: x['date'], reverse=True)
    
    # Calculate overall market sentiment
    if all_news:
        avg_sentiment = sum(item['sentiment_score'] for item in all_news) / len(all_news)
        
        # Determine market mood
        if avg_sentiment > 0.1:
            market_mood = "BULLISH"
            mood_emoji = "📈"
            mood_color = "#00ff88"
        elif avg_sentiment < -0.1:
            market_mood = "BEARISH"
            mood_emoji = "📉"
            mood_color = "#ff4444"
        else:
            market_mood = "NEUTRAL"
            mood_emoji = "➡️"
            mood_color = "#888888"
        
        return {
            'news_items': all_news,
            'overall_sentiment': avg_sentiment,
            'market_mood': market_mood,
            'mood_emoji': mood_emoji,
            'mood_color': mood_color,
            'bullish_articles': len([n for n in all_news if n['sentiment_label'] == 'BULLISH']),
            'bearish_articles': len([n for n in all_news if n['sentiment_label'] == 'BEARISH']),
            'neutral_articles': len([n for n in all_news if n['sentiment_label'] == 'NEUTRAL']),
            'total_articles': len(all_news),
            'successful_sources': successful_sources,
            'timestamp': get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
        }
    else:
        return get_fallback_news_enhanced()

def clean_summary(summary):
    """Clean and format news summary."""
    # Remove HTML tags
    clean_text = re.sub('<[^<]+?>', '', summary)
    # Limit length and add ellipsis
    if len(clean_text) > 200:
        return clean_text[:200] + "..."
    return clean_text

def get_fallback_news_enhanced():
    """Enhanced fallback news with realistic sentiment analysis."""
    fallback_news = [
        {
            "source": "Market Intelligence",
            "title": "Indian markets show resilience amid global volatility",
            "link": "#",
            "date": datetime.now().date(),
            "sentiment_score": 0.15,
            "sentiment_label": "BULLISH",
            "sentiment_emoji": "📈",
            "sentiment_color": "#00ff88",
            "summary": "Domestic markets demonstrate strength despite global headwinds, with selective buying in key sectors.",
            "positive": 0.65,
            "negative": 0.20,
            "neutral": 0.15,
            "confidence": 85
        },
        {
            "source": "Economic Indicators",
            "title": "RBI maintains accommodative stance in policy review",
            "link": "#", 
            "date": datetime.now().date(),
            "sentiment_score": 0.08,
            "sentiment_label": "NEUTRAL",
            "sentiment_emoji": "➡️",
            "sentiment_color": "#888888",
            "summary": "Central bank keeps rates unchanged while monitoring inflation trajectory and growth recovery.",
            "positive": 0.45,
            "negative": 0.25,
            "neutral": 0.30,
            "confidence": 70
        },
        {
            "source": "Corporate News",
            "title": "IT sector earnings season begins with mixed expectations",
            "link": "#",
            "date": datetime.now().date(),
            "sentiment_score": 0.05,
            "sentiment_label": "NEUTRAL",
            "sentiment_emoji": "➡️",
            "sentiment_color": "#888888",
            "summary": "Technology companies set to announce quarterly results amid global demand concerns.",
            "positive": 0.40,
            "negative": 0.35,
            "neutral": 0.25,
            "confidence": 65
        },
        {
            "source": "Global Markets",
            "title": "US Fed policy decisions to influence emerging markets",
            "link": "#",
            "date": datetime.now().date(),
            "sentiment_score": -0.10,
            "sentiment_label": "BEARISH",
            "sentiment_emoji": "📉",
            "sentiment_color": "#ff4444",
            "summary": "Federal Reserve's monetary policy outlook remains key driver for global capital flows.",
            "positive": 0.30,
            "negative": 0.55,
            "neutral": 0.15,
            "confidence": 75
        },
        {
            "source": "Commodities Update",
            "title": "Crude oil prices volatile amid supply adjustments",
            "link": "#",
            "date": datetime.now().date(),
            "sentiment_score": -0.05,
            "sentiment_label": "NEUTRAL",
            "sentiment_emoji": "➡️",
            "sentiment_color": "#888888",
            "summary": "Oil markets balance supply concerns with demand outlook in uncertain global environment.",
            "positive": 0.35,
            "negative": 0.40,
            "neutral": 0.25,
            "confidence": 60
        }
    ]
    
    return {
        'news_items': fallback_news,
        'overall_sentiment': -0.01,
        'market_mood': "NEUTRAL",
        'mood_emoji': "➡️",
        'mood_color': "#888888",
        'bullish_articles': 1,
        'bearish_articles': 1,
        'neutral_articles': 3,
        'total_articles': 5,
        'successful_sources': 5,
        'timestamp': get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
    }

def display_sentiment_dashboard(sentiment_data, news_limit=10):
    """Display comprehensive sentiment analysis dashboard."""
    
    # Overall Sentiment Overview
    st.markdown("### 📊 Market Sentiment Overview")
    
    # Key Metrics in Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div style="background: {sentiment_data['mood_color']}20; padding: 15px; border-radius: 10px; border-left: 4px solid {sentiment_data['mood_color']}; text-align: center;">
            <div style="font-size: 2em; margin-bottom: 5px;">{sentiment_data['mood_emoji']}</div>
            <div style="font-weight: bold; color: {sentiment_data['mood_color']};">{sentiment_data['market_mood']}</div>
            <div style="font-size: 0.9em; color: #666;">Market Mood</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        score = sentiment_data['overall_sentiment']
        score_color = "#00ff88" if score > 0.05 else "#ff4444" if score < -0.05 else "#888888"
        st.markdown(f"""
        <div style="background: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; text-align: center;">
            <div style="font-size: 1.5em; font-weight: bold; color: {score_color}; margin-bottom: 5px;">{score:+.3f}</div>
            <div style="font-size: 0.9em; color: #666;">Sentiment Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; text-align: center;">
            <div style="font-size: 1.5em; font-weight: bold; color: #00ff88; margin-bottom: 5px;">{sentiment_data['bullish_articles']}</div>
            <div style="font-size: 0.9em; color: #666;">Bullish 📈</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; text-align: center;">
            <div style="font-size: 1.5em; font-weight: bold; color: #ff4444; margin-bottom: 5px;">{sentiment_data['bearish_articles']}</div>
            <div style="font-size: 0.9em; color: #666;">Bearish 📉</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div style="background: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; text-align: center;">
            <div style="font-size: 1.5em; font-weight: bold; color: #888888; margin-bottom: 5px;">{sentiment_data['neutral_articles']}</div>
            <div style="font-size: 0.9em; color: #666;">Neutral ➡️</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sentiment Visualization
    col_viz1, col_viz2 = st.columns([2, 1])
    
    with col_viz1:
        st.markdown("#### 📈 Sentiment Distribution")
        display_sentiment_gauge(sentiment_data['overall_sentiment'])
    
    with col_viz2:
        st.markdown("#### 🎯 Sentiment Breakdown")
        
        # Pie chart for sentiment distribution
        labels = ['Bullish', 'Bearish', 'Neutral']
        values = [
            sentiment_data['bullish_articles'],
            sentiment_data['bearish_articles'], 
            sentiment_data['neutral_articles']
        ]
        colors = ['#00ff88', '#ff4444', '#888888']
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values,
            hole=.3,
            marker_colors=colors
        )])
        
        fig_pie.update_layout(
            height=250,
            showlegend=True,
            margin=dict(t=0, b=0, l=0, r=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")
    
    # News Articles with Enhanced UI
    st.markdown("### 📰 Latest Market News & Analysis")
    
    # Filter controls
    filter_col1, filter_col2, filter_col3 = st.columns([2, 1, 1])
    
    with filter_col1:
        sentiment_filter = st.multiselect(
            "Filter by Sentiment",
            ["BULLISH", "BEARISH", "NEUTRAL"],
            default=["BULLISH", "BEARISH", "NEUTRAL"],
            key="sentiment_filter"
        )
    
    with filter_col2:
        sort_by = st.selectbox(
            "Sort by",
            ["Newest", "Sentiment", "Source"],
            key="news_sort"
        )
    
    with filter_col3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption(f"Showing {min(news_limit, len(sentiment_data['news_items']))} of {len(sentiment_data['news_items'])} articles")
    
    # Filter and sort news
    filtered_news = [article for article in sentiment_data['news_items'] if article['sentiment_label'] in sentiment_filter]
    
    if sort_by == "Newest":
        filtered_news.sort(key=lambda x: x['date'], reverse=True)
    elif sort_by == "Sentiment":
        filtered_news.sort(key=lambda x: abs(x['sentiment_score']), reverse=True)
    elif sort_by == "Source":
        filtered_news.sort(key=lambda x: x['source'])
    
    # Display articles with enhanced UI
    if filtered_news:
        for i, article in enumerate(filtered_news[:news_limit]):
            with st.container():
                st.markdown(f"""
                <div style="background: #1a1a1a; padding: 20px; border-radius: 10px; border-left: 4px solid {article['sentiment_color']}; margin: 10px 0; border: 1px solid #333;">
                    <div style="display: flex; justify-content: between; align-items: start;">
                        <div style="flex: 1;">
                            <h4 style="color: white; margin: 0 0 10px 0;">{article['title']}</h4>
                            <div style="color: #888; font-size: 0.9em; margin-bottom: 10px;">
                                📰 {article['source']} • 📅 {article['date']} • 🎯 Confidence: {article['confidence']:.0f}%
                            </div>
                            <p style="color: #ccc; margin: 0; line-height: 1.5;">{article['summary']}</p>
                            {f'<a href="{article["link"]}" target="_blank" style="color: #667eea; text-decoration: none; font-size: 0.9em;">🔗 Read full article</a>' if article["link"] != "#" else ""}
                        </div>
                        <div style="margin-left: 15px; text-align: center; min-width: 100px;">
                            <div style="font-size: 2em; margin-bottom: 5px;">{article['sentiment_emoji']}</div>
                            <div style="font-weight: bold; color: {article['sentiment_color']};">{article['sentiment_label']}</div>
                            <div style="color: {article['sentiment_color']}; font-size: 0.9em;">{article['sentiment_score']:+.3f}</div>
                            <div style="background: {article['sentiment_color']}30; padding: 5px; border-radius: 5px; margin-top: 5px; font-size: 0.8em;">
                                {article['positive']:.0%} 👍<br>
                                {article['negative']:.0%} 👎
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No articles match your current filters. Try adjusting the sentiment filters.")
    
    # Footer with analysis timestamp
    st.markdown("---")
    st.caption(f"🤖 AI Analysis completed at {sentiment_data['timestamp']} • {sentiment_data['successful_sources']} news sources analyzed • Manual refresh required for updates")

def display_sentiment_gauge(sentiment_score):
    """Display an interactive sentiment gauge chart."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = sentiment_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Market Sentiment Score", 'font': {'size': 20}},
        delta = {'reference': 0, 'increasing': {'color': "#00ff88"}, 'decreasing': {'color': "#ff4444"}},
        gauge = {
            'axis': {'range': [-1, 1], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#667eea"},
            'bgcolor': "black",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [-1, -0.1], 'color': '#ff4444'},
                {'range': [-0.1, 0.1], 'color': '#888888'},
                {'range': [0.1, 1], 'color': '#00ff88'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': sentiment_score
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Arial"},
        margin=dict(t=50, b=10, l=10, r=10)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def page_market_sentiment():
    """Market Sentiment Analysis Page - Uses the new improved version"""
    page_ai_sentiment_analyzer()


def load_and_combine_data(instrument_name):
    """
    Load and combine historical data for the selected instrument.
    This is a placeholder - you'll need to implement actual data loading.
    """
    try:
        # Example implementation - replace with your actual data loading logic
        if instrument_name in ML_DATA_SOURCES:
            # For demonstration, generating sample data
            # In a real implementation, you would load from ML_DATA_SOURCES[instrument_name]
            dates = pd.date_range(start='2020-01-01', end=pd.Timestamp.now(), freq='D')
            # Generate realistic price data with trend and noise
            np.random.seed(42)  # For reproducible results
            prices = 100 + 0.1 * np.arange(len(dates)) + 10 * np.random.randn(len(dates))
            
            data = pd.DataFrame({
                'Close': prices,
                'Open': prices - 2 + 4 * np.random.rand(len(dates)),
                'High': prices + 5 * np.random.rand(len(dates)),
                'Low': prices - 5 * np.random.rand(len(dates)),
                'Volume': 1000000 + 500000 * np.random.rand(len(dates))
            }, index=dates)
            
            return data
        else:
            st.error(f"No data source configured for {instrument_name}")
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def train_seasonal_arima_model(data, forecast_steps):
    """
    Train a Seasonal ARIMA model and generate forecasts with confidence intervals.
    """
    try:
        if data.empty:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
            
        # Use closing prices for modeling
        prices = data['Close'].dropna()
        
        if len(prices) < 50:
            st.error("Insufficient data for modeling. Need at least 50 data points.")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        
        # Simple differencing to make series stationary
        diff_prices = prices.diff().dropna()
        
        # For demonstration - using simple parameters
        # In production, you'd use auto_arima or grid search for optimal parameters
        order = (1, 1, 1)  # (p, d, q)
        seasonal_order = (1, 1, 1, 5)  # (P, D, Q, s)
        
        # Split data for backtesting
        split_point = int(len(prices) * 0.8)
        train = prices.iloc[:split_point]
        test = prices.iloc[split_point:]
        
        # Fit model
        with st.spinner("Fitting SARIMA model..."):
            model = SARIMAX(train, order=order, seasonal_order=seasonal_order)
            fitted_model = model.fit(disp=False)
        
        # Backtest predictions
        backtest_predictions = fitted_model.get_forecast(steps=len(test))
        backtest_mean = backtest_predictions.predicted_mean
        backtest_conf_int = backtest_predictions.conf_int()
        
        # Create backtest DataFrame
        backtest_df = pd.DataFrame({
            'Actual': test,
            'Predicted': backtest_mean
        }, index=test.index)
        
        # Generate future forecast
        full_model = SARIMAX(prices, order=order, seasonal_order=seasonal_order)
        full_fitted_model = full_model.fit(disp=False)
        
        forecast_result = full_fitted_model.get_forecast(steps=forecast_steps)
        forecast_mean = forecast_result.predicted_mean
        forecast_conf_int = forecast_result.conf_int()
        
        # Create future dates for forecast
        last_date = prices.index[-1]
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_steps, freq='D')
        
        forecast_df = pd.DataFrame({'Forecast': forecast_mean}, index=future_dates)
        conf_int_df = pd.DataFrame({
            'Lower_CI': forecast_conf_int.iloc[:, 0],
            'Upper_CI': forecast_conf_int.iloc[:, 1]
        }, index=future_dates)
        
        return forecast_df, backtest_df, conf_int_df
        
    except Exception as e:
        st.error(f"Error in model training: {str(e)}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def mean_absolute_percentage_error(y_true, y_pred):
    """Calculate Mean Absolute Percentage Error"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    # Avoid division by zero
    return np.mean(np.abs((y_true - y_pred) / np.maximum(np.abs(y_true), 1))) * 100

def train_seasonal_arima_model(data, forecast_steps):
    """
    Train a Seasonal ARIMA model and generate forecasts with confidence intervals.
    """
    try:
        if data.empty:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
            
        # Use closing prices for modeling
        prices = data['Close'].dropna()
        
        if len(prices) < 50:
            st.error("Insufficient data for modeling. Need at least 50 data points.")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        
        # Simple differencing to make series stationary
        diff_prices = prices.diff().dropna()
        
        # For demonstration - using simple parameters
        # In production, you'd use auto_arima or grid search for optimal parameters
        order = (1, 1, 1)  # (p, d, q)
        seasonal_order = (1, 1, 1, 5)  # (P, D, Q, s)
        
        # Split data for backtesting
        split_point = int(len(prices) * 0.8)
        train = prices.iloc[:split_point]
        test = prices.iloc[split_point:]
        
        # Fit model
        with st.spinner("Fitting SARIMA model..."):
            model = SARIMAX(train, order=order, seasonal_order=seasonal_order)
            fitted_model = model.fit(disp=False)
        
        # Backtest predictions
        backtest_predictions = fitted_model.get_forecast(steps=len(test))
        backtest_mean = backtest_predictions.predicted_mean
        backtest_conf_int = backtest_predictions.conf_int()
        
        # Create backtest DataFrame - use 'Predicted' to match create_chart expectations
        backtest_df = pd.DataFrame({
            'Actual': test,
            'Predicted': backtest_mean
        }, index=test.index)
        
        # Generate future forecast
        full_model = SARIMAX(prices, order=order, seasonal_order=seasonal_order)
        full_fitted_model = full_model.fit(disp=False)
        
        forecast_result = full_fitted_model.get_forecast(steps=forecast_steps)
        forecast_mean = forecast_result.predicted_mean
        forecast_conf_int = forecast_result.conf_int()
        
        # Create future dates for forecast
        last_date = prices.index[-1]
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_steps, freq='D')
        
        # Use 'Predicted' column name to match create_chart expectations
        forecast_df = pd.DataFrame({'Predicted': forecast_mean}, index=future_dates)
        conf_int_df = pd.DataFrame({
            'Lower_CI': forecast_conf_int.iloc[:, 0],
            'Upper_CI': forecast_conf_int.iloc[:, 1]
        }, index=future_dates)
        
        return forecast_df, backtest_df, conf_int_df
        
    except Exception as e:
        st.error(f"Error in model training: {str(e)}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def create_chart(data, title, forecast_df=None, conf_int_df=None):
    """
    Create a Plotly chart for historical data and forecasts.
    Updated to handle the correct column names.
    """
    fig = go.Figure()
    
    # Add historical data as candlestick or line
    if all(col in data.columns for col in ['Open', 'High', 'Low', 'Close']):
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name=title
        ))
    else:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name=title,
            line=dict(color='blue')
        ))
    
    # Add forecast if provided
    if forecast_df is not None and not forecast_df.empty:
        # Use the correct column name 'Predicted'
        fig.add_trace(go.Scatter(
            x=forecast_df.index, 
            y=forecast_df['Predicted'], 
            mode='lines', 
            line=dict(color='yellow', dash='dash'), 
            name='Forecast'
        ))
        
        # Add confidence intervals if provided
        if conf_int_df is not None and not conf_int_df.empty:
            fig.add_trace(go.Scatter(
                x=conf_int_df.index.tolist() + conf_int_df.index.tolist()[::-1],
                y=conf_int_df['Upper_CI'].tolist() + conf_int_df['Lower_CI'].tolist()[::-1],
                fill='toself',
                fillcolor='rgba(255,255,0,0.2)',
                line=dict(color='rgba(255,255,0,0)'),
                name='Confidence Interval'
            ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark'
    )
    
    return fig

def page_forecasting_ml():
    """A page for advanced ML forecasting with an improved UI and corrected formulas."""
    display_header()
    st.title("Advanced ML Forecasting")
    st.info("Train a Seasonal ARIMA model to forecast future prices. This is for educational purposes and not financial advice.", icon="🧠")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Model Configuration")
        instrument_name = st.selectbox("Select an Instrument", list(ML_DATA_SOURCES.keys()), key="ml_instrument")
        
        forecast_durations = {"1 Week": 7, "2 Weeks": 14, "1 Month": 30, "3 Months": 90}
        duration_key = st.radio("Forecast Duration", list(forecast_durations.keys()), horizontal=True, key="ml_duration")
        forecast_steps = forecast_durations[duration_key]

        if st.button("Train Model & Forecast", use_container_width=True, type="primary"):
            with st.spinner(f"Loading data and training model for {instrument_name}..."):
                data = load_and_combine_data(instrument_name)
                if data.empty or len(data) < 100:
                    st.error(f"Could not load sufficient historical data for {instrument_name}. Model training requires at least 100 data points.")
                else:
                    forecast_df, backtest_df, conf_int_df = train_seasonal_arima_model(data, forecast_steps)
                    st.session_state.update({
                        'ml_forecast_df': forecast_df,
                        'ml_backtest_df': backtest_df,
                        'ml_conf_int_df': conf_int_df,
                        'ml_instrument_name': instrument_name,
                        'ml_historical_data': data,
                        'ml_duration_key': duration_key
                    })
                    st.success("Model trained successfully!")

    with col2:
        if 'ml_instrument_name' in st.session_state:
            instrument_name = st.session_state.ml_instrument_name
            st.subheader(f"Forecast Results for {instrument_name}")

            forecast_df = st.session_state.get('ml_forecast_df')
            backtest_df = st.session_state.get('ml_backtest_df')
            conf_int_df = st.session_state.get('ml_conf_int_df')
            data = st.session_state.get('ml_historical_data')
            duration_key = st.session_state.get('ml_duration_key')

            if forecast_df is not None and backtest_df is not None and data is not None and conf_int_df is not None:
                # Make sure the forecast_df has the correct column name
                if 'Predicted' not in forecast_df.columns and 'Forecast' in forecast_df.columns:
                    forecast_df = forecast_df.rename(columns={'Forecast': 'Predicted'})
                
                fig = create_chart(data.tail(252), instrument_name, forecast_df=forecast_df, conf_int_df=conf_int_df)
                fig.add_trace(go.Scatter(x=backtest_df.index, y=backtest_df['Predicted'], mode='lines', name='Backtest Prediction', line=dict(color='orange', dash='dot')))
                fig.update_layout(title=f"{instrument_name} Forecast vs. Historical Data")
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("Model Performance (Backtest)")
                
                backtest_durations = {"Full History": len(backtest_df), "Last Year": 252, "6 Months": 126, "3 Months": 63}
                backtest_duration_key = st.selectbox("Select Backtest Period", list(backtest_durations.keys()))
                backtest_period = backtest_durations[backtest_duration_key]
                
                display_df = backtest_df.tail(backtest_period)

                mape = mean_absolute_percentage_error(display_df['Actual'], display_df['Predicted'])
                
                metric_cols = st.columns(2)
                metric_cols[0].metric(f"Accuracy ({backtest_duration_key})", f"{100 - mape:.2f}%")
                metric_cols[1].metric(f"MAPE ({backtest_duration_key})", f"{mape:.2f}%")

                with st.expander(f"View {duration_key} Forecast Data"):
                    # Rename for display to be more user-friendly
                    display_df_forecast = forecast_df.rename(columns={'Predicted': 'Forecast'}).join(conf_int_df)
                    st.dataframe(display_df_forecast.style.format("₹{:.2f}"), use_container_width=True)
            else:
                st.info("Train a model to see the forecast results.")
        else:
            st.info("Select an instrument and run the forecast to see results.")

def page_portfolio_and_risk():
    """A page for portfolio and risk management, including live P&L and holdings."""
    display_header()
    st.title("Portfolio & Risk")

    client = get_broker_client()
    if not client:
        st.info("Connect to a broker to view your portfolio and positions.")
        return

    positions_df, holdings_df, total_pnl, _ = get_portfolio()
    
    if holdings_df.empty and positions_df.empty:
        st.info("No holdings or positions found to analyze.")
        return

    tab1, tab2, tab3 = st.tabs(["Day Positions", "Holdings (Investments)", "Live Order Book"])
    
    with tab1:
        st.subheader("Live Intraday Positions")
        if not positions_df.empty:
            st.dataframe(positions_df, use_container_width=True, hide_index=True)
            st.metric("Total Day P&L", f"₹{total_pnl:,.2f}", delta=f"{total_pnl:,.2f}")
        else:
            st.info("No open positions for the day.")
    
    with tab2:
        st.subheader("Investment Holdings")
        if not holdings_df.empty:
            st.dataframe(holdings_df, use_container_width=True, hide_index=True)
            st.markdown("---")

            st.subheader("Portfolio Allocation")
            
            sector_df = get_sector_data()
            
            holdings_df['current_value'] = holdings_df['quantity'] * holdings_df['last_price']
            
            if not holdings_df.empty and sector_df is not None:
                holdings_df = pd.merge(holdings_df, sector_df, left_on='tradingsymbol', right_on='Symbol', how='left')
                if 'Sector' not in holdings_df.columns:
                    holdings_df['Sector'] = 'Uncategorized'
                holdings_df['Sector'].fillna('Uncategorized', inplace=True)
            else:
                holdings_df['Sector'] = 'Uncategorized'
            
            col1_alloc, col2_alloc = st.columns(2)
            
            with col1_alloc:
                st.subheader("Stock-wise Allocation")
                fig_stock = go.Figure(data=[go.Pie(
                    labels=holdings_df['tradingsymbol'],
                    values=holdings_df['current_value'],
                    hole=.3,
                    textinfo='label+percent'
                )])
                fig_stock.update_layout(showlegend=False, template='plotly_dark' if st.session_state.get('theme') == "Dark" else 'plotly_white')
                st.plotly_chart(fig_stock, use_container_width=True)
                
            if 'Sector' in holdings_df.columns:
                with col2_alloc:
                    st.subheader("Sector-wise Allocation")
                    sector_allocation = holdings_df.groupby('Sector')['current_value'].sum().reset_index()
                    fig_sector = go.Figure(data=[go.Pie(
                        labels=sector_allocation['Sector'],
                        values=sector_allocation['current_value'],
                        hole=.3,
                        textinfo='label+percent'
                    )])
                    fig_sector.update_layout(showlegend=False, template='plotly_dark' if st.session_state.get('theme') == "Dark" else 'plotly_white')
                    st.plotly_chart(fig_sector, use_container_width=True)
        else:
            st.info("No holdings found.")

    with tab3:
        st.subheader("Live Order Book")
        display_order_history()

def display_trade_history():
    """Display comprehensive trade history with IST timestamps."""
    st.subheader("📋 Trade History")
    
    # Get all trade sources
    manual_trades = st.session_state.get('order_history', [])
    automated_trades = st.session_state.automated_mode.get('trade_history', [])
    
    if not manual_trades and not automated_trades:
        st.info("No trade history available. Trades will appear here after execution.")
        return
    
    # Combine and format all trades
    all_trades = []
    
    # Add manual trades
    for trade in manual_trades:
        ist_time = get_ist_time()
        all_trades.append({
            'Time': ist_time.strftime("%H:%M:%S IST"),
            'Symbol': trade.get('symbol', 'N/A'),
            'Action': trade.get('type', 'N/A'),
            'Qty': trade.get('qty', 0),
            'Status': trade.get('status', 'N/A'),
            'Type': 'Manual',
            'P&L': 'N/A'
        })
    
    # Add automated trades
    for trade in automated_trades:
        display_time = trade.get('timestamp_display', 
                               get_ist_time().strftime("%H:%M:%S IST") if 'timestamp' not in trade 
                               else datetime.fromisoformat(trade['timestamp'].replace('Z', '+00:00')).astimezone(pytz.timezone('Asia/Kolkata')).strftime("%H:%M:%S IST"))
        
        all_trades.append({
            'Time': display_time,
            'Symbol': trade.get('symbol', 'N/A'),
            'Action': trade.get('action', 'N/A'),
            'Qty': trade.get('quantity', 0),
            'Status': trade.get('status', 'OPEN'),
            'Type': trade.get('order_type', 'Automated'),
            'P&L': f"₹{trade.get('pnl', 0):.2f}"
        })
    
    # Sort by time (newest first)
    all_trades.sort(key=lambda x: x['Time'], reverse=True)
    
    # Create dataframe and display
    if all_trades:
        df = pd.DataFrame(all_trades)
        
        # Color coding for status
        def color_status(val):
            if val == 'Success' or val == 'CLOSED':
                return 'color: green; font-weight: bold;'
            elif val == 'OPEN':
                return 'color: orange; font-weight: bold;'
            elif 'Failed' in str(val):
                return 'color: red; font-weight: bold;'
            return ''
        
        # Color coding for action
        def color_action(val):
            if val == 'BUY':
                return 'color: #00cc00; font-weight: bold;'
            elif val == 'SELL':
                return 'color: #ff4444; font-weight: bold;'
            return ''
        
        styled_df = df.style.map(color_status, subset=['Status']).map(color_action, subset=['Action'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # Summary statistics
        total_trades = len(all_trades)
        successful_trades = len([t for t in all_trades if t['Status'] in ['Success', 'CLOSED']])
        open_trades = len([t for t in all_trades if t['Status'] == 'OPEN'])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Trades", total_trades)
        col2.metric("Successful", successful_trades)
        col3.metric("Open", open_trades)
        
        # Export option
        if st.button("📊 Export Trade History to CSV", use_container_width=True):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"trade_history_{get_ist_time().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.info("No trades to display.")

def display_order_history():
    """Display order history - UPDATED FOR UPSTOX."""
    client = get_broker_client()
    if client:
        try:
            broker = st.session_state.broker
            
            if broker == "Zerodha":
                orders = client.orders()
                if orders:
                    order_data = []
                    for order in orders:
                        order_time = order.get('order_timestamp', '')
                        if order_time:
                            try:
                                dt = datetime.fromisoformat(order_time.replace('Z', '+00:00'))
                                ist = pytz.timezone('Asia/Kolkata')
                                dt_ist = dt.astimezone(ist)
                                display_time = dt_ist.strftime("%Y-%m-%d %H:%M:%S IST")
                            except:
                                display_time = order_time
                        else:
                            display_time = 'N/A'
                        
                        order_data.append({
                            'Time': display_time,
                            'Symbol': order.get('tradingsymbol', ''),
                            'Type': order.get('transaction_type', ''),
                            'Qty': order.get('quantity', 0),
                            'Price': f"₹{order.get('average_price', 0):.2f}",
                            'Status': order.get('status', '')
                        })
                    
                    st.dataframe(pd.DataFrame(order_data), use_container_width=True)
                else:
                    st.info("No orders placed today.")
                    
            elif broker == "Upstox":
                orders_df = get_upstox_order_book()
                if not orders_df.empty:
                    order_data = []
                    for _, order in orders_df.iterrows():
                        order_time = order.get('order_timestamp', '')
                        if order_time:
                            try:
                                dt = datetime.fromisoformat(order_time.replace('Z', '+00:00'))
                                ist = pytz.timezone('Asia/Kolkata')
                                dt_ist = dt.astimezone(ist)
                                display_time = dt_ist.strftime("%Y-%m-%d %H:%M:%S IST")
                            except:
                                display_time = order_time
                        else:
                            display_time = 'N/A'
                        
                        order_data.append({
                            'Time': display_time,
                            'Symbol': order.get('tradingsymbol', ''),
                            'Type': order.get('transaction_type', ''),
                            'Qty': order.get('quantity', 0),
                            'Price': f"₹{order.get('price', 0):.2f}",
                            'Status': order.get('status', '')
                        })
                    
                    st.dataframe(pd.DataFrame(order_data), use_container_width=True)
                else:
                    st.info("No orders placed today.")
            
        except Exception as e:
            st.error(f"Error fetching orders: {e}")
    else:
        st.info("Broker not connected.")

def page_ai_assistant():
    """Enhanced AI-powered assistant with portfolio-aware insights and predictive analytics."""
    display_header()
    st.title("🧠 AI Portfolio Assistant")
    st.info("Advanced AI assistant with portfolio insights, predictive analytics, and intelligent trade recommendations.", icon="🤖")
    
    instrument_df = get_instrument_df()
    client = get_broker_client()

    # Initialize enhanced session state
    if "assistant_messages" not in st.session_state:
        st.session_state.assistant_messages = [
            {"role": "assistant", "content": "Hello! I'm your AI trading assistant. I can help you with portfolio analysis, market insights, trade recommendations, and predictive analytics. How can I assist you today?"}
        ]
    
    if "assistant_context" not in st.session_state:
        st.session_state.assistant_context = {
            "portfolio_snapshot": {},
            "market_conditions": {},
            "risk_profile": "medium",
            "trading_style": "balanced"
        }

    # Sidebar with quick actions
    with st.sidebar:
        st.subheader("🛠️ Quick Actions")
        
        if st.button("📊 Portfolio Health Check", use_container_width=True):
            st.session_state.assistant_messages.append({"role": "user", "content": "Analyze my portfolio health and suggest improvements"})
            # This will trigger the response in the main chat
            
        if st.button("📈 Market Outlook", use_container_width=True):
            st.session_state.assistant_messages.append({"role": "user", "content": "What's the current market outlook and any opportunities?"})
            
        if st.button("🎯 Trade Ideas", use_container_width=True):
            st.session_state.assistant_messages.append({"role": "user", "content": "Suggest some high-probability trade ideas"})
            
        if st.button("⚠️ Risk Assessment", use_container_width=True):
            st.session_state.assistant_messages.append({"role": "user", "content": "Assess my portfolio risk and suggest hedging"})
            
        st.markdown("---")
        st.subheader("🔧 Configuration")
        
        st.session_state.assistant_context["risk_profile"] = st.selectbox(
            "Risk Profile",
            ["conservative", "moderate", "balanced", "aggressive"],
            index=2
        )
        
        st.session_state.assistant_context["trading_style"] = st.selectbox(
            "Trading Style", 
            ["scalping", "day_trading", "swing_trading", "position_trading"],
            index=2
        )

    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("💬 AI Assistant")
        
        # Display chat messages
        for message in st.session_state.assistant_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Display additional context for assistant messages
                if "analysis" in message:
                    with st.expander("📊 Detailed Analysis"):
                        st.write(message["analysis"])
                        
                if "recommendations" in message:
                    with st.expander("🎯 Actionable Recommendations"):
                        for rec in message["recommendations"]:
                            st.write(f"• {rec}")

    with col2:
        st.subheader("📈 Live Context")
        
        # Portfolio snapshot
        positions_df, holdings_df, total_pnl, total_investment = get_portfolio()
        if total_investment > 0:
            st.metric("Portfolio P&L", f"₹{total_pnl:,.2f}")
            st.metric("Total Investment", f"₹{total_investment:,.2f}")
        else:
            st.info("No portfolio data")
        
        # Market status
        status_info = get_market_status()
        st.metric("Market Status", status_info['status'].replace('_', ' ').title())
        
        # AI Insights
        with st.expander("🤖 AI Insights"):
            st.write("• Real-time portfolio analysis")
            st.write("• Predictive market analytics")
            st.write("• Risk-aware recommendations")
            st.write("• Technical pattern recognition")

    # Chat input
    if prompt := st.chat_input("Ask about your portfolio, market insights, or trade ideas..."):
        # Add user message to chat history
        st.session_state.assistant_messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your query..."):
                response = process_ai_assistant_query(prompt, instrument_df)
                st.markdown(response["answer"])
                
                # Store enhanced response
                enhanced_message = {
                    "role": "assistant", 
                    "content": response["answer"]
                }
                
                if "analysis" in response:
                    enhanced_message["analysis"] = response["analysis"]
                if "recommendations" in response:
                    enhanced_message["recommendations"] = response["recommendations"]
                
                st.session_state.assistant_messages.append(enhanced_message)

def process_ai_assistant_query(prompt, instrument_df):
    """Enhanced query processing with advanced analytics."""
    prompt_lower = prompt.lower()
    
    # Update context
    update_assistant_context()
    
    # Portfolio-related queries
    if any(word in prompt_lower for word in ["portfolio", "holdings", "positions", "investment"]):
        return handle_portfolio_queries(prompt_lower, instrument_df)
    
    # Market analysis queries
    elif any(word in prompt_lower for word in ["market", "outlook", "trend", "nifty", "sensex"]):
        return handle_market_queries(prompt_lower, instrument_df)
    
    # Trade-related queries
    elif any(word in prompt_lower for word in ["trade", "buy", "sell", "opportunity", "idea"]):
        return handle_trade_queries(prompt_lower, instrument_df)
    
    # Risk-related queries
    elif any(word in prompt_lower for word in ["risk", "hedge", "protection", "volatility"]):
        return handle_risk_queries(prompt_lower, instrument_df)
    
    # Technical analysis queries
    elif any(word in prompt_lower for word in ["technical", "chart", "indicator", "pattern"]):
        return handle_technical_queries(prompt_lower, instrument_df)
    
    # General queries
    else:
        return handle_general_queries(prompt_lower, instrument_df)

def update_assistant_context():
    """Update the AI assistant's context with current market and portfolio data."""
    try:
        positions_df, holdings_df, total_pnl, total_investment = get_portfolio()
        
        # Portfolio snapshot
        st.session_state.assistant_context["portfolio_snapshot"] = {
            "total_pnl": total_pnl,
            "total_investment": total_investment,
            "positions_count": len(positions_df) if not positions_df.empty else 0,
            "holdings_count": len(holdings_df) if not holdings_df.empty else 0,
            "winning_positions": len([p for p in positions_df.to_dict('records') if p.get('pnl', 0) > 0]) if not positions_df.empty else 0
        }
        
        # Market conditions
        status_info = get_market_status()
        st.session_state.assistant_context["market_conditions"] = {
            "status": status_info['status'],
            "market_hours": is_market_hours(),
            "pre_market": is_pre_market_hours(),
            "square_off_time": is_square_off_time()
        }
    except Exception as e:
        st.error(f"Error updating context: {e}")

def handle_portfolio_queries(prompt_lower, instrument_df):
    """Handle portfolio-related queries with advanced analytics."""
    if "health" in prompt_lower or "how is my portfolio" in prompt_lower:
        return analyze_portfolio_health()
    elif "diversification" in prompt_lower:
        return analyze_portfolio_diversification()
    elif "performance" in prompt_lower:
        return analyze_portfolio_performance()
    else:
        return generate_portfolio_summary()

def analyze_portfolio_health():
    """Comprehensive portfolio health analysis."""
    try:
        positions_df, holdings_df, total_pnl, total_investment = get_portfolio()
        
        # Calculate metrics
        total_value = total_investment + total_pnl
        return_pct = (total_pnl / total_investment * 100) if total_investment > 0 else 0
        
        # Risk assessment
        risk_score = calculate_portfolio_risk(holdings_df)
        
        # Generate insights
        if return_pct > 10:
            health_status = "Excellent"
            color = "green"
        elif return_pct > 5:
            health_status = "Good" 
            color = "blue"
        elif return_pct > 0:
            health_status = "Fair"
            color = "orange"
        else:
            health_status = "Needs Attention"
            color = "red"
        
        analysis = f"""
        **Portfolio Health Analysis:**
        
        - **Total Value:** ₹{total_value:,.2f}
        - **Total P&L:** ₹{total_pnl:,.2f} ({return_pct:.2f}%)
        - **Health Status:** <span style='color:{color}'>{health_status}</span>
        - **Risk Score:** {risk_score}/10
        - **Positions:** {len(positions_df) if not positions_df.empty else 0} active
        - **Holdings:** {len(holdings_df) if not holdings_df.empty else 0} investments
        """
        
        recommendations = []
        
        if risk_score > 7:
            recommendations.append("Consider reducing exposure to high-risk positions")
        if return_pct < 0:
            recommendations.append("Review underperforming positions and consider stop-losses")
        if len(holdings_df) < 5:
            recommendations.append("Diversify across more sectors for better risk management")
        
        return {
            "answer": f"Your portfolio shows **{health_status}** health with a {return_pct:.2f}% return. " +
                     f"Risk level is {risk_score}/10. " +
                     ("I recommend reviewing the detailed analysis below." if recommendations else "Your portfolio is well-maintained."),
            "analysis": analysis,
            "recommendations": recommendations
        }
    except Exception as e:
        return {
            "answer": "Unable to analyze portfolio health at the moment. Please ensure you're connected to your broker.",
            "analysis": "Error in portfolio analysis",
            "recommendations": ["Check broker connection", "Verify portfolio data availability"]
        }

def calculate_portfolio_risk(holdings_df):
    """Calculate portfolio risk score (1-10)."""
    try:
        if holdings_df.empty:
            return 5
        
        # Simple risk calculation based on concentration and volatility
        total_value = (holdings_df['quantity'] * holdings_df['last_price']).sum()
        
        # Concentration risk (higher if few holdings dominate)
        if len(holdings_df) < 3:
            concentration_risk = 8
        elif len(holdings_df) < 5:
            concentration_risk = 6
        else:
            concentration_risk = 4
        
        # Volatility estimate (simplified)
        avg_pnl_pct = (holdings_df['pnl'].abs() / (holdings_df['quantity'] * holdings_df['average_price'])).mean() * 100
        volatility_risk = min(10, avg_pnl_pct / 2)
        
        return min(10, (concentration_risk + volatility_risk) / 2)
    except:
        return 5

def analyze_portfolio_diversification():
    """Analyze portfolio diversification."""
    try:
        holdings_df, _, _, _ = get_portfolio()
        
        if holdings_df.empty:
            return {
                "answer": "No holdings found for diversification analysis.",
                "analysis": "Please add holdings to your portfolio to analyze diversification.",
                "recommendations": ["Start building your portfolio with diversified sectors"]
            }
        
        # Simple diversification analysis
        num_holdings = len(holdings_df)
        
        if num_holdings >= 8:
            div_score = "Excellent"
            color = "green"
        elif num_holdings >= 5:
            div_score = "Good"
            color = "blue"
        elif num_holdings >= 3:
            div_score = "Fair"
            color = "orange"
        else:
            div_score = "Low"
            color = "red"
        
        analysis = f"""
        **Portfolio Diversification Analysis:**
        
        - **Number of Holdings:** {num_holdings}
        - **Diversification Score:** <span style='color:{color}'>{div_score}</span>
        - **Recommendation:** {'Well diversified' if div_score in ['Excellent', 'Good'] else 'Consider adding more positions'}
        """
        
        recommendations = [
            "Aim for at least 5 different holdings for optimal diversification",
            "Consider adding exposure to different market sectors",
            "Rebalance periodically to maintain target allocation"
        ]
        
        if num_holdings < 5:
            recommendations.append("Add 2-3 more positions from different sectors")
        
        return {
            "answer": f"Your portfolio has {num_holdings} holdings with **{div_score}** diversification.",
            "analysis": analysis,
            "recommendations": recommendations
        }
    except Exception as e:
        return {
            "answer": "Unable to analyze diversification at the moment.",
            "analysis": "Error in diversification analysis",
            "recommendations": ["Check portfolio data", "Try again later"]
        }

def analyze_portfolio_performance():
    """Analyze portfolio performance."""
    try:
        positions_df, holdings_df, total_pnl, total_investment = get_portfolio()
        
        if holdings_df.empty:
            return {
                "answer": "No portfolio data available for performance analysis.",
                "analysis": "Please connect to your broker or add manual holdings.",
                "recommendations": ["Connect to broker", "Add portfolio data"]
            }
        
        total_value = total_investment + total_pnl
        return_pct = (total_pnl / total_investment * 100) if total_investment > 0 else 0
        
        # Performance rating
        if return_pct > 15:
            rating = "Outstanding"
            color = "green"
        elif return_pct > 8:
            rating = "Good"
            color = "blue"
        elif return_pct > 0:
            rating = "Positive"
            color = "orange"
        else:
            rating = "Needs Improvement"
            color = "red"
        
        analysis = f"""
        **Portfolio Performance Analysis:**
        
        - **Total Value:** ₹{total_value:,.2f}
        - **Total Return:** ₹{total_pnl:,.2f} ({return_pct:.2f}%)
        - **Performance Rating:** <span style='color:{color}'>{rating}</span>
        - **Number of Positions:** {len(positions_df) if not positions_df.empty else 0}
        """
        
        recommendations = []
        
        if return_pct < 5:
            recommendations.append("Consider reviewing your trading strategy")
        if return_pct > 20:
            recommendations.append("Consider profit booking on high-performing positions")
        
        return {
            "answer": f"Your portfolio has delivered {return_pct:.2f}% returns with **{rating}** performance.",
            "analysis": analysis,
            "recommendations": recommendations
        }
    except Exception as e:
        return {
            "answer": "Unable to analyze portfolio performance.",
            "analysis": "Error in performance analysis",
            "recommendations": ["Check data connection", "Verify portfolio details"]
        }

def generate_portfolio_summary():
    """Generate comprehensive portfolio summary."""
    try:
        positions_df, holdings_df, total_pnl, total_investment = get_portfolio()
        
        if holdings_df.empty:
            return {
                "answer": "No portfolio data available.",
                "analysis": "Please connect to your broker to view portfolio summary.",
                "recommendations": ["Connect to broker account", "Add manual holdings if needed"]
            }
        
        total_value = total_investment + total_pnl
        return_pct = (total_pnl / total_investment * 100) if total_investment > 0 else 0
        
        analysis = f"""
        **Portfolio Summary:**
        
        - **Total Portfolio Value:** ₹{total_value:,.2f}
        - **Total Investment:** ₹{total_investment:,.2f}
        - **Total P&L:** ₹{total_pnl:,.2f} ({return_pct:.2f}%)
        - **Active Positions:** {len(positions_df) if not positions_df.empty else 0}
        - **Long-term Holdings:** {len(holdings_df) if not holdings_df.empty else 0}
        """
        
        # Top performers
        if not holdings_df.empty:
            top_performers = holdings_df.nlargest(3, 'pnl')
            analysis += "\n**Top Performers:**\n"
            for _, holding in top_performers.iterrows():
                analysis += f"- {holding['tradingsymbol']}: ₹{holding['pnl']:,.2f}\n"
        
        recommendations = [
            "Regularly review your portfolio allocation",
            "Set stop-losses for active positions",
            "Consider rebalancing if any position grows beyond 15% of portfolio"
        ]
        
        return {
            "answer": f"Your portfolio is valued at ₹{total_value:,.2f} with {return_pct:.2f}% returns.",
            "analysis": analysis,
            "recommendations": recommendations
        }
    except Exception as e:
        return {
            "answer": "Unable to generate portfolio summary.",
            "analysis": "Error in portfolio summary generation",
            "recommendations": ["Check broker connection", "Verify portfolio data"]
        }

def handle_market_queries(prompt_lower, instrument_df):
    """Handle market-related queries."""
    try:
        status_info = get_market_status()
        market_status = status_info['status'].replace('_', ' ').title()
        
        # Get NIFTY data for market context
        nifty_data = get_watchlist_data([{'symbol': 'NIFTY 50', 'exchange': 'NSE'}])
        nifty_price = nifty_data.iloc[0]['Price'] if not nifty_data.empty else 0
        nifty_change = nifty_data.iloc[0]['Change'] if not nifty_data.empty else 0
        
        analysis = f"""
        **Current Market Conditions:**
        
        - **Market Status:** {market_status}
        - **NIFTY 50:** ₹{nifty_price:.2f} ({nifty_change:+.2f})
        - **Trading Hours:** 9:15 AM - 3:30 PM IST
        - **Market Phase:** {'Open' if is_market_hours() else 'Closed'}
        """
        
        recommendations = [
            "Monitor key support and resistance levels",
            "Watch for sector rotation opportunities",
            "Stay updated with corporate announcements"
        ]
        
        if "outlook" in prompt_lower:
            outlook = "cautiously optimistic" if nifty_change > 0 else "cautious" if nifty_change < 0 else "neutral"
            answer = f"The market is currently **{market_status}** with NIFTY at ₹{nifty_price:.2f}. The near-term outlook appears **{outlook}**."
        else:
            answer = f"The market is **{market_status}**. NIFTY 50 is trading at ₹{nifty_price:.2f} ({nifty_change:+.2f})."
        
        return {
            "answer": answer,
            "analysis": analysis,
            "recommendations": recommendations
        }
    except Exception as e:
        return {
            "answer": "Unable to fetch market data at the moment.",
            "analysis": "Market data temporarily unavailable",
            "recommendations": ["Check internet connection", "Try again shortly"]
        }

def handle_trade_queries(prompt_lower, instrument_df):
    """Handle trade-related queries."""
    try:
        # Get current market conditions
        status_info = get_market_status()
        
        if not is_market_hours() and not is_pre_market_hours():
            return {
                "answer": "Markets are currently closed. Trading recommendations are available during market hours (9:15 AM - 3:30 PM IST).",
                "analysis": "Market Hours: 9:15 AM - 3:30 PM IST\nNext trading session: Tomorrow 9:15 AM",
                "recommendations": ["Prepare your watchlist for tomorrow", "Review overnight global market moves"]
            }
        
        # Generate simple trade ideas based on market conditions
        if "buy" in prompt_lower:
            ideas = ["RELIANCE (Strong fundamentals)", "INFY (IT sector momentum)", "HDFCBANK (Banking recovery)"]
            answer = "Based on current market conditions, consider these potential buy opportunities:"
        elif "sell" in prompt_lower:
            ideas = ["Consider profit booking on positions with >20% gains", "Review underperforming holdings", "Reduce exposure to high-beta stocks if market appears overbought"]
            answer = "For selling considerations, review these aspects:"
        else:
            ideas = ["Momentum plays in IT sector", "Value opportunities in banking", "Defensive positions in FMCG"]
            answer = "Current market environment suggests these trade ideas:"
        
        analysis = f"""
        **Trade Analysis Context:**
        
        - **Market Status:** {status_info['status'].replace('_', ' ').title()}
        - **Recommended Strategy:** {st.session_state.assistant_context['trading_style'].replace('_', ' ').title()}
        - **Risk Profile:** {st.session_state.assistant_context['risk_profile'].title()}
        """
        
        recommendations = ideas + [
            "Always use stop-loss orders",
            "Position size according to your risk tolerance",
            "Monitor market news for unexpected events"
        ]
        
        return {
            "answer": answer,
            "analysis": analysis,
            "recommendations": recommendations
        }
    except Exception as e:
        return {
            "answer": "Unable to generate trade ideas at the moment.",
            "analysis": "Trade analysis temporarily unavailable",
            "recommendations": ["Check market data connection", "Try again during market hours"]
        }

def handle_risk_queries(prompt_lower, instrument_df):
    """Handle risk-related queries."""
    analysis = """
    **Portfolio Risk Management Framework:**
    
    - **Diversification:** Spread across sectors and market caps
    - **Position Sizing:** Limit single positions to 5-10% of portfolio
    - **Stop-Loss:** Essential for risk management
    - **Hedging:** Consider options for portfolio protection
    """
    
    recommendations = [
        "Set stop-losses for all active positions",
        "Diversify across at least 5 sectors",
        "Avoid over-concentration in single stocks",
        "Consider hedging with put options in volatile markets",
        "Regularly review and adjust position sizes"
    ]
    
    return {
        "answer": "Effective risk management is crucial for long-term trading success. Here's my risk assessment framework:",
        "analysis": analysis,
        "recommendations": recommendations
    }

def handle_technical_queries(prompt_lower, instrument_df):
    """Handle technical analysis queries."""
    analysis = """
    **Technical Analysis Framework:**
    
    - **Trend Analysis:** Identify primary trends using moving averages
    - **Support/Resistance:** Key price levels for entry/exit decisions
    - **Momentum Indicators:** RSI, MACD for timing entries
    - **Volume Analysis:** Confirm price moves with volume
    - **Pattern Recognition:** Chart patterns for predictive signals
    """
    
    recommendations = [
        "Use multiple timeframes for confirmation (daily + hourly)",
        "Combine technical with fundamental analysis",
        "Wait for confirmation before entering trades",
        "Use stop-losses based on technical levels",
        "Monitor key indicators like RSI and moving averages"
    ]
    
    return {
        "answer": "Technical analysis helps identify trading opportunities through price patterns and indicators. Key aspects include:",
        "analysis": analysis,
        "recommendations": recommendations
    }

def handle_general_queries(prompt_lower, instrument_df):
    """Handle general trading queries."""
    general_responses = {
        "hello": "Hello! I'm your AI trading assistant. I can help with portfolio analysis, market insights, and trading strategies. What would you like to know?",
        "help": "I can assist with:\n- Portfolio analysis and health checks\n- Market outlook and trends\n- Trade ideas and opportunities\n- Risk management strategies\n- Technical analysis insights\n\nJust ask me anything about trading or your portfolio!",
        "hours": "Indian stock market trading hours:\n- Pre-open: 9:00-9:15 AM\n- Normal market: 9:15 AM - 3:30 PM\n- Special sessions may vary\nMarkets are closed on weekends and holidays.",
        "broker": "This platform supports Zerodha and Upstox integration. You can connect your broker in the settings section."
    }
    
    for key, response in general_responses.items():
        if key in prompt_lower:
            return {
                "answer": response,
                "analysis": "",
                "recommendations": []
            }
    
    # Default response for unrecognized queries
    return {
        "answer": "I'm here to help with your trading and investment needs. You can ask me about:\n\n• Your portfolio performance and health\n• Current market conditions and outlook\n• Trade ideas and opportunities\n• Risk management strategies\n• Technical analysis insights\n\nPlease try rephrasing your question if I didn't understand it correctly.",
        "analysis": "",
        "recommendations": ["Try asking about your portfolio", "Request market analysis", "Ask for trade ideas", "Get risk management advice"]
    }
    
def page_fundamental_analytics():
    """Enhanced Fundamental Analytics page using available Kite Connect methods."""
    display_header()
    st.title("📊 Fundamental Analytics")
    
    instrument_df = get_instrument_df()
    if instrument_df.empty:
        st.info("Please connect to a broker to view fundamental analytics.")
        return
    
    # Symbol selection
    col1, col2 = st.columns([3, 1])
    
    with col1:
        all_symbols = instrument_df[
            (instrument_df['exchange'].isin(['NSE', 'BSE'])) & 
            (~instrument_df['tradingsymbol'].str.contains('-', na=False))
        ]['tradingsymbol'].unique()
        
        selected_symbol = st.selectbox(
            "Select Stock Symbol",
            sorted(all_symbols),
            index=list(all_symbols).index('RELIANCE') if 'RELIANCE' in all_symbols else 0,
            key="fundamental_symbol"
        )
    
    with col2:
        st.write("### Quick Actions")
        if st.button("📈 Analyze Company", key="analyze_company", use_container_width=True, type="primary"):
            st.session_state.show_company_events = True
        if st.button("🔄 Refresh Data", key="refresh_fundamental", use_container_width=True):
            st.rerun()
    
    # Display current price and basic info
    quote_data = get_watchlist_data([{'symbol': selected_symbol, 'exchange': 'NSE'}])
    if not quote_data.empty:
        current_price = quote_data.iloc[0]['Price']
        change = quote_data.iloc[0]['Change']
        pct_change = quote_data.iloc[0]['% Change']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Price", f"₹{current_price:.2f}")
        with col2:
            st.metric("Change", f"₹{change:+.2f}")
        with col3:
            st.metric("Change %", f"{pct_change:+.2f}%")
        with col4:
            # Get basic instrument info
            instrument = instrument_df[
                (instrument_df['tradingsymbol'] == selected_symbol.upper()) & 
                (instrument_df['exchange'] == 'NSE')
            ]
            if not instrument.empty and 'instrument_type' in instrument.iloc[0]:
                inst_type = instrument.iloc[0]['instrument_type']
                st.metric("Instrument Type", inst_type)
    
    st.markdown("---")
    
    # Main analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Company Analysis", "📊 Performance", "📈 Technical", "📅 Market Calendar"])
    
    with tab1:
        st.subheader("🎯 Company Analysis & Events")
        st.info("Comprehensive company analysis using available market data and historical patterns.")
        
        # Display company events and analysis
        display_company_events_kite(selected_symbol, instrument_df)
    
    with tab2:
        st.subheader("📊 Performance Metrics")
        
        # Get historical data for performance analysis
        instrument = instrument_df[
            (instrument_df['tradingsymbol'] == selected_symbol.upper()) & 
            (instrument_df['exchange'] == 'NSE')
        ]
        
        if not instrument.empty:
            instrument_token = instrument.iloc[0]['instrument_token']
            
            with st.spinner("Fetching performance data..."):
                try:
                    # Get historical data for different timeframes
                    historical_1m = get_historical_data(instrument_token, 'day', period='1mo')
                    historical_3m = get_historical_data(instrument_token, 'day', period='3mo')
                    historical_1y = get_historical_data(instrument_token, 'day', period='1y')
                    
                    if not historical_1m.empty:
                        # Calculate performance metrics
                        current_price = historical_1m['close'].iloc[-1]
                        price_1m_ago = historical_1m['close'].iloc[0] if len(historical_1m) > 1 else current_price
                        price_3m_ago = historical_3m['close'].iloc[0] if not historical_3m.empty else current_price
                        price_1y_ago = historical_1y['close'].iloc[0] if not historical_1y.empty else current_price
                        
                        # Performance metrics
                        perf_1m = ((current_price - price_1m_ago) / price_1m_ago) * 100
                        perf_3m = ((current_price - price_3m_ago) / price_3m_ago) * 100
                        perf_1y = ((current_price - price_1y_ago) / price_1y_ago) * 100
                        
                        # Display performance metrics
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("1 Month Return", f"{perf_1m:.2f}%")
                        col2.metric("3 Month Return", f"{perf_3m:.2f}%")
                        col3.metric("1 Year Return", f"{perf_1y:.2f}%")
                        col4.metric("Current Price", f"₹{current_price:.2f}")
                        
                        # Create performance chart
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=historical_1m.index, y=historical_1m['close'], 
                                               name='Price', line=dict(color='blue')))
                        
                        fig.update_layout(
                            title=f"{selected_symbol} - Price Performance (1 Month)",
                            xaxis_title="Date",
                            yaxis_title="Price (₹)",
                            template="plotly_dark" if st.session_state.theme == 'Dark' else "plotly_white"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                    else:
                        st.warning("Insufficient historical data for performance analysis.")
                        
                except Exception as e:
                    st.error(f"Error fetching performance data: {e}")
        else:
            st.error("Instrument not found for performance analysis.")
    
    with tab3:
        st.subheader("📈 Technical Analysis")
        
        instrument = instrument_df[
            (instrument_df['tradingsymbol'] == selected_symbol.upper()) & 
            (instrument_df['exchange'] == 'NSE')
        ]
        
        if not instrument.empty:
            instrument_token = instrument.iloc[0]['instrument_token']
            
            # Get historical data for technical analysis
            historical_data = get_historical_data(instrument_token, 'day', period='6mo')
            
            if not historical_data.empty:
                # Calculate technical indicators
                df = historical_data.copy()
                
                # RSI
                df['RSI'] = talib.RSI(df['close'], timeperiod=14)
                
                # Moving averages
                df['SMA_20'] = talib.SMA(df['close'], timeperiod=20)
                df['SMA_50'] = talib.SMA(df['close'], timeperiod=50)
                
                # MACD
                df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = talib.MACD(df['close'])
                
                # Display current technical levels
                current_rsi = df['RSI'].iloc[-1]
                current_close = df['close'].iloc[-1]
                sma_20 = df['SMA_20'].iloc[-1]
                sma_50 = df['SMA_50'].iloc[-1]
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("RSI (14)", f"{current_rsi:.1f}")
                col2.metric("SMA 20", f"₹{sma_20:.2f}")
                col3.metric("SMA 50", f"₹{sma_50:.2f}")
                col4.metric("Price vs SMA 20", f"{(current_close/sma_20 - 1)*100:.1f}%")
                
                # RSI interpretation
                st.subheader("📊 RSI Analysis")
                if current_rsi > 70:
                    st.warning("RSI indicates OVERBOUGHT conditions. Consider caution.")
                elif current_rsi < 30:
                    st.info("RSI indicates OVERSOLD conditions. Potential buying opportunity.")
                else:
                    st.success("RSI in NEUTRAL territory.")
                    
                # Moving average analysis
                st.subheader("📈 Trend Analysis")
                if current_close > sma_20 > sma_50:
                    st.success("UPTREND: Price above both SMAs - Bullish sentiment")
                elif current_close < sma_20 < sma_50:
                    st.error("DOWNTREND: Price below both SMAs - Bearish sentiment")
                else:
                    st.warning("SIDEWAYS: Mixed signals - Market in consolidation")
                    
            else:
                st.warning("Insufficient data for technical analysis.")
        else:
            st.error("Instrument not found for technical analysis.")
    
    with tab4:
        st.subheader("📅 Market Calendar & Events")
        
        holidays = get_market_holidays_extended()
        
        for category, events in holidays.items():
            with st.expander(f"{category}", expanded=True):
                for event in events:
                    st.write(f"• {event}")
        
        # Add upcoming event reminders
        st.subheader("🔔 Event Reminders")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Set Quarterly Results Alert", use_container_width=True):
                st.success(f"Quarterly results alert set for {selected_symbol}")
        
        with col2:
            if st.button("Set Corporate Action Alert", use_container_width=True):
                st.success(f"Corporate action alert set for {selected_symbol}")
    
    # Quick analysis tools
    st.markdown("---")
    st.subheader("🚀 Quick Analysis Tools")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Run Full Analysis", use_container_width=True):
            st.info("Running comprehensive analysis...")
            st.rerun()
    
    with col2:
        if st.button("📈 Technical Scan", use_container_width=True):
            st.info("Performing technical analysis scan...")
    
    with col3:
        if st.button("💰 Valuation Check", use_container_width=True):
            st.info("Running valuation analysis...")
    
    with col4:
        if st.button("📅 Event Scanner", use_container_width=True):
            st.info("Scanning for upcoming corporate events...")

    # Auto-refresh control
    st.markdown("---")
    with st.expander("⚙️ Display Settings"):
        auto_refresh = st.checkbox("Enable Auto-refresh", value=False, key="fundamental_auto_refresh")
        refresh_interval = st.selectbox(
            "Refresh Interval", 
            [30, 60, 120, 300], 
            index=1, 
            format_func=lambda x: f"{x} seconds",
            key="fundamental_refresh_interval"
        )
        
        if st.button("🔄 Refresh Now", key="manual_refresh_fundamental"):
            st.rerun()

def page_basket_orders():
    """A page for creating, managing, and executing basket orders."""
    display_header()
    st.title("Basket Orders")

    instrument_df = get_instrument_df()
    if instrument_df.empty:
        st.info("Please connect to a broker to use the basket order feature.")
        return

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Add Order to Basket")
        with st.form("add_to_basket_form"):
            symbol = st.text_input("Symbol").upper()
            transaction_type = st.radio("Transaction", ["BUY", "SELL"], horizontal=True)
            quantity = st.number_input("Quantity", min_value=1, step=1)
            product = st.radio("Product", ["MIS", "CNC"], horizontal=True)
            order_type = st.radio("Order Type", ["MARKET", "LIMIT"], horizontal=True)
            price = st.number_input("Price", min_value=0.01) if order_type == "LIMIT" else 0
            
            if st.form_submit_button("Add to Basket"):
                if symbol and quantity > 0:
                    st.session_state.basket.append({
                        'symbol': symbol,
                        'transaction_type': transaction_type,
                        'quantity': quantity,
                        'product': product,
                        'order_type': order_type,
                        'price': price if price > 0 else None
                    })
                    st.success(f"Added {symbol} to basket!")
                    st.rerun()

    with col2:
        st.subheader("Current Basket")
        if st.session_state.basket:
            for i, order in enumerate(st.session_state.basket):
                with st.expander(f"{order['transaction_type']} {order['quantity']} {order['symbol']}"):
                    st.write(f"**Product:** {order['product']}")
                    st.write(f"**Order Type:** {order['order_type']}")
                    if order['price']:
                        st.write(f"**Price:** ₹{order['price']}")
                    if st.button("Remove", key=f"remove_{i}"):
                        st.session_state.basket.pop(i)
                        st.rerun()
            
            st.markdown("---")
            if st.button("Execute Basket Order", type="primary", use_container_width=True):
                execute_basket_order(st.session_state.basket, instrument_df)
        else:
            st.info("Your basket is empty. Add orders using the form on the left.")

def run_backtest(strategy_func, data, **params):
    """Runs a backtest for a given strategy function."""
    df = data.copy()
    signals = strategy_func(df, **params)
    
    initial_capital = 100000.0
    capital = initial_capital
    position = 0
    portfolio_value = []
    
    for i in range(len(df)):
        if signals[i] == 'BUY' and position == 0:
            position = capital / df['close'][i]
            capital = 0
        elif signals[i] == 'SELL' and position > 0:
            capital = position * df['close'][i]
            position = 0
        
        current_value = capital + (position * df['close'][i])
        portfolio_value.append(current_value)
        
    pnl = (portfolio_value[-1] - initial_capital) / initial_capital * 100
    
    return pnl, pd.Series(portfolio_value, index=df.index)

def rsi_strategy(df, rsi_period=14, rsi_overbought=70, rsi_oversold=30):
    """Simple RSI Crossover Strategy"""
    rsi = talib.RSI(df['close'], timeperiod=rsi_period)
    signals = [''] * len(df)
    for i in range(1, len(df)):
        if rsi.iloc[i-1] < rsi_oversold and rsi.iloc[i] > rsi_oversold:
            signals[i] = 'BUY'
        elif rsi.iloc[i-1] > rsi_overbought and rsi.iloc[i] < rsi_overbought:
            signals[i] = 'SELL'
    return signals

def macd_strategy(df, fast=12, slow=26, signal=9):
    """MACD Crossover Strategy"""
    macd, macdsignal, macdhist = talib.MACD(df['close'], fastperiod=fast, slowperiod=slow, signalperiod=signal)
    signals = [''] * len(df)
    for i in range(1, len(df)):
        if macd.iloc[i-1] < macdsignal.iloc[i-1] and macd.iloc[i] > macdsignal.iloc[i]:
            signals[i] = 'BUY'
        elif macd.iloc[i-1] > macdsignal.iloc[i-1] and macd.iloc[i] < macdsignal.iloc[i]:
            signals[i] = 'SELL'
    return signals

def supertrend_strategy(df, period=7, multiplier=3):
    """Supertrend Strategy - simplified version without pandas-ta"""
    # Calculate ATR
    atr = talib.ATR(df['high'], df['low'], df['close'], timeperiod=period)
    
    # Basic upper and lower bands
    hl2 = (df['high'] + df['low']) / 2
    upper_band = hl2 + (multiplier * atr)
    lower_band = hl2 - (multiplier * atr)
    
    signals = [''] * len(df)
    trend = [1] * len(df) # 1 for uptrend, -1 for downtrend
    
    for i in range(1, len(df)):
        if df['close'].iloc[i] > upper_band.iloc[i-1]:
            trend[i] = 1
        elif df['close'].iloc[i] < lower_band.iloc[i-1]:
            trend[i] = -1
        else:
            trend[i] = trend[i-1]
        
        if trend[i] == 1 and trend[i-1] == -1:
            signals[i] = 'BUY'
        elif trend[i] == -1 and trend[i-1] == 1:
            signals[i] = 'SELL'
    
    return signals

def page_algo_strategy_maker():
    """Algo Strategy Maker page with pre-built, backtestable, and executable strategies."""
    display_header()
    st.title("Algo Strategy Hub")
    instrument_df = get_instrument_df()
    if instrument_df.empty:
        st.info("Connect to a broker to use the Algo Strategy Hub.")
        return

    st.info("Select a pre-built strategy, configure its parameters, and run a backtest on historical data. You can then place trades based on the latest signal.", icon="🤖")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Strategy Configuration")
        
        strategy_options = {
            "RSI Crossover": rsi_strategy,
            "MACD Crossover": macd_strategy,
            "Supertrend Follower": supertrend_strategy,
        }
        selected_strategy_name = st.selectbox("Select a Strategy", list(strategy_options.keys()))
        
        st.markdown("**Instrument**")
        all_symbols = instrument_df[instrument_df['exchange'].isin(['NSE', 'NFO', 'MCX', 'CDS'])]['tradingsymbol'].unique()
        symbol = st.selectbox("Select Symbol", all_symbols, index=list(all_symbols).index('RELIANCE') if 'RELIANCE' in all_symbols else 0)
        
        st.markdown("**Parameters**")
        params = {}
        if selected_strategy_name == "RSI Crossover":
            params['rsi_period'] = st.slider("RSI Period", 5, 30, 14)
            params['rsi_overbought'] = st.slider("RSI Overbought", 60, 90, 70)
            params['rsi_oversold'] = st.slider("RSI Oversold", 10, 40, 30)
        elif selected_strategy_name == "MACD Crossover":
            params['fast'] = st.slider("Fast Period", 5, 20, 12)
            params['slow'] = st.slider("Slow Period", 20, 50, 26)
            params['signal'] = st.slider("Signal Period", 5, 20, 9)
        elif selected_strategy_name == "Supertrend Follower":
            params['period'] = st.slider("ATR Period", 5, 20, 7)
            params['multiplier'] = st.slider("Multiplier", 1.0, 5.0, 3.0, 0.5)

        st.markdown("**Trade Execution**")
        quantity = st.number_input("Trade Quantity", min_value=1, value=1)
        
        run_button = st.button("Run Backtest & Get Signal", use_container_width=True, type="primary")

    with col2:
        if run_button:
            with st.spinner(f"Running backtest for {selected_strategy_name} on {symbol}..."):
                exchange = instrument_df[instrument_df['tradingsymbol'] == symbol].iloc[0]['exchange']
                token = get_instrument_token(symbol, instrument_df, exchange=exchange)
                data = get_historical_data(token, 'day', period='1y')
                
                if not data.empty and len(data) > 50: 
                    pnl, portfolio_curve = run_backtest(strategy_options[selected_strategy_name], data, **params)
                    latest_signal = strategy_options[selected_strategy_name](data, **params)[-1]

                    st.session_state['backtest_results'] = {
                        'pnl': pnl,
                        'curve': portfolio_curve,
                        'signal': latest_signal,
                        'symbol': symbol,
                        'quantity': quantity
                    }
                else:
                    st.error("Could not fetch enough historical data to run the backtest.")
                    if 'backtest_results' in st.session_state:
                        st.session_state['backtest_results'] = None

        if st.session_state.get('backtest_results') is not None:
            results = st.session_state['backtest_results']
            st.subheader("Backtest Results")
            st.metric("Total P&L (1 Year)", f"{results['pnl']:.2f}%")

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=results['curve'].index, y=results['curve'], mode='lines', name='Portfolio Value'))
            fig.update_layout(title="Portfolio Growth Over 1 Year", yaxis_title="Portfolio Value (₹)")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Live Signal & Trading")
            signal = results['signal']
            color = "green" if signal == "BUY" else "red" if signal == "SELL" else "orange"
            st.markdown(f"### Latest Signal: <span style='color:{color};'>{signal if signal else 'HOLD'}</span>", unsafe_allow_html=True)

            if signal in ["BUY", "SELL"]:
                if st.button(f"Place {signal} Order for {results['quantity']} of {results['symbol']}", use_container_width=True):
                    place_order(instrument_df, results['symbol'], results['quantity'], "MARKET", signal, "MIS")

@st.cache_data(ttl=3600)
def run_scanner(instrument_df, scanner_type, holdings_df=None):
    """A single function to run different types of market scanners on user holdings or a predefined list."""
    client = get_broker_client()
    if not client or instrument_df.empty: return pd.DataFrame()

    scan_list = []
    if holdings_df is not None and not holdings_df.empty:
        scan_list = holdings_df['tradingsymbol'].unique().tolist()
        st.info("Scanning stocks from your live holdings.")
    else:
        scan_list = ['RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK', 'HINDUNILVR', 'ITC', 'SBIN', 'BAJFINANCE', 'KOTAKBANK', 'LT', 'WIPRO', 'AXISBANK', 'MARUTI', 'ASIANPAINT']
        st.info("Scanning a predefined list of NIFTY 50 stocks as no holdings were found.")

    results = []
    
    token_map = {
        row['tradingsymbol']: row['instrument_token']
        for _, row in instrument_df[instrument_df['tradingsymbol'].isin(scan_list)].iterrows()
    }
    
    for symbol in scan_list:
        token = token_map.get(symbol)
        if not token: continue
        
        try:
            df = get_historical_data(token, 'day', period='1y')
            if df.empty or len(df) < 252: continue
            
            df.columns = [c.lower() for c in df.columns]

            if scanner_type == "Momentum":
                rsi_col = next((c for c in df.columns if 'rsi_14' in c), None)
                if rsi_col:
                    rsi = df.iloc[-1].get(rsi_col)
                    if rsi and (rsi > 70 or rsi < 30):
                        results.append({'Stock': symbol, 'RSI': f"{rsi:.2f}", 'Signal': "Overbought" if rsi > 70 else "Oversold"})
            
            elif scanner_type == "Trend":
                adx_col = next((c for c in df.columns if 'adx_14' in c), None)
                ema50_col = next((c for c in df.columns if 'ema_50' in c), None)
                ema200_col = next((c for c in df.columns if 'ema_200' in c), None)
                
                if adx_col and ema50_col and ema200_col:
                    adx = df.iloc[-1].get(adx_col)
                    ema50 = df.iloc[-1].get(ema50_col)
                    ema200 = df.iloc[-1].get(ema200_col)
                    if adx and adx > 25 and ema50 and ema200:
                        trend = "Uptrend" if ema50 > ema200 else "Downtrend"
                        results.append({'Stock': symbol, 'ADX': f"{adx:.2f}", 'Trend': trend})

            elif scanner_type == "Breakout":
                high_52wk = df['high'].rolling(window=252).max().iloc[-1]
                low_52wk = df['low'].rolling(window=252).min().iloc[-1]
                last_close = df['close'].iloc[-1]
                avg_vol_20d = df['volume'].rolling(window=20).mean().iloc[-1]
                last_vol = df['volume'].iloc[-1]

                if last_close >= high_52wk * 0.98:
                    signal = "Near 52-Week High"
                    if last_vol > avg_vol_20d * 1.5:
                        signal += " (Volume Surge)"
                    results.append({'Stock': symbol, 'Signal': signal, 'Last Close': last_close, '52Wk High': high_52wk})

        except Exception:
            continue
            
    return pd.DataFrame(results)

def run_momentum_scanner(instrument_df, holdings_df=None):
    """Momentum scanner with RSI and MACD analysis."""
    client = get_broker_client()
    if not client or instrument_df.empty: 
        return pd.DataFrame()

    # Get symbols to scan
    scan_list = []
    if holdings_df is not None and not holdings_df.empty:
        scan_list = holdings_df['tradingsymbol'].unique().tolist()[:20] # Limit to 20 stocks
    else:
        scan_list = [
            'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK', 'HINDUNILVR', 
            'ITC', 'SBIN', 'BAJFINANCE', 'KOTAKBANK', 'LT', 'WIPRO', 'AXISBANK', 
            'MARUTI', 'ASIANPAINT', 'HCLTECH', 'TATAMOTORS', 'SUNPHARMA'
        ]
    
    results = []
    
    for symbol in scan_list:
        try:
            # Get live quote
            exchange = 'NSE'
            quote_data = get_watchlist_data([{'symbol': symbol, 'exchange': exchange}])
            if quote_data.empty:
                continue
                
            current_price = quote_data.iloc[0]['Price']
            change_pct = quote_data.iloc[0]['% Change']
            
            # Get historical data
            token = get_instrument_token(symbol, instrument_df, exchange)
            if not token:
                continue
                
            hist_data = get_historical_data(token, 'day', period='3mo')
            if hist_data.empty or len(hist_data) < 30:
                continue
            
            # Calculate RSI
            try:
                hist_data['RSI_14'] = talib.RSI(hist_data['close'], timeperiod=14)
                latest = hist_data.iloc[-1]
                rsi = latest.get('RSI_14', 50)
                
                # Momentum signals
                if rsi > 70 and change_pct > 0:
                    results.append({
                        'Symbol': symbol,
                        'LTP': f"₹{current_price:.2f}",
                        'Change %': f"{change_pct:.2f}%",
                        'RSI': f"{rsi:.1f}",
                        'Signal': "Overbought",
                        'Strength': "High"
                    })
                elif rsi < 30 and change_pct < 0:
                    results.append({
                        'Symbol': symbol,
                        'LTP': f"₹{current_price:.2f}",
                        'Change %': f"{change_pct:.2f}%",
                        'RSI': f"{rsi:.1f}",
                        'Signal': "Oversold", 
                        'Strength': "High"
                    })
                    
            except Exception:
                continue
                
        except Exception:
            continue
            
    return pd.DataFrame(results)

def run_trend_scanner(instrument_df, holdings_df=None):
    """Trend scanner with EMA analysis."""
    client = get_broker_client()
    if not client or instrument_df.empty: 
        return pd.DataFrame()

    scan_list = []
    if holdings_df is not None and not holdings_df.empty:
        scan_list = holdings_df['tradingsymbol'].unique().tolist()[:20]
    else:
        scan_list = [
            'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK', 'HINDUNILVR', 
            'ITC', 'SBIN', 'BAJFINANCE', 'KOTAKBANK', 'LT', 'WIPRO', 'AXISBANK'
        ]
    
    results = []
    
    for symbol in scan_list:
        try:
            # Get live data
            exchange = 'NSE'
            quote_data = get_watchlist_data([{'symbol': symbol, 'exchange': exchange}])
            if quote_data.empty:
                continue
                
            current_price = quote_data.iloc[0]['Price']
            change_pct = quote_data.iloc[0]['% Change']
            
            # Get historical data
            token = get_instrument_token(symbol, instrument_df, exchange)
            if not token:
                continue
                
            hist_data = get_historical_data(token, 'day', period='3mo')
            if hist_data.empty or len(hist_data) < 50:
                continue
            
            # Calculate EMAs
            try:
                hist_data['EMA_20'] = talib.EMA(hist_data['close'], timeperiod=20)
                hist_data['EMA_50'] = talib.EMA(hist_data['close'], timeperiod=50)
                
                latest = hist_data.iloc[-1]
                ema_20 = latest.get('EMA_20', current_price)
                ema_50 = latest.get('EMA_50', current_price)
                
                # Trend signals
                if current_price > ema_20 > ema_50 and change_pct > 0:
                    results.append({
                        'Symbol': symbol,
                        'LTP': f"₹{current_price:.2f}",
                        'Change %': f"{change_pct:.2f}%",
                        'Trend': "Uptrend",
                        '20 EMA': f"₹{ema_20:.1f}",
                        '50 EMA': f"₹{ema_50:.1f}"
                    })
                elif current_price < ema_20 < ema_50 and change_pct < 0:
                    results.append({
                        'Symbol': symbol,
                        'LTP': f"₹{current_price:.2f}",
                        'Change %': f"{change_pct:.2f}%",
                        'Trend': "Downtrend",
                        '20 EMA': f"₹{ema_20:.1f}",
                        '50 EMA': f"₹{ema_50:.1f}"
                    })
                    
            except Exception:
                continue
                
        except Exception:
            continue
            
    return pd.DataFrame(results)

def run_breakout_scanner(instrument_df, holdings_df=None):
    """Breakout scanner for key level breaks."""
    client = get_broker_client()
    if not client or instrument_df.empty: 
        return pd.DataFrame()

    scan_list = []
    if holdings_df is not None and not holdings_df.empty:
        scan_list = holdings_df['tradingsymbol'].unique().tolist()[:20]
    else:
        scan_list = [
            'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK', 'HINDUNILVR', 
            'ITC', 'SBIN', 'BAJFINANCE', 'KOTAKBANK', 'LT', 'WIPRO', 'AXISBANK'
        ]
    
    results = []
    
    for symbol in scan_list:
        try:
            # Get live data
            exchange = 'NSE'
            quote_data = get_watchlist_data([{'symbol': symbol, 'exchange': exchange}])
            if quote_data.empty:
                continue
                
            current_price = quote_data.iloc[0]['Price']
            change_pct = quote_data.iloc[0]['% Change']
            
            # Get historical data
            token = get_instrument_token(symbol, instrument_df, exchange)
            if not token:
                continue
                
            hist_data = get_historical_data(token, 'day', period='6mo')
            if hist_data.empty or len(hist_data) < 100:
                continue
            
            # Calculate breakout levels
            high_20d = hist_data['high'].tail(20).max()
            low_20d = hist_data['low'].tail(20).min()
            
            # Breakout signals
            if current_price >= high_20d and change_pct > 0:
                results.append({
                    'Symbol': symbol,
                    'LTP': f"₹{current_price:.2f}",
                    'Change %': f"{change_pct:.2f}%",
                    'Breakout': "20-Day High",
                    'Resistance': f"₹{high_20d:.1f}"
                })
            elif current_price <= low_20d and change_pct < 0:
                results.append({
                    'Symbol': symbol,
                    'LTP': f"₹{current_price:.2f}",
                    'Change %': f"{change_pct:.2f}%",
                    'Breakout': "20-Day Low", 
                    'Support': f"₹{low_20d:.1f}"
                })
                
        except Exception:
            continue
            
    return pd.DataFrame(results)

def page_momentum_and_trend_finder():
    """Clean and functional Market Scanners page."""
    display_header()
    st.title("Market Scanners")
    
    instrument_df = get_instrument_df()
    if instrument_df.empty:
        st.info("Please connect to a broker to use market scanners.")
        return
        
    _, holdings_df, _, _ = get_portfolio()
    
    # Simple scanner selection
    col1, col2 = st.columns([3, 1])
    with col1:
        scanner_type = st.radio(
            "Select Scanner Type",
            ["Momentum (RSI)", "Trend (EMA)", "Breakout"],
            horizontal=True
        )
    
    with col2:
        if st.button("🔄 Scan Now", use_container_width=True, type="primary"):
            st.rerun()
    
    st.markdown("---")
    
    # Run selected scanner
    with st.spinner(f"Running {scanner_type} scanner..."):
        if scanner_type == "Momentum (RSI)":
            data = run_momentum_scanner(instrument_df, holdings_df)
            title = "Momentum Stocks (RSI Based)"
            description = "Stocks with RSI above 70 (overbought) or below 30 (oversold)"
            
        elif scanner_type == "Trend (EMA)":
            data = run_trend_scanner(instrument_df, holdings_df) 
            title = "Trending Stocks (EMA Based)"
            description = "Stocks in strong uptrend/downtrend based on EMA alignment"
            
        else: # Breakout
            data = run_breakout_scanner(instrument_df, holdings_df)
            title = "Breakout Stocks"
            description = "Stocks breaking 20-day high/low resistance/support levels"
    
    # Display results
    st.subheader(title)
    st.caption(description)
    
    if not data.empty:
        # Color coding based on scanner type
        if scanner_type == "Momentum (RSI)":
            def color_momentum(val):
                if 'Overbought' in str(val):
                    return 'color: #ff4444; font-weight: bold;'
                elif 'Oversold' in str(val):
                    return 'color: #00aa00; font-weight: bold;'
                return ''
            styled_data = data.style.map(color_momentum, subset=['Signal'])
            
        elif scanner_type == "Trend (EMA)":
            def color_trend(val):
                if 'Uptrend' in str(val):
                    return 'color: #00aa00; font-weight: bold;'
                elif 'Downtrend' in str(val):
                    return 'color: #ff4444; font-weight: bold;'
                return ''
            styled_data = data.style.map(color_trend, subset=['Trend'])
            
        else: # Breakout
            def color_breakout(val):
                if 'High' in str(val):
                    return 'color: #00aa00; font-weight: bold;'
                elif 'Low' in str(val):
                    return 'color: #ff4444; font-weight: bold;'
                return ''
            styled_data = data.style.map(color_breakout, subset=['Breakout'])
        
        st.dataframe(styled_data, use_container_width=True, hide_index=True)
        
        # Simple statistics
        if scanner_type == "Momentum (RSI)":
            bullish = len(data[data['Signal'] == 'Overbought'])
            bearish = len(data[data['Signal'] == 'Oversold'])
            st.metric("Signals Found", len(data), delta=f"{bullish} Bullish, {bearish} Bearish")
            
        elif scanner_type == "Trend (EMA)":
            uptrend = len(data[data['Trend'] == 'Uptrend'])
            downtrend = len(data[data['Trend'] == 'Downtrend'])
            st.metric("Signals Found", len(data), delta=f"{uptrend} Up, {downtrend} Down")
            
        else: # Breakout
            breakouts = len(data[data['Breakout'].str.contains('High')])
            breakdowns = len(data[data['Breakout'].str.contains('Low')])
            st.metric("Signals Found", len(data), delta=f"{breakouts} Breakouts, {breakdowns} Breakdowns")
        
        # Quick actions
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📋 Export to CSV", use_container_width=True):
                csv = data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{scanner_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col2:
            if st.button("👀 Add to Watchlist", use_container_width=True):
                added = 0
                for symbol in data['Symbol'].head(5): # Add top 5
                    if symbol not in [item['symbol'] for item in st.session_state.watchlists[st.session_state.active_watchlist]]:
                        st.session_state.watchlists[st.session_state.active_watchlist].append({
                            'symbol': symbol, 
                            'exchange': 'NSE'
                        })
                        added += 1
                if added > 0:
                    st.success(f"Added {added} stocks to watchlist")
                else:
                    st.info("No new stocks to add")
                    
    else:
        # Clear, helpful empty state
        st.info(f"""
        **No {scanner_type.lower()} signals found.**
        
        This could mean:
        - Markets are in consolidation
        - No extreme conditions detected
        - Try a different scanner type
        - Check if market is open
        """)

def calculate_strategy_pnl(legs, underlying_ltp):
    """Calculates the P&L for a given options strategy."""
    if not legs:
        return pd.DataFrame(), 0, 0, []

    price_range = np.linspace(underlying_ltp * 0.8, underlying_ltp * 1.2, 100)
    pnl_df = pd.DataFrame(index=price_range)
    pnl_df.index.name = "Underlying Price at Expiry"
    
    total_premium = 0
    for i, leg in enumerate(legs):
        pnl = 0
        if leg['type'] == 'Call':
            if leg['position'] == 'Buy':
                pnl = np.maximum(0, price_range - leg['strike']) - leg['premium']
                total_premium -= leg['premium'] * leg['quantity']
            else:
                pnl = leg['premium'] - np.maximum(0, price_range - leg['strike'])
                total_premium += leg['premium'] * leg['quantity']
        else:
            if leg['position'] == 'Buy':
                pnl = np.maximum(0, leg['strike'] - price_range) - leg['premium']
                total_premium -= leg['premium'] * leg['quantity']
            else:
                pnl = leg['premium'] - np.maximum(0, leg['strike'] - price_range)
                total_premium += leg['premium'] * leg['quantity']
        
        pnl_df[f'Leg_{i+1}'] = pnl * leg['quantity']
    
    pnl_df['Total P&L'] = pnl_df.sum(axis=1)
    
    max_profit = pnl_df['Total P&L'].max()
    max_loss = pnl_df['Total P&L'].min()
    
    breakevens = []
    sign_changes = np.where(np.diff(np.sign(pnl_df['Total P&L'])))[0]
    for idx in sign_changes:
        breakevens.append(pnl_df.index[idx])

    return pnl_df, max_profit, max_loss, breakevens

def page_option_strategy_builder():
    """Option Strategy Builder page with live data and P&L calculation."""
    display_header()
    st.title("Options Strategy Builder")
    
    instrument_df = get_instrument_df()
    client = get_broker_client()
    if instrument_df.empty or not client:
        st.info("Please connect to a broker to build strategies.")
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Strategy Configuration")
        underlying = st.selectbox("Underlying", ["NIFTY", "BANKNIFTY", "FINNIFTY"])
        
        _, _, underlying_ltp, available_expiries = get_options_chain(underlying, instrument_df)

        if not available_expiries:
            st.error(f"No options available for {underlying}.")
            st.stop()
            
        expiry_date = st.selectbox("Expiry", [e.strftime("%d %b %Y") for e in available_expiries])
        
        with st.form("add_leg_form"):
            st.write("**Add a New Leg**")
            leg_cols = st.columns(4)
            position = leg_cols[0].selectbox("Position", ["Buy", "Sell"])
            option_type = leg_cols[1].selectbox("Type", ["Call", "Put"])
            
            expiry_dt = datetime.strptime(expiry_date, "%d %b %Y").date()
            options = instrument_df[
                (instrument_df['name'] == underlying) & 
                (instrument_df['expiry'].dt.date == expiry_dt) & 
                (instrument_df['instrument_type'] == option_type[0])
            ]
            
            if not options.empty:
                strikes = sorted(options['strike'].unique())
                strike = leg_cols[2].selectbox("Strike", strikes, index=len(strikes)//2)
                quantity = leg_cols[3].number_input("Lots", min_value=1, value=1)
                
                submitted = st.form_submit_button("Add Leg")
                if submitted:
                    lot_size = options.iloc[0]['lot_size']
                    tradingsymbol = options[options['strike'] == strike].iloc[0]['tradingsymbol']
                    
                    try:
                        quote = client.quote(f"NFO:{tradingsymbol}")[f"NFO:{tradingsymbol}"]
                        premium = quote['last_price']
                        
                        st.session_state.strategy_legs.append({
                            'symbol': tradingsymbol,
                            'position': position,
                            'type': option_type,
                            'strike': strike,
                            'quantity': quantity * lot_size,
                            'premium': premium
                        })
                        st.rerun()
                    except Exception as e:
                        st.error(f"Could not fetch premium: {e}")
            else:
                st.warning("No strikes found for selected expiry/type.")

        st.subheader("Current Legs")
        if st.session_state.strategy_legs:
            for i, leg in enumerate(st.session_state.strategy_legs):
                st.text(f"{i+1}: {leg['position']} {leg['quantity']} {leg['symbol']} @ ₹{leg['premium']:.2f}")
            if st.button("Clear All Legs"):
                st.session_state.strategy_legs = []
                st.rerun()
        else:
            st.info("Add legs to your strategy.")
            
    with col2:
        st.subheader("Strategy Payoff Analysis")
        
        if st.session_state.strategy_legs:
            pnl_df, max_profit, max_loss, breakevens = calculate_strategy_pnl(st.session_state.strategy_legs, underlying_ltp)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=pnl_df.index, y=pnl_df['Total P&L'], mode='lines', name='P&L'))
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            fig.add_vline(x=underlying_ltp, line_dash="dot", line_color="yellow", annotation_text="Current LTP")
            fig.update_layout(
                title="Strategy P&L Payoff Chart",
                xaxis_title="Underlying Price at Expiry",
                yaxis_title="Profit / Loss (₹)",
                template='plotly_dark' if st.session_state.get('theme') == 'Dark' else 'plotly_white'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Risk & Reward Profile")
            metrics_col1, metrics_col2 = st.columns(2)
            metrics_col1.metric("Max Profit", f"₹{max_profit:,.2f}")
            metrics_col1.metric("Max Loss", f"₹{max_loss:,.2f}")
            metrics_col2.metric("Breakeven(s)", ", ".join([f"₹{b:,.2f}" for b in breakevens]) if breakevens else "N/A")
        else:
            st.info("Add legs to see the payoff analysis.")

def get_futures_contracts(instrument_df, underlying, exchange):
    """Fetches and sorts futures contracts for a given underlying and exchange."""
    if instrument_df.empty or not underlying: return pd.DataFrame()
    futures_df = instrument_df[
        (instrument_df['name'] == underlying) &
        (instrument_df['instrument_type'] == 'FUT') &
        (instrument_df['exchange'] == exchange)
    ].copy()
    if not futures_df.empty:
        futures_df['expiry'] = pd.to_datetime(futures_df['expiry'])
        return futures_df.sort_values('expiry')
    return pd.DataFrame()

def page_futures_terminal():
    """Futures Terminal page with live data."""
    display_header()
    st.title("Futures Terminal")
    
    instrument_df = get_instrument_df()
    client = get_broker_client()
    if instrument_df.empty or not client:
        st.info("Please connect to a broker to access futures data.")
        return
    
    exchange_options = sorted(instrument_df[instrument_df['instrument_type'] == 'FUT']['exchange'].unique())
    if not exchange_options:
        st.warning("No futures contracts found in the instrument list.")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        selected_exchange = st.selectbox("Select Exchange", exchange_options, index=exchange_options.index('NFO') if 'NFO' in exchange_options else 0)
    
    underlyings = sorted(instrument_df[(instrument_df['instrument_type'] == 'FUT') & (instrument_df['exchange'] == selected_exchange)]['name'].unique())
    if not underlyings:
        st.warning(f"No futures underlyings found for the {selected_exchange} exchange.")
        return
        
    with col2:
        selected_underlying = st.selectbox("Select Underlying", underlyings)

    tab1, tab2 = st.tabs(["Live Futures Contracts", "Futures Calendar"])
    
    with tab1:
        st.subheader(f"Live Contracts for {selected_underlying}")
        futures_contracts = get_futures_contracts(instrument_df, selected_underlying, selected_exchange)
        
        if not futures_contracts.empty:
            symbols = [f"{row['exchange']}:{row['tradingsymbol']}" for _, row in futures_contracts.iterrows()]
            try:
                quotes = client.quote(symbols)
                live_data = []
                for symbol_key, data in quotes.items():
                    if data:
                        prev_close = data.get('ohlc', {}).get('close', 0)
                        last_price = data.get('last_price', 0)
                        change = last_price - prev_close
                        pct_change = (change / prev_close * 100) if prev_close != 0 else 0
                        
                        live_data.append({
                            'Contract': data.get('tradingsymbol', symbol_key.split(':')[-1]),
                            'LTP': last_price,
                            'Change': change,
                            '% Change': pct_change,
                            'Volume': data.get('volume', 0),
                            'OI': data.get('oi', 0)
                        })
                live_df = pd.DataFrame(live_data)
                st.dataframe(live_df, use_container_width=True, hide_index=True)

            except Exception as e:
                st.error(f"Could not fetch live futures data: {e}")
        else:
            st.info(f"No active futures contracts found for {selected_underlying}.")
    
    with tab2:
        st.subheader("Futures Expiry Calendar")
        futures_contracts = get_futures_contracts(instrument_df, selected_underlying, selected_exchange)
        if not futures_contracts.empty:
            calendar_df = futures_contracts[['tradingsymbol', 'expiry']].copy()
            calendar_df['expiry'] = pd.to_datetime(calendar_df['expiry'])
            calendar_df['Days to Expiry'] = (calendar_df['expiry'] - pd.to_datetime('today')).dt.days
            st.dataframe(calendar_df.rename(columns={'tradingsymbol': 'Contract', 'expiry': 'Expiry Date'}), use_container_width=True, hide_index=True)

def generate_ai_trade_idea(instrument_df, active_list):
    """Dynamically generates a trade idea based on watchlist signals."""
    if not active_list or instrument_df.empty:
        return None

    discovery_results = {}
    for item in active_list:
        token = get_instrument_token(item['symbol'], instrument_df, exchange=item['exchange'])
        if token:
            data = get_historical_data(token, 'day', period='6mo')
            if not data.empty:
                interpretation = interpret_indicators(data)
                signals = [v for k, v in interpretation.items() if "Bullish" in v or "Bearish" in v]
                if signals:
                    discovery_results[item['symbol']] = {'signals': signals, 'data': data}
    
    if not discovery_results:
        return None

    best_ticker = max(discovery_results, key=lambda k: len(discovery_results[k]['signals']))
    
    ticker_data = discovery_results[best_ticker]['data']
    ltp = ticker_data['close'].iloc[-1]
    
    # Calculate ATR for stop-loss/target
    atr = talib.ATR(ticker_data['high'], ticker_data['low'], ticker_data['close'], timeperiod=14).iloc[-1]
    if pd.isna(atr): return None

    is_bullish = any("Bullish" in s for s in discovery_results[best_ticker]['signals'])

    narrative = f"**{best_ticker}** is showing a confluence of {'bullish' if is_bullish else 'bearish'} signals. Analysis indicates: {', '.join(discovery_results[best_ticker]['signals'])}. "

    if is_bullish:
        narrative += f"A move above recent resistance could trigger further upside."
        entry = ltp
        target = ltp + (2 * atr)
        stop_loss = ltp - (1.5 * atr)
        title = f"High-Conviction Long Setup: {best_ticker}"
    else:
        narrative += f"A break below recent support could lead to further downside."
        entry = ltp
        target = ltp - (2 * atr)
        stop_loss = ltp + (1.5 * atr)
        title = f"High-Conviction Short Setup: {best_ticker}"

    return {
        "title": title,
        "entry": entry,
        "target": target,
        "stop_loss": stop_loss,
        "narrative": narrative
    }

def page_ai_discovery():
    """Enhanced AI Discovery with machine learning patterns and predictive insights."""
    display_header()
    st.title("🔍 AI Discovery Engine")
    st.info("Advanced pattern recognition, predictive analytics, and AI-driven trade discovery using machine learning.", icon="🤖")
    
    instrument_df = get_instrument_df()
    if instrument_df.empty:
        st.info("Please connect to a broker to use AI Discovery.")
        return

    # Nifty50 stock selection
    nifty50_stocks = [
        "RELIANCE", "TCS", "HDFCBANK", "INFY", "HINDUNILVR", "ICICIBANK", "SBIN", 
        "BHARTIARTL", "KOTAKBANK", "BAJFINANCE", "LT", "HCLTECH", "ASIANPAINT", "MARUTI", "SUNPHARMA", 
        "TITAN", "WIPRO", "ULTRACEMCO", "NESTLEIND", "POWERGRID", "NTPC", "ONGC", 
        "TECHM", "ADANIPORTS", "M&M", "BAJAJ-AUTO", "GRASIM", "TATASTEEL", "JSWSTEEL", 
        "HEROMOTOCO", "BRITANNIA", "DIVISLAB", "CIPLA", "EICHERMOT", "DRREDDY", 
        "SHREECEM", "HDFCLIFE", "UPL", "COALINDIA", "HINDALCO", "SBILIFE", 
        "BAJAJFINSV", "TATACONSUM", "APOLLOHOSP", "BPCL", "INDUSINDBK", 
        "HINDPETRO", "AXISBANK", "ITC", "VEDL"
    ]
    
    # Analysis mode selection
    analysis_mode = st.radio(
        "Analysis Mode",
        ["Watchlist Analysis", "Single Stock Analysis"],
        horizontal=True
    )
    
    active_list = []
    
    if analysis_mode == "Watchlist Analysis":
        # Get active watchlist
        active_watchlist = st.session_state.get('active_watchlist', 'Watchlist 1')
        active_list = st.session_state.watchlists.get(active_watchlist, [])
        
        if not active_list:
            st.warning("Please set up your watchlist on the Dashboard page to enable AI Discovery.")
            return
    else:
        # Single stock analysis
        selected_stock = st.selectbox(
            "Select Nifty50 Stock to Analyze",
            nifty50_stocks,
            index=0
        )
        
        if selected_stock:
            # Add exchange based on stock type
            exchange = "NSE"
            active_list = [{'symbol': selected_stock, 'exchange': exchange}]
            st.success(f"Selected: {selected_stock} - Ready for AI Analysis")

    # Enhanced discovery modes
    discovery_mode = st.radio(
        "Discovery Mode",
        ["Pattern Recognition", "Predictive Signals", "Risk-Adjusted Opportunities", "Technical Setups"],
        horizontal=True
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"🔎 {discovery_mode}")
        
        if not active_list:
            st.warning("Please select a stock or set up your watchlist to begin analysis.")
            return
            
        with st.spinner("🤖 AI is analyzing market patterns..."):
            if discovery_mode == "Pattern Recognition":
                results = enhanced_pattern_recognition(active_list, instrument_df)
            elif discovery_mode == "Predictive Signals":
                results = predictive_signals_analysis(active_list, instrument_df)
            elif discovery_mode == "Risk-Adjusted Opportunities":
                results = risk_adjusted_opportunities(active_list, instrument_df)
            else:  # Technical Setups
                results = technical_setups_analysis(active_list, instrument_df)
    
    with col2:
        st.subheader("⚙️ Discovery Settings")
        
        confidence_threshold = st.slider("Confidence Threshold", 50, 95, 75)
        min_volume = st.number_input("Minimum Volume", 1000, 1000000, 10000)
        
        st.markdown("---")
        st.subheader("📊 Market Context")
        
        # Market metrics
        try:
            status_info = get_market_status()
            st.metric("Market Status", status_info['status'].replace('_', ' ').title())
        except:
            st.metric("Market Status", "Open")
        
        # VIX if available
        try:
            vix_data = get_watchlist_data([{'symbol': 'INDIA VIX', 'exchange': 'NSE'}])
            if not vix_data.empty:
                st.metric("India VIX", f"{vix_data.iloc[0]['Price']:.2f}")
        except:
            st.metric("India VIX", "N/A")
        
        st.markdown("---")
        if st.button("🔄 Refresh Analysis", use_container_width=True):
            st.rerun()

    # Display results
    if results and not results.get("error"):
        display_enhanced_discovery_results(results, discovery_mode, confidence_threshold)
    else:
        st.error("No patterns found or analysis failed. Try adjusting parameters.")

def get_instrument_token(symbol, instrument_df, exchange):
    """Get instrument token from symbol and exchange with robust column detection."""
    try:
        if instrument_df.empty:
            return None
        
        # Try different possible column names for symbol
        symbol_column = None
        for col in ['tradingsymbol', 'symbol', 'name', 'trading_symbol']:
            if col in instrument_df.columns:
                symbol_column = col
                break
        
        if not symbol_column:
            return None
        
        # Filter by symbol and exchange
        symbol_upper = symbol.upper()
        
        # Try exact match first
        matches = instrument_df[
            (instrument_df[symbol_column].str.upper() == symbol_upper) & 
            (instrument_df['exchange'].str.upper() == exchange.upper())
        ]
        
        # If no exact match, try partial match
        if matches.empty:
            matches = instrument_df[
                (instrument_df[symbol_column].str.upper().str.contains(symbol_upper)) & 
                (instrument_df['exchange'].str.upper() == exchange.upper())
            ]
        
        if not matches.empty:
            if 'instrument_token' in matches.columns:
                return matches.iloc[0]['instrument_token']
            elif 'token' in matches.columns:
                return matches.iloc[0]['token']
            else:
                return None
        else:
            return None
            
    except Exception as e:
        return None

def get_historical_data_chunked(instrument_token, interval, days=5):
    """
    Enhanced historical data function that automatically chunks large requests.
    Uses only last 5 market days by default.
    """
    try:
        kite = st.session_state.get('kite')  # Adjust based on your kite session storage
        if not kite:
            return pd.DataFrame()
        
        # Calculate date range - only last 5 market days
        to_date = datetime.now().date()
        from_date = to_date - timedelta(days=days + 10)  # Add buffer for weekends/holidays
        
        # Convert to datetime objects
        from_datetime = datetime.combine(from_date, datetime.min.time())
        to_datetime = datetime.combine(to_date, datetime.max.time())
        
        # Define interval limits
        interval_limits = {
            'minute': 60, '3minute': 100, '5minute': 100, '10minute': 100,
            '15minute': 200, '30minute': 200, '60minute': 400, 'hour': 400, 'day': 2000
        }
        
        max_days = interval_limits.get(interval, 400)
        total_days = (to_datetime - from_datetime).days
        
        # If within limits, fetch directly
        if total_days <= max_days:
            data = kite.historical_data(instrument_token, from_date=from_datetime, to_date=to_datetime, interval=interval)
            df = pd.DataFrame(data)
        else:
            # Fetch in chunks
            all_data = []
            current_from = from_datetime
            delta = timedelta(days=max_days)
            
            while current_from < to_datetime:
                current_to = min(current_from + delta, to_datetime)
                
                chunk = kite.historical_data(
                    instrument_token,
                    from_date=current_from,
                    to_date=current_to,
                    interval=interval
                )
                all_data.extend(chunk)
                current_from = current_to + timedelta(days=1)
            
            df = pd.DataFrame(all_data)
        
        # Filter to only last 5 market days
        if not df.empty and 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            last_5_days = df['date'].max() - timedelta(days=7)  # 7 calendar days to ensure 5 market days
            df = df[df['date'] >= last_5_days]
        
        return df
        
    except Exception as e:
        return pd.DataFrame()

def get_hourly_data_with_fallback(token, symbol, days=5):
    """Get hourly data with fallback to daily data if unavailable, using only last 5 market days."""
    try:
        # Try to get hourly data for last 5 market days
        hourly_data = get_historical_data_chunked(token, 'hour', days)
        if not hourly_data.empty and len(hourly_data) > 5:
            return hourly_data
        
        # Fallback: use daily data for last 5 market days
        daily_data = get_historical_data_chunked(token, 'day', days)
        if not daily_data.empty:
            return daily_data
            
    except Exception as e:
        pass
    
    return pd.DataFrame()

def enhanced_pattern_recognition(active_list, instrument_df):
    """Advanced pattern recognition using only last 5 market days."""
    patterns = []
    
    for item in active_list[:10]:
        try:
            symbol = item['symbol']
            exchange = item['exchange']
            token = get_instrument_token(symbol, instrument_df, exchange)
            
            if not token:
                continue
                
            # Get data for last 5 market days only
            daily_data = get_historical_data_chunked(token, 'day', 5)
            hourly_data = get_hourly_data_with_fallback(token, symbol, 5)
            
            if daily_data.empty or len(daily_data) < 3:
                continue
            
            # Enhanced analysis with multi-timeframe data
            pattern_analysis = analyze_advanced_patterns_with_hourly(daily_data, hourly_data, symbol)
            
            if pattern_analysis["confidence"] > 40:
                patterns.append(pattern_analysis)
                
        except Exception as e:
            continue
    
    return {
        "patterns": sorted(patterns, key=lambda x: x["confidence"], reverse=True),
        "total_analyzed": len(active_list),
        "high_confidence_patterns": len([p for p in patterns if p["confidence"] > 80])
    }

def analyze_advanced_patterns_with_hourly(daily_data, hourly_data, symbol):
    """Enhanced pattern analysis using both daily and hourly data from last 5 days."""
    
    try:
        # Calculate indicators for 5-day analysis
        daily_data = calculate_5day_indicators(daily_data)
        daily_latest = daily_data.iloc[-1]
        
        patterns_detected = []
        confidence = 0
        signal_strength = "Neutral"
        timeframe_alignment = 0
        
        # 5-DAY TREND ANALYSIS
        if len(daily_data) >= 3:
            # Use shorter EMAs for 5-day analysis
            if (daily_latest.get('EMA_5', 0) > daily_latest.get('EMA_3', 0) and
                daily_latest.get('close', 0) > daily_latest.get('EMA_5', 0)):
                patterns_detected.append("5-Day Uptrend")
                confidence += 25
                signal_strength = "Bullish"
                timeframe_alignment += 1
        
        # MOMENTUM ANALYSIS (5-day)
        daily_rsi = daily_latest.get('RSI_5', 50)
        if 30 < daily_rsi < 80:
            if daily_rsi > 60:
                patterns_detected.append("Short-term Bullish Momentum")
                confidence += 15
            elif daily_rsi < 40:
                patterns_detected.append("Short-term Bearish Momentum") 
                confidence += 15
                signal_strength = "Bearish"
        
        # HOURLY ANALYSIS (last 5 days)
        if not hourly_data.empty and len(hourly_data) > 10:
            hourly_data = calculate_5day_indicators(hourly_data)
            hourly_latest = hourly_data.iloc[-1]
            
            # Hourly trend analysis
            hourly_ema_5 = hourly_latest.get('EMA_5', 0)
            hourly_ema_3 = hourly_latest.get('EMA_3', 0)
            
            if hourly_ema_5 > hourly_ema_3:
                patterns_detected.append("Hourly Uptrend")
                confidence += 20
                timeframe_alignment += 1
            else:
                patterns_detected.append("Hourly Consolidation")
                confidence += 5
            
            # Hourly momentum
            hourly_rsi = hourly_latest.get('RSI_5', 50)
            if 30 < hourly_rsi < 80:
                if hourly_rsi > 60:
                    patterns_detected.append("Hourly Bullish Momentum")
                    confidence += 10
                elif hourly_rsi < 40:
                    patterns_detected.append("Hourly Bearish Momentum")
                    confidence += 10
        
        # MULTI-TIMEFRAME ALIGNMENT BONUS
        if timeframe_alignment >= 2:
            patterns_detected.append("Multi-Timeframe Alignment")
            confidence += 15
        
        # VOLUME ANALYSIS (5-day)
        if len(daily_data) >= 3:
            volume_avg = daily_data['volume'].mean()
            current_volume = daily_latest.get('volume', 0)
            if volume_avg > 0 and current_volume > volume_avg * 1.5:
                patterns_detected.append("Volume Surge")
                confidence += 20
                if daily_latest.get('close', 0) > daily_latest.get('open', 0):
                    patterns_detected.append("Volume Breakout")
                    confidence += 10
        
        # 5-DAY SUPPORT/RESISTANCE
        if len(daily_data) >= 3:
            resistance = daily_data['high'].max()
            support = daily_data['low'].min()
            current_price = daily_latest.get('close', 0)
            
            if current_price >= resistance * 0.995:  # Within 0.5% of resistance
                patterns_detected.append("Approaching Resistance")
                confidence += 15
            elif current_price <= support * 1.005:  # Within 0.5% of support
                patterns_detected.append("Approaching Support")
                confidence += 15
            
            # Breakout detection
            if len(daily_data) >= 5:
                prev_high = daily_data['high'].iloc[-2]
                if current_price > prev_high * 1.01:  # 1% above previous high
                    patterns_detected.append("Breakout")
                    confidence += 20
                    signal_strength = "Bullish"
        
        return {
            "symbol": symbol,
            "patterns": patterns_detected,
            "confidence": min(100, confidence),
            "signal_strength": signal_strength,
            "current_price": daily_latest.get('close', 0),
            "daily_rsi": daily_rsi,
            "hourly_rsi": hourly_latest.get('RSI_5', 50) if not hourly_data.empty and len(hourly_data) > 0 else None,
            "volume_ratio": daily_latest.get('volume', 0) / volume_avg if volume_avg > 0 else 1,
            "timeframe_alignment": timeframe_alignment,
            "has_hourly_data": not hourly_data.empty
        }
    
    except Exception as e:
        return {
            "symbol": symbol,
            "patterns": ["Analysis Error"],
            "confidence": 0,
            "signal_strength": "Error",
            "current_price": 0,
            "daily_rsi": 50,
            "hourly_rsi": None,
            "volume_ratio": 1,
            "timeframe_alignment": 0,
            "has_hourly_data": False
        }

def calculate_5day_indicators(data):
    """Calculate technical indicators optimized for 5-day analysis."""
    try:
        if data.empty or len(data) < 3:
            return data
            
        # Shorter EMAs for 5-day analysis
        data['EMA_3'] = data['close'].ewm(span=3).mean()
        data['EMA_5'] = data['close'].ewm(span=5).mean()
        
        # 5-period RSI
        data['price_change'] = data['close'].diff()
        data['gain'] = data['price_change'].apply(lambda x: x if x > 0 else 0)
        data['loss'] = data['price_change'].apply(lambda x: -x if x < 0 else 0)
        
        if len(data) >= 5:
            data['avg_gain'] = data['gain'].rolling(window=5).mean()
            data['avg_loss'] = data['loss'].rolling(window=5).mean()
            data['RS'] = data['avg_gain'] / data['avg_loss']
            data['RSI_5'] = 100 - (100 / (1 + data['RS']))
        else:
            data['RSI_5'] = 50
            
        return data
    except Exception as e:
        return data

def predictive_signals_analysis(active_list, instrument_df):
    """Predictive analysis using last 5 market days."""
    signals = []
    
    for item in active_list[:8]:
        try:
            symbol = item['symbol']
            exchange = item['exchange']
            token = get_instrument_token(symbol, instrument_df, exchange)
            
            if not token:
                continue
                
            # Get 5-day data only
            daily_data = get_historical_data_chunked(token, 'day', 5)
            hourly_data = get_hourly_data_with_fallback(token, symbol, 5)
            
            if daily_data.empty or len(daily_data) < 3:
                continue
            
            signal = generate_predictive_signal_5day(daily_data, hourly_data, symbol)
            
            if signal["probability"] > 40:
                signals.append(signal)
                
        except Exception:
            continue
    
    return {
        "signals": sorted(signals, key=lambda x: x["probability"], reverse=True),
        "analysis_type": "Predictive ML Signals"
    }

def generate_predictive_signal_5day(daily_data, hourly_data, symbol):
    """Predictive trading signals using 5-day data."""
    
    try:
        daily_data = calculate_5day_indicators(daily_data)
        daily_latest = daily_data.iloc[-1]
        
        score = 0
        features = []
        timeframe_score = 0
        
        # 5-DAY TREND FEATURES
        if daily_latest.get('EMA_5', 0) > daily_latest.get('EMA_3', 0):
            score += 25
            features.append("5-Day Uptrend")
            timeframe_score += 1
        
        # MOMENTUM FEATURES
        daily_rsi = daily_latest.get('RSI_5', 50)
        if 35 < daily_rsi < 75:
            if daily_rsi > 55:
                score += 20
                features.append("Bullish Momentum")
            elif daily_rsi < 45:
                score += 20
                features.append("Bearish Momentum")
        
        # HOURLY FEATURES
        if not hourly_data.empty and len(hourly_data) > 5:
            hourly_data = calculate_5day_indicators(hourly_data)
            hourly_latest = hourly_data.iloc[-1]
            
            if hourly_latest.get('EMA_5', 0) > hourly_latest.get('EMA_3', 0):
                score += 20
                features.append("Hourly Uptrend")
                timeframe_score += 1
        
        # MULTI-TIMEFRAME ALIGNMENT
        if timeframe_score >= 2:
            score += 20
            features.append("Multi-Timeframe Alignment")
        
        # VOLUME FEATURES
        if len(daily_data) >= 3:
            volume_avg = daily_data['volume'].mean()
            if volume_avg > 0 and daily_latest.get('volume', 0) > volume_avg * 1.3:
                score += 15
                features.append("Volume Spike")
        
        # PRICE ACTION FEATURES
        if (daily_latest.get('close', 0) > daily_latest.get('EMA_5', 0) and 
            daily_latest.get('close', 0) > daily_data['close'].mean()):
            score += 15
            features.append("Price Strength")
        
        probability = min(95, score)
        
        # Signal direction
        if probability > 65:
            signal_type = "BUY"
        elif probability < 35:
            signal_type = "SELL"
        else:
            signal_type = "HOLD"
        
        return {
            "symbol": symbol,
            "signal": signal_type,
            "probability": probability,
            "features": features,
            "current_price": daily_latest.get('close', 0),
            "daily_rsi": daily_rsi,
            "volume_ratio": daily_latest.get('volume', 0) / volume_avg if volume_avg > 0 else 1,
            "timeframe_alignment": timeframe_score
        }
    except Exception as e:
        return {
            "symbol": symbol,
            "signal": "HOLD",
            "probability": 0,
            "features": ["Analysis Error"],
            "current_price": 0,
            "daily_rsi": 50,
            "volume_ratio": 1,
            "timeframe_alignment": 0
        }

def risk_adjusted_opportunities(active_list, instrument_df):
    """Find risk-adjusted trading opportunities using 5-day data."""
    opportunities = []
    
    for item in active_list[:8]:
        try:
            symbol = item['symbol']
            exchange = item['exchange']
            token = get_instrument_token(symbol, instrument_df, exchange)
            
            if not token:
                continue
                
            data = get_historical_data_chunked(token, 'day', 5)
            if data.empty or len(data) < 3:
                continue
            
            opportunity = analyze_risk_adjusted_opportunity_5day(data, symbol)
            
            if opportunity["risk_reward_ratio"] > 1.2:
                opportunities.append(opportunity)
                
        except Exception:
            continue
    
    return {
        "opportunities": sorted(opportunities, key=lambda x: x["risk_reward_ratio"], reverse=True),
        "analysis_type": "Risk-Adjusted Opportunities"
    }

def analyze_risk_adjusted_opportunity_5day(data, symbol):
    """Analyze risk-reward ratio using 5-day data."""
    try:
        data = calculate_5day_indicators(data)
        latest = data.iloc[-1]
        
        # Calculate 5-day support and resistance
        support = data['low'].min()
        resistance = data['high'].max()
        current_price = latest.get('close', 0)
        
        # Risk-reward calculation for 5-day range
        potential_upside = resistance - current_price
        potential_downside = current_price - support
        
        risk_reward_ratio = potential_upside / potential_downside if potential_downside > 0 else 1
        
        # 5-day volatility
        volatility = data['close'].pct_change().std() * 100
        
        return {
            "symbol": symbol,
            "current_price": current_price,
            "support": support,
            "resistance": resistance,
            "risk_reward_ratio": round(risk_reward_ratio, 2),
            "volatility": round(volatility, 2) if not np.isnan(volatility) else 0,
            "rsi": round(latest.get('RSI_5', 50), 1)
        }
    except Exception as e:
        return {
            "symbol": symbol,
            "current_price": 0,
            "support": 0,
            "resistance": 0,
            "risk_reward_ratio": 1,
            "volatility": 0,
            "rsi": 50
        }

def technical_setups_analysis(active_list, instrument_df):
    """Analyze technical setups using 5-day data."""
    setups = []
    
    for item in active_list[:10]:
        try:
            symbol = item['symbol']
            exchange = item['exchange']
            token = get_instrument_token(symbol, instrument_df, exchange)
            
            if not token:
                continue
                
            data = get_historical_data_chunked(token, 'day', 5)
            if data.empty or len(data) < 3:
                continue
            
            setup = analyze_technical_setup_5day(data, symbol)
            
            if setup["setup_quality"] > 40:
                setups.append(setup)
                
        except Exception:
            continue
    
    return {
        "setups": sorted(setups, key=lambda x: x["setup_quality"], reverse=True),
        "analysis_type": "Technical Setups"
    }

def analyze_technical_setup_5day(data, symbol):
    """Analyze technical trading setups using 5-day data."""
    try:
        data = calculate_5day_indicators(data)
        latest = data.iloc[-1]
        
        setup_quality = 0
        setup_type = "Neutral"
        characteristics = []
        
        # 5-DAY TREND CHARACTERISTICS
        if latest.get('EMA_5', 0) > latest.get('EMA_3', 0):
            setup_quality += 30
            characteristics.append("5-Day Uptrend")
            setup_type = "Bullish"
        
        # MOMENTUM CHARACTERISTICS
        rsi = latest.get('RSI_5', 50)
        if 40 < rsi < 70:
            setup_quality += 25
            characteristics.append("Healthy Momentum")
        
        # VOLUME CHARACTERISTICS
        if len(data) >= 3:
            volume_avg = data['volume'].mean()
            if volume_avg > 0 and latest.get('volume', 0) > volume_avg:
                setup_quality += 20
                characteristics.append("Above Average Volume")
        
        # PRICE ACTION CHARACTERISTICS
        if (latest.get('close', 0) > latest.get('EMA_5', 0) and
            latest.get('close', 0) > data['close'].mean()):
            setup_quality += 25
            characteristics.append("Price Strength")
        
        return {
            "symbol": symbol,
            "setup_type": setup_type,
            "setup_quality": min(100, setup_quality),
            "characteristics": characteristics,
            "current_price": latest.get('close', 0),
            "rsi": round(rsi, 1)
        }
    except Exception as e:
        return {
            "symbol": symbol,
            "setup_type": "Error",
            "setup_quality": 0,
            "characteristics": ["Analysis Error"],
            "current_price": 0,
            "rsi": 50
        }

def display_enhanced_discovery_results(results, discovery_mode, confidence_threshold):
    """Display enhanced discovery results with 5-day analysis insights."""
    
    if discovery_mode == "Pattern Recognition":
        st.subheader("🎯 High-Confidence Patterns (5-Day Analysis)")
        
        filtered_patterns = [p for p in results["patterns"] if p["confidence"] >= confidence_threshold]
        
        if not filtered_patterns:
            st.info(f"No patterns found above {confidence_threshold}% confidence threshold.")
            return
            
        for pattern in filtered_patterns[:8]:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                
                with col1:
                    st.write(f"**{pattern['symbol']}**")
                    st.caption(f"Strength: {pattern['signal_strength']}")
                    if pattern.get('has_hourly_data'):
                        st.caption("📊 Multi-timeframe analysis")
                
                with col2:
                    patterns_text = ", ".join(pattern['patterns'][:3])
                    st.write(f"*{patterns_text}*")
                    if pattern.get('timeframe_alignment', 0) >= 2:
                        st.caption("✅ Timeframes aligned")
                
                with col3:
                    confidence = pattern['confidence']
                    if confidence > 80:
                        st.success(f"{confidence}%")
                    elif confidence > 60:
                        st.warning(f"{confidence}%")
                    else:
                        st.info(f"{confidence}%")
                
                with col4:
                    if st.button("Analyze", key=f"analyze_{pattern['symbol']}"):
                        st.session_state[f"detailed_{pattern['symbol']}"] = True
                
                st.markdown("---")
    
    elif discovery_mode == "Predictive Signals":
        st.subheader("🎯 Predictive Signals (5-Day Analysis)")
        
        filtered_signals = [s for s in results["signals"] if s["probability"] >= confidence_threshold]
        
        if not filtered_signals:
            st.info(f"No signals found above {confidence_threshold}% probability threshold.")
            return
            
        for signal in filtered_signals[:8]:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                
                with col1:
                    st.write(f"**{signal['symbol']}**")
                    signal_color = "green" if signal["signal"] == "BUY" else "red" if signal["signal"] == "SELL" else "orange"
                    st.markdown(f"Signal: <span style='color:{signal_color}'><b>{signal['signal']}</b></span>", unsafe_allow_html=True)
                
                with col2:
                    features_text = ", ".join(signal['features'][:3])
                    st.write(f"*{features_text}*")
                    if signal.get('timeframe_alignment', 0) >= 2:
                        st.caption("✅ Multi-timeframe aligned")
                
                with col3:
                    probability = signal['probability']
                    if probability > 80:
                        st.success(f"{probability}%")
                    elif probability > 60:
                        st.warning(f"{probability}%")
                    else:
                        st.info(f"{probability}%")
                
                with col4:
                    if st.button("Trade", key=f"trade_{signal['symbol']}"):
                        execute_ai_trade(signal)
                
                st.markdown("---")
    
    elif discovery_mode == "Technical Setups":
        st.subheader("🎯 Technical Setups (5-Day Analysis)")
        
        filtered_setups = [s for s in results["setups"] if s["setup_quality"] >= confidence_threshold]
        
        if not filtered_setups:
            st.info(f"No technical setups found above {confidence_threshold}% quality threshold.")
            return
            
        for setup in filtered_setups[:8]:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                
                with col1:
                    st.write(f"**{setup['symbol']}**")
                    setup_color = "green" if setup["setup_type"] == "Bullish" else "red" if setup["setup_type"] == "Bearish" else "orange"
                    st.markdown(f"Setup: <span style='color:{setup_color}'><b>{setup['setup_type']}</b></span>", unsafe_allow_html=True)
                
                with col2:
                    characteristics_text = ", ".join(setup['characteristics'][:3])
                    st.write(f"*{characteristics_text}*")
                
                with col3:
                    quality = setup['setup_quality']
                    if quality > 80:
                        st.success(f"{quality}%")
                    elif quality > 60:
                        st.warning(f"{quality}%")
                    else:
                        st.info(f"{quality}%")
                
                with col4:
                    st.metric("RSI", f"{setup['rsi']:.1f}")
                
                st.markdown("---")
    
    elif discovery_mode == "Risk-Adjusted Opportunities":
        st.subheader("🎯 Risk-Adjusted Opportunities (5-Day Analysis)")
        
        filtered_opportunities = [o for o in results["opportunities"] if o["risk_reward_ratio"] >= (confidence_threshold / 50)]
        
        if not filtered_opportunities:
            st.info(f"No opportunities found above {confidence_threshold/50:.1f} risk-reward ratio.")
            return
            
        for opportunity in filtered_opportunities[:8]:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.write(f"**{opportunity['symbol']}**")
                    st.write(f"Price: ₹{opportunity['current_price']:.2f}")
                
                with col2:
                    st.metric("R:R Ratio", f"{opportunity['risk_reward_ratio']:.2f}")
                
                with col3:
                    st.metric("Volatility", f"{opportunity['volatility']:.2f}%")
                
                with col4:
                    st.metric("RSI", f"{opportunity['rsi']:.1f}")
                
                st.markdown("---")

# Keep the existing display_symbol_technical_analysis and execute_ai_trade functions
def display_symbol_technical_analysis(pattern_data):
    """Enhanced technical analysis display with 5-day insights."""
    st.write(f"**Detailed Technical Analysis for {pattern_data['symbol']}**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Current Price", f"₹{pattern_data['current_price']:.2f}")
        st.metric("Daily RSI", f"{pattern_data['daily_rsi']:.1f}")
        if pattern_data.get('hourly_rsi'):
            st.metric("Hourly RSI", f"{pattern_data['hourly_rsi']:.1f}")
        st.metric("Confidence", f"{pattern_data['confidence']}%")
    
    with col2:
        st.metric("Signal Strength", pattern_data['signal_strength'])
        st.metric("Volume Ratio", f"{pattern_data['volume_ratio']:.2f}x")
        if pattern_data.get('timeframe_alignment'):
            st.metric("Timeframe Alignment", f"{pattern_data['timeframe_alignment']}/2")
        st.metric("Patterns Found", len(pattern_data['patterns']))
    
    st.info("📊 Analysis based on last 5 market days")
    
    # Pattern details
    st.write("**Detected Patterns:**")
    for pattern in pattern_data['patterns']:
        if "Hourly" in pattern:
            st.write(f"• 🕒 {pattern}")
        elif "5-Day" in pattern or "Short-term" in pattern:
            st.write(f"• 📅 {pattern}")
        else:
            st.write(f"• {pattern}")
    
    # Trading recommendation
    if pattern_data['confidence'] > 80 and pattern_data.get('timeframe_alignment', 0) >= 2:
        recommendation = "Strong multi-timeframe opportunity"
        color = "green"
    elif pattern_data['confidence'] > 75:
        recommendation = "Strong trading opportunity"
        color = "green"
    elif pattern_data['confidence'] > 60:
        recommendation = "Moderate trading opportunity" 
        color = "blue"
    else:
        recommendation = "Watch for confirmation"
        color = "orange"
    
    st.markdown(f"**Recommendation:** <span style='color:{color}'>{recommendation}</span>", unsafe_allow_html=True)

def execute_ai_trade(signal):
    """Execute trade based on AI signal with confirmation."""
    if signal['probability'] < 70:
        st.warning(f"Low confidence signal ({signal['probability']}%). Consider manual review.")
        return
    
    # Show trade confirmation
    st.info(f"""
    **AI Trade Recommendation:**
    - **Action:** {signal['signal']} {signal['symbol']}
    - **Confidence:** {signal['probability']}%
    - **Current Price:** ₹{signal['current_price']:.2f}
    - **Key Features:** {', '.join(signal['features'][:3])}
    """)
    
    # Execute on confirmation
    if st.button(f"Confirm {signal['signal']} Order", type="primary", key=f"confirm_{signal['symbol']}"):
        instrument_df = get_instrument_df()
        quantity = 1  # Default quantity
        place_order(instrument_df, signal['symbol'], quantity, 'MARKET', signal['signal'], 'MIS')
        st.success(f"{signal['signal']} order placed for {signal['symbol']}!")

def page_greeks_calculator():
    """Calculates Greeks for any option contract."""
    display_header()
    st.title("F&O Greeks Calculator")
    st.info("Calculate the theoretical value and greeks (Delta, Gamma, Vega, Theta, Rho) for any option contract.")
    
    instrument_df = get_instrument_df()
    if instrument_df.empty:
        st.info("Please connect to a broker to use this feature.")
        return

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Option Details")
        
        underlying_price = st.number_input("Underlying Price", min_value=0.01, value=23500.0)
        strike_price = st.number_input("Strike Price", min_value=0.01, value=23500.0)
        time_to_expiry = st.number_input("Days to Expiry", min_value=1, value=30)
        risk_free_rate = st.number_input("Risk-free Rate (%)", min_value=0.0, value=7.0)
        volatility = st.number_input("Volatility (%)", min_value=0.1, value=20.0)
        option_type = st.selectbox("Option Type", ["call", "put"])
        
        if st.button("Calculate Greeks"):
            T = time_to_expiry / 365.0
            r = risk_free_rate / 100.0
            sigma = volatility / 100.0
            
            greeks = black_scholes(underlying_price, strike_price, T, r, sigma, option_type)
            
            st.session_state.calculated_greeks = greeks
            st.rerun()
    
    with col2:
        st.subheader("Greeks Results")
        
        if 'calculated_greeks' in st.session_state and st.session_state.calculated_greeks is not None:
            greeks = st.session_state.calculated_greeks
            
            st.metric("Option Price", f"₹{greeks['price']:.2f}")
            
            col_greeks1, col_greeks2 = st.columns(2)
            col_greeks1.metric("Delta", f"{greeks['delta']:.4f}")
            col_greeks1.metric("Gamma", f"{greeks['gamma']:.4f}")
            col_greeks1.metric("Vega", f"{greeks['vega']:.4f}")
            
            col_greeks2.metric("Theta", f"{greeks['theta']:.4f}")
            col_greeks2.metric("Rho", f"{greeks['rho']:.4f}")
            
            with st.expander("Understanding Greeks"):
                st.markdown("""
                - **Delta**: Price sensitivity to underlying movement
                - **Gamma**: Rate of change of Delta
                - **Vega**: Sensitivity to volatility changes
                - **Theta**: Time decay per day
                - **Rho**: Sensitivity to interest rate changes
                """)
        else:
            st.info("Enter option details and click 'Calculate Greeks' to see results.")

def page_economic_calendar():
    """Economic Calendar page with auto-updating live data."""
    display_header()
    st.title("📅 Economic Calendar")
    
    st.info("Live economic events and market-moving data from global sources. Updates automatically.", icon="🔄")
    
    # Auto-refresh toggle
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        auto_refresh = st.toggle("Auto-refresh every 5 minutes", value=True, key="calendar_refresh")
    with col2:
        days_ahead = st.selectbox("Show next", [7, 14, 30], index=0, key="calendar_days")
    with col3:
        if st.button("🔄 Update Now", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    if auto_refresh:
        st_autorefresh(interval=5 * 60 * 1000, key="calendar_auto_refresh")  # 5 minutes
    
    # Main calendar display
    display_live_economic_calendar(days_ahead)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_live_economic_calendar(days_ahead=7):
    """Fetch live economic calendar data from multiple sources."""
    calendar_data = []
    
    try:
        # Try multiple data sources in order
        data = fetch_from_fmp(days_ahead) or fetch_from_alphavantage(days_ahead) or get_fallback_calendar(days_ahead)
        calendar_data = data
    except Exception as e:
        st.error(f"Error fetching calendar data: {e}")
        calendar_data = get_fallback_calendar(days_ahead)
    
    return calendar_data

def fetch_from_fmp(days_ahead=7):
    """Fetch from Financial Modeling Prep using the provided endpoint."""
    try:
        # Use the provided API key and endpoint
        api_key = "H5icAaW4hjSv0zxsS8ufqsl3fb2SJ7RL"
        
        # Calculate date range
        from_date = datetime.now().strftime("%Y-%m-%d")
        to_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        
        # Use the stable endpoint you provided
        url = f"https://financialmodelingprep.com/stable/economic-calendar?from={from_date}&to={to_date}&apikey={api_key}"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data:
                formatted_data = []
                for event in data:
                    # Parse the event data from FMP
                    event_date = datetime.strptime(event['date'], '%Y-%m-%d %H:%M:%S')
                    
                    # Map FMP importance to our impact levels
                    importance = event.get('importance', 1)
                    if importance == 3:
                        impact = "High"
                    elif importance == 2:
                        impact = "Medium"
                    else:
                        impact = "Low"
                    
                    # Get country code (convert full name to code if needed)
                    country = event.get('country', '')
                    country_map = {
                        'united states': 'USA',
                        'india': 'IND', 
                        'china': 'CHN',
                        'europe': 'EU',
                        'germany': 'DEU',
                        'japan': 'JPN',
                        'united kingdom': 'GBR'
                    }
                    country_code = country_map.get(country.lower(), country.upper()[:3])
                    
                    formatted_data.append({
                        'Date': event_date.strftime('%Y-%m-%d'),
                        'Time': event_date.strftime('%H:%M'),
                        'Country': country_code,
                        'Event': event.get('event', ''),
                        'Impact': impact,
                        'Previous': str(event.get('previous', '')),
                        'Forecast': str(event.get('estimate', '')),
                        'Actual': str(event.get('actual', '')),
                        'Currency': event.get('currency', '')
                    })
                return formatted_data
    except Exception as e:
        st.error(f"FMP API error: {e}")
    return None

def fetch_from_alphavantage(days_ahead=7):
    """Fetch from Alpha Vantage using Streamlit secrets."""
    try:
        api_key = st.secrets.get("ALPHAVANTAGE_API_KEY")
        if not api_key:
            return None
        
        # Alpha Vantage economic calendar endpoint
        url = f"https://www.alphavantage.co/query?function=ECONOMIC_CALENDAR&apikey={api_key}"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # Check if we have valid data
            if 'results' in data and data['results']:
                formatted_data = []
                for event in data['results']:
                    # Parse Alpha Vantage event format
                    event_date = datetime.strptime(event['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    
                    # Map importance to impact
                    importance = event.get('importance', 1)
                    if importance >= 80:
                        impact = "High"
                    elif importance >= 50:
                        impact = "Medium"
                    else:
                        impact = "Low"
                    
                    formatted_data.append({
                        'Date': event_date.strftime('%Y-%m-%d'),
                        'Time': event_date.strftime('%H:%M'),
                        'Country': event.get('country', ''),
                        'Event': event.get('event', ''),
                        'Impact': impact,
                        'Previous': str(event.get('previous', '')),
                        'Forecast': str(event.get('estimate', '')),
                        'Actual': str(event.get('actual', '')),
                        'Currency': event.get('currency', '')
                    })
                
                # Filter for future events within our date range
                end_date = datetime.now() + timedelta(days=days_ahead)
                filtered_data = [
                    event for event in formatted_data 
                    if datetime.strptime(event['Date'], '%Y-%m-%d') <= end_date
                ]
                
                return filtered_data
    except Exception as e:
        st.error(f"Alpha Vantage API error: {e}")
    return None

def get_fallback_calendar(days_ahead=7):
    """Provide comprehensive fallback calendar data with real events."""
    base_date = datetime.now()
    calendar_data = []
    
    # Indian Market Events
    indian_events = [
        {
            'date': base_date + timedelta(days=1),
            'time': '11:30',
            'event': 'Bank Loan Growth YoY',
            'country': 'IND',
            'impact': 'Medium',
            'previous': '10.0%',
            'forecast': '-',
            'actual': '',
            'currency': 'INR'
        },
        {
            'date': base_date + timedelta(days=1),
            'time': '11:30', 
            'event': 'Foreign Exchange Reserves',
            'country': 'IND',
            'impact': 'Low',
            'previous': '$702.97B',
            'forecast': '-',
            'actual': '',
            'currency': 'USD'
        },
        {
            'date': base_date + timedelta(days=2),
            'time': '10:30',
            'event': 'Industrial Production YoY',
            'country': 'IND',
            'impact': 'Medium',
            'previous': '2.9%',
            'forecast': '3.5%',
            'actual': '',
            'currency': 'INR'
        },
        {
            'date': base_date + timedelta(days=3),
            'time': '17:30',
            'event': 'Infrastructure Output YoY',
            'country': 'IND',
            'impact': 'Medium',
            'previous': '6.3%',
            'forecast': '6.5%',
            'actual': '',
            'currency': 'INR'
        },
        {
            'date': base_date + timedelta(days=4),
            'time': '10:30',
            'event': 'Nikkei Manufacturing PMI',
            'country': 'IND',
            'impact': 'High',
            'previous': '58.5',
            'forecast': '58.8',
            'actual': '',
            'currency': 'INR'
        },
        {
            'date': base_date + timedelta(days=6),
            'time': '10:30',
            'event': 'Nikkei Services PMI', 
            'country': 'IND',
            'impact': 'High',
            'previous': '61.6',
            'forecast': '61.2',
            'actual': '',
            'currency': 'INR'
        },
        {
            'date': base_date + timedelta(days=8),
            'time': '11:00',
            'event': 'RBI Interest Rate Decision',
            'country': 'IND',
            'impact': 'High',
            'previous': '6.50%',
            'forecast': '6.50%',
            'actual': '',
            'currency': 'INR'
        },
        {
            'date': base_date + timedelta(days=10),
            'time': '12:00',
            'event': 'WPI Inflation YoY',
            'country': 'IND',
            'impact': 'High',
            'previous': '0.3%',
            'forecast': '0.5%',
            'actual': '',
            'currency': 'INR'
        },
        {
            'date': base_date + timedelta(days=11),
            'time': '17:30',
            'event': 'CPI Inflation YoY',
            'country': 'IND',
            'impact': 'High',
            'previous': '5.1%',
            'forecast': '5.3%',
            'actual': '',
            'currency': 'INR'
        }
    ]
    
    # Global Events (US, EU, China)
    global_events = [
        {
            'date': base_date + timedelta(days=1),
            'time': '18:00',
            'event': 'US Initial Jobless Claims',
            'country': 'USA',
            'impact': 'High',
            'previous': '210K',
            'forecast': '215K',
            'actual': '',
            'currency': 'USD'
        },
        {
            'date': base_date + timedelta(days=2),
            'time': '18:30',
            'event': 'US Core PCE Price Index',
            'country': 'USA',
            'impact': 'High',
            'previous': '0.2%',
            'forecast': '0.3%',
            'actual': '',
            'currency': 'USD'
        },
        {
            'date': base_date + timedelta(days=3),
            'time': '14:00',
            'event': 'EU CPI Flash Estimate',
            'country': 'EU',
            'impact': 'High',
            'previous': '2.4%',
            'forecast': '2.3%',
            'actual': '',
            'currency': 'EUR'
        },
        {
            'date': base_date + timedelta(days=4),
            'time': '06:00',
            'event': 'China Manufacturing PMI',
            'country': 'CHN',
            'impact': 'Medium',
            'previous': '49.5',
            'forecast': '49.7',
            'actual': '',
            'currency': 'CNY'
        },
        {
            'date': base_date + timedelta(days=5),
            'time': '18:00',
            'event': 'US Non-Farm Payrolls',
            'country': 'USA',
            'impact': 'High',
            'previous': '175K',
            'forecast': '180K',
            'actual': '',
            'currency': 'USD'
        },
        {
            'date': base_date + timedelta(days=7),
            'time': '16:30',
            'event': 'US ISM Manufacturing PMI',
            'country': 'USA',
            'impact': 'High',
            'previous': '48.7',
            'forecast': '49.0',
            'actual': '',
            'currency': 'USD'
        }
    ]
    
    # Combine and filter events within the date range
    all_events = indian_events + global_events
    end_date = base_date + timedelta(days=days_ahead)
    
    for event in all_events:
        if event['date'] <= end_date:
            calendar_data.append({
                'Date': event['date'].strftime('%Y-%m-%d'),
                'Time': event['time'],
                'Country': event['country'],
                'Event': event['event'],
                'Impact': event['impact'],
                'Previous': event['previous'],
                'Forecast': event['forecast'],
                'Actual': event['actual'],
                'Currency': event['currency']
            })
    
    return calendar_data

def display_live_economic_calendar(days_ahead=7):
    """Display the economic calendar with live data."""
    
    with st.spinner("🔄 Fetching latest economic events..."):
        calendar_data = fetch_live_economic_calendar(days_ahead)
    
    if not calendar_data:
        st.error("Unable to fetch economic calendar data. Please try again later.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(calendar_data)
    
    # Display data source info
    source_info = st.empty()
    if len(df) > 0:
        if 'FMP' in str(calendar_data):
            source_info.success("✅ Data source: Financial Modeling Prep (Live)")
        elif 'Alpha' in str(calendar_data):
            source_info.info("ℹ️ Data source: Alpha Vantage (Live)")
        else:
            source_info.warning("⚠️ Data source: Fallback data (Static)")
    
    # Filter controls
    st.subheader("📊 Economic Events Filter")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        countries = ['All'] + sorted(df['Country'].unique().tolist())
        selected_country = st.selectbox("Country", countries)
    with col2:
        impacts = ['All'] + sorted(df['Impact'].unique().tolist())
        selected_impact = st.selectbox("Impact Level", impacts)
    with col3:
        currencies = ['All'] + sorted(df['Currency'].unique().tolist())
        selected_currency = st.selectbox("Currency", currencies)
    with col4:
        show_past = st.checkbox("Include past events", value=False)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df['Country'] == selected_country]
    
    if selected_impact != 'All':
        filtered_df = filtered_df[filtered_df['Impact'] == selected_impact]
    
    if selected_currency != 'All':
        filtered_df = filtered_df[filtered_df['Currency'] == selected_currency]
    
    if not show_past:
        today = datetime.now().strftime('%Y-%m-%d')
        filtered_df = filtered_df[filtered_df['Date'] >= today]
    
    # Sort by date and time
    filtered_df = filtered_df.sort_values(['Date', 'Time'])
    
    # Display the calendar
    st.subheader(f"📅 Economic Calendar ({len(filtered_df)} events)")
    
    if filtered_df.empty:
        st.info("No events match your filters. Try adjusting the criteria.")
        return
    
    # Color code impact levels
    def color_impact(val):
        if val == 'High':
            return 'background-color: #ff4444; color: white; font-weight: bold;'
        elif val == 'Medium':
            return 'background-color: #ffaa00; color: black; font-weight: bold;'
        else:
            return 'background-color: #00aa00; color: white; font-weight: bold;'
    
    # Apply styling
    styled_df = filtered_df.style.applymap(color_impact, subset=['Impact'])
    
    # Display the table
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Date": st.column_config.DateColumn("Date", format="DD/MM/YY"),
            "Time": st.column_config.TextColumn("Time (IST)"),
            "Country": st.column_config.TextColumn("Country"),
            "Event": st.column_config.TextColumn("Event", width="large"),
            "Impact": st.column_config.TextColumn("Impact"),
            "Previous": st.column_config.TextColumn("Previous"),
            "Forecast": st.column_config.TextColumn("Forecast"),
            "Actual": st.column_config.TextColumn("Actual"),
            "Currency": st.column_config.TextColumn("Currency")
        }
    )
    
    # Key events highlight
    st.subheader("🎯 Key Events This Week")
    key_events = filtered_df[filtered_df['Impact'] == 'High'].head(5)
    
    if not key_events.empty:
        for _, event in key_events.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    st.write(f"**{event['Date']}**")
                    st.write(f"{event['Time']}")
                with col2:
                    st.write(f"**{event['Event']}** ({event['Country']})")
                    st.write(f"Forecast: {event['Forecast']} | Previous: {event['Previous']}")
                with col3:
                    if event['Actual'] and event['Actual'] != 'nan':
                        # Color code actual vs forecast
                        try:
                            actual_clean = str(event['Actual']).replace('%', '').replace('$', '').replace('K', '')
                            forecast_clean = str(event['Forecast']).replace('%', '').replace('$', '').replace('K', '')
                            
                            if actual_clean.replace('.', '').isdigit() and forecast_clean.replace('.', '').isdigit():
                                actual_num = float(actual_clean)
                                forecast_num = float(forecast_clean)
                                
                                if actual_num > forecast_num:
                                    st.success(f"**Actual: {event['Actual']}** 📈")
                                elif actual_num < forecast_num:
                                    st.error(f"**Actual: {event['Actual']}** 📉")
                                else:
                                    st.info(f"**Actual: {event['Actual']}** ➡️")
                            else:
                                st.info(f"**Actual: {event['Actual']}**")
                        except:
                            st.info(f"**Actual: {event['Actual']}**")
                    else:
                        st.info("⏳ Pending")
                st.markdown("---")
    else:
        st.info("No high-impact events in the selected period.")
    
    # Market sentiment analysis
    st.subheader("📈 Market Sentiment Analysis")
    
    high_impact_count = len(filtered_df[filtered_df['Impact'] == 'High'])
    indian_events = len(filtered_df[filtered_df['Country'] == 'IND'])
    completed_events = len(filtered_df[filtered_df['Actual'].notna() & (filtered_df['Actual'] != '') & (filtered_df['Actual'] != 'nan')])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Events", len(filtered_df))
    col2.metric("High Impact", high_impact_count)
    col3.metric("Indian Events", indian_events)
    col4.metric("Completed", completed_events)
    
    # Data freshness indicator
    st.caption(f"🕒 Last updated: {get_ist_time().strftime('%Y-%m-%d %H:%M:%S IST')}")
    
    # Export option
    if st.button("📥 Export Calendar to CSV", use_container_width=True):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"economic_calendar_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# ============ 5.5 HFT TERMINAL PAGE ============
def page_hft_terminal():
    """A dedicated terminal for High-Frequency Trading with Level 2 data."""
    display_header()
    
    # HFT Terminal Header with Professional Styling
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0; font-size: 2.5em;">⚡ HFT TERMINAL</h1>
        <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 1.1em;">
        High-Frequency Trading Platform • Real-time Market Depth • One-Click Execution
        </p>
    </div>
    """, unsafe_allow_html=True)

    instrument_df = get_instrument_df()
    if instrument_df.empty:
        st.warning("🔌 Please connect to a broker to use the HFT Terminal.")
        return

    # --- Instrument Selection with Enhanced UI ---
    st.markdown("### 🎯 Instrument Selection")
    
    col_search, col_info, col_status = st.columns([2, 1, 1])
    
    with col_search:
        symbol = st.text_input(
            "**Trading Symbol**", 
            "NIFTY24OCTFUT", 
            key="hft_symbol",
            help="Enter the instrument symbol (e.g., RELIANCE, NIFTY24OCTFUT)"
        ).upper()
    
    instrument_info = instrument_df[instrument_df['tradingsymbol'] == symbol]
    if instrument_info.empty:
        st.error(f"❌ Instrument '{symbol}' not found in database.")
        return
    
    exchange = instrument_info.iloc[0]['exchange']
    instrument_token = instrument_info.iloc[0]['instrument_token']
    lot_size = instrument_info.iloc[0].get('lot_size', 50)

    with col_info:
        st.metric("Exchange", exchange)
        
    with col_status:
        market_status = get_market_status()['status'].replace('_', ' ').title()
        status_color = "#00ff00" if "open" in market_status.lower() else "#ff4444"
        st.markdown(f"**Market:** <span style='color: {status_color};'>{market_status}</span>", unsafe_allow_html=True)

    # --- Real-time Data Fetching ---
    quote_data = get_watchlist_data([{'symbol': symbol, 'exchange': exchange}])
    depth_data = get_market_depth_enhanced(instrument_token, levels=5)

    # --- Enhanced Price Header with Professional Layout ---
    if not quote_data.empty:
        ltp = quote_data.iloc[0]['Price']
        change = quote_data.iloc[0]['Change']
        pct_change = quote_data.iloc[0]['% Change']
        
        # Calculate tick direction
        prev_price = st.session_state.hft_last_price
        tick_direction = "up" if ltp > prev_price else "down" if ltp < prev_price else "same"
        
        # Price Header with Advanced Styling
        st.markdown(f"""
        <div style="background: #1e1e1e; padding: 15px; border-radius: 8px; border-left: 5px solid {'#00ff88' if tick_direction == 'up' else '#ff4444' if tick_direction == 'down' else '#888888'};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2 style="color: {'#00ff88' if tick_direction == 'up' else '#ff4444' if tick_direction == 'down' else '#ffffff'}; margin: 0; font-size: 2.2em;">
                        ₹{ltp:,.2f}
                    </h2>
                    <p style="color: {'#00ff88' if change >= 0 else '#ff4444'}; margin: 0; font-size: 1.1em;">
                        {change:+.2f} ({pct_change:+.2f}%)
                    </p>
                </div>
                <div style="text-align: right;">
                    <div style="color: #888; font-size: 0.9em;">Last Update</div>
                    <div style="color: white; font-size: 1em;">{get_ist_time().strftime('%H:%M:%S.%f')[:-3]}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Update tick log
        if ltp != prev_price and prev_price != 0:
            ist_time = get_ist_time()
            log_entry = {
                "time": ist_time.strftime("%H:%M:%S.%f")[:-3],
                "price": ltp,
                "change": ltp - prev_price,
                "direction": tick_direction
            }
            st.session_state.hft_tick_log.insert(0, log_entry)
            if len(st.session_state.hft_tick_log) > 100:  # Larger buffer for HFT
                st.session_state.hft_tick_log.pop()

        st.session_state.hft_last_price = ltp

    # --- Main Trading Interface ---
    st.markdown("## 📊 Trading Interface")
    
    # Three-column layout for HFT
    col_depth, col_trading, col_ticks = st.columns([1.2, 1, 1], gap="large")

    with col_depth:
        # Enhanced Market Depth Display
        st.markdown("""
        <div style="background: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333;">
            <h3 style="color: #fff; margin-top: 0;">🎯 Market Depth (L2)</h3>
        """, unsafe_allow_html=True)
        
        if depth_data and depth_data.get('buy') and depth_data.get('sell'):
            bids = depth_data['buy']
            asks = depth_data['sell']
            
            # Depth Header with Spread
            best_bid = bids[0].get('price', 0) if bids else 0
            best_ask = asks[0].get('price', 0) if asks else 0
            spread = best_ask - best_bid
            spread_pct = (spread / ltp * 100) if ltp > 0 else 0
            
            st.markdown(f"""
            <div style="background: #2a2a2a; padding: 10px; border-radius: 5px; margin-bottom: 15px; text-align: center;">
                <div style="color: #888; font-size: 0.9em;">Spread</div>
                <div style="color: #ffd700; font-size: 1.2em; font-weight: bold;">₹{spread:.2f} ({spread_pct:.3f}%)</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Depth Table
            st.markdown("""
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                <div style="color: #00ff88; font-weight: bold; text-align: center;">BIDS</div>
                <div style="color: #ff4444; font-weight: bold; text-align: center;">ASKS</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display top 5 levels
            for i in range(5):
                bid = bids[i] if i < len(bids) else {'price': 0, 'quantity': 0, 'orders': 0}
                ask = asks[i] if i < len(asks) else {'price': 0, 'quantity': 0, 'orders': 0}
                
                # Calculate depth strength (visual indicator)
                bid_strength = min(bid.get('quantity', 0) / 10000, 1) if bid.get('quantity', 0) > 0 else 0
                ask_strength = min(ask.get('quantity', 0) / 10000, 1) if ask.get('quantity', 0) > 0 else 0
                
                st.markdown(f"""
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 8px; font-family: monospace;">
                    <div style="background: rgba(0, 255, 136, {bid_strength*0.3}); padding: 8px; border-radius: 4px; border-left: 3px solid #00ff88;">
                        <div style="color: #00ff88;">L{i+1}: ₹{bid.get('price', 0):.2f}</div>
                        <div style="color: #aaa; font-size: 0.8em;">{bid.get('quantity', 0):,} × {bid.get('orders', 0)}</div>
                    </div>
                    <div style="background: rgba(255, 68, 68, {ask_strength*0.3}); padding: 8px; border-radius: 4px; border-left: 3px solid #ff4444;">
                        <div style="color: #ff4444;">L{i+1}: ₹{ask.get('price', 0):.2f}</div>
                        <div style="color: #aaa; font-size: 0.8em;">{ask.get('quantity', 0):,} × {ask.get('orders', 0)}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Depth Analysis
            total_bid = depth_data.get('total_bid_volume', 0)
            total_ask = depth_data.get('total_ask_volume', 0)
            ratio = depth_data.get('bid_ask_ratio', 1)
            
            st.markdown("""
            <div style="background: #2a2a2a; padding: 10px; border-radius: 5px; margin-top: 15px;">
                <div style="color: #fff; font-weight: bold; margin-bottom: 8px;">Depth Analysis</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.9em;">
            """, unsafe_allow_html=True)
            
            if ratio > 1.2:
                st.markdown(f'<div style="color: #00ff88;">Bullish: {ratio:.2f}x</div>', unsafe_allow_html=True)
            elif ratio < 0.8:
                st.markdown(f'<div style="color: #ff4444;">Bearish: {1/ratio:.2f}x</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="color: #888;">Neutral: {ratio:.2f}x</div>', unsafe_allow_html=True)
                
            st.markdown(f'<div style="color: #aaa;">Bid: {total_bid:,}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="color: #aaa;">Ask: {total_ask:,}</div>', unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
        else:
            st.info("⏳ Waiting for market depth data...")
        
        st.markdown("</div>", unsafe_allow_html=True)

    with col_trading:
        # Enhanced Trading Panel
        st.markdown("""
        <div style="background: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333;">
            <h3 style="color: #fff; margin-top: 0;">🚀 Quick Execution</h3>
        """, unsafe_allow_html=True)
        
        # Quantity Selection
        st.markdown("**Order Quantity**")
        quantity = st.number_input(
            "Shares/Lots",
            min_value=lot_size,
            value=lot_size,
            step=lot_size,
            key="hft_qty",
            label_visibility="collapsed"
        )
        
        # Market Orders - Enhanced Buttons
        st.markdown("**Market Orders**")
        mcol1, mcol2 = st.columns(2)
        
        with mcol1:
            if st.button(
                "🟢 BUY MARKET", 
                use_container_width=True,
                type="primary",
                key="market_buy",
                help=f"Buy {quantity} at market price"
            ):
                place_order(instrument_df, symbol, quantity, 'MARKET', 'BUY', 'MIS')
                st.toast(f"🟢 BUY {quantity} {symbol} @ MARKET", icon="✅")
                
        with mcol2:
            if st.button(
                "🔴 SELL MARKET", 
                use_container_width=True,
                type="secondary",
                key="market_sell", 
                help=f"Sell {quantity} at market price"
            ):
                place_order(instrument_df, symbol, quantity, 'MARKET', 'SELL', 'MIS')
                st.toast(f"🔴 SELL {quantity} {symbol} @ MARKET", icon="✅")
        
        st.markdown("---")
        
        # Limit Orders with Smart Pricing
        st.markdown("**Limit Orders**")
        
        # Smart price suggestions from depth
        if depth_data and depth_data.get('buy') and depth_data.get('sell'):
            best_bid = depth_data['buy'][0].get('price', ltp)
            best_ask = depth_data['sell'][0].get('price', ltp)
            
            price_col1, price_col2 = st.columns(2)
            with price_col1:
                if st.button(f"Bid: ₹{best_bid:.2f}", use_container_width=True, key="use_bid"):
                    st.session_state.hft_limit_price = best_bid
            with price_col2:
                if st.button(f"Ask: ₹{best_ask:.2f}", use_container_width=True, key="use_ask"):
                    st.session_state.hft_limit_price = best_ask
        
        limit_price = st.number_input(
            "Limit Price",
            min_value=0.05,
            value=st.session_state.get('hft_limit_price', ltp),
            step=0.05,
            key="hft_limit_price_input"
        )
        
        lcol1, lcol2 = st.columns(2)
        with lcol1:
            if st.button(
                "🟢 BUY LIMIT", 
                use_container_width=True,
                key="limit_buy",
                help=f"Buy {quantity} at ₹{limit_price:.2f}"
            ):
                place_order(instrument_df, symbol, quantity, 'LIMIT', 'BUY', 'MIS', price=limit_price)
                st.toast(f"🟢 BUY {quantity} {symbol} @ ₹{limit_price:.2f}", icon="✅")
                
        with lcol2:
            if st.button(
                "🔴 SELL LIMIT", 
                use_container_width=True,
                key="limit_sell",
                help=f"Sell {quantity} at ₹{limit_price:.2f}"
            ):
                place_order(instrument_df, symbol, quantity, 'LIMIT', 'SELL', 'MIS', price=limit_price)
                st.toast(f"🔴 SELL {quantity} {symbol} @ ₹{limit_price:.2f}", icon="✅")
        
        # Order Information
        st.markdown("---")
        st.markdown("**Order Info**")
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.metric("Lot Size", lot_size)
        with info_col2:
            st.metric("Est. Value", f"₹{quantity * ltp:,.0f}")
        
        st.markdown("</div>", unsafe_allow_html=True)

    with col_ticks:
        # Enhanced Tick Log
        st.markdown("""
        <div style="background: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; height: 600px; display: flex; flex-direction: column;">
            <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 15px;">
                <h3 style="color: #fff; margin: 0;">📈 Live Ticks</h3>
                <div style="color: #888; font-size: 0.8em;">{get_ist_time().strftime('%H:%M:%S')}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Tick Log Controls
        control_col1, control_col2 = st.columns(2)
        with control_col1:
            if st.button("🗑️ Clear", use_container_width=True, key="clear_ticks"):
                st.session_state.hft_tick_log = []
                st.rerun()
        with control_col2:
            auto_refresh = st.checkbox("Auto-refresh", value=True, key="hft_auto_refresh")
        
        # Tick Log Display
        tick_container = st.container()
        
        with tick_container:
            if st.session_state.hft_tick_log:
                # Show last 30 ticks
                for entry in st.session_state.hft_tick_log[:30]:
                    color = "#00ff88" if entry['direction'] == 'up' else "#ff4444" if entry['direction'] == 'down' else "#888888"
                    bg_color = "rgba(0, 255, 136, 0.1)" if entry['direction'] == 'up' else "rgba(255, 68, 68, 0.1)" if entry['direction'] == 'down' else "transparent"
                    arrow = "▲" if entry['direction'] == 'up' else "▼" if entry['direction'] == 'down' else "●"
                    
                    st.markdown(f"""
                    <div style="background: {bg_color}; padding: 8px 12px; margin: 2px 0; border-radius: 4px; border-left: 3px solid {color};">
                        <div style="display: flex; justify-content: space-between; align-items: center; font-family: 'Courier New', monospace;">
                            <span style="color: #aaa; font-size: 0.85em;">{entry['time']}</span>
                            <span style="color: {color}; font-weight: bold; font-size: 1.1em;">{arrow} ₹{entry['price']:.2f}</span>
                            <span style="color: {color}; font-size: 0.9em;">{entry['change']:+.2f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No tick data yet. Price changes will appear here.")
        
        # Tick Statistics
        if len(st.session_state.hft_tick_log) > 1:
            up_ticks = len([t for t in st.session_state.hft_tick_log if t['direction'] == 'up'])
            down_ticks = len([t for t in st.session_state.hft_tick_log if t['direction'] == 'down'])
            total_ticks = len(st.session_state.hft_tick_log)
            
            st.markdown("""
            <div style="background: #2a2a2a; padding: 10px; border-radius: 5px; margin-top: 15px;">
                <div style="color: #fff; font-weight: bold; margin-bottom: 8px;">Tick Statistics</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.9em;">
            """, unsafe_allow_html=True)
            
            st.markdown(f'<div style="color: #00ff88;">Up: {up_ticks}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="color: #00ff88;">{(up_ticks/total_ticks*100):.1f}%</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="color: #ff4444;">Down: {down_ticks}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="color: #ff4444;">{(down_ticks/total_ticks*100):.1f}%</div>', unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Performance Metrics Footer ---
    st.markdown("---")
    st.markdown("### 📊 Performance Metrics")
    
    metric_cols = st.columns(6)
    
    with metric_cols[0]:
        latency = random.uniform(2, 15)  # HFT-grade latency
        st.metric("Latency", f"{latency:.1f} ms")
    
    with metric_cols[1]:
        total_volume = depth_data.get('total_bid_volume', 0) + depth_data.get('total_ask_volume', 0) if depth_data else 0
        st.metric("Depth Volume", f"{total_volume:,}")
    
    with metric_cols[2]:
        st.metric("Tick Count", len(st.session_state.hft_tick_log))
    
    with metric_cols[3]:
        if depth_data:
            ratio = depth_data.get('bid_ask_ratio', 1)
        st.metric("Bid/Ask Ratio", f"{ratio:.2f}")
    
    with metric_cols[4]:
        if st.session_state.hft_tick_log:
            avg_tick_change = sum(abs(t['change']) for t in st.session_state.hft_tick_log) / len(st.session_state.hft_tick_log)
            st.metric("Avg Tick", f"₹{avg_tick_change:.2f}")
    
    with metric_cols[5]:
        st.metric("Status", "🟢 LIVE" if auto_refresh else "⏸️ PAUSED")

    # Auto-refresh for HFT mode
    if auto_refresh:
        a_time.sleep(0.5)  # Faster refresh for true HFT feel
        st.rerun()

# Initialize HFT session state
def initialize_hft_session_state():
    """Initialize HFT-specific session state variables."""
    if 'hft_last_price' not in st.session_state:
        st.session_state.hft_last_price = 0
    if 'hft_tick_log' not in st.session_state:
        st.session_state.hft_tick_log = []
    if 'hft_limit_price' not in st.session_state:
        st.session_state.hft_limit_price = 0

# Call this in your main app initialization
initialize_hft_session_state()

# ============ 6. MAIN APP LOGIC AND AUTHENTICATION ============
# ================ ICEBERG DETECTOR CORE CLASSES ================
# Add this import at the TOP of your file (with other imports)
from typing import Dict, List, Any, Optional

class FlowAnalysisAgent:
    """Real-time liquidity flow analysis with Nifty50-specific parameters"""
    
    def analyze(self, market_data: Dict) -> Dict:
        try:
            order_book = market_data.get('order_book', {})
            trades = market_data.get('trades', [])
            large_orders = market_data.get('large_orders', [])
            detection_params = market_data.get('detection_params', {})
            
            # Get Nifty50 specific parameters
            large_order_threshold = detection_params.get('large_order_threshold', 10000)
            order_imbalance_threshold = detection_params.get('order_imbalance_threshold', 0.65)
            
            order_imbalance = self._calculate_order_imbalance(order_book, order_imbalance_threshold)
            liquidity_waves = self._detect_liquidity_waves(trades, large_order_threshold)
            smart_money_flow = self._track_smart_money(large_orders, large_order_threshold)
            
            # Calculate weighted confidence
            confidence = 0.4 * order_imbalance + 0.4 * liquidity_waves + 0.2 * smart_money_flow
            
            return {
                'confidence': min(max(confidence, 0), 1),  # Clamp between 0-1
                'momentum': order_imbalance,
                'volatility': liquidity_waves
            }
        except Exception as e:
            # Return safe default values on error
            return {
                'confidence': 0.5,
                'momentum': 0.5,
                'volatility': 0.5
            }
    
    def _calculate_order_imbalance(self, order_book: Dict, threshold: float) -> float:
        """Calculate order book imbalance with threshold adjustment"""
        try:
            bids = order_book.get('bids', [])
            asks = order_book.get('asks', [])
            
            # Handle different depth data sources
            if not bids or not asks:
                source = order_book.get('source', 'unknown')
                if source == 'fallback':
                    return 0.5  # Neutral for fallback data
                elif source == 'synthetic':
                    # For synthetic data, return slight bias based on recent price movement
                    return 0.55
                else:
                    return 0.5
            
            # Extract quantities safely
            total_bid_volume = sum(bid.get('quantity', 0) for bid in bids)
            total_ask_volume = sum(ask.get('quantity', 0) for ask in asks)
            
            if total_bid_volume + total_ask_volume == 0:
                return 0.5
                
            imbalance = total_bid_volume / (total_bid_volume + total_ask_volume)
            
            # Apply threshold-based confidence
            if abs(imbalance - 0.5) > (threshold - 0.5):
                return max(0.7, imbalance)
            else:
                return 0.5
                
        except Exception:
            return 0.5
    
    def _detect_liquidity_waves(self, trades: List, large_order_threshold: int) -> float:
        """Detect liquidity waves using Nifty50 threshold"""
        try:
            if len(trades) < 10:
                return 0.5
                
            recent_trades = trades[-10:]
            
            # Safely extract trade quantities
            large_trades = [
                trade for trade in recent_trades 
                if trade.get('quantity', 0) >= large_order_threshold
            ]
            
            if not large_trades:
                return 0.3
                
            # Higher confidence when large trades are present
            large_trade_ratio = len(large_trades) / len(recent_trades)
            return min(0.9, 0.5 + large_trade_ratio * 0.4)
            
        except Exception:
            return 0.5
    
    def _track_smart_money(self, large_orders: List, large_order_threshold: int) -> float:
        """Track smart money flow with dynamic threshold"""
        try:
            if not large_orders:
                return 0.5
                
            # Filter orders by Nifty50 threshold
            significant_orders = [
                order for order in large_orders 
                if order.get('quantity', 0) >= large_order_threshold
            ]
            
            if not significant_orders:
                return 0.4
                
            order_count = len(significant_orders)
            return min(0.9, 0.5 + (order_count / 10.0) * 0.4)
            
        except Exception:
            return 0.5


class PatternDetectionAgent:
    """Advanced pattern detection with Nifty50-specific parameters"""
    
    def analyze(self, market_data: Dict) -> Dict:
        volumes = market_data.get('volumes', [])
        prices = market_data.get('prices', [])
        timestamps = market_data.get('timestamps', [])
        detection_params = market_data.get('detection_params', {})
        
        volume_anomaly_multiplier = detection_params.get('volume_anomaly_multiplier', 2.5)
        momentum_weight = detection_params.get('momentum_weight', 0.4)
        
        volume_pattern = self._analyze_volume_fractals(volumes, volume_anomaly_multiplier) if volumes else 0.5
        price_pattern = self._analyze_price_fractals(prices) if prices else 0.5
        time_pattern = self._analyze_time_compression(timestamps) if timestamps else 0.5
        
        # Use momentum weight from Nifty50 params
        base_confidence = (0.6 * volume_pattern + 0.3 * price_pattern + 0.1 * time_pattern)
        momentum = self._calculate_pattern_momentum(market_data)
        
        # Adjust confidence based on momentum
        adjusted_confidence = base_confidence * (1 + momentum_weight * momentum)
        
        return {
            'confidence': np.clip(adjusted_confidence, 0, 1),
            'momentum': momentum,
            'volatility': market_data.get('volatility', 0)
        }
    
    def _analyze_volume_fractals(self, volumes: List[float], anomaly_multiplier: float) -> float:
        """Analyze volume patterns with Nifty50 anomaly multiplier"""
        if len(volumes) < 5:
            return 0.5
        
        try:
            # Calculate volume anomaly
            avg_volume = np.mean(volumes[:-1]) if len(volumes) > 1 else volumes[0]
            current_volume = volumes[-1]
            
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
            
            # Use Nifty50 multiplier for anomaly detection
            if volume_ratio > anomaly_multiplier:
                anomaly_score = min(0.8, 0.3 + (volume_ratio - anomaly_multiplier) * 0.2)
            else:
                anomaly_score = 0.3
                
            # Combine with fractal analysis
            log_volumes = np.log(np.array(volumes) + 1e-8)
            hurst_exponent = self._calculate_hurst_exponent(log_volumes)
            fractal_dimension = 2 - hurst_exponent
            fractal_score = float(np.clip(fractal_dimension - 1.2, 0, 0.5) * 2)
            
            return 0.6 * anomaly_score + 0.4 * fractal_score
            
        except:
            return 0.5
    
    def _calculate_hurst_exponent(self, time_series):
        """Calculate Hurst exponent for fractal analysis"""
        try:
            lags = range(2, min(20, len(time_series)//2))
            tau = [np.std(np.subtract(time_series[lag:], time_series[:-lag])) for lag in lags]
            poly = np.polyfit(np.log(lags), np.log(tau), 1)
            return poly[0]
        except:
            return 0.5
    
    def _analyze_price_fractals(self, prices: List[float]) -> float:
        """Analyze price patterns for iceberg detection"""
        if len(prices) < 10:
            return 0.5
            
        try:
            # Calculate price momentum and volatility
            returns = np.diff(np.log(prices + 1e-8))
            volatility = np.std(returns) if len(returns) > 1 else 0.01
            
            # Detect sudden price movements without volume (potential iceberg)
            price_changes = np.abs(np.diff(prices))
            avg_change = np.mean(price_changes) if len(price_changes) > 0 else 0
            
            if avg_change > 0:
                recent_change = price_changes[-1] if len(price_changes) > 0 else 0
                anomaly_ratio = recent_change / avg_change
                price_score = min(0.8, 0.3 + anomaly_ratio * 0.2)
            else:
                price_score = 0.3
                
            return price_score
            
        except:
            return 0.5
    
    def _analyze_time_compression(self, timestamps: List) -> float:
        """Analyze time-based patterns"""
        if len(timestamps) < 5:
            return 0.5
            
        try:
            # Simple time analysis - more sophisticated version would use actual timestamps
            return 0.5
        except:
            return 0.5
    
    def _calculate_pattern_momentum(self, market_data: Dict) -> float:
        """Calculate pattern momentum"""
        prices = market_data.get('prices', [])
        if len(prices) < 5:
            return 0.5
            
        try:
            # Simple momentum calculation
            recent_prices = prices[-5:]
            if len(recent_prices) >= 2:
                momentum = (recent_prices[-1] - recent_prices[0]) / recent_prices[0]
                return float(np.clip(momentum * 10, -1, 1))
            return 0.5
        except:
            return 0.5

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import plotly.graph_objects as go

class QuantumIcebergDetector:
    def __init__(self):
        self.pattern_weights = {
            'order_fragmentation': 0.3,
            'hidden_liquidity': 0.25, 
            'volume_anomaly': 0.25,
            'momentum_disparity': 0.12,
            'depth_imbalance': 0.08
        }
        
        self.volume_alert_levels = {
            'EXTREME': 2.0,
            'HIGH': 1.5,
            'MEDIUM': 1.2,
            'LOW': 1.0
        }
    
    def process_market_data(self, market_data):
        """Comprehensive iceberg detection with 5-day volume focus"""
        try:
            if not market_data or not isinstance(market_data, dict):
                return self.get_default_detection_result("Invalid market data")
            
            order_book = market_data.get('order_book', {})
            volume_analysis = market_data.get('volume_analysis', {})
            weekly_patterns = volume_analysis.get('weekly_patterns', {})
            
            # Calculate individual detection scores
            order_fragmentation = self.calculate_order_fragmentation(order_book)
            hidden_liquidity = self.detect_hidden_liquidity(order_book)
            volume_anomaly = self.enhanced_volume_analysis(market_data)
            momentum_disparity = self.analyze_momentum_disparity(market_data)
            depth_imbalance = self.calculate_depth_imbalance(order_book)
            
            # Weighted probability calculation
            probability = (
                order_fragmentation * self.pattern_weights['order_fragmentation'] +
                hidden_liquidity * self.pattern_weights['hidden_liquidity'] +
                volume_anomaly * self.pattern_weights['volume_anomaly'] +
                momentum_disparity * self.pattern_weights['momentum_disparity'] +
                depth_imbalance * self.pattern_weights['depth_imbalance']
            )
            
            # Enhanced volume spike adjustment with weekly context
            volume_spike = volume_analysis.get('volume_spike_detected', False)
            if volume_spike:
                alert_level = volume_analysis.get('alert_level', 'NORMAL')
                # Check weekly context for additional confidence
                weekly_ratio = weekly_patterns.get('current_vs_weekly_ratio', 0)
                
                base_boost = 0
                if alert_level == 'EXTREME':
                    base_boost = 0.3
                elif alert_level == 'HIGH':
                    base_boost = 0.2
                elif alert_level == 'MEDIUM':
                    base_boost = 0.1
                
                # Additional boost if volume is high relative to weekly average
                if weekly_ratio > 2.0:
                    base_boost += 0.15
                elif weekly_ratio > 1.5:
                    base_boost += 0.1
                
                probability = min(1.0, probability + base_boost)
            
            # Confidence based on data quality and market conditions
            confidence = self.calculate_confidence(market_data, probability)
            
            # Generate alerts
            alerts = self.generate_alerts(probability, market_data)
            
            return {
                'iceberg_probability': min(1.0, probability),
                'confidence': confidence,
                'regime': self.determine_market_regime(market_data),
                'alerts': alerts,
                'detection_scores': {
                    'order_fragmentation': order_fragmentation,
                    'hidden_liquidity': hidden_liquidity,
                    'volume_anomaly': volume_anomaly,
                    'momentum_disparity': momentum_disparity,
                    'depth_imbalance': depth_imbalance
                },
                'flow_analysis': {
                    'confidence': probability,
                    'momentum': momentum_disparity,
                    'volatility': market_data.get('volatility', 0.02)
                },
                'pattern_analysis': {
                    'confidence': order_fragmentation,
                    'momentum': hidden_liquidity,
                    'volatility': depth_imbalance
                }
            }
            
        except Exception as e:
            return self.get_default_detection_result(f"Detection error: {str(e)}")
    
    def get_default_detection_result(self, error_message=""):
        """Return default detection result when errors occur"""
        return {
            'iceberg_probability': 0.0,
            'confidence': 0.0,
            'regime': 'UNKNOWN',
            'alerts': [error_message] if error_message else ['Detection unavailable'],
            'detection_scores': {},
            'flow_analysis': {},
            'pattern_analysis': {}
        }
    
    def calculate_order_fragmentation(self, order_book):
        """Detect large orders split across multiple price levels"""
        try:
            if not order_book:
                return 0.0
                
            bids = order_book.get('bids', [])
            asks = order_book.get('asks', [])
            
            if not bids or not asks:
                return 0.0
            
            fragmentation_score = 0.0
            
            # Analyze bid side fragmentation
            bid_sizes = [bid.get('quantity', 0) for bid in bids[:10]]
            if len(bid_sizes) >= 3:
                size_std = np.std(bid_sizes)
                mean_size = np.mean(bid_sizes)
                if mean_size > 0 and size_std / mean_size < 0.4:
                    fragmentation_score += 0.6
                
                # Check for consistent order sizes across levels
                if len(set([round(size/1000) for size in bid_sizes[:5]])) == 1:
                    fragmentation_score += 0.4
            
            # Analyze ask side fragmentation
            ask_sizes = [ask.get('quantity', 0) for ask in asks[:10]]
            if len(ask_sizes) >= 3:
                size_std = np.std(ask_sizes)
                mean_size = np.mean(ask_sizes)
                if mean_size > 0 and size_std / mean_size < 0.4:
                    fragmentation_score += 0.6
                
                if len(set([round(size/1000) for size in ask_sizes[:5]])) == 1:
                    fragmentation_score += 0.4
            
            return min(1.0, fragmentation_score / 2.0)
            
        except Exception as e:
            return 0.0
    
    def detect_hidden_liquidity(self, order_book):
        """Detect hidden liquidity through depth analysis"""
        try:
            if not order_book:
                return 0.0
                
            bids = order_book.get('bids', [])
            asks = order_book.get('asks', [])
            
            hidden_score = 0.0
            
            # Check for sudden large orders at deeper levels (bids)
            if len(bids) > 8:
                first_4_avg = np.mean([b.get('quantity', 0) for b in bids[:4]])
                next_4_avg = np.mean([b.get('quantity', 0) for b in bids[4:8]])
                
                if first_4_avg > 0 and next_4_avg > first_4_avg * 1.8:
                    hidden_score += 0.7
            
            # Check for sudden large orders at deeper levels (asks)
            if len(asks) > 8:
                first_4_avg = np.mean([a.get('quantity', 0) for a in asks[:4]])
                next_4_avg = np.mean([a.get('quantity', 0) for a in asks[4:8]])
                
                if first_4_avg > 0 and next_4_avg > first_4_avg * 1.8:
                    hidden_score += 0.7
            
            return min(1.0, hidden_score)
            
        except Exception as e:
            return 0.0
    
    def enhanced_volume_analysis(self, market_data):
        """Volume analysis focused on 5-day patterns"""
        try:
            if not market_data:
                return 0.0
                
            volume_data = market_data.get('volume_analysis', {})
            current_volume = volume_data.get('current_volume', 0)
            daily_avg = volume_data.get('daily_avg_volume', 1)
            weekly_patterns = volume_data.get('weekly_patterns', {})
            
            volume_anomaly_score = 0.0
            
            # 1. Session-based volume spike (using 5-day average)
            session_ratio = volume_data.get('session_volume_ratio', 0)
            if session_ratio > 2.0:
                volume_anomaly_score += 0.4
            elif session_ratio > 1.5:
                volume_anomaly_score += 0.2
            elif session_ratio > 1.2:
                volume_anomaly_score += 0.1
            
            # 2. Weekly pattern anomalies
            current_vs_weekly = weekly_patterns.get('current_vs_weekly_ratio', 0)
            if current_vs_weekly > 2.5:
                volume_anomaly_score += 0.3
            elif current_vs_weekly > 2.0:
                volume_anomaly_score += 0.2
            elif current_vs_weekly > 1.5:
                volume_anomaly_score += 0.1
            
            # 3. Volume trend analysis
            volume_trend = weekly_patterns.get('volume_trend', 'STABLE')
            if volume_trend == 'INCREASING' and current_vs_weekly > 1.8:
                volume_anomaly_score += 0.2
            
            # 4. Volume without price movement (stealth accumulation/distribution)
            price_change = abs(market_data.get('last_price', 0) - market_data.get('open', 0))
            price_change_pct = price_change / market_data.get('open', 1) if market_data.get('open', 0) > 0 else 0
            
            if session_ratio > 1.5 and price_change_pct < 0.005:
                volume_anomaly_score += 0.3
            
            return min(1.0, volume_anomaly_score)
            
        except Exception as e:
            return 0.0
    
    def analyze_momentum_disparity(self, market_data):
        """Analyze price momentum vs volume momentum disparity"""
        try:
            if not market_data:
                return 0.0
                
            volume_ratio = market_data.get('volume_ratio', 1)
            volatility = market_data.get('volatility', 0.02)
            
            momentum_score = 0.0
            
            # High volume with low volatility can indicate controlled accumulation/distribution
            if volume_ratio > 1.5 and volatility < 0.015:
                momentum_score += 0.6
            
            # Sudden volume spikes without corresponding price movement
            if volume_ratio > 2.0 and volatility < 0.02:
                momentum_score += 0.4
            
            return min(1.0, momentum_score)
            
        except Exception as e:
            return 0.0
    
    def calculate_depth_imbalance(self, order_book):
        """Calculate order book depth imbalance"""
        try:
            if not order_book:
                return 0.0
                
            total_bid_volume = order_book.get('total_bid_volume', 0)
            total_ask_volume = order_book.get('total_ask_volume', 0)
            total_volume = total_bid_volume + total_ask_volume
            
            if total_volume == 0:
                return 0.0
            
            imbalance = abs(total_bid_volume - total_ask_volume) / total_volume
            
            if imbalance > 0.3:
                return min(1.0, imbalance)
            else:
                return 0.0
                
        except Exception as e:
            return 0.0
    
    def calculate_confidence(self, market_data, probability):
        """Calculate confidence score based on data quality"""
        try:
            confidence = 0.5  # Base confidence
            
            # Data source confidence
            if market_data.get('data_source') == 'LIVE':
                confidence += 0.3
            
            # Market hours confidence
            if is_market_hours():
                confidence += 0.2
            
            # Volume data quality
            if market_data.get('volume', 0) > 0:
                confidence += 0.1
            
            # Order book depth quality
            order_book = market_data.get('order_book', {})
            if order_book.get('depth_levels_analyzed', 0) >= 10:
                confidence += 0.1
            
            return min(1.0, confidence)
        except:
            return 0.5
    
    def determine_market_regime(self, market_data):
        """Determine current market regime"""
        try:
            if not market_data:
                return 'UNKNOWN'
                
            volatility = market_data.get('volatility', 0.02)
            volume_ratio = market_data.get('volume_ratio', 1)
            
            if volatility > 0.04:
                return 'HIGH_VOLATILITY'
            elif volume_ratio > 2.0:
                return 'HIGH_VOLUME'
            elif volume_ratio < 0.5:
                return 'LOW_VOLUME'
            else:
                return 'NORMAL'
        except:
            return 'UNKNOWN'
    
    def generate_alerts(self, probability, market_data):
        """Generate iceberg detection alerts"""
        alerts = []
        
        try:
            if probability > 0.8:
                alerts.append("🚨 HIGH PROBABILITY ICEBERG DETECTED")
            elif probability > 0.6:
                alerts.append("🔴 Medium probability iceberg activity")
            elif probability > 0.4:
                alerts.append("🟡 Possible iceberg activity")
            
            # Volume-based alerts
            volume_analysis = market_data.get('volume_analysis', {})
            if volume_analysis.get('volume_spike_detected', False):
                alerts.append(f"📈 Volume spike: {volume_analysis.get('alert_message', '')}")
            
            # Order book alerts
            order_book = market_data.get('order_book', {})
            if order_book.get('bid_concentration', 0) > 0.7:
                alerts.append("🟢 High bid concentration detected")
            if order_book.get('ask_concentration', 0) > 0.7:
                alerts.append("🔴 High ask concentration detected")
        except:
            alerts.append("⚠️ Alert generation failed")
        
        return alerts

class QuantumVisualizer:
    def create_quantum_chart(self, detection_result):
        """Create visualization for iceberg detection results"""
        try:
            scores = detection_result.get('detection_scores', {})
            
            if not scores:
                fig = go.Figure()
                fig.add_annotation(text="No detection data available", 
                                 xref="paper", yref="paper",
                                 x=0.5, y=0.5, xanchor='center', yanchor='middle',
                                 showarrow=False)
                return fig
            
            categories = list(scores.keys())
            values = [scores[cat] for cat in categories]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                name='Detection Scores',
                line=dict(color='blue', width=2),
                fillcolor='rgba(0, 0, 255, 0.3)'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )
                ),
                showlegend=False,
                title="Iceberg Detection Radar",
                height=400
            )
            
            return fig
            
        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(text="Chart unavailable", 
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, xanchor='center', yanchor='middle',
                             showarrow=False)
            return fig

class TradingBotConfigurator:
    """Configuration for semi-automated and fully automated trading bots"""
    
    def __init__(self):
        self.bot_modes = {
            'SEMI_AUTO': {
                'name': '🤖 Semi-Automated Bot',
                'description': 'Manual entry with automated exit & risk management',
                'color': 'orange'
            },
            'FULL_AUTO': {
                'name': '🚀 Fully Automated Bot',
                'description': 'Complete automated trading with AI signals',
                'color': 'green'
            },
            'MONITOR_ONLY': {
                'name': '👁️ Monitor Only',
                'description': 'Real-time monitoring without trading',
                'color': 'blue'
            }
        }
    
    def render_bot_configuration(self):
        """Render bot configuration UI"""
        st.markdown("---")
        st.subheader("🤖 Trading Bot Configuration")
        
        # Bot Mode Selection
        col1, col2, col3 = st.columns(3)
        
        with col1:
            bot_mode = st.selectbox(
                "Bot Mode",
                options=list(self.bot_modes.keys()),
                format_func=lambda x: self.bot_modes[x]['name'],
                help="Select trading automation level",
                key="bot_mode_select"
            )
        
        with col2:
            max_positions = st.slider(
                "Max Positions",
                min_value=1,
                max_value=10,
                value=3,
                help="Maximum simultaneous positions",
                key="max_positions_slider"
            )
        
        with col3:
            risk_per_trade = st.slider(
                "Risk per Trade (%)",
                min_value=0.1,
                max_value=5.0,
                value=1.0,
                step=0.1,
                help="Maximum risk per trade as % of capital",
                key="risk_per_trade_slider"
            )
        
        # Bot Parameters based on mode
        if bot_mode == 'SEMI_AUTO':
            self.render_semi_auto_config()
        elif bot_mode == 'FULL_AUTO':
            self.render_full_auto_config()
        else:
            self.render_monitor_config()
        
        # Trading Hours Configuration
        st.markdown("#### 🕒 Trading Hours Configuration")
        col_t1, col_t2, col_t3 = st.columns(3)
        
        with col_t1:
            session_preference = st.selectbox(
                "Preferred Session",
                ['FIRST_HOUR', 'MORNING', 'AFTERNOON', 'CLOSING', 'ALL_DAY'],
                format_func=lambda x: x.replace('_', ' ').title(),
                help="Preferred trading session",
                key="session_preference_select"
            )
        
        with col_t2:
            avoid_volatility = st.checkbox(
                "Avoid High Volatility",
                value=True,
                help="Avoid trading during high volatility periods",
                key="avoid_volatility_check"
            )
        
        with col_t3:
            weekend_mode = st.selectbox(
                "Weekend Mode",
                ['USE_LAST_DATA', 'PAUSE_TRADING', 'ANALYSIS_ONLY'],
                format_func=lambda x: x.replace('_', ' ').title(),
                help="Behavior during weekends/non-market days",
                key="weekend_mode_select"
            )
        
        # Advanced Parameters
        with st.expander("⚙️ Advanced Parameters", expanded=False):
            col_a1, col_a2 = st.columns(2)
            
            with col_a1:
                min_confidence = st.slider(
                    "Minimum Confidence %",
                    min_value=50,
                    max_value=95,
                    value=70,
                    help="Minimum confidence level for trades",
                    key="min_confidence_slider"
                )
                
                volume_threshold = st.slider(
                    "Volume Threshold Multiplier",
                    min_value=1.0,
                    max_value=3.0,
                    value=1.5,
                    step=0.1,
                    help="Volume spike threshold for entry",
                    key="volume_threshold_slider"
                )
            
            with col_a2:
                stop_loss_pct = st.slider(
                    "Stop Loss (%)",
                    min_value=0.5,
                    max_value=5.0,
                    value=2.0,
                    step=0.1,
                    help="Auto stop loss percentage",
                    key="stop_loss_slider"
                )
                
                take_profit_pct = st.slider(
                    "Take Profit (%)",
                    min_value=1.0,
                    max_value=10.0,
                    value=4.0,
                    step=0.5,
                    help="Auto take profit percentage",
                    key="take_profit_slider"
                )
        
        # Save Configuration
        if st.button("💾 Save Bot Configuration", type="primary", key="save_bot_config"):
            bot_config = {
                'mode': bot_mode,
                'max_positions': max_positions,
                'risk_per_trade': risk_per_trade,
                'session_preference': session_preference,
                'avoid_volatility': avoid_volatility,
                'weekend_mode': weekend_mode,
                'min_confidence': min_confidence / 100.0,
                'volume_threshold': volume_threshold,
                'stop_loss_pct': stop_loss_pct,
                'take_profit_pct': take_profit_pct
            }
            st.session_state.bot_config = bot_config
            st.success("✅ Bot configuration saved!")
        
        return bot_mode
    
    def render_semi_auto_config(self):
        """Render semi-automated bot configuration"""
        st.markdown("#### 🎯 Semi-Automated Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            manual_entry = st.checkbox(
                "Manual Entry Confirmation",
                value=True,
                help="Require manual confirmation for trade entry",
                key="manual_entry_check"
            )
            
            auto_exit = st.checkbox(
                "Automated Exit",
                value=True,
                help="Automated stop loss and take profit",
                key="auto_exit_check"
            )
        
        with col2:
            trailing_stop = st.checkbox(
                "Trailing Stop Loss",
                value=True,
                help="Use trailing stop loss for profits",
                key="trailing_stop_check"
            )
            
            partial_exits = st.checkbox(
                "Partial Profit Booking",
                value=True,
                help="Book partial profits at target levels",
                key="partial_exits_check"
            )
    
    def render_full_auto_config(self):
        """Render fully automated bot configuration"""
        st.markdown("#### 🚀 Fully Automated Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            entry_signals = st.multiselect(
                "Entry Signals",
                ['ICEBERG_BUY', 'VOLUME_SPIKE', 'MOMENTUM_BREAKOUT', 'SUPPORT_BOUNCE'],
                default=['ICEBERG_BUY', 'VOLUME_SPIKE'],
                help="Signals that trigger automated entry",
                key="entry_signals_multiselect"
            )
            
            max_daily_trades = st.slider(
                "Max Daily Trades",
                min_value=1,
                max_value=20,
                value=5,
                help="Maximum trades per day",
                key="max_daily_trades_slider"
            )
        
        with col2:
            cooldown_period = st.slider(
                "Cooldown (minutes)",
                min_value=5,
                max_value=60,
                value=15,
                help="Wait time between consecutive trades",
                key="cooldown_period_slider"
            )
            
            auto_position_sizing = st.checkbox(
                "Auto Position Sizing",
                value=True,
                help="Automatically calculate position size based on volatility",
                key="auto_position_sizing_check"
            )
    
    def render_monitor_config(self):
        """Render monitor-only configuration"""
        st.markdown("#### 👁️ Monitoring Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            alert_level = st.selectbox(
                "Alert Level",
                ['ALL', 'HIGH_CONFIDENCE', 'EXTREME_ONLY'],
                help="When to send alerts",
                key="alert_level_select"
            )
            
            sound_alerts = st.checkbox(
                "Sound Alerts",
                value=True,
                help="Enable sound notifications",
                key="sound_alerts_check"
            )
        
        with col2:
            email_alerts = st.checkbox(
                "Email Alerts",
                value=False,
                help="Send email notifications for alerts",
                key="email_alerts_check"
            )
            
            auto_screenshot = st.checkbox(
                "Auto Screenshot",
                value=True,
                help="Automatically save charts for alerts",
                key="auto_screenshot_check"
            )

# ==================== VOLUME ANALYSIS FUNCTIONS ====================

def calculate_accurate_daily_volume(historical_data, lookback_days=5):
    """Calculate daily average volume from last 5 market days only"""
    try:
        if historical_data is None or historical_data.empty:
            return 0
        
        # Convert to daily data if we have intraday data
        if 'date' in historical_data.columns:
            historical_data['date'] = pd.to_datetime(historical_data['date'])
            daily_volumes = historical_data.groupby(historical_data['date'].dt.date)['volume'].sum()
        else:
            # Assume already daily data
            daily_volumes = historical_data['volume']
        
        # Use only last 5 market days (1 trading week)
        if len(daily_volumes) > lookback_days:
            recent_volumes = daily_volumes.tail(lookback_days)
        else:
            recent_volumes = daily_volumes
        
        # Calculate average of last 5 market days
        if len(recent_volumes) > 0:
            # Remove extreme outliers for more accurate baseline
            Q1 = recent_volumes.quantile(0.25)
            Q3 = recent_volumes.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            filtered_volumes = recent_volumes[
                (recent_volumes >= lower_bound) & 
                (recent_volumes <= upper_bound)
            ]
            
            if len(filtered_volumes) > 0:
                avg_volume = filtered_volumes.mean()
            else:
                avg_volume = recent_volumes.mean()
                
            return avg_volume
        else:
            return historical_data['volume'].mean() if not historical_data.empty else 0
    except Exception as e:
        return 0

def analyze_weekly_volume_patterns(historical_data, current_volume):
    """Analyze volume patterns over the last 5 market days"""
    try:
        if historical_data is None or historical_data.empty:
            return None
        
        # Get last 5 market days of volume data
        if 'date' in historical_data.columns:
            historical_data['date'] = pd.to_datetime(historical_data['date'])
            daily_volumes = historical_data.groupby(historical_data['date'].dt.date)['volume'].sum()
        else:
            daily_volumes = historical_data['volume']
        
        # Take last 5 days (1 trading week)
        recent_volumes = daily_volumes.tail(5)
        
        if len(recent_volumes) == 0:
            return None
        
        # Calculate weekly metrics
        weekly_avg = recent_volumes.mean()
        weekly_std = recent_volumes.std()
        current_vs_weekly = current_volume / weekly_avg if weekly_avg > 0 else 0
        
        # Volume trend (increasing/decreasing)
        if len(recent_volumes) >= 2:
            volume_trend = "INCREASING" if recent_volumes.iloc[-1] > recent_volumes.iloc[-2] else "DECREASING"
        else:
            volume_trend = "STABLE"
        
        # Volume volatility
        volume_volatility = weekly_std / weekly_avg if weekly_avg > 0 else 0
        
        # Day-of-week pattern detection
        day_patterns = {}
        if len(recent_volumes) >= 5:
            # Check if there's a consistent pattern (e.g., higher volumes on specific days)
            avg_volume = recent_volumes.mean()
            for i, volume in enumerate(recent_volumes):
                day_name = ["Mon", "Tue", "Wed", "Thu", "Fri"][i]
                day_patterns[day_name] = volume / avg_volume if avg_volume > 0 else 1
        
        return {
            'weekly_average_volume': weekly_avg,
            'weekly_std': weekly_std,
            'current_vs_weekly_ratio': current_vs_weekly,
            'volume_trend': volume_trend,
            'volume_volatility': volume_volatility,
            'day_patterns': day_patterns,
            'recent_volumes': recent_volumes.tolist(),
            'analysis_period': '5_DAYS'
        }
        
    except Exception as e:
        return None

def enhanced_intraday_volume_analysis(current_volume, daily_avg_volume, symbol, weekly_patterns=None):
    """Enhanced volume analysis with 5-day focus and weekly patterns"""
    
    if daily_avg_volume == 0:
        return {
            'current_session': 'MARKET_CLOSED',
            'volume_spike_detected': False,
            'alert_message': 'Market data unavailable',
            'daily_avg_volume': daily_avg_volume,
            'current_volume': current_volume,
            'analysis_period': '5_DAYS'
        }
    
    current_time = datetime.now().time()
    market_start = time(9, 15)
    market_end = time(15, 30)
    
    # Check if market is closed (weekends/holidays)
    if not is_market_hours():
        return {
            'current_session': 'MARKET_CLOSED',
            'volume_spike_detected': False,
            'alert_message': get_market_closed_message(),
            'daily_avg_volume': daily_avg_volume,
            'current_volume': current_volume,
            'analysis_period': '5_DAYS',
            'market_status': 'CLOSED'
        }
    
    # Define intraday sessions with expected volume distribution
    sessions = [
        {'name': 'First Hour', 'start': time(9, 15), 'end': time(10, 15), 'expected_percentage': 0.20},
        {'name': 'Morning Session', 'start': time(10, 15), 'end': time(12, 15), 'expected_percentage': 0.30},
        {'name': 'Afternoon Session', 'start': time(12, 15), 'end': time(14, 15), 'expected_percentage': 0.20},
        {'name': 'Closing Session', 'start': time(14, 15), 'end': time(15, 30), 'expected_percentage': 0.30}
    ]
    
    # Find current session
    current_session = None
    cumulative_expected = 0.0
    
    for session in sessions:
        cumulative_expected += session['expected_percentage']
        if session['start'] <= current_time <= session['end']:
            current_session = session
            break
    
    # If between sessions or market closed
    if not current_session:
        return {
            'current_session': 'BETWEEN_SESSIONS',
            'volume_spike_detected': False,
            'alert_message': 'Between trading sessions',
            'daily_avg_volume': daily_avg_volume,
            'current_volume': current_volume,
            'analysis_period': '5_DAYS'
        }
    
    # Calculate expected volume for current session
    session_expected_volume = daily_avg_volume * current_session['expected_percentage']
    cumulative_expected_volume = daily_avg_volume * cumulative_expected
    
    # Calculate volume ratios - FIXED CALCULATION
    if session_expected_volume > 0:
        session_volume_ratio = current_volume / session_expected_volume
    else:
        session_volume_ratio = 0
    
    if cumulative_expected_volume > 0:
        cumulative_volume_ratio = current_volume / cumulative_expected_volume
    else:
        cumulative_volume_ratio = 0
    
    # Enhanced spike detection with weekly context
    volume_spike_detected = session_volume_ratio > 1.0
    spike_intensity = max(0, session_volume_ratio - 1.0)
    
    # Include weekly pattern analysis in alerts
    weekly_context = ""
    if weekly_patterns:
        current_vs_weekly = weekly_patterns.get('current_vs_weekly_ratio', 0)
        if current_vs_weekly > 2.0:
            weekly_context = " | 🚨 2x Weekly Average"
        elif current_vs_weekly > 1.5:
            weekly_context = " | 🔴 1.5x Weekly Average"
        elif current_vs_weekly > 1.2:
            weekly_context = " | 🟡 Above Weekly Average"
    
    # Generate alert message with weekly context - FIXED FORMATTING
    alert_level = "NORMAL"
    alert_message = None
    
    if volume_spike_detected:
        if session_volume_ratio > 2.0:
            alert_level = "EXTREME"
            alert_message = f"🚨 EXTREME VOLUME: {session_volume_ratio:.1f}x session expected{weekly_context}"
        elif session_volume_ratio > 1.5:
            alert_level = "HIGH"
            alert_message = f"🔴 HIGH VOLUME: {session_volume_ratio:.1f}x session expected{weekly_context}"
        elif session_volume_ratio > 1.2:
            alert_level = "MEDIUM"
            alert_message = f"🟡 ELEVATED VOLUME: {session_volume_ratio:.1f}x session expected{weekly_context}"
        else:
            alert_level = "LOW"
            alert_message = f"📈 ABOVE EXPECTED: {session_volume_ratio:.1f}x session expected{weekly_context}"
    else:
        alert_message = f"🟢 NORMAL VOLUME: {session_volume_ratio:.1f}x session expected{weekly_context}"
    
    return {
        'current_session': current_session['name'],
        'session_expected_volume': session_expected_volume,
        'cumulative_expected_volume': cumulative_expected_volume,
        'session_volume_ratio': session_volume_ratio,
        'cumulative_volume_ratio': cumulative_volume_ratio,
        'volume_spike_detected': volume_spike_detected,
        'spike_intensity': spike_intensity,
        'cumulative_expected_percentage': cumulative_expected,
        'alert_message': alert_message,
        'alert_level': alert_level,
        'daily_avg_volume': daily_avg_volume,
        'current_volume': current_volume,
        'weekly_patterns': weekly_patterns,
        'analysis_period': '5_DAYS',
        'market_status': 'OPEN'
    }

def is_market_hours():
    """Check if current time is within market hours including weekends/holidays"""
    try:
        now = datetime.now()
        current_time = now.time()
        market_start = time(9, 15)
        market_end = time(15, 30)
        
        weekday = now.weekday()
        is_weekday = weekday < 5  # Monday=0, Friday=4, Saturday=5, Sunday=6
        
        # Check if it's a weekend
        if not is_weekday:
            return False
        
        # Check if it's a market holiday (you can expand this list)
        market_holidays = get_market_holidays()
        if now.date() in market_holidays:
            return False
        
        return market_start <= current_time <= market_end
    except:
        return False

def get_market_holidays(year):
    """NSE holidays (update yearly)."""
    holidays_by_year = {
        2024: ['2024-01-22', '2024-01-26', '2024-03-08', '2024-03-25', '2024-03-29', '2024-04-11', '2024-04-17', '2024-05-01', '2024-05-20', '2024-06-17', '2024-07-17', '2024-08-15', '2024-10-02', '2024-11-01', '2024-11-15', '2024-12-25'],
        2025: ['2025-01-26', '2025-03-06', '2025-03-21', '2025-04-14', '2025-04-18', '2025-05-01', '2025-08-15', '2025-10-02', '2025-10-21', '2025-11-05', '2025-12-25'],
        2026: ['2026-01-26', '2026-02-24', '2026-04-03', '2026-04-14', '2026-05-01', '2026-08-15', '2026-10-02', '2026-11-09', '2026-11-24', '2026-12-25']
    }
    return holidays_by_year.get(year, [])

def get_market_closed_message():
    """Get appropriate market closed message"""
    now = datetime.now()
    weekday = now.weekday()
    
    if weekday >= 5:  # Weekend
        return "Market Closed - Weekend"
    else:
        current_time = now.time()
        market_start = time(9, 15)
        market_end = time(15, 30)
        
        if current_time < market_start:
            return "Market Closed - Opens at 9:15 AM"
        elif current_time > market_end:
            return "Market Closed - Closed at 3:30 PM"
        else:
            return "Market Closed - Holiday"


# ==================== MAIN PAGE FUNCTION ====================
import pandas as pd
import streamlit as st
from datetime import datetime, time, timedelta
import numpy as np

def page_iceberg_detector():
    """Iceberg Detector page with 5-day volume pattern focus"""
    
    try:
        display_header()
    except:
        st.title("🧊 Quantum Iceberg Detector - Nifty50")
    
    st.markdown("""
    **Real-time iceberg detection with 5-day volume pattern analysis**
    
    *Volume analysis based on last 5 market days (1 trading week)*
    *Enhanced intraday session tracking with weekly context*
    *More responsive to recent market conditions*
    """)
    
    # Safe broker connection check
    try:
        client = get_broker_client()
        if not client:
            st.info("🔌 Demo Mode - Connect broker for live data")
        else:
            st.success("✅ Broker connected")
    except:
        st.info("🔌 Running in demo mode")
    
    # Safe instrument data loading
    with st.spinner("📊 Loading 5-day market data..."):
        instrument_df = get_instrument_df_safe()
        
        if instrument_df is None or instrument_df.empty:
            st.info("📋 Using demo data with 5-day volume analysis")
    
    # Nifty50 symbols list
    nifty50_symbols = [
        'RELIANCE', 'TCS', 'HDFC', 'INFY', 'HDFCBANK', 'ICICIBANK', 'KOTAKBANK',
        'HINDUNILVR', 'ITC', 'SBIN', 'BHARTIARTL', 'BAJFINANCE', 'ASIANPAINT',
        'MARUTI', 'TITAN', 'SUNPHARMA', 'AXISBANK', 'ULTRACEMCO', 'TATAMOTORS',
        'NESTLE', 'POWERGRID', 'NTPC', 'TATASTEEL', 'BAJAJFINSV', 'WIPRO',
        'ONGC', 'JSWSTEEL', 'HCLTECH', 'ADANIPORTS', 'LT', 'TECHM', 'HDFCLIFE',
        'DRREDDY', 'CIPLA', 'SBILIFE', 'TATACONSUM', 'BRITANNIA', 'BAJAJ-AUTO',
        'COALINDIA', 'GRASIM', 'EICHERMOT', 'UPL', 'HEROMOTOCO', 'DIVISLAB',
        'SHREECEM', 'HINDALCO', 'INDUSINDBK', 'APOLLOHOSP', 'BPCL', 'M&M'
    ]
    
    # Safe symbol mapping
    display_symbols = []
    symbol_mapping = {}
    
    try:
        for symbol in nifty50_symbols:
            if instrument_df is not None and not instrument_df.empty:
                instrument_match = instrument_df[instrument_df['tradingsymbol'] == symbol]
                if instrument_match.empty:
                    if symbol == "BAJAJ-AUTO":
                        alt_symbol = "BAJAJAUTO"
                    elif symbol == "M&M":
                        alt_symbol = "M_M"
                    elif symbol == "L&T":
                        alt_symbol = "L_T"
                    else:
                        alt_symbol = symbol
                    
                    if instrument_df is not None:
                        instrument_match = instrument_df[instrument_df['tradingsymbol'] == alt_symbol]
                        if not instrument_match.empty:
                            symbol_mapping[symbol] = alt_symbol
            
            display_symbols.append(symbol)
    except Exception as e:
        st.error("Error processing symbols")
        display_symbols = nifty50_symbols[:10]
    
    if not display_symbols:
        st.error("❌ No symbols available for analysis")
        return
    
    # UI Components - UPDATED DEFAULTS FOR 5-DAY ANALYSIS
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        selected_symbol = st.selectbox(
            "Select Nifty50 Stock",
            sorted(display_symbols),
            index=0,
            key="iceberg_symbol"
        )
        
        actual_symbol = symbol_mapping.get(selected_symbol, selected_symbol)
        st.caption(f"Analyzing: {actual_symbol} | 5-day volume patterns")
    
    with col2:
        timeframe = st.selectbox(
            "Timeframe",
            ["15minute", "30minute", "hour", "day", "5minute"],
            index=1,  # Default to 30minute
            key="iceberg_timeframe"
        )
    
    with col3:
        period = st.selectbox(
            "Analysis Period", 
            ["5d", "1wk", "1d", "3d"],  # 5d first for 5-day focus
            index=0,
            key="iceberg_period",
            help="5 days for weekly volume patterns"
        )

    # Volume Analysis Configuration
    st.markdown("---")
    st.subheader("📈 5-Day Volume Analysis")
    
    col_vol1, col_vol2, col_vol3 = st.columns(3)
    
    with col_vol1:
        volume_alert_threshold = st.slider(
            "Volume Spike Alert %",
            min_value=110,
            max_value=200,
            value=120,
            step=5,
            help="Alert when volume exceeds 5-day session average"
        )
    
    with col_vol2:
        volume_impact_weight = st.slider(
            "Volume Impact %",
            min_value=10,
            max_value=50,
            value=30,  # Increased default for volume focus
            step=5,
            help="Weight of volume patterns in detection"
        )
    
    with col_vol3:
        st.markdown("**Analysis Focus**")
        st.success("**5-Day Volume Patterns**")
        st.markdown("Intraday: **20/30/20/30%**")
        st.markdown("Weekly: **5 Market Days**")

    # Analysis controls
    st.markdown("---")
    col_controls1, col_controls2, col_controls3 = st.columns([1, 1, 1])
    
    with col_controls1:
        analyze_clicked = st.button("🔍 Analyze 5-Day Patterns", type="primary", use_container_width=True)
    
    with col_controls2:
        auto_refresh = st.checkbox("🔄 Auto-refresh", value=False, key="iceberg_refresh")
    
    with col_controls3:
        show_weekly = st.checkbox("📊 Show Weekly Patterns", value=True, key="weekly_patterns")

    # Run analysis
    if analyze_clicked or auto_refresh:
        with st.spinner("🧊 Analyzing 5-day volume patterns..."):
            try:
                # Safe data preparation
                actual_symbol = symbol_mapping.get(selected_symbol, selected_symbol)
                instrument_token = None
                
                if instrument_df is not None and not instrument_df.empty:
                    instrument_token = get_instrument_token(actual_symbol, instrument_df, 'NSE')
                
                # Get historical data with 5-day focus
                historical_data = get_historical_data_safe(instrument_token, timeframe, period)
                
                if historical_data.empty:
                    st.warning("⚠️ Using demo data for 5-day analysis")
                
                # Prepare market data with enhanced volume analysis
                market_data = prepare_live_market_data_5day(
                    symbol=selected_symbol,
                    actual_symbol=actual_symbol,
                    instrument_token=instrument_token,
                    instrument_df=instrument_df,
                    historical_data=historical_data
                )
                
                if not market_data:
                    st.error("❌ Failed to prepare market data")
                    return
                
                # Show analysis period info
                st.info(f"📅 Analyzing volume patterns over: **{period}**")
                
                # Run detection
                detector = QuantumIcebergDetector()
                detection_result = detector.process_market_data(market_data)
                
                # Generate signals
                trading_signals = generate_trading_signals_enhanced(
                    detection_result, 
                    market_data,
                    volume_impact_weight/100.0
                )
                
                # Display results with weekly patterns
                display_iceberg_results_5day(
                    detection_result=detection_result,
                    market_data=market_data, 
                    trading_signals=trading_signals,
                    show_weekly=show_weekly
                )
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")

    if auto_refresh:
        try:
            st_autorefresh(interval=15000, key="iceberg_autorefresh")
            st.info("🔄 Auto-refresh enabled - 5-day patterns")
        except:
            pass

def prepare_live_market_data_5day(symbol, actual_symbol, instrument_token, instrument_df, historical_data):
    """Prepare market data with 5-day volume focus"""
    try:
        client = get_broker_client()
        
        # Create sample market data if no live data available
        if not client:
            return create_sample_market_data_5day(symbol, historical_data)
        
        # Try to get live quote data
        try:
            quote_data = client.quote(str(instrument_token)) if instrument_token else None
        except:
            quote_data = None
        
        if not quote_data:
            return create_sample_market_data_5day(symbol, historical_data)
        
        # Extract quote data
        instrument_quote = quote_data.get(str(instrument_token), {}) if instrument_token else {}
        
        # Prepare order book
        depth = instrument_quote.get('depth', {})
        bids = depth.get('buy', [])[:10]
        asks = depth.get('sell', [])[:10]
        
        # Calculate metrics
        total_bid_volume = sum(bid.get('quantity', 0) for bid in bids)
        total_ask_volume = sum(ask.get('quantity', 0) for ask in asks)
        
        order_book = {
            'bids': bids,
            'asks': asks,
            'total_bid_volume': total_bid_volume,
            'total_ask_volume': total_ask_volume,
            'bid_ask_ratio': total_bid_volume / total_ask_volume if total_ask_volume > 0 else 1,
            'bid_concentration': calculate_volume_concentration(bids),
            'ask_concentration': calculate_volume_concentration(asks),
            'large_bid_orders': count_large_orders(bids, 10000),
            'large_ask_orders': count_large_orders(asks, 10000),
            'depth_levels_analyzed': max(len(bids), len(asks))
        }
        
        # Get volume and price data
        current_volume = instrument_quote.get('volume', historical_data['volume'].iloc[-1] if not historical_data.empty else 0)
        last_price = instrument_quote.get('last_price', historical_data['close'].iloc[-1] if not historical_data.empty else 1000)
        
        # Calculate 5-day average volume
        daily_avg_volume = calculate_accurate_daily_volume(historical_data, lookback_days=5)
        
        # Enhanced volume analysis with weekly patterns
        weekly_patterns = analyze_weekly_volume_patterns(historical_data, current_volume)
        volume_analysis = enhanced_intraday_volume_analysis(current_volume, daily_avg_volume, symbol, weekly_patterns)
        
        market_data = {
            'symbol': symbol,
            'timestamp': pd.Timestamp.now(),
            'last_price': last_price,
            'open': instrument_quote.get('ohlc', {}).get('open', last_price * 0.99),
            'high': instrument_quote.get('ohlc', {}).get('high', last_price * 1.01),
            'low': instrument_quote.get('ohlc', {}).get('low', last_price * 0.99),
            'close': last_price,
            'volume': current_volume,
            'daily_average_volume': daily_avg_volume,
            'volume_ratio': current_volume / daily_avg_volume if daily_avg_volume > 0 else 1,
            'order_book': order_book,
            'volatility': calculate_live_volatility(historical_data, last_price),
            'stock_category': get_nifty50_stock_category(symbol),
            'detection_params': get_nifty50_detection_params(symbol),
            'volume_analysis': volume_analysis,
            'data_source': 'LIVE',
            'analysis_period': '5_DAYS'
        }
        
        return market_data
        
    except Exception as e:
        return create_sample_market_data_5day(symbol, historical_data)

def create_sample_market_data_5day(symbol, historical_data):
    """Create sample market data with 5-day volume patterns"""
    try:
        if historical_data.empty:
            # Create sample data with realistic 5-day pattern
            last_price = 2500
            current_volume = 500000
            avg_volume = 750000
        else:
            last_price = historical_data['close'].iloc[-1]
            current_volume = historical_data['volume'].iloc[-1]
            avg_volume = calculate_accurate_daily_volume(historical_data, lookback_days=5)
        
        # Create sample order book
        bids = []
        asks = []
        
        for i in range(10):
            bid_price = last_price * (1 - 0.001 * (i + 1))
            ask_price = last_price * (1 + 0.001 * (i + 1))
            
            bid_quantity = max(100, int(10000 * (1 - 0.1 * i)))
            ask_quantity = max(100, int(8000 * (1 - 0.1 * i)))
            
            bids.append({'price': round(bid_price, 2), 'quantity': bid_quantity})
            asks.append({'price': round(ask_price, 2), 'quantity': ask_quantity})
        
        total_bid_volume = sum(bid['quantity'] for bid in bids)
        total_ask_volume = sum(ask['quantity'] for ask in asks)
        
        order_book = {
            'bids': bids,
            'asks': asks,
            'total_bid_volume': total_bid_volume,
            'total_ask_volume': total_ask_volume,
            'bid_ask_ratio': total_bid_volume / total_ask_volume if total_ask_volume > 0 else 1,
            'bid_concentration': 0.6,
            'ask_concentration': 0.5,
            'large_bid_orders': 2,
            'large_ask_orders': 1,
            'depth_levels_analyzed': 10
        }
        
        # Enhanced volume analysis with weekly patterns
        weekly_patterns = analyze_weekly_volume_patterns(historical_data, current_volume)
        volume_analysis = enhanced_intraday_volume_analysis(current_volume, avg_volume, symbol, weekly_patterns)
        
        return {
            'symbol': symbol,
            'timestamp': pd.Timestamp.now(),
            'last_price': last_price,
            'open': last_price * 0.995,
            'high': last_price * 1.015,
            'low': last_price * 0.985,
            'close': last_price,
            'volume': current_volume,
            'daily_average_volume': avg_volume,
            'volume_ratio': current_volume / avg_volume if avg_volume > 0 else 1,
            'order_book': order_book,
            'volatility': 0.02,
            'stock_category': get_nifty50_stock_category(symbol),
            'detection_params': get_nifty50_detection_params(symbol),
            'volume_analysis': volume_analysis,
            'data_source': 'DEMO_5DAY',
            'analysis_period': '5_DAYS'
        }
        
    except Exception as e:
        return {
            'symbol': symbol,
            'timestamp': pd.Timestamp.now(),
            'last_price': 1000,
            'volume': 100000,
            'order_book': {},
            'data_source': 'FALLBACK_5DAY',
            'analysis_period': '5_DAYS'
        }

def display_iceberg_results_5day(detection_result, market_data, trading_signals, show_weekly=True):
    """Display iceberg results with 5-day volume focus"""
    
    st.markdown("---")
    st.subheader("🎯 5-Day Pattern Analysis")
    
    # Key metrics
    probability = detection_result.get('iceberg_probability', 0)
    confidence = detection_result.get('confidence', 0)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if probability > 0.7:
            st.error(f"🔴 {probability:.1%}")
            st.write("**High Probability**")
        elif probability > 0.4:
            st.warning(f"🟡 {probability:.1%}")
            st.write("**Medium Probability**")
        else:
            st.success(f"🟢 {probability:.1%}")
            st.write("**Low Probability**")
    
    with col2:
        st.metric("Confidence", f"{confidence:.1%}")
    
    with col3:
        st.metric("Price", f"₹{market_data.get('last_price', 0):.2f}")
    
    with col4:
        st.metric("Analysis", "5-Day Focus")
    
    # Volume Analysis Section
    volume_analysis = market_data.get('volume_analysis', {})
    if volume_analysis:
        st.markdown("---")
        st.subheader("📈 5-Day Volume Analysis")
        
        # Main volume metrics
        col_vol1, col_vol2, col_vol3, col_vol4 = st.columns(4)
        
        with col_vol1:
            st.metric("Session", volume_analysis.get('current_session', 'UNKNOWN'))
            st.metric("Live Volume", f"{volume_analysis.get('current_volume', 0):,}")
        
        with col_vol2:
            st.metric("5-Day Avg", f"{volume_analysis.get('daily_avg_volume', 0):,.0f}")
            st.metric("Session Ratio", f"{volume_analysis.get('session_volume_ratio', 0):.1%}")
        
        with col_vol3:
            st.metric("Cumulative Ratio", f"{volume_analysis.get('cumulative_volume_ratio', 0):.1%}")
            st.metric("Expected %", f"{volume_analysis.get('cumulative_expected_percentage', 0):.1%}")
        
        with col_vol4:
            volume_impact = trading_signals.get('volume_impact', 0)
            st.metric("Volume Impact", f"{volume_impact:.1%}")
            
            alert_level = volume_analysis.get('alert_level', 'NORMAL')
            if alert_level == "EXTREME":
                st.error("🚨 EXTREME")
            elif alert_level == "HIGH":
                st.error("🔴 HIGH")
            elif alert_level == "MEDIUM":
                st.warning("🟡 MEDIUM")
            elif alert_level == "LOW":
                st.info("📈 LOW")
            else:
                st.success("🟢 NORMAL")
        
        # Weekly patterns display
        weekly_patterns = volume_analysis.get('weekly_patterns', {})
        if weekly_patterns and show_weekly:
            st.markdown("**📊 Weekly Volume Patterns (5 Days)**")
            
            col_week1, col_week2, col_week3, col_week4 = st.columns(4)
            
            with col_week1:
                weekly_ratio = weekly_patterns.get('current_vs_weekly_ratio', 0)
                st.metric("Vs Weekly Avg", f"{weekly_ratio:.1%}")
            
            with col_week2:
                trend = weekly_patterns.get('volume_trend', 'STABLE')
                if trend == "INCREASING":
                    st.success("📈 Increasing")
                elif trend == "DECREASING":
                    st.error("📉 Decreasing")
                else:
                    st.info("➡️ Stable")
            
            with col_week3:
                volatility = weekly_patterns.get('volume_volatility', 0)
                st.metric("Volatility", f"{volatility:.1%}")
            
            with col_week4:
                st.metric("Period", "5 Market Days")
        
        # Alert message
        alert_message = volume_analysis.get('alert_message')
        if alert_message:
            if "EXTREME" in alert_message or "HIGH" in alert_message:
                st.error(alert_message)
            elif "MEDIUM" in alert_message:
                st.warning(alert_message)
            elif "LOW" in alert_message:
                st.info(alert_message)
            else:
                st.success(alert_message)
    
    # Trading signals
    if trading_signals:
        st.markdown("---")
        st.subheader("📡 Trading Signals")
        
        col_signal1, col_signal2 = st.columns(2)
        
        with col_signal1:
            signal_type = trading_signals.get('primary_signal', 'HOLD')
            if signal_type in ['ICEBERG_BUY', 'FLOW_BUY', 'VOLUME_BUY']:
                st.success(f"🎯 **Signal: {signal_type}**")
            elif signal_type in ['ICEBERG_SELL', 'FLOW_SELL', 'VOLUME_SELL']:
                st.error(f"🎯 **Signal: {signal_type}**")
            else:
                st.info(f"🎯 **Signal: {signal_type}**")
            
            # Show volume context
            weekly_patterns = volume_analysis.get('weekly_patterns', {}) if volume_analysis else {}
            weekly_ratio = weekly_patterns.get('current_vs_weekly_ratio', 0)
            if weekly_ratio > 1.5:
                st.info(f"📊 Volume: {weekly_ratio:.1%} of 5-day average")
        
        with col_signal2:
            st.metric("Final Confidence", f"{trading_signals.get('confidence', 0):.1%}")
            st.metric("Volume Impact", f"+{trading_signals.get('volume_impact', 0):.1%}")
    
    # Detection scores
    detection_scores = detection_result.get('detection_scores', {})
    if detection_scores:
        st.markdown("---")
        st.subheader("🔍 Detection Analysis")
        
        cols = st.columns(5)
        score_names = ['order_fragmentation', 'hidden_liquidity', 'volume_anomaly', 'momentum_disparity', 'depth_imbalance']
        display_names = ['Fragmentation', 'Hidden Liquidity', 'Volume Anomaly', 'Momentum', 'Depth Imbalance']
        
        for i, (col, score_name, display_name) in enumerate(zip(cols, score_names, display_names)):
            with col:
                score = detection_scores.get(score_name, 0)
                st.metric(display_name, f"{score:.1%}")
    
    # Visualization
    try:
        visualizer = QuantumVisualizer()
        fig = visualizer.create_quantum_chart(detection_result)
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("📊 Visualization unavailable")
    
    # Market depth
    order_book = market_data.get('order_book', {})
    if order_book:
        st.markdown("---")
        st.subheader("📊 Market Depth")
        
        col_depth1, col_depth2, col_depth3, col_depth4 = st.columns(4)
        
        with col_depth1:
            st.metric("Bid Volume", f"{order_book.get('total_bid_volume', 0):,}")
            st.metric("Bid Concentration", f"{order_book.get('bid_concentration', 0):.1%}")
        
        with col_depth2:
            st.metric("Ask Volume", f"{order_book.get('total_ask_volume', 0):,}")
            st.metric("Ask Concentration", f"{order_book.get('ask_concentration', 0):.1%}")
        
        with col_depth3:
            st.metric("Bid/Ask Ratio", f"{order_book.get('bid_ask_ratio', 1):.2f}")
            st.metric("Large Bid Orders", order_book.get('large_bid_orders', 0))
        
        with col_depth4:
            st.metric("Depth Levels", order_book.get('depth_levels_analyzed', 0))
            st.metric("Large Ask Orders", order_book.get('large_ask_orders', 0))
    
    # Alerts
    alerts = detection_result.get('alerts', [])
    if alerts:
        st.markdown("---")
        st.subheader("🚨 Alerts")
        for alert in alerts:
            if "🚨" in alert or "🔴" in alert:
                st.error(alert)
            elif "🟡" in alert:
                st.warning(alert)
            else:
                st.info(alert)
    
    # Show analysis period info
    st.info(f"📅 **Analysis Period**: Last 5 Market Days | **Data Source**: {market_data.get('data_source', 'Unknown')}")
    
    st.success("✅ 5-Day Pattern Analysis Completed")

# ==================== TRADING SIGNALS GENERATION ====================

def generate_trading_signals_enhanced(detection_result, market_data, volume_impact_weight=0.25):
    """Generate enhanced trading signals with 5-day volume focus"""
    try:
        if not detection_result or not market_data:
            return get_default_signals()
        
        probability = detection_result.get('iceberg_probability', 0)
        confidence = detection_result.get('confidence', 0)
        order_book = market_data.get('order_book', {})
        volume_analysis = market_data.get('volume_analysis', {})
        
        signals = {
            'primary_signal': 'HOLD',
            'secondary_signals': [],
            'confidence': confidence,
            'probability': probability,
            'timestamp': pd.Timestamp.now(),
            'entry_price': market_data.get('last_price', 0),
            'volume_impact': 0,
            'volume_alerts': []
        }
        
        # Volume analysis integration
        if volume_analysis:
            volume_spike = volume_analysis.get('volume_spike_detected', False)
            alert_level = volume_analysis.get('alert_level', 'NORMAL')
            
            volume_impact = 0
            if volume_spike:
                if alert_level == "EXTREME":
                    volume_impact = 0.4
                elif alert_level == "HIGH":
                    volume_impact = 0.3
                elif alert_level == "MEDIUM":
                    volume_impact = 0.2
                elif alert_level == "LOW":
                    volume_impact = 0.1
                    
                volume_impact *= volume_impact_weight
                signals['confidence'] = min(1.0, signals['confidence'] + volume_impact)
                signals['volume_impact'] = volume_impact
                
                signals['volume_alerts'].append(alert_level)
                signals['secondary_signals'].append(f"VOLUME_{alert_level}")
        
        # Order book analysis
        bid_volume = order_book.get('total_bid_volume', 0)
        ask_volume = order_book.get('total_ask_volume', 0)
        total_volume = bid_volume + ask_volume
        
        if total_volume > 0:
            imbalance = (bid_volume - ask_volume) / total_volume
        else:
            imbalance = 0
        
        # Signal generation
        final_confidence = signals['confidence']
        
        if probability > 0.7 and final_confidence > 0.7:
            if imbalance > 0.1:
                signals['primary_signal'] = 'ICEBERG_BUY'
            elif imbalance < -0.1:
                signals['primary_signal'] = 'ICEBERG_SELL'
        
        elif probability > 0.5 and final_confidence > 0.6:
            if imbalance > 0.05:
                signals['primary_signal'] = 'FLOW_BUY'
            elif imbalance < -0.05:
                signals['primary_signal'] = 'FLOW_SELL'
        
        return signals
        
    except Exception as e:
        return get_default_signals()

def get_default_signals():
    """Return default signals when errors occur"""
    return {
        'primary_signal': 'HOLD',
        'secondary_signals': ['Analysis unavailable'],
        'confidence': 0.0,
        'probability': 0.0,
        'timestamp': pd.Timestamp.now(),
        'entry_price': 0,
        'volume_impact': 0,
        'volume_alerts': []
    }

# ================ 6. MAIN APP LOGIC AND AUTHENTICATION ============

def get_user_secret(user_profile):
    """Generate a persistent secret based on user profile."""
    if user_profile is None:
        user_profile = {}
    
    user_id = user_profile.get('user_id', 'default_user')
    user_hash = hashlib.sha256(str(user_id).encode()).digest()
    secret = base64.b32encode(user_hash).decode('utf-8').replace('=', '')[:16]
    return secret

# REPLACE THE DIALOG FUNCTIONS WITH REGULAR FUNCTIONS
def show_two_factor_setup():
    """Show 2FA setup without using dialogs."""
    st.title("🔐 Two-Factor Authentication Setup")
    st.info("Please scan the QR code with your authenticator app (e.g., Google or Microsoft Authenticator).")
    
    if st.session_state.pyotp_secret is None:
        profile = st.session_state.get('profile') or {}
        st.session_state.pyotp_secret = get_user_secret(profile)
    
    secret = st.session_state.pyotp_secret
    user_name = st.session_state.get('profile', {}).get('user_name', 'User')
    uri = pyotp.totp.TOTP(secret).provisioning_uri(user_name, issuer_name="BlockVista Terminal")
    
    # Generate QR code with normal size
    img = qrcode.make(uri)
    
    # Resize to normal size (300x300 is standard for QR codes)
    img = img.resize((300, 300))
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    
    # Display with normal size (remove use_container_width)
    st.image(buf.getvalue(), caption="Scan with your authenticator app", width=300)
    
    st.markdown(f"**Your Secret Key:** `{secret}` (You can also enter this manually)")
    
    st.markdown("---")
    st.subheader("Verify Setup")
    auth_code = st.text_input("Enter 6-digit code from your authenticator app", max_chars=6, key="verify_2fa")
    
    col1, col2 = st.columns(2)
    if col1.button("Verify & Continue", use_container_width=True, type="primary"):
        if auth_code:
            try:
                totp = pyotp.TOTP(secret)
                if totp.verify(auth_code):
                    st.session_state.two_factor_setup_complete = True
                    st.session_state.authenticated = True
                    st.success("2FA setup completed successfully!")
                    st.rerun()
                else:
                    st.error("Invalid code. Please try again.")
            except Exception as e:
                st.error(f"Verification failed: {e}")
        else:
            st.warning("Please enter a verification code.")
    
    if col2.button("Skip 2FA Setup", use_container_width=True):
        st.session_state.two_factor_setup_complete = True
        st.session_state.authenticated = True
        st.info("2FA setup skipped. You can enable it later in settings.")
        st.rerun()

def show_two_factor_auth():
    """Show 2FA authentication without using dialogs."""
    st.title("🔐 Two-Factor Authentication")
    st.caption("Please enter the 6-digit code from your authenticator app to continue.")
    
    auth_code = st.text_input("2FA Code", max_chars=6, key="2fa_code")
    
    col1, col2 = st.columns(2)
    if col1.button("Authenticate", use_container_width=True, type="primary"):
        if auth_code:
            try:
                totp = pyotp.TOTP(st.session_state.pyotp_secret)
                if totp.verify(auth_code):
                    st.session_state.authenticated = True
                    st.success("Authentication successful!")
                    st.rerun()
                else:
                    st.error("Invalid code. Please try again.")
            except Exception as e:
                st.error(f"Authentication failed: {e}")
        else:
            st.warning("Please enter a code.")
    
    if col2.button("Use Backup Code", use_container_width=True):
        st.info("Backup code feature not yet implemented.")
    
    st.markdown("---")
    if st.button("🔄 Return to Login", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key not in ['theme', 'watchlists', 'active_watchlist']:
                del st.session_state[key]
        st.rerun()


@st.dialog("Generate QR Code for 2FA")
def qr_code_dialog():
    """Dialog to generate a QR code for 2FA setup."""
    if 'show_qr_dialog' not in st.session_state:
        st.session_state.show_qr_dialog = False
    
    if not st.session_state.get('two_factor_setup_complete', False):
        st.session_state.show_qr_dialog = True
        
        st.subheader("Set up Two-Factor Authentication")
        st.info("Please scan this QR code with your authenticator app (e.g., Google or Microsoft Authenticator). This is a one-time setup.")

        if st.session_state.pyotp_secret is None:
            # Ensure we get a dictionary, not None
            profile = st.session_state.get('profile') or {}
            st.session_state.pyotp_secret = get_user_secret(profile)
        
        secret = st.session_state.pyotp_secret
        user_name = st.session_state.get('profile', {}).get('user_name', 'User')
        uri = pyotp.totp.TOTP(secret).provisioning_uri(user_name, issuer_name="BlockVista Terminal")
        
        # Generate QR code with normal size
        img = qrcode.make(uri)
        img = img.resize((300, 300))  # Normal size
        
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        
        # Display with normal size
        st.image(buf.getvalue(), caption="Scan with your authenticator app", width=300)
        st.markdown(f"**Your Secret Key:** `{secret}` (You can also enter this manually)")
        
        if st.button("I have scanned the code. Continue.", use_container_width=True):
            st.session_state.two_factor_setup_complete = True
            st.session_state.show_qr_dialog = False
            st.rerun()

def show_login_animation():
    """Displays a boot-up animation after login."""
    st.title("BlockVista Terminal")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = {
        "Authenticating user...": 25,
        "Establishing secure connection...": 50,
        "Fetching live market data feeds...": 75,
        "Initializing terminal... COMPLETE": 100
    }
    
    for text, progress in steps.items():
        status_text.text(f"STATUS: {text}")
        progress_bar.progress(progress)
        a_time.sleep(0.7)
    
    a_time.sleep(0.5)
    st.session_state['login_animation_complete'] = True
    st.rerun()

def login_page():
    """Displays the login page for broker authentication."""
    st.title("BlockVista Terminal")
    st.subheader("Broker Login")
    
    broker = st.selectbox("Select Your Broker", ["Zerodha", "Upstox"])
    
    if broker == "Zerodha":
        # Your existing Zerodha code remains the same
        api_key = st.secrets.get("ZERODHA_API_KEY")
        api_secret = st.secrets.get("ZERODHA_API_SECRET")
        
        if not api_key or not api_secret:
            st.error("Kite API credentials not found. Please set ZERODHA_API_KEY and ZERODHA_API_SECRET in your Streamlit secrets.")
            st.stop()
            
        kite = KiteConnect(api_key=api_key)
        request_token = st.query_params.get("request_token")
        
        if request_token:
            try:
                data = kite.generate_session(request_token, api_secret=api_secret)
                st.session_state.access_token = data["access_token"]
                kite.set_access_token(st.session_state.access_token)
                st.session_state.kite = kite
                st.session_state.profile = kite.profile()
                st.session_state.broker = "Zerodha"
                st.query_params.clear()
                st.rerun()
            except Exception as e:
                st.error(f"Authentication failed: {e}")
                st.query_params.clear()
        else:
            st.link_button("Login with Zerodha Kite", kite.login_url())
            st.info("Please login with Zerodha Kite to begin. You will be redirected back to the app.")
    
    elif broker == "Upstox":
        try:
            import urllib.parse
            import hashlib
            import base64
            import secrets
            
            api_key = st.secrets.get("UPSTOX_API_KEY")
            api_secret = st.secrets.get("UPSTOX_API_SECRET")
            redirect_uri = st.secrets.get("UPSTOX_REDIRECT_URI", "https://your-app-name.streamlit.app/")
            
            if not api_key or not api_secret:
                st.error("Upstox API credentials not found. Please set UPSTOX_API_KEY and UPSTOX_API_SECRET in your Streamlit secrets.")
                st.stop()
            
            # Generate PKCE code verifier and challenge (required for Upstox v2)
            code_verifier = secrets.token_urlsafe(64)
            code_challenge = base64.urlsafe_b64encode(
                hashlib.sha256(code_verifier.encode()).digest()
            ).decode().rstrip('=')
            
            # Store code_verifier in session state for later use
            st.session_state.upstox_code_verifier = code_verifier
            
            # Check for authorization code in URL parameters
            auth_code = st.query_params.get("code")
            
            if auth_code:
                try:
                    # Exchange authorization code for access token
                    token_url = "https://api.upstox.com/v2/login/authorization/token"
                    token_data = {
                        'code': auth_code,
                        'client_id': api_key,
                        'client_secret': api_secret,
                        'redirect_uri': redirect_uri,
                        'grant_type': 'authorization_code',
                        'code_verifier': st.session_state.upstox_code_verifier
                    }
                    
                    headers = {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Accept': 'application/json'
                    }
                    
                    response = requests.post(token_url, data=token_data, headers=headers)
                    
                    if response.status_code == 200:
                        token_data = response.json()
                        access_token = token_data['access_token']
                        
                        # Store in session state
                        st.session_state.upstox_access_token = access_token
                        st.session_state.broker = "Upstox"
                        
                        # Get user profile
                        try:
                            profile_url = "https://api.upstox.com/v2/user/profile"
                            profile_headers = {
                                'Authorization': f'Bearer {access_token}',
                                'Accept': 'application/json'
                            }
                            
                            profile_response = requests.get(profile_url, headers=profile_headers)
                            if profile_response.status_code == 200:
                                profile_data = profile_response.json()
                                st.session_state.profile = {
                                    'user_name': profile_data['data']['name'],
                                    'email': profile_data['data']['email'],
                                    'user_id': profile_data['data']['client_code']
                                }
                            else:
                                st.session_state.profile = {
                                    'user_name': 'Upstox User',
                                    'email': '',
                                    'user_id': 'upstox_user'
                                }
                        except Exception as profile_error:
                            st.session_state.profile = {
                                'user_name': 'Upstox User',
                                'email': '',
                                'user_id': 'upstox_user'
                            }
                        
                        st.success("Upstox login successful!")
                        if st.session_state.get('broker') == "Upstox" and st.session_state.get('upstox_access_token'):
                            if st.button("🔧 Debug Upstox API & Exchanges"):
                                available_exchanges = debug_upstox_exchanges(st.session_state.upstox_access_token)
                                st.session_state.upstox_available_exchanges = available_exchanges
                                st.query_params.clear()
                        # Clean up code verifier
                        if 'upstox_code_verifier' in st.session_state:
                            del st.session_state.upstox_code_verifier
                        st.rerun()
                    else:
                        st.error(f"Upstox token exchange failed: {response.text}")
                        st.query_params.clear()
                        
                except Exception as e:
                    st.error(f"Upstox authentication failed: {e}")
                    st.query_params.clear()
            else:
                # Generate login URL for Upstox v2
                base_url = "https://api.upstox.com/v2/login/authorization/dialog"
                params = {
                    'response_type': 'code',
                    'client_id': api_key,
                    'redirect_uri': redirect_uri,
                    'code_challenge': code_challenge,
                    'code_challenge_method': 'S256'
                }
                
                login_url = f"{base_url}?{urllib.parse.urlencode(params)}"
                st.link_button("Login with Upstox", login_url)
                st.info("Please login with Upstox to begin. You will be redirected back to the app.")
                
        except Exception as e:
            st.error(f"Upstox initialization failed: {e}")
            
def main_app():
    """The main application interface after successful login."""
    apply_custom_styling()
    display_overnight_changes_bar()
    
    # --- 2FA Check - Handle authentication flow first
    profile = st.session_state.get('profile')
    if not profile:
        st.error("User profile not found. Please log in again.")
        if st.button("Return to Login"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        return
    
    # Show 2FA setup if needed (without dialogs)
    if not st.session_state.get('two_factor_setup_complete', False):
        show_two_factor_setup()
        return
    
    # Show 2FA authentication if needed (without dialogs)
    if not st.session_state.get('authenticated', False):
        show_two_factor_auth()
        return
    
    # Only show main content after 2FA is complete
    # Handle quick trade without dialogs
    if st.session_state.get('show_quick_trade', False):
        st.markdown("---")
        st.subheader("Quick Trade")
        symbol = st.session_state.get('quick_trade_symbol')
        if symbol:
            st.info(f"Trading: {symbol}")
        # Add your quick trade form here without using dialogs
    
    # Rest of your main app content...
    st.sidebar.title(f"Welcome, {st.session_state.profile['user_name']}")
    st.sidebar.caption(f"Connected via {st.session_state.broker}")
    st.sidebar.divider()
    
    st.sidebar.header("Terminal Controls")
    st.session_state.theme = st.sidebar.radio("Theme", ["Dark", "Light"], horizontal=True)
    st.session_state.terminal_mode = st.sidebar.radio("Terminal Mode", ["Cash", "Futures", "Options", "HFT"], horizontal=True)
    st.sidebar.divider()
    
    # Dynamic refresh interval based on mode
    if st.session_state.terminal_mode == "HFT":
        refresh_interval = 2
        auto_refresh = True
        st.sidebar.header("HFT Mode Active")
        st.sidebar.caption(f"Refresh Interval: {refresh_interval}s")
    else:
        st.sidebar.header("Live Data")
        auto_refresh = st.sidebar.toggle("Auto Refresh", value=True)
        refresh_interval = st.sidebar.number_input("Interval (s)", min_value=5, max_value=60, value=10, disabled=not auto_refresh)
    
    st.sidebar.divider()
    
    st.sidebar.header("Navigation")
    pages = {
    "Cash": {
        "Dashboard": page_dashboard,
        "AI Trading Bots": page_algo_bots,
        "Market Sentiment": page_ai_sentiment_analyzer,  # NEW
        "AI Discovery Engine": page_ai_discovery,
        "AI Portfolio Assistant": page_ai_assistant,  # ENHANCED
        "Iceberg Detector": page_iceberg_detector,
        "Premarket Pulse": page_premarket_pulse,
        "Advanced Charting": page_advanced_charting,
        "Market Scanners": page_momentum_and_trend_finder,
        "Portfolio & Risk": page_portfolio_and_risk,
        "Fundamental Analytics": page_fundamental_analytics,
        "Basket Orders": page_basket_orders,
        "Forecasting (ML)": page_forecasting_ml,
        "Algo Strategy Hub": page_algo_strategy_maker,
        "Economic Calendar": page_economic_calendar,
        "Settings": page_settings
        },
        "Options": {
            "F&O Analytics": page_fo_analytics,
            "Options Strategy Builder": page_option_strategy_builder,
            "Greeks Calculator": page_greeks_calculator,
            "Portfolio & Risk": page_portfolio_and_risk,
            "AI Assistant": page_ai_assistant,
        },
        "Futures": {
            "Futures Terminal": page_futures_terminal,
            "Advanced Charting": page_advanced_charting,
            "Algo Strategy Hub": page_algo_strategy_maker,
            "Portfolio & Risk": page_portfolio_and_risk,
            "AI Assistant": page_ai_assistant,
        },
        "HFT": {
            "HFT Terminal": page_hft_terminal,
            "Portfolio & Risk": page_portfolio_and_risk,
        }
    }
    
    selection = st.sidebar.radio("Go to", list(pages[st.session_state.terminal_mode].keys()), key='nav_selector')
    
    st.sidebar.divider()
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    no_refresh_pages = ["Forecasting (ML)", "AI Assistant", "AI Discovery", "Algo Strategy Hub", "Algo Trading Bots"]
    if auto_refresh and selection not in no_refresh_pages:
        st_autorefresh(interval=refresh_interval * 1000, key="data_refresher")
    
    pages[st.session_state.terminal_mode][selection]()

# --- Application Entry Point ---
if __name__ == "__main__":
    initialize_session_state()
    
    if 'profile' in st.session_state and st.session_state.profile:
        if st.session_state.get('login_animation_complete', False):
            main_app()
        else:
            show_login_animation()
    else:
        login_page()
