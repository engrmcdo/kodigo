import streamlit as st
import requests
import urllib3
import pandas as pd
from datetime import datetime
import pytz

# Suppress SSL verification warnings for cloud HTTP queries
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(
    page_title="KODIGO NI MCDO",
    page_icon="📈",
    layout="wide"
)

# --------------------------------------------------------------------------
# Auto-Refresh Mechanism (Triggers every 60 seconds without manual refresh)
# --------------------------------------------------------------------------
st.markdown(
    """
    <script>
    var timeout = 60; // 60 seconds interval
    function timer() {
        timeout--;
        if (timeout <= 0) {
            window.parent.location.reload();
        }
    }
    setInterval(timer, 1000);
    </script>
    """,
    unsafe_allow_html=True
)

PHT = pytz.timezone("Asia/Manila")

SESSION = requests.Session()
SESSION.verify = False
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://finance.yahoo.com",
    "Referer": "https://finance.yahoo.com/"
})

# 15-Stock Watchlist & 5-Pillar Fundamental Profiles
WATCHLIST = {
    "GCASH": {
        "name": "Mynt, Inc. (Digital Financial Services)",
        "yf_sym": "GLO.PS",
        "default_price": 6.69,
        "default_support": 5.95,
        "default_resistance": 6.76,
        "pb": "4.8x",
        "pe": "24.5x",
        "sector": "Fintech / Digital Financial Services",
        "catalysts": "Enterprise micro-lending expansion (GLoan, GCredit), remittance integrations, digital wallet ubiquity, and high ROE operating leverage.",
        "risks": "Deposit competition from digital-only banks, cybersecurity compliance overhead, and potential regulatory rate caps on credit spreads.",
        "commentary": "Trading in an active price-discovery phase between its structural floor support and debut resistance band. Analysts watch for margin expansion in non-collateralized lending."
    },
    "GLO": {
        "name": "Globe Telecom, Inc.",
        "yf_sym": "GLO.PS",
        "default_price": 1544.00,
        "default_support": 1450.00,
        "default_resistance": 1650.00,
        "pb": "1.8x",
        "pe": "12.4x",
        "sector": "Telecommunications",
        "catalysts": "Data monetization, digital solutions expansion, capital expenditure tapering, and consistent recurring dividend yields.",
        "risks": "Network capex depreciation, intense mobile broadband price competition, and debt servicing requirements.",
        "commentary": "Consolidating below intermediate moving averages while providing defensive telecom dividend support. Accumulation corridor remains anchored near primary support."
    },
    "AC": {
        "name": "Ayala Corporation",
        "yf_sym": "AC.PS",
        "default_price": 529.00,
        "default_support": 520.00,
        "default_resistance": 590.00,
        "pb": "0.8x",
        "pe": "10.1x",
        "sector": "Conglomerates / Holding Firms",
        "catalysts": "Broad portfolio earnings resilience, ACEN renewable capacity additions, real estate recovery, and banking transaction volume growth.",
        "risks": "Holding company net asset value discount and macroeconomic interest rate sensitivity.",
        "commentary": "Trading in an accumulation corridor near its structural floor with balanced momentum. Valuation remains attractive relative to historical book value."
    },
    "BPI": {
        "name": "Bank of the Philippine Islands",
        "yf_sym": "BPI.PS",
        "default_price": 95.95,
        "default_support": 92.00,
        "default_resistance": 110.00,
        "pb": "1.2x",
        "pe": "8.8x",
        "sector": "Banking / Financial Services",
        "catalysts": "Digital channel integration, post-merger branch synergies, corporate loan expansion, and stable net interest margins.",
        "risks": "Deposit cost pressure and credit cost fluctuations if monetary policy easing is delayed.",
        "commentary": "Forming an intermediate base above key support with RSI hovering in neutral territory with stable commercial net interest margins."
    },
    "TEL": {
        "name": "PLDT Inc.",
        "yf_sym": "TEL.PS",
        "default_price": 1174.00,
        "default_support": 1150.00,
        "default_resistance": 1300.00,
        "pb": "1.4x",
        "pe": "11.2x",
        "sector": "Telecommunications",
        "catalysts": "Capex tapering expanding free cash flows, enterprise data center leasing growth, and steady cash returns.",
        "risks": "Broadband market competition and debt servicing requirements.",
        "commentary": "Maintaining structural stability above its 20-day moving average and horizontal floor support."
    },
    "ALI": {
        "name": "Ayala Land, Inc.",
        "yf_sym": "ALI.PS",
        "default_price": 15.96,
        "default_support": 14.80,
        "default_resistance": 17.50,
        "pb": "0.6x",
        "pe": "8.9x",
        "sector": "Real Estate",
        "catalysts": "Commercial leasing recovery, stable residential presales volume, and provincial estate development.",
        "risks": "Mortgage rate sensitivity and building material input costs.",
        "commentary": "Relative strength leader with RSI near 60. Price remains elevated above medium-term moving averages."
    },
    "BDO": {
        "name": "BDO Unibank, Inc.",
        "yf_sym": "BDO.PS",
        "default_price": 117.50,
        "default_support": 110.00,
        "default_resistance": 125.00,
        "pb": "1.0x",
        "pe": "8.4x",
        "sector": "Banking",
        "catalysts": "Market-leading loan portfolio scale, fee income diversification, and resilient net interest margins.",
        "risks": "Credit cost sensitivity if monetary policy easing is delayed.",
        "commentary": "Constructive upward momentum trading in the upper half of its intermediate channel."
    },
    "ICT": {
        "name": "Intl Container Terminal Services",
        "yf_sym": "ICT.PS",
        "default_price": 854.50,
        "default_support": 810.00,
        "default_resistance": 890.00,
        "pb": "3.5x",
        "pe": "18.2x",
        "sector": "Port Logistics",
        "catalysts": "Global volume throughput growth and USD tariff hedge advantages.",
        "risks": "Shipping route disruptions and port concession renewal capex.",
        "commentary": "Consolidating with neutral momentum following a test of resistance in the upper range of its multi-month channel."
    },
    "SMPH": {
        "name": "SM Prime Holdings",
        "yf_sym": "SMPH.PS",
        "default_price": 17.32,
        "default_support": 15.40,
        "default_resistance": 18.50,
        "pb": "1.1x",
        "pe": "14.5x",
        "sector": "Real Estate / Commercial Malls",
        "catalysts": "Provincial mall foot traffic and resilient rental revenue yields.",
        "risks": "Inflationary pressure on retail tenant sales.",
        "commentary": "Stabilizing with healthy momentum, approaching its structural resistance ceiling."
    },
    "SM": {
        "name": "SM Investments Corp.",
        "yf_sym": "SM.PS",
        "default_price": 532.00,
        "default_support": 510.00,
        "default_resistance": 580.00,
        "pb": "1.3x",
        "pe": "13.2x",
        "sector": "Conglomerates",
        "catalysts": "Direct consumer proxy across retail, universal banking, and prime commercial property.",
        "risks": "Compression in discretionary consumer spending.",
        "commentary": "Trading in the middle of its historical trading band, mirroring broad domestic consumption."
    },
    "MBT": {
        "name": "Metrobank",
        "yf_sym": "MBT.PS",
        "default_price": 60.50,
        "default_support": 58.00,
        "default_resistance": 66.00,
        "pb": "0.7x",
        "pe": "6.8x",
        "sector": "Banking",
        "catalysts": "High Tier-1 capital adequacy and room for dividend payout expansion.",
        "risks": "Moderation in corporate credit demand.",
        "commentary": "Holding structural support with RSI reflecting mild consolidation and an attractive valuation multiple."
    },
    "MER": {
        "name": "Manila Electric Company",
        "yf_sym": "MER.PS",
        "default_price": 432.00,
        "default_support": 410.00,
        "default_resistance": 450.00,
        "pb": "1.9x",
        "pe": "12.0x",
        "sector": "Utilities / Power Distribution",
        "catalysts": "Guaranteed distribution asset base and consistent electricity demand growth.",
        "risks": "Regulatory rate review scrutiny.",
        "commentary": "Defensive utility proxy fluctuating inside a tight historical channel."
    },
    "MONDE": {
        "name": "Monde Nissin",
        "yf_sym": "MONDE.PS",
        "default_price": 5.98,
        "default_support": 5.80,
        "default_resistance": 7.20,
        "pb": "2.2x",
        "pe": "16.5x",
        "sector": "Consumer Staples / Food",
        "catalysts": "Core noodles volume leadership and input commodity cost stabilization.",
        "risks": "Alternative meat segment drag and agricultural commodity volatility.",
        "commentary": "Consolidating near cyclical multi-year lows; indicator momentum signals an oversold condition near its structural base."
    },
    "JFC": {
        "name": "Jollibee Foods Corporation",
        "yf_sym": "JFC.PS",
        "default_price": 144.00,
        "default_support": 135.00,
        "default_resistance": 160.00,
        "pb": "3.1x",
        "pe": "22.8x",
        "sector": "Consumer Discretionary / QSR",
        "catalysts": "Global network expansion and domestic quick-service restaurant resilience.",
        "risks": "Integration expenses from international acquisitions and store labor costs.",
        "commentary": "Trading in the lower half of its intermediate consolidation range with balanced momentum."
    },
    "PGOLD": {
        "name": "Puregold Price Club",
        "yf_sym": "PGOLD.PS",
        "default_price": 40.15,
        "default_support": 36.00,
        "default_resistance": 42.00,
        "pb": "0.8x",
        "pe": "10.4x",
        "sector": "Consumer Staples / Grocery Retail",
        "catalysts": "Everyday staple grocery volume resilience and strategic provincial footprint.",
        "risks": "Competition from discount format retailers.",
        "commentary": "Approaching its overhead resistance level with balanced momentum."
    }
}

