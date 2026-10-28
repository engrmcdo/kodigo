import streamlit as st
import requests
import json
import os
import pandas as pd

st.set_page_config(
    page_title="PSE Stock Analyst & Insight Engine",
    page_icon="📈",
    layout="wide"
)

# 1. REPLACE WITH YOUR EXACT GITHUB USERNAME AND REPO NAME
GITHUB_USER = "engrmcdo"  # e.g., "mcsolis"
GITHUB_REPO = "kodigo"            # your exact repo name
BRANCH = "main"

RAW_JSON_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{BRANCH}/public/market_data.json"

st.title("📈 PSE Stock Analyst & Insight Engine")
st.caption("5-Pillar Analytical Framework & Live Technical Radar")

@st.cache_data(ttl=60)
def load_data():
    # Attempt 1: Fetch directly from Raw GitHub URL
    try:
        url = f"{RAW_JSON_URL}?t={pd.Timestamp.now().timestamp()}"
        resp = requests.get(url, timeout=6)
        if resp.status_code == 200:
            payload = resp.json()
            if payload and "stocks" in payload and len(payload["stocks"]) > 0:
                return payload
        else:
            st.sidebar.warning(f"GitHub fetch returned HTTP {resp.status_code}")
    except Exception as e:
        st.sidebar.warning(f"GitHub fetch failed: {e}")
    
    # Attempt 2: Read from local repository file in the container
    possible_paths = [
        "public/market_data.json",
        "market_data.json"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                    if payload and "stocks" in payload:
                        return payload
            except Exception:
                continue

    return None

data = load_data()

if data and "stocks" in data:
    st.sidebar.markdown("**Feed Status:** 🟢 Active (GitHub Cloud)")
    st.sidebar.markdown(f"**Last Sync:** `{data.get('last_updated', 'Just now')}`")
    
    if st.sidebar.button("🔄 Refresh Market Data"):
        st.cache_data.clear()
        st.rerun()

    stocks = data["stocks"]

    # Table Overview
    table_rows = []
    for ticker, info in stocks.items():
        table_rows.append({
            "Issue": ticker,
            "Name": info.get("name", ""),
            "Price": f"₱{Number(info.get('price', 0)):,.2f}" if isinstance(info.get('price'), (int, float)) else f"₱{info.get('price')}",
            "Recommended Buying Zone (Accumulation)": info.get("buy_band", "N/A"),
            "Key Support": f"₱{Number(info.get('support', 0)):,.2f}" if isinstance(info.get('support'), (int, float)) else f"₱{info.get('support')}",
            "Key Resistance": f"₱{Number(info.get('resistance', 0)):,.2f}" if isinstance(info.get('resistance'), (int, float)) else f"₱{info.get('resistance')}",
            "RSI (14D)": str(info.get("rsi", "N/A")),
            "Status": info.get("status", "NEUTRAL")
        })

    df = pd.DataFrame(table_rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # 5-Pillar Stock Detail Viewer
    st.divider()
    selected_ticker = st.selectbox("Select a stock for 5-Pillar Deep Dive:", list(stocks.keys()))
    
    if selected_ticker:
        s = stocks[selected_ticker]
        st.subheader(f"{selected_ticker} — {s.get('name')}")

        col1, col2, col3, col4 = st.columns(4)
        p_val = s.get('price', 0)
        s_val = s.get('support', 0)
        r_val = s.get('resistance', 0)
        col1.metric("Last Price", f"₱{p_val:,.2f}" if isinstance(p_val, (int, float)) else f"₱{p_val}")
        col2.metric("Support", f"₱{s_val:,.2f}" if isinstance(s_val, (int, float)) else f"₱{s_val}")
        col3.metric("Resistance", f"₱{r_val:,.2f}" if isinstance(r_val, (int, float)) else f"₱{r_val}")
        col4.metric("RSI (14D)", str(s.get("rsi", "N/A")))

        tab1, tab2, tab3 = st.tabs(["1 & 2. Technical & Corridors", "3. Fundamental Profile", "4. Analyst Commentary"])

        with tab1:
            st.markdown(f"**Moving Average Trend:** `{s.get('trend', 'Neutral')}`")
            st.info(f"🟢 **Accumulation Zone (Near Support):** {s.get('buy_band', 'N/A')}")
            st.warning(f"🔴 **Profit-Taking Zone (Near Resistance):** {s.get('sell_band', 'N/A')}")
            st.caption("*Calculated technical boundaries; analytical reference points, not purchase or sell orders.")

        with tab2:
            st.markdown(f"**Sector:** {s.get('sector', 'N/A')}")
            st.markdown(f"**Price-to-Book (P/B):** {s.get('pb', 'N/A')}")
            st.markdown(f"**Growth Catalysts:** {s.get('catalysts', 'N/A')}")
            st.markdown(f"**Key Operational Risks:** {s.get('risks', 'N/A')}")

        with tab3:
            st.write(s.get('commentary', 'No analyst commentary recorded.'))
else:
    st.error("Unable to load market data. Please verify that public/market_data.json exists on GitHub and contains valid JSON.")
    st.info(f"Target URL: `{RAW_JSON_URL}`")

st.divider()
st.caption(
    "**Mandatory Safety Disclaimer:** All technical indicators, structural levels, valuation multiples, "
    "and suggested price bands are generated strictly as analytical reference points for educational and market "
    "tracking purposes. They do not constitute financial advice, investment recommendations, trade instructions, "
    "or guarantees of future price performance[cite: 1]. Always consult a licensed financial advisor before making investment decisions[cite: 1]."
)
