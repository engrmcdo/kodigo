import streamlit as st
import requests
import json
import pandas as pd

st.set_page_config(
    page_title="PSE Stock Analyst & Insight Engine",
    page_icon="📈",
    layout="wide"
)

# Replace with your actual GitHub username and repository name
RAW_JSON_URL = "https://raw.githubusercontent.com/<YOUR_GITHUB_USERNAME>/pse-stock-analyst/main/public/market_data.json"

st.title("📈 PSE Stock Analyst & Insight Engine")
st.caption("5-Pillar Analytical Framework & Live Technical Radar")

@st.cache_data(ttl=60)  # Re-fetches from GitHub every 60 seconds
def load_data():
    try:
        # Pulls live data directly from the GitHub repository
        resp = requests.get(f"{RAW_JSON_URL}?t={pd.Timestamp.now().timestamp()}", timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        st.error(f"Error fetching data from GitHub: {e}")
    
    # Fallback: Read local file inside the deployed container
    try:
        with open("public/market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

data = load_data()

if data and "stocks" in data:
    st.sidebar.markdown(f"**Feed Status:** 🟢 Active (GitHub Cloud)")
    st.sidebar.markdown(f"**Last Sync:** {data.get('last_updated', 'N/A')}")
    
    if st.sidebar.button("🔄 Refresh Market Data"):
        st.cache_data.clear()
        st.rerun()

    stocks = data["stocks"]

    # Table View
    table_rows = []
    for ticker, info in stocks.items():
        table_rows.append({
            "Issue": ticker,
            "Name": info.get("name", ""),
            "Price (₱)": f"₱{info.get('price', 0):,.2f}",
            "Recommended Buying Zone (Accumulation)": info.get("buy_band", "N/A"),
            "Support (₱)": f"₱{info.get('support', 0):,.2f}",
            "Resistance (₱)": f"₱{info.get('resistance', 0):,.2f}",
            "RSI (14D)": info.get("rsi", "N/A"),
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
        col1.metric("Last Price", f"₱{s.get('price', 0):,.2f}")
        col2.metric("Support", f"₱{s.get('support', 0):,.2f}")
        col3.metric("Resistance", f"₱{s.get('resistance', 0):,.2f}")
        col4.metric("RSI (14D)", s.get("rsi", "N/A"))

        tab1, tab2, tab3 = st.tabs(["1 & 2. Technical & Corridors", "3. Fundamental Profile", "4. Analyst Commentary"])

        with tab1:
            st.markdown(f"**Moving Average Trend:** `{s.get('trend', 'Neutral')}`")
            st.info(f"🟢 **Accumulation Zone (Near Support):** {s.get('buy_band')}")
            st.warning(f"🔴 **Profit-Taking Zone (Near Resistance):** {s.get('sell_band')}")
            st.caption("*Calculated technical boundaries; analytical reference points, not purchase or sell orders.")

        with tab2:
            st.markdown(f"**Sector:** {s.get('sector', 'N/A')}")
            st.markdown(f"**Price-to-Book (P/B):** {s.get('pb', 'N/A')}")
            st.markdown(f"**Growth Catalysts:** {s.get('catalysts', 'N/A')}")
            st.markdown(f"**Key Operational Risks:** {s.get('risks', 'N/A')}")

        with tab3:
            st.write(s.get('commentary', 'No analyst commentary recorded.'))
else:
    st.warning("Connecting to GitHub data feed...")

# Mandatory Safety Disclaimer
st.divider()
st.caption(
    "**Mandatory Safety Disclaimer:** All technical indicators, structural levels, valuation multiples, "
    "and suggested price bands are generated strictly as analytical reference points for educational and market "
    "tracking purposes. They do not constitute financial advice, investment recommendations, trade instructions, "
    "or guarantees of future price performance. Always consult a licensed financial advisor before making investment decisions."
)