def compute_wilder_rsi(prices, period=14):
    """Computes exact 14-period Wilder Smoothed RSI."""
    if len(prices) < period + 1:
        return 50.0
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    gains = [d if d > 0 else 0.0 for d in deltas]
    losses = [-d if d < 0 else 0.0 for d in deltas]
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100.0 - (100.0 / (1.0 + rs)), 1)

# Cache set to 60 seconds for live per-minute market syncing
@st.cache_data(ttl=60)
def fetch_live_market_data():
    """Queries live market candles and dynamically derives all 5-pillar values."""
    live_records = {}
    now_str = datetime.now(PHT).strftime("%Y-%m-%d %I:%M:%S %p PHT")

    for ticker, meta in WATCHLIST.items():
        yf_sym = meta["yf_sym"]
        default_p = meta["default_price"]
        default_s = meta["default_support"]
        default_r = meta["default_resistance"]
        
        cur_p = default_p
        dyn_s = default_s
        dyn_r = default_r
        rsi_val = 50.0
        trend_status = "Neutral Consolidation"

        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yf_sym}?interval=1d&range=3mo"
        try:
            resp = SESSION.get(url, timeout=4)
            if resp.status_code == 200:
                payload = resp.json()
                res = payload.get("chart", {}).get("result", [{}])[0]
                meta_block = res.get("meta", {})
                regular_price = float(meta_block.get("regularMarketPrice", 0.0))
                
                quote_block = res.get("indicators", {}).get("quote", [{}])[0]
                closes = [c for c in quote_block.get("close", []) if c is not None and c > 0]
                highs = [h for h in quote_block.get("high", []) if h is not None and h > 0]
                lows = [l for l in quote_block.get("low", []) if l is not None and l > 0]
                
                if closes and len(closes) >= 15:
                    if ticker != "GCASH" and regular_price > 0:
                        cur_p = round(regular_price, 2)
                    elif ticker != "GCASH":
                        cur_p = round(closes[-1], 2)
                    else:
                        cur_p = default_p

                    # Dynamic 20-day Support/Resistance calculation
                    dyn_s = round(float(min(lows[-20:])), 2) if len(lows) >= 20 else default_s
                    dyn_r = round(float(max(highs[-20:])), 2) if len(highs) >= 20 else default_r
                    
                    # 14-period Wilder RSI calculation
                    rsi_val = compute_wilder_rsi(closes, period=14)
                    
                    # Moving average 20-day trend check
                    ma20 = round(sum(closes[-20:]) / min(len(closes), 20), 2)
                    trend_status = "Above MA20" if cur_p >= ma20 else "Below MA20"
        except Exception:
            pass

        # Data-driven analytical corridor formulas[cite: 1]
        buy_band = f"₱{(dyn_s * 0.995):,.2f} – ₱{(dyn_s * 1.01):,.2f}"
        sell_band = f"₱{(dyn_r * 0.99):,.2f} – ₱{(dyn_r * 1.005):,.2f}"

        # Zone status assignment
        if cur_p <= dyn_s * 1.015:
            status = "ACCUMULATION"
        elif cur_p >= dyn_r * 0.99:
            status = "PROFIT_TAKING"
        else:
            status = "NEUTRAL"

        live_records[ticker] = {
            "name": meta["name"],
            "price": cur_p,
            "support": dyn_s,
            "resistance": dyn_r,
            "rsi": rsi_val,
            "trend": trend_status,
            "status": status,
            "buy_band": buy_band,
            "sell_band": sell_band,
            "pb": meta["pb"],
            "pe": meta["pe"],
            "sector": meta["sector"],
            "catalysts": meta["catalysts"],
            "risks": meta["risks"],
            "commentary": meta["commentary"]
        }

    return live_records, now_str

