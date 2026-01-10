import streamlit as st
import json
import requests

# ── Configuration ───────────────────────────────────────
st.set_page_config(page_title="UGC Kernel | Debug Console", layout="wide", initial_sidebar_state="expanded")

# ── Advanced Styling ────────────────────────────────────
st.markdown("""
<style>
    /* Main background and fonts */
    .stApp { background-color: #0E1117; }
    
    /* Modern Glass Cards */
    .block-container { padding-top: 2rem; }
    .st-emotion-cache-12w0qpk { padding: 1.5rem; border-radius: 15px; border: 1px solid #30363d; background: #161b22; }
    
    /* Execution Trace Styling */
    .trace-card {
        background: #0d1117;
        border-left: 4px solid #58a6ff;
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 4px;
        font-family: 'Source Code Pro', monospace;
    }
    .op-tag { color: #58a6ff; font-weight: 600; text-transform: uppercase; font-size: 0.8rem; }
    
    /* Custom Header */
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#58a6ff, #2ea043);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar Info ────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🛠️ Developer Resources")
    st.info("**UGC Kernel** is a machine-to-machine engine. This UI serves as a human-readable bridge.")
    
    st.markdown("---")
    st.write("TEST ADDRESSES")
    
    st.write("ETH Testnet")
    st.code("0xA34A13e95CE831953e598689e864a97B7DE949eb", language="text")


    st.write("Solana Testnet")
    st.code("75BgVvMNZ8Es1JffEDNYxWNVE2yoBTndLxViARhYWPF", language="text")
    
    
    st.markdown("---")
    st.warning("⚠️ **Mode:** Balance Inquiries Only (Infura/Helius)")

# ── Header ──────────────────────────────────────────────
st.markdown('<p class="main-header">🧬 UGC Execution Kernel</p>', unsafe_allow_html=True)
st.markdown("---")

# ── Layout ──────────────────────────────────────────────
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("🤖 Agent Request")
    
    with st.container(border=True):
        operation = st.selectbox(
            "Kernel Operation Type",
            ["InfuraRPC", "HeliusAPI", "EthereumSigner", "SolanaSigner", "EthereumPayment", "SolanaPayment"],
            help="Select the DAG entry point for the execution engine."
        )
        
        address = st.text_input("Source Address", placeholder="0x... or Base58...")
        
        # Dynamic Fields with Expanders to save vertical space
        to = amount = payload = None
        
        if "Payment" in operation:
            st.markdown("---")
            to = st.text_input("Destination Address")
            amount = st.number_input("Amount", min_value=0.0, format="%.4f")
            
        if "Signer" in operation:
            st.markdown("---")
            payload = st.text_area("Hex Payload", placeholder="0x48656c6c6f...")

        st.markdown(" ")
        run = st.button("⚡ EXECUTE KERNEL", use_container_width=True, type="primary")

with col2:
    st.subheader("🧠 Live Kernel State")
    
    # Building State Object
    state = {k: v for k, v in {"address": address, "to": to, "amount": amount, "payload": payload}.items() if v}
    
    # Visualizing the State
    with st.container(border=True):
        if not state:
            st.write("Kernel Idle: Waiting for agent input parameters...")
        else:
            st.json(state)

    if run:
        st.subheader("⚙️ Execution Trace")
        
        try:
            with st.status("Initializing UGC DAG...", expanded=True) as status:
                st.write("Encoding request for machine-layer...")
                
                response = requests.post(
                    "https://itsvelocity-ucg-v1.hf.space/ucg",
                    json={"operation": operation, "state": state},
                    timeout=15
                )
                
                if response.status_code == 200:
                    json_res = response.json()
                    status.update(label="Kernel Execution Complete", state="complete", expanded=False)
                    
                    # Process Operations
                    executed_ops_raw = json_res.get("executed", "")
                    ops = [op.strip().strip("'") for op in executed_ops_raw.strip("{}").split(",") if op]
                    
                    # Display Ops in a timeline-like fashion
                    for op in ops:
                        st.markdown(f"""
                            <div class="trace-card">
                                <span class="op-tag">Executed</span><br>
                                <code>{op}</code>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # Blockchain link
                    resp_data = json_res.get("response", {})
                    if "tx_hash" in resp_data:
                        st.success(f"**Transaction Confirmed:** `{resp_data['tx_hash']}`")
                    
                    # Show Raw Output in an expander
                    with st.expander("View Raw Response"):
                        st.write(json_res)
                else:
                    status.update(label="Execution Failed", state="error")
                    st.error(f"Kernel returned error: {response.status_code}")

        except Exception as e:
            st.error(f"Kernel Connection Error: {str(e)}")

# ── Footer ──────────────────────────────────────────────
st.divider()
st.caption("UGC Kernel v1.0.4-stable | Deterministic Execution Graph Active")
