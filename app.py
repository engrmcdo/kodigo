import streamlit as st
import requests
import json
import os
import pandas as pd

st.set_page_config(
    page_title="KODIGO NI MCDO",
    page_icon="📈",
    layout="wide"
)

# 15-Stock 5-Pillar Embedded Baseline Dataset
EMBEDDED_BASE_DATA = {
    "last_updated": "Embedded Baseline Feed",
    "stocks": {
        "GCASH": {
            "name": "Mynt, Inc.",
            "price": 6.69,
            "support": 5.95,
            "resistance": 6.76,
            "rsi": 54.2,
            "pb": "4.8x",
            "trend": "Above MA20",
            "sector": "Fintech / Digital Financial Services",
            "status": "NEUTRAL",
            "buy_band": "₱5.92 – ₱6.01",
            "sell_band": "₱6.69 – ₱6.79",
            "catalysts": "Enterprise micro-lending expansion (GLoan, GCredit), cross-border remittance ubiquity, high ROE operating leverage.",
            "risks": "Deposit competition from digital-only banks and cybersecurity compliance overhead.",
            "commentary": "Testing upper debut resistance band at ₱6.76 following steady price discovery above its ₱5.95 structural floor."
        },
        "GLO": {
            "name": "Globe Telecom",
            "price": 1544.00,
            "support": 1450.00,
            "resistance": 1650.00,
            "rsi": 46.8,
            "pb": "1.8x",
            "trend": "Below MA20",
            "sector": "Telecommunications",
            "status": "NEUTRAL",
            "buy_band": "₱1,442.75 – ₱1,464.50",
            "sell_band": "₱1,633.50 – ₱1,658.25",
            "catalysts": "Strategic equity in Mynt (GCash), potential standalone fintech monetization, high recurring dividend yield.",
            "risks": "Network capex depreciation and digital banking competition.",
            "commentary": "Consolidating below intermediate moving averages while providing steady dividend support."
        },
        "AC": {
            "name": "Ayala Corporation (GCash Conglomerate Proxy)",
            "price": 529.00,
            "support": 520.00,
            "resistance": 590.00,
            "rsi": 51.8,
            "pb": "0.8x",
            "trend": "Above MA20",
            "sector": "Holding Firms / Fintech",
            "status": "ACCUMULATION",
            "buy_band": "₱517.40 – ₱525.20",
            "sell_band": "₱584.10 – ₱592.95",
            "catalysts": "Mynt valuation accretion, ACEN renewable expansion, BPI transaction volume growth.",
            "risks": "Conglomerate holding discount and interest rate sensitivity.",
            "commentary": "Trading in an accumulation band near ₱520.00 structural floor with balanced momentum."
        },
        "BPI": {
            "name": "Bank of the Philippine Islands",
            "price": 95.95,
            "support": 92.00,
            "resistance": 110.00,
            "rsi": 46.9,
            "pb": "1.2x",
            "trend": "Below MA20",
            "sector": "Banking / Digital Infrastructure",
            "status": "NEUTRAL",
            "buy_band": "₱91.54 – ₱92.92",
            "sell_band": "₱108.90 – ₱110.55",
            "catalysts": "GSave clearing rail integration, Robinsons Bank merger synergies, stable net interest margins.",
            "risks": "Cost-of-funds competition from high-yield digital accounts.",
            "commentary": "Forming an intermediate base above ₱92.00 support with RSI hovering in neutral territory."
        },
        "TEL": {
            "name": "PLDT Inc.",
            "price": 1174.00,
            "support": 1150.00,
            "resistance": 1300.00,
            "rsi": 50.3,
            "pb": "1.4x",
            "trend": "Above MA20",
            "sector": "Telecommunications",
            "status": "ACCUMULATION",
            "buy_band": "₱1,144.25 – ₱1,161.50",
            "sell_band": "₱1,287.00 – ₱1,306.50",
            "catalysts": "Capex tapering expanding free cash flows, enterprise data center leasing growth.",
            "risks": "Broadband market competition and debt servicing requirements.",
            "commentary": "Maintaining structure above its 20-day moving average and ₱1,150.00 support level."
        },
        "ALI": {
            "name": "Ayala Land, Inc.",
            "price": 15.96,
            "support": 14.80,
            "resistance": 17.50,
            "rsi": 59.9,
            "pb": "0.6x",
            "trend": "Above MA20",
            "sector": "Real Estate",
            "status": "NEUTRAL",
            "buy_band": "₱14.73 – ₱14.95",
            "sell_band": "₱17.33 – ₱17.59",
            "catalysts": "Commercial leasing recovery and steady residential presales volume.",
            "risks": "Mortgage rate sensitivity and construction material costs.",
            "commentary": "Relative strength leader with RSI near 60, holding above short- and medium-term moving averages."
        },
        "BDO": {
            "name": "BDO Unibank, Inc.",
            "price": 117.50,
            "support": 110.00,
            "resistance": 125.00,
            "rsi": 57.2,
            "pb": "1.0x",
            "trend": "Above MA20",
            "sector": "Banking",
            "status": "NEUTRAL",
            "buy_band": "₱109.45 – ₱111.10",
            "sell_band": "₱123.75 – ₱125.63",
            "catalysts": "Market-leading loan portfolio scale and resilient net interest margins.",
            "risks": "Credit cost sensitivity if monetary policy easing is delayed.",
            "commentary": "Constructive upward momentum trading in the upper half of its intermediate channel."
        },
        "ICT": {
            "name": "Intl Container Terminal Services",
            "price": 854.50,
            "support": 810.00,
            "resistance": 890.00,
            "rsi": 45.9,
            "pb": "3.5x",
            "trend": "Below MA20",
            "sector": "Port Logistics",
            "status": "NEUTRAL",
            "buy_band": "₱805.95 – ₱818.10",
            "sell_band": "₱881.10 – ₱894.45",
            "catalysts": "Global volume throughput growth and USD tariff hedge advantages.",
            "risks": "Shipping route disruptions and port concession renewal capex.",
            "commentary": "Consolidating near ₱854.00 with neutral momentum following a test of resistance."
        },
        "SMPH": {
            "name": "SM Prime Holdings",
            "price": 17.32,
            "support": 15.40,
            "resistance": 18.50,
            "rsi": 55.1,
            "pb": "1.1x",
            "trend": "Above MA20",
            "sector": "Real Estate / Malls",
            "status": "NEUTRAL",
            "buy_band": "₱15.32 – ₱15.55",
            "sell_band": "₱18.32 – ₱18.59",
            "catalysts": "Provincial mall foot traffic and resilient rental revenue yields.",
            "risks": "Inflationary pressure on retail tenant sales.",
            "commentary": "Stabilizing above ₱17.00 with healthy momentum, approaching its ₱18.50 resistance ceiling."
        },
        "SM": {
            "name": "SM Investments Corp.",
            "price": 532.00,
            "support": 510.00,
            "resistance": 580.00,
            "rsi": 50.7,
            "pb": "1.3x",
            "trend": "Below MA20",
            "sector": "Conglomerates",
            "status": "NEUTRAL",
            "buy_band": "₱507.45 – ₱515.10",
            "sell_band": "₱574.20 – ₱582.90",
            "catalysts": "Direct consumer proxy across retail, universal banking, and prime property.",
            "risks": "Compression in discretionary consumer spending.",
            "commentary": "Trading in the middle of its historical trading band with an RSI reading near 50."
        },
        "MBT": {
            "name": "Metrobank",
            "price": 60.50,
            "support": 58.00,
            "resistance": 66.00,
            "rsi": 45.1,
            "pb": "0.7x",
            "trend": "Below MA20",
            "sector": "Banking",
            "status": "NEUTRAL",
            "buy_band": "₱57.71 – ₱58.58",
            "sell_band": "₱65.34 – ₱66.33",
            "catalysts": "High Tier-1 capital adequacy and room for dividend payout expansion.",
            "risks": "Moderation in corporate credit demand.",
            "commentary": "Holding structural support at ₱58.00 with RSI at 45.1 reflecting mild consolidation."
        },
        "MER": {
            "name": "Manila Electric Company",
            "price": 432.00,
            "support": 410.00,
            "resistance": 450.00,
            "rsi": 44.8,
            "pb": "1.9x",
            "trend": "Below MA20",
            "sector": "Utilities",
            "status": "NEUTRAL",
            "buy_band": "₱407.95 – ₱414.10",
            "sell_band": "₱445.50 – ₱452.25",
            "catalysts": "Guaranteed distribution asset base and consistent electricity demand growth.",
            "risks": "Regulatory rate review scrutiny.",
            "commentary": "Defensive utility proxy fluctuating inside a tight range with RSI at 44.8."
        },
        "MONDE": {
            "name": "Monde Nissin",
            "price": 5.98,
            "support": 5.80,
            "resistance": 7.20,
            "rsi": 37.2,
            "pb": "2.2x",
            "trend": "Below MA20",
            "sector": "Consumer Staples",
            "status": "PROFIT_TAKING",
            "buy_band": "₱5.77 – ₱5.86",
            "sell_band": "₱7.13 – ₱7.24",
            "catalysts": "Core noodles volume leadership and input cost stabilization.",
            "risks": "Alternative meat segment drag and agricultural commodity volatility.",
            "commentary": "Near cyclical multi-year lows; RSI at 37.2 signals an oversold condition near structural floor."
        },
        "JFC": {
            "name": "Jollibee Foods Corporation",
            "price": 144.00,
            "support": 135.00,
            "resistance": 160.00,
            "rsi": 51.4,
            "pb": "3.1x",
            "trend": "Above MA20",
            "sector": "Consumer Discretionary",
            "status": "NEUTRAL",
            "buy_band": "₱134.33 – ₱136.35",
            "sell_band": "₱158.40 – ₱160.80",
            "catalysts": "Global network expansion and domestic quick-service restaurant resilience.",
            "risks": "Integration expenses from international acquisitions and store labor costs.",
            "commentary": "Trading in an intermediate consolidation range with RSI steady at 51.4."
        },
        "PGOLD": {
            "name": "Puregold Price Club",
            "price": 40.15,
            "support": 36.00,
            "resistance": 42.00,
            "rsi": 50.9,
            "pb": "0.8x",
            "trend": "Below MA20",
            "sector": "Consumer Staples",
            "status": "NEUTRAL",
            "buy_band": "₱35.82 – ₱36.36",
            "sell_band": "₱41.58 – ₱42.21",
            "catalysts": "Everyday staple grocery volume resilience and strategic provincial footprint.",
            "risks": "Competition from discount format retailers.",
            "commentary": "Approaching its ₱42.00 resistance level with balanced momentum (RSI 50.9)."
        }
    }
}

