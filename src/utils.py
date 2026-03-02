import streamlit as st

def apply_terminal_theme():
    """
    Injects custom CSS for a high-tech dark UI with a focus on data readability.
    """
    st.markdown("""
        <style>
        /* Base Page Styling */
        .stApp {
            background-color: #050505;
            color: #e0e0e0;
        }

        /* Sidebar and Container Styling */
        section[data-testid="stSidebar"] {
            background-color: #0a0a0a;
            border-right: 1px solid #1f1f1f;
        }
        
        div[data-testid="stExpander"] {
            background-color: #0a0a0a;
            border: 1px solid #1f1f1f;
        }

        /* High-Tech Button Styling */
        @keyframes pulse-glow {
            0% { border-color: #00f2ff; box-shadow: 0 0 5px #00f2ff; }
            50% { border-color: #00f2ff; box-shadow: 0 0 15px #00f2ff; }
            100% { border-color: #00f2ff; box-shadow: 0 0 5px #00f2ff; }
        }

        .stButton>button {
            width: 100%;
            background-color: transparent !important;
            color: #00f2ff !important;
            border: 1px solid #00f2ff !important;
            border-radius: 4px !important;
            font-family: 'Courier New', monospace !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            animation: pulse-glow 3s infinite;
        }

        .stButton>button:hover {
            background-color: #00f2ff !important;
            color: #000000 !important;
        }

        /* File Uploader Customization */
        div[data-testid="stFileUploader"] {
            border: 1px dashed #333;
            background-color: #0a0a0a;
            padding: 1rem;
            border-radius: 5px;
        }

        /* Terminal Log Styling */
        .terminal-text {
            color: #00ff41;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            margin: 0;
            line-height: 1.4;
        }

        /* Metric and Dataframe Styling */
        div[data-testid="stMetricValue"] {
            color: #00f2ff !important;
            font-family: 'Courier New', monospace;
        }
        
        .stDataFrame {
            border: 1px solid #1f1f1f;
        }
        </style>
        """, unsafe_allow_html=True)

def print_terminal_log(message):
    """
    Outputs system status updates in a professional terminal format.
    """
    st.markdown(f'<p class="terminal-text">[SYSTEM]: {message}</p>', unsafe_allow_html=True)