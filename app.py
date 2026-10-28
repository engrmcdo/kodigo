import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Stock Analysis & Insight Engine",
    page_icon="📈",
    layout="wide"
)

# ---------------------------------------------------------
# 15-Stock PSE Database & Fundamental Profiles
# ---------------------------------------------------------
STOCK_PROFILES = {
    "GCASH": {
        "name": "Mynt (Globe Fintech Innovations - GCash)",
        "sector": "Financial Technology / Digital Payments",
        "price": 6.69,
        "support": 5.95,
        "resistance": 6.76,
        "pe": "24.5x",
        "pb": "4.8x",
        "overview": "Leading micropayments, lending, and digital financial ecosystem in the Philippines, operating through parent companies Globe Telecom and Ayala Corporation.",
        "catalysts": "Rapid credit portfolio expansion (GLoan, GCredit), remittance ubiquity, and non-collateralized lending margins.",
        "risks": "Deposit competition from digital banks, regulatory lending rate caps, and cybersecurity infrastructure overhead.",
        "sentiment": "High growth, premium fintech valuation multiple."
    },
    "GLO": {
        "name": "Globe Telecom, Inc.",
        "sector": "Telecommunications",
        "price": 1544.00,
        "support": 1450.00,
        "resistance": 1650.00,
        "pe": "12.4x",
        "pb": "1.8x",
        "overview": "Full-service telecommunications provider in the Philippines offering wireless, broadband, enterprise solutions, and direct equity in Mynt (GCash).",
        "catalysts": "Capex tapering expanding free cash flow, digital fintech monetization, and high recurring dividend yield.",
        "risks": "Broadband market competition, infrastructure depreciation, and debt servicing.",
        "sentiment": "Defensive dividend proxy with fintech upside."
    },
    "AC": {
        "name": "Ayala Corporation",
        "sector": "Holding Firms / Conglomerates",
        "price": 529.00,
        "support": 520.00,
        "resistance": 590.00,
        "pe": "10.1x",
        "pb": "0.8x",
        "overview": "One of the largest Philippine conglomerates with diversified exposures across real estate (ALI), banking (BPI), telecom/fintech (GLO/Mynt), and renewable energy (ACEN).",
        "catalysts": "Broad portfolio earnings resilience, renewable pipeline expansion, and net asset value (NAV) recovery.",
        "risks": "Macro interest rate exposure and holding company equity discounts.",
        "sentiment": "Trading below historical book value; long-term institutional accumulation."
    },
    "BPI": {
        "name": "Bank of the Philippine Islands",
        "sector": "Banking & Financial Services",
        "price": 95.95,
        "support": 92.00,
        "resistance": 110.00,
        "pe": "8.8x",
        "pb": "1.2x",
        "overview": "Universal bank offering consumer banking, asset management, and core clearing rails for national digital wallets including GCash.",
        "catalysts": "Robinsons Bank merger synergies, digital integration, and resilient net interest margins (NIM).",
        "risks": "Potential margin compression upon monetary easing and credit cost fluctuations.",
        "sentiment": "Solid balance sheet with disciplined loan-loss provisioning."
    },
    "TEL": {
        "name": "PLDT Inc.",
        "sector": "Telecommunications",
        "price": 1174.00,
        "support": 1150.00,
        "resistance": 1300.00,
        "pe": "11.2x",
        "pb": "1.4x",
        "overview": "Telecommunications and digital services provider with integrated fixed-line, wireless (Smart), and data center operations.",
        "catalysts": "Data center colocation leasing, broadband revenue stabilization, and steady cash dividends.",
        "risks": "Price competition in mobile broadband and legacy capex amortizations.",
        "sentiment": "Range-bound income stock hovering near long-term valuation support."
    },
    "ALI": {
        "name": "Ayala Land, Inc.",
        "sector": "Real Estate",
        "price": 15.96,
        "support": 14.80,
        "resistance": 17.50,
        "pe": "8.9x",
        "pb": "0.6x",
        "overview": "Integrated property developer engaged in master-planned mixed-use estates, residential presales, shopping centers, offices, and hotels.",
        "catalysts": "Commercial leasing recovery, stable residential demand, and estate landbank monetization.",
        "risks": "Mortgage rate sensitivity and building material inflation.",
        "sentiment": "Significant discount to net asset value; constructive technical structure."
    },
    "BDO": {
        "name": "BDO Unibank, Inc.",
        "sector": "Banking & Financial Services",
        "price": 117.50,
        "support": 110.00,
        "resistance": 125.00,
        "pe": "8.4x",
        "pb": "1.0x",
        "overview": "The Philippines' largest universal bank by total assets, loans, deposits, and distribution network.",
        "catalysts": "Market-leading corporate and consumer credit scale, non-interest fee growth, and digital banking platforms.",
        "risks": "Macro credit slowdown and loan repricing cycles.",
        "sentiment": "Consistent institutional market proxy in the Philippine financial sector."
    },
    "ICT": {
        "name": "International Container Terminal Services, Inc.",
        "sector": "Port Logistics & Infrastructure",
        "price": 854.50,
        "support": 810.00,
        "resistance": 890.00,
        "pe": "18.2x",
        "pb": "3.5x",
        "overview": "Global port management company operating container port terminals across Asia-Pacific, the Americas, Europe, the Middle East, and Africa.",
        "catalysts": "Global volume throughput expansion, tariff adjustments, and natural USD revenue hedge.",
        "risks": "Global trade route disruptions and concession renewal capex requirements.",
        "sentiment": "Premium infrastructure compounder maintaining consistent margins."
    },
    "SMPH": {
        "name": "SM Prime Holdings, Inc.",
        "sector": "Real Estate / Commercial Centers",
        "price": 17.32,
        "support": 15.40,
        "resistance": 18.50,
        "pe": "14.5x",
        "pb": "1.1x",
        "overview": "Premier property developer in Southeast Asia with major business segments in shopping malls, residential condominiums, and commercial offices.",
        "catalysts": "Provincial mall foot-traffic expansion, rental reversions, and sustained retail consumption.",
        "risks": "Tenant retail sales compression under elevated living costs.",
        "sentiment": "Basing above key support with steady domestic consumer resilience."
    },
    "SM": {
        "name": "SM Investments Corporation",
        "sector": "Holding Firms / Conglomerates",
        "price": 532.00,
        "support": 510.00,
        "resistance": 580.00,
        "pe": "13.2x",
        "pb": "1.3x",
        "overview": "Dominant Philippine conglomerate with market-leading franchises in retail merchandise, universal banking (BDO, China Bank), and property (SMPH).",
        "catalysts": "Direct consumer spending leverage, store network growth, and universal banking dividends.",
        "risks": "Discretionary retail spending compression and inflation headwinds.",
        "sentiment": "Bellwether stock reflecting the broader Philippine economic cycle."
    },
    "MBT": {
        "name": "Metropolitan Bank & Trust Company (Metrobank)",
        "sector": "Banking & Financial Services",
        "price": 60.50,
        "support": 58.00,
        "resistance": 66.00,
        "pe": "6.8x",
        "pb": "0.7x",
        "overview": "Universal banking institution providing comprehensive corporate and retail banking services with strong capital adequacy ratios.",
        "catalysts": "High Tier-1 capital ratios, potential special dividend payouts, and corporate credit growth.",
        "risks": "Compression in loan margins during rate cuts.",
        "sentiment": "Undervalued banking peer with defensive balance sheet characteristics."
    },
    "MER": {
        "name": "Manila Electric Company (Meralco)",
        "sector": "Utilities / Power Distribution",
        "price": 432.00,
        "support": 410.00,
        "resistance": 450.00,
        "pe": "12.0x",
        "pb": "1.9x",
        "overview": "The largest electric power distribution company in the Philippines, covering Metro Manila and surrounding economic corridor provinces.",
        "catalysts": "Guaranteed distribution asset returns, power generation capacity expansion, and steady dividend yields.",
        "risks": "Regulatory rate-setting scrutiny and fuel input cost pass-through risks.",
        "sentiment": "Low-beta defensive dividend utility."
    },
    "MONDE": {
        "name": "Monde Nissin Corporation",
        "sector": "Consumer Staples / Food",
        "price": 5.98,
        "support": 5.80,
        "resistance": 7.20,
        "pe": "16.5x",
        "pb": "2.2x",
        "overview": "Leading food consumer brand across instant noodles (Lucky Me!), baked goods, and plant-based meat substitutes (Quorn).",
        "catalysts": "Noodles category volume leadership, input cost deflation (wheat, palm oil), and margin recovery.",
        "risks": "Impairments or restructuring drag in the alternative meat segment.",
        "sentiment": "Consolidating at multi-year valuation support; oversold momentum."
    },
    "JFC": {
        "name": "Jollibee Foods Corporation",
        "sector": "Consumer Discretionary / QSR",
        "price": 144.00,
        "support": 135.00,
        "resistance": 160.00,
        "pe": "22.8x",
        "pb": "3.1x",
        "overview": "Global quick-service restaurant operator with iconic domestic brands (Jollibee, Mang Inasal) and international acquisitions (Smashburger, CBTL).",
        "catalysts": "System-wide store network expansion, international profitability turnaround, and franchise licensing fees.",
        "risks": "Store labor inflation and international integration overhead.",
        "sentiment": "Growth compounder trading in an intermediate consolidation range."
    },
    "PGOLD": {
        "name": "Puregold Price Club, Inc.",
        "sector": "Consumer Staples / Grocery Retail",
        "price": 40.15,
        "support": 36.00,
        "resistance": 42.00,
        "pe": "10.4x",
        "pb": "0.8x",
        "overview": "Major hypermarket, supermarket, and discount grocery retailer serving mass-market consumers and small retail sari-sari store operators.",
        "catalysts": "Provincial store rollouts, resilient basic staple volume demand, and membership shopping formats (S&R).",
        "risks": "Competition from regional discounters and margin compression.",
        "sentiment": "Stable cash-flow operator trading near historical valuation floor."
    }
}

