import streamlit as st
import requests

# ── Configuration ───────────────────────────────────────
st.set_page_config(page_title="UGC Kernel | Prompt Bridge", layout="wide")

# ── Styling ────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #C9D1D9; }
    .main-header { font-size: 2rem; font-weight: 800; background: -webkit-linear-gradient(#58a6ff, #2ea043); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem; }
    .response-card { background: #161b22; border-left: 4px solid #58a6ff; padding: 10px 15px; margin: 10px 0; border-radius: 6px; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🧬 UGC Prompt Bridge</p>', unsafe_allow_html=True)

# ── User Prompt Input ──────────────────────────────────
prompt = st.text_area("Enter your request for the UGC kernel:", placeholder="e.g., Get balance of 0x449555", height=100)

if st.button("⚡ EXECUTE", type="primary") and prompt.strip():
    st.subheader("⚙️ Execution Trace")
    try:
        with st.spinner("Sending prompt to UGC kernel..."):
            # Safe API call to UGC backend
            response = requests.post(
                "https://itsvelocity-ucg-v1.hf.space/ucg",
                json={"prompt": prompt},  # we just send the prompt
                timeout=15
            )
        
        if response.status_code == 200:
            json_res = response.json()
            
            # Display raw response safely
            st.markdown('<div class="response-card">', unsafe_allow_html=True)
            st.text(json_res.get("response", json_res))
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error(f"UGC kernel returned error {response.status_code}")
    
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")

