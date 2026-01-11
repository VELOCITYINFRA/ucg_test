import streamlit as st
import requests
import json
import time

# ── Configuration & Page Setup ──────────────────────────
st.set_page_config(
    page_title="UCG KERNEL | PROMPT BRIDGE",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Million Dollar Styling (Custom CSS) ──────────────────
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1f2e 0%, #0a0c10 100%);
        color: #E6EDF3;
        font-family: 'Inter', sans-serif;
    }

    /* Header Styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -2px;
        background: linear-gradient(90deg, #58a6ff, #bc85ff, #2ea043);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 5s linear infinite;
        margin-bottom: 0.5rem;
    }
    
    @keyframes shine {
        to { background-position: 200% center; }
    }

    .subtitle {
        color: #8b949e;
        font-size: 1.1rem;
        margin-bottom: 3rem;
        font-weight: 400;
    }

    /* Input Area Styling */
    .stTextArea textarea {
        background-color: rgba(22, 27, 34, 0.5) !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        color: #c9d1d9 !important;
        font-family: 'JetBrains Mono', monospace !important;
        backdrop-filter: blur(10px);
    }
    
    .stTextArea textarea:focus {
        border-color: #58a6ff !important;
        box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.3) !important;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #238636, #2ea043) !important;
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 0.75rem !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(46, 160, 67, 0.4);
    }

    /* Response Card */
    .response-container {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 24px;
        margin-top: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .status-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(88, 166, 255, 0.1);
        color: #58a6ff;
        border: 1px solid rgba(88, 166, 255, 0.2);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────
st.markdown('<h1 class="main-header">UGC KERNEL</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Next-gen bridge for prompt-driven kernel execution.</p>', unsafe_allow_html=True)

# ── Layout ─────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    prompt = st.text_area(
        "SYSTEM PROMPT", 
        placeholder="", 
        height=180,
        label_visibility="collapsed"
    )
    
    btn_col1, btn_col2 = st.columns([1, 2])
    with btn_col1:
        execute = st.button("⚡ RUN KERNEL")

with col2:
    st.info("💡 use this ETH Address: 0xA34A13e95CE831953e598689e864a97B7DE949eb and this SOL Address 75BgVvMNZ8Es1JffEDNYxWNVE2yoBTndLxViARhYWPF to test")

# ── Execution Logic ────────────────────────────────────
if execute and prompt.strip():
    st.divider()
    
    # Visual Progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("Connecting to UGC Node...")
        progress_bar.progress(30)
        
        # Actual API Call
        response = requests.post(
            "https://itsvelocity-ucg-v1.hf.space/ucg",
            json={"prompt": prompt},
            timeout=15
        )
        
        progress_bar.progress(100)
        status_text.text("Execution Complete.")
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()

        if response.status_code == 200:
            json_res = response.json()
            output = json_res.get("response", json_res)
            
            # Display Results in a Professional Card
            st.markdown(f"""
                <div class="response-container">
                    <span class="status-tag">🟢 SUCCESS: KERNEL_ID_{int(time.time())}</span>
                    <h3 style="margin-top:0;">Output Trace</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Pretty print JSON or Text
            st.code(output, language="json" if isinstance(output, (dict, list)) else "markdown")
            
        else:
            st.error(f"Kernel Error: {response.status_code}")
            st.toast("Execution Failed", icon="❌")
            
    except Exception as e:
        st.error(f"Connection Timeout: {str(e)}")
        st.toast("Network Error", icon="⚠️")

# ── Footer ─────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; margin-top: 5rem; color: #484f58; font-size: 0.8rem;">
    UGC Kernel Infrastructure • Powered by Velocity • © 2024
</div>
""", unsafe_allow_html=True)