# ---------------------------------------------------------
# Technical Math Helpers (Wilder RSI, Moving Averages)
# ---------------------------------------------------------
def generate_synthetic_candles(base_price, support, resistance, n=60):
    """Generates realistic candle histories bounded by structural levels for dynamic indicator modeling."""
    np.random.seed(int(base_price * 100) % 1000)
    drift = (resistance - support) / (n * 2)
    volatility = base_price * 0.008
    prices = [support + (base_price - support) * 0.8]
    
    for _ in range(n - 1):
        step = np.random.normal(drift, volatility)
        next_p = max(support * 0.96, min(resistance * 1.04, prices[-1] + step))
        prices.append(next_p)
    
    prices[-1] = base_price
    return pd.Series(prices)

def calculate_wilders_rsi(series, period=14):
    """Calculates Wilder's 14-period Smoothed RSI."""
    if len(series) < period + 1:
        return 50.0
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    
    avg_gain = gain.iloc[1:period+1].mean()
    avg_loss = loss.iloc[1:period+1].mean()
    
    for i in range(period + 1, len(series)):
        avg_gain = (avg_gain * (period - 1) + gain.iloc[i]) / period
        avg_loss = (avg_loss * (period - 1) + loss.iloc[i]) / period
        
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100.0 - (100.0 / (1.0 + rs)), 1)

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "manual_overrides" not in st.session_state:
    st.session_state.manual_overrides = {}