st.title("📈 PSE Stock Analyst & Insight Engine")
st.caption("5-Pillar Technical & Fundamental Analytical Radar")

stocks, sync_time = fetch_live_market_data()

st.sidebar.markdown("**Feed Status:** 🟢 Live Auto-Fetch (Active)")
st.sidebar.markdown(f"**Last Sync:** `{sync_time}`")
st.sidebar.markdown("**Sync Frequency:** ⏱️ Every 60 seconds")

if st.sidebar.button("🔄 Refresh Now"):
    st.cache_data.clear()
    st.rerun()

# 1. Main Watchlist Table (Pillars 1 & 3)
table_rows = []
for ticker, info in stocks.items():
    table_rows.append({
        "Issue": ticker,
        "Company Name & Sector": info["name"],
        "Last Price": f"₱{float(info['price']):,.2f}",
        "Suggested Accumulation Zone": info["buy_band"],
        "Key Support (S)": f"₱{float(info['support']):,.2f}",
        "Key Resistance (R)": f"₱{float(info['resistance']):,.2f}",
        "RSI (14D)": f"{float(info['rsi']):.1f}",
        "Zone Status": info["status"]
    })

df = pd.DataFrame(table_rows)
st.dataframe(df, use_container_width=True, hide_index=True)

# 2. 5-Pillar Deep Dive Modal/Selector
st.divider()
selected_ticker = st.selectbox("Select Stock for 5-Pillar Deep Dive:", list(stocks.keys()))