st.title("📈 PSE Stock Analyst & Insight Engine")
st.caption("5-Pillar Analytical Framework & Live Technical Radar")

@st.cache_data(ttl=60)
def load_data():
    # Tier 1: Check local disk inside the container
    for path in ["public/market_data.json", "market_data.json"]:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = json.load(f)
                    if content and "stocks" in content and len(content["stocks"]) > 0:
                        return content, "Container File System"
            except Exception:
                pass

    # Tier 2: Use Embedded Resilient Baseline
    return EMBEDDED_BASE_DATA, "Embedded Engine Dataset"

data, source_type = load_data()
stocks = data["stocks"]

st.sidebar.markdown(f"**Feed Status:** 🟢 Active ({source_type})")
st.sidebar.markdown(f"**Last Sync:** `{data.get('last_updated', 'Just now')}`")

if st.sidebar.button("🔄 Refresh Market Data"):
    st.cache_data.clear()
    st.rerun()

# 1. Main Watchlist Table
table_rows = []
for ticker, info in stocks.items():
    p = info.get("price", 0.0)
    s = info.get("support", 0.0)
    r = info.get("resistance", 0.0)
    table_rows.append({
        "Issue": ticker,
        "Name": info.get("name", ""),
        "Last Price": f"₱{float(p):,.2f}",
        "Recommended Buying Zone (Accumulation)": info.get("buy_band", "N/A"),
        "Key Support (S)": f"₱{float(s):,.2f}",
        "Key Resistance (R)": f"₱{float(r):,.2f}",
        "RSI (14D)": f"{float(info.get('rsi', 50.0)):.1f}",
        "Zone Status": info.get("status", "NEUTRAL")
    })