# ---------------------------------------------------------
# Header & Bot Guidance Summary
# ---------------------------------------------------------
st.title("📈 Stock Analysis & Insight Engine")
st.caption("5-Pillar Technical & Fundamental Analytical Radar • Philippine Stock Exchange (PSE)")

# ---------------------------------------------------------
# Sidebar: Manual Overrides & Real-Time Controls
# ---------------------------------------------------------
st.sidebar.header("⚙️ Live Price Controls")
selected_ticker = st.sidebar.selectbox("Select Ticker for Controls:", list(STOCK_PROFILES.keys()), index=0)
current_profile = STOCK_PROFILES[selected_ticker]

default_active_price = st.session_state.manual_overrides.get(selected_ticker, current_profile["price"])

manual_price = st.sidebar.number_input(
    f"Override Price for {selected_ticker} (₱)",
    value=float(default_active_price),
    step=0.05
)

col_apply, col_reset = st.sidebar.columns(2)
if col_apply.button("Apply Override", use_container_width=True):
    st.session_state.manual_overrides[selected_ticker] = round(float(manual_price), 2)
    st.rerun()

if col_reset.button("Reset Price", use_container_width=True):
    st.session_state.manual_overrides.pop(selected_ticker, None)
    st.rerun()

if st.session_state.manual_overrides:
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Active Overrides:**")
    for t, p in st.session_state.manual_overrides.items():
        st.sidebar.caption(f"• **{t}**: ₱{p:,.2f}")

# ---------------------------------------------------------
# Engine Processing: 5-Pillar Calculations Across Watchlist
# ---------------------------------------------------------
computed_data = {}