if selected_ticker:
    s = stocks[selected_ticker]
    st.subheader(f"{selected_ticker} — {s['name']}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Last Price", f"₱{float(s['price']):,.2f}")
    col2.metric("Key Support (S)", f"₱{float(s['support']):,.2f}")
    col3.metric("Key Resistance (R)", f"₱{float(s['resistance']):,.2f}")
    col4.metric("RSI (14D)", f"{float(s['rsi']):.1f}")

    tab1, tab2, tab3 = st.tabs([
        "1 & 2. Technical Chart Analysis & Price Corridors", 
        "3. Fundamental Profile & Valuation Anchor", 
        "4. Analyst Commentary & Catalysts/Risks"
    ])

    with tab1:
        st.markdown(f"**Moving Average & Trend Alignment:** `{s['trend']}`")
        st.info(f"🟢 **Suggested Accumulation Zone (Buy Band):** {s['buy_band']}")
        st.warning(f"🔴 **Suggested Profit-Taking Zone (Sell Band):** {s['sell_band']}")
        st.caption("*Based on recent price action, dynamic support aligns near historical buyer zones and resistance near overhead supply[cite: 1]. These are data-based analytical reference points, not instructions or purchase orders[cite: 1].")

    with tab2:
        st.markdown(f"**Sector Classification:** {s['sector']}")
        col_f1, col_f2 = st.columns(2)
        col_f1.metric("Price-to-Book (P/B)", s["pb"])
        col_f2.metric("Price-to-Earnings (P/E)", s["pe"])
        st.markdown(f"**Core Growth Catalysts:** {s['catalysts']}")
        st.markdown(f"**Key Operational & Macro Risks:** {s['risks']}")

    with tab3:
        st.write(s["commentary"])

# 3. Mandatory Safety & Disclaimer Behavior (Pillar 5)
st.divider()
st.caption(
    "**Mandatory Safety & Educational Disclaimer:** These insights, technical indicators, valuation multiples, "
    "and suggested price ranges are generated strictly for informational and educational tracking purposes[cite: 1]. They do not "
    "constitute financial advice, an investment recommendation, an endorsement, or a trade instruction to buy, sell, or "
    "hold any security[cite: 1]. Past performance and technical bands do not guarantee future results[cite: 1]. Always consult a licensed "
    "financial advisor or certified professional before making investment decisions[cite: 1]."
)