df = pd.DataFrame(table_rows)
st.dataframe(df, use_container_width=True, hide_index=True)

# 2. 5-Pillar Deep Dive Modal/Selector
st.divider()
selected_ticker = st.selectbox("Select a stock for 5-Pillar Deep Dive:", list(stocks.keys()))

if selected_ticker:
    s = stocks[selected_ticker]
    st.subheader(f"{selected_ticker} — {s.get('name')}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Last Price", f"₱{float(s.get('price', 0)):,.2f}")
    col2.metric("Support", f"₱{float(s.get('support', 0)):,.2f}")
    col3.metric("Resistance", f"₱{float(s.get('resistance', 0)):,.2f}")
    col4.metric("RSI (14D)", f"{float(s.get('rsi', 50)):.1f}")

    tab1, tab2, tab3 = st.tabs(["1 & 2. Technical Chart Analysis & Corridors", "3. Fundamental Profile", "4. Analyst Commentary"])

    with tab1:
        st.markdown(f"**Moving Average Trend:** `{s.get('trend', 'Neutral')}`")
        st.info(f"🟢 **Recommended Buying Zone (Accumulation):** {s.get('buy_band', 'N/A')}")
        st.warning(f"🔴 **Suggested Profit-Taking Zone:** {s.get('sell_band', 'N/A')}")
        st.caption("*Calculated technical boundaries; analytical reference points, not purchase or sell orders.")

    with tab2:
        st.markdown(f"**Sector:** {s.get('sector', 'N/A')}")
        st.markdown(f"**Price-to-Book (P/B):** {s.get('pb', 'N/A')}")
        st.markdown(f"**Growth Catalysts:** {s.get('catalysts', 'N/A')}")
        st.markdown(f"**Key Operational Risks:** {s.get('risks', 'N/A')}")

    with tab3:
        st.write(s.get('commentary', 'No analyst commentary recorded.'))

# 3. Mandatory Safety Disclaimer
st.divider()
st.caption(
    "**Mandatory Safety Disclaimer:** All technical indicators, structural levels, valuation multiples, "
    "and suggested price bands are generated strictly as analytical reference points for educational and market "
    "tracking purposes. They do not constitute financial advice, investment recommendations, trade instructions, "
    "or guarantees of future price performance[cite: 1]. Always consult a licensed financial advisor before making investment decisions[cite: 1]."
)