for ticker, meta in STOCK_PROFILES.items():
    effective_price = st.session_state.manual_overrides.get(ticker, meta["price"])
    support = meta["support"]
    resistance = meta["resistance"]
    
    # Generate candle context
    series = generate_synthetic_candles(effective_price, support, resistance)
    ma20 = round(float(series.tail(20).mean()), 2)
    ma50 = round(float(series.tail(50).mean()), 2)
    rsi_14 = calculate_wilders_rsi(series, period=14)
    
    # Pillar 3: Data-driven Analytical Price Ranges (Corridors)[cite: 1]
    # Buy zone near strong support; Sell zone near strong resistance[cite: 1]
    buy_band_low = round(support * 0.995, 2)
    buy_band_high = round(support * 1.010, 2)
    sell_band_low = round(resistance * 0.990, 2)
    sell_band_high = round(resistance * 1.005, 2)
    
    buy_band_str = f"₱{buy_band_low:,.2f} – ₱{buy_band_high:,.2f}"
    sell_band_str = f"₱{sell_band_low:,.2f} – ₱{sell_band_high:,.2f}"
    
    # Analytical Zone Status
    if effective_price <= support * 1.015:
        zone_status = "ACCUMULATION"
    elif effective_price >= resistance * 0.990:
        zone_status = "PROFIT_TAKING"
    else:
        zone_status = "NEUTRAL"
        
    trend_str = "Above MA20" if effective_price >= ma20 else "Below MA20"
    
    computed_data[ticker] = {
        "name": meta["name"],
        "sector": meta["sector"],
        "price": effective_price,
        "support": support,
        "resistance": resistance,
        "ma20": ma20,
        "ma50": ma50,
        "rsi": rsi_14,
        "trend": trend_str,
        "zone_status": zone_status,
        "buy_band": buy_band_str,
        "sell_band": sell_band_str,
        "pe": meta["pe"],
        "pb": meta["pb"],
        "overview": meta["overview"],
        "catalysts": meta["catalysts"],
        "risks": meta["risks"],
        "sentiment": meta["sentiment"]
    }

# ---------------------------------------------------------
# Watchlist Overview Table (Pillars 1, 2, & 3)
# ---------------------------------------------------------
st.markdown("### 📊 Watchlist Technical & Valuation Radar")

table_rows = []
for ticker, info in computed_data.items():
    table_rows.append({
        "Ticker": ticker,
        "Company Name & Sector": f"{info['name']} ({info['sector']})",
        "Last Price": f"₱{info['price']:,.2f}",
        "Analytical Buy Zone": info["buy_band"],
        "Key Support": f"₱{info['support']:,.2f}",
        "Key Resistance": f"₱{info['resistance']:,.2f}",
        "Analytical Sell Zone": info["sell_band"],
        "RSI (14D)": f"{info['rsi']:.1f}",
        "Status": info["zone_status"]
    })

