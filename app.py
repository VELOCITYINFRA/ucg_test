import streamlit as st
import json
import requests


st.set_page_config(page_title="UGC Kernel", layout="wide")

# ── Styling ─────────────────────────────────────────────
st.markdown("""
<style>
body { background-color: #0f1117; color: #e6e6e6; }
.stButton>button {
    background-color: #5b7cfa;
    color: white;
    border-radius: 10px;
    height: 48px;
    font-size: 16px;
    font-weight: bold;
}
.block {
    background: #151923;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #2a2f45;
}
.kernel {
    background: #0b0d14;
    padding: 14px;
    border-radius: 10px;
    border: 1px solid #3a3f5a;
}
.op {
    color: #7aa2ff;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────
st.markdown("## 🧬 UGC Execution Kernel")
st.markdown("""
This interface is a **human debug console** for a machine-to-machine execution engine.  
In production, **AI agents, DAOs, bots, and backend services** call UGC directly.
""")

st.text("Use this  Ethereum  test Address: 0xA34A13e95CE831953e598689e864a97B7DE949eb")
st.text("Use this Solana test Address: 75BgVvMNZ8Es1JffEDNYxWNVE2yoBTndLxViARhYWPF")

st.divider()

# ── Layout ──────────────────────────────────────────────
left, right = st.columns([1, 1.4])

# ── Left: Agent Request ─────────────────────────────────
with left:
    st.markdown("### 🤖 Agent Call", unsafe_allow_html=True)
    st.markdown('<div class="block">', unsafe_allow_html=True)

    operation = st.selectbox(
        "Kernel Operation",
        ["InfuraRPC", "HeliusAPI", "EthereumSigner", "SolanaSigner", "EthereumPayment", "SolanaPayment"]
    )

    address = st.text_input("Source Address")

    to = amount = payload = None

    if "Payment" in operation:
        to = st.text_input("Destination Address")
        amount = st.text_input("Amount")

    if "Signer" in operation:
        payload = st.text_input("Payload")

    run = st.button("⚡ Execute Kernel")

    st.markdown('</div>', unsafe_allow_html=True)

# ── Right: Kernel View ──────────────────────────────────
with right:
    st.markdown("### 🧠 Kernel State (What an AI Agent Sees)")

    state = {}
    if address: state["address"] = address
    if to: state["to"] = to
    if amount: state["amount"] = amount
    if payload: state["payload"] = payload

    st.json(state if state else {"kernel": "waiting for agent input"})

    if run:
        st.divider()
        st.markdown("### ⚙️ Execution Trace")

        try:
            with st.spinner("UGC Kernel executing DAG…"):
                result =requests.post(
                    "https://itsvelocity-ucg-v1.hf.space/ucg",
                    json={"operation":operation,"state":state}
                    )
                jsonresult=result.json()
                st.write(jsonresult)

            executed_ops_raw = jsonresult.get("executed", "")
            #Convert string set to list safely
            executed_ops = [op.strip().strip("'") for op in executed_ops_raw.strip("{}").split(",") if op]
            st.markdown("### ⚙️ Execution Trace (Op-by-Op)")
            for op in executed_ops:
                st.markdown(f'<div class="kernel"><span class="op">{op}</span> executed</div>', unsafe_allow_html=True)

            st.success("Kernel execution finished")

# ── Blockchain Transaction (if exists) ───────────────
            response_state = jsonresult.get("response", {})
            if "tx_hash" in response_state:
                st.markdown("### 🔗 Blockchain Transaction")
                st.code(response_state["tx_hash"])

        except Exception as e:
            st.error("error")

        # ── Final Machine State ───────────────────────────────
        #st.markdown("### 📦 Final Machine State")
        #st.json(response_state)

# ── Footer ──────────────────────────────────────────────
st.divider()
st.caption("""
UGC is a deterministic execution graph.  
This UI is only a **human inspection layer** over the same engine used by autonomous agents.
""")