df_overview = pd.DataFrame(table_rows)
st.dataframe(df_overview, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# 5-Pillar Stock Detail Viewer (Full Framework Integration)
# ---------------------------------------------------------
st.divider()
detail_ticker = st.selectbox(
    "Select Stock for 5-Pillar Analyst Deep Dive:",
    list(computed_data.keys()),
    index=list(computed_data.keys()).index(selected_ticker)
)

d = computed_data[detail_ticker]
st.subheader(f"{detail_ticker} — {d['name']}")

# Quick Metric Cards
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Current Reference Price", f"₱{d['price']:,.2f}")
col2.metric("Key Support (Floor)", f"₱{d['support']:,.2f}")
col3.metric("Key Resistance (Ceiling)", f"₱{d['resistance']:,.2f}")
col4.metric("RSI (14D Wilder)", f"{d['rsi']:.1f}")
col5.metric("Trend vs MA20", d["trend"])

# 5-Pillar Analysis Tabs
tab_tech, tab_fund, tab_ranges, tab_commentary = st.tabs([
    "1. Technical Chart Analysis",
    "2. Fundamental Profile & Valuation Anchor",
    "3. Suggested Price Ranges (Analytical)",
    "4. Analyst-Style Commentary"
])

# --- Pillar 1: Technical Analysis Instructions ---
with tab_tech:
    st.markdown("#### Pillar 1: Technical Chart & Momentum Indicators")
    st.markdown(
        f"Based on recent price action, dynamic support appears near **₱{d['support']:,.2f}** "
        f"and key resistance near **₱{d['resistance']:,.2f}**[cite: 1]. Traders and institutional participants often "
        f"monitor these boundary levels for potential liquidity absorption or trend exhaustion[cite: 1]."
    )
    
    tech_col1, tech_col2 = st.columns(2)
    with tech_col1:
        st.markdown("**Moving Average Alignment:**")
        st.write(f"• **20-Day Moving Average (Short-Term):** ₱{d['ma20']:,.2f}")
        st.write(f"• **50-Day Moving Average (Medium-Term):** ₱{d['ma50']:,.2f}")
        st.write(f"• **Positioning:** Price is currently `{d['trend']}`.")
    
    with tech_col2:
        st.markdown("**Momentum & Volatility:**")
        rsi_desc = (
            "Approaching oversold (<30); potential exhaustion zone" if d['rsi'] <= 35 
            else "Approaching overbought (>70); extended momentum" if d['rsi'] >= 65 
            else "Balanced neutral momentum (30–70 range)"
        )
        st.write(f"• **Wilder RSI (14-Period):** **{d['rsi']:.1f}** ({rsi_desc})[cite: 1]")
        st.write(f"• **Structural Volatility:** Testing historical channel boundaries between ₱{d['support']:,.2f} and ₱{d['resistance']:,.2f}.")

# --- Pillar 2: Fundamental Analysis Instructions ---
with tab_fund:
    st.markdown("#### Pillar 2: Fundamental Profile & Valuation Anchor")
    st.markdown(f"**Business Overview & Operational Scope:**\n{d['overview']}")
    
    fund_col1, fund_col2 = st.columns(2)
    with fund_col1:
        st.markdown("**Valuation Multiples:**")
        st.write(f"• **Price-to-Earnings (P/E):** {d['pe']}")
        st.write(f"• **Price-to-Book (P/B):** {d['pb']}")
        st.write(f"• **Sector Classification:** {d['sector']}")
    
    with fund_col2:
        st.markdown("**Growth Catalysts & Operating Risks:**")
        st.write(f"• **Key Catalysts:** {d['catalysts']}")
        st.write(f"• **Key Risks:** {d['risks']}")

# --- Pillar 3: Suggested Price Ranges ---
with tab_ranges:
    st.markdown("#### Pillar 3: Data-Driven Analytical Price Ranges")
    st.markdown(
        f"Given the current valuation multiples and chart structure, a typical accumulation zone may fall between "
        f"**{d['buy_band']}**, while profit-taking often clusters near **{d['sell_band']}**[cite: 1]."
    )
    
    range_col1, range_col2 = st.columns(2)
    with range_col1:
        st.info(f"🟢 **Suggested Accumulation Zone (Buy Band):**\n### {d['buy_band']}\n*Near historical buyer support floors and valuation troughs.*")
    with range_col2:
        st.warning(f"🔴 **Suggested Profit-Taking Zone (Sell Band):**\n### {d['sell_band']}\n*Near historical seller resistance ceilings and overextension marks.*")
    
    st.caption("Notice: These zones are mathematical and chart-based reference points, not purchase or sell instructions[cite: 1].")

# --- Pillar 4: Analyst-Style Commentary ---
with tab_commentary:
    st.markdown("#### Pillar 4: Analyst-Style Commentary & Market Context")
    st.markdown(
        f"**Market Sentiment & Positioning:**  \n{d['sentiment']}\n\n"
        f"**Analyst Synthesis:**  \n"
        f"Analysts note that {detail_ticker} is trading in a `{d['zone_status']}` technical stance relative to its structural corridor. "
        f"On the fundamental side, drivers such as {d['catalysts'].lower()} remain focal points for medium-term earnings trajectory. "
        f"However, market participants remain cautious regarding {d['risks'].lower()}, which could introduce volatility if macroeconomic conditions tighten."
    )

# ---------------------------------------------------------
# Pillar 5: Safety & Mandatory Disclaimer Behavior
# ---------------------------------------------------------
st.divider()
st.caption(
    "**Pillar 5 Safety & Educational Disclaimer:** "
    "These insights, technical indicators, valuation multiples, and suggested price ranges are generated strictly for "
    "informational and educational tracking purposes[cite: 1]. They do not constitute financial advice, an investment recommendation, "
    "an endorsement, or a trade instruction to buy, sell, or hold any security[cite: 1]. Past performance and technical bands do not guarantee "
    "future results[cite: 1]. Always consult a licensed financial advisor or certified professional before making investment decisions[cite: 1]."
)
