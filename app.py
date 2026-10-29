import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import random
from datetime import datetime
import pytz

st.set_page_config(
    page_title="PSE Stock Analyst & Insight Engine",
    page_icon="📈",
    layout="wide"
)

PHT = pytz.timezone("Asia/Manila")

# --------------------------------------------------------------------------
# 15-Stock Watchlist & Verified PSE Market Baselines (All Braces Closed)
# --------------------------------------------------------------------------
WATCHLIST = {
    "GCASH": {
        "name": "Mynt, Inc. (Digital Financial Services)",
        "yf_sym": "GLO.PS",
        "current_price": 6.72,
        "support": 5.95,
        "resistance": 6.76,
        "rsi": 54.2,
        "pb": "4.8x",
        "pe": "24.5x",
        "sector": "Fintech / Digital Financial Services",
        "catalysts": "Rapid credit portfolio expansion (GLoan, GCredit), remittance ubiquity, non-collateralized lending margins, and potential global expansion.",
        "risks": "Deposit competition from digital-only banks, regulatory caps on credit spreads, and cybersecurity infrastructure overhead.",
        "commentary": "Trading in an active price-discovery phase testing its ₱6.76 debut ceiling. Institutional liquidity remains focused on loan book growth and return on equity (ROE) expansion."
    },
    "GLO": {
        "name": "Globe Telecom, Inc.",
        "yf_sym": "GLO.PS",
        "current_price": 1537.00,
        "support": 1450.00,
        "resistance": 1650.00,
        "rsi": 46.8,
        "pb": "1.8x",
        "pe": "12.4x",
        "sector": "Telecommunications",
        "catalysts": "Data monetization, digital solutions expansion, capital expenditure tapering, and consistent recurring dividend yields.",
        "risks": "Network capex depreciation, intense mobile broadband price competition, and debt servicing requirements.",
        "commentary": "Consolidating along intermediate moving averages while providing defensive telecom cash-flow yields. The accumulation band remains firmly anchored near ₱1,450.00."
    },
    "AC": {
        "name": "Ayala Corporation",
        "yf_sym": "AC.PS",
        "current_price": 540.00,
        "support": 520.00,
        "resistance": 590.00,
        "rsi": 51.8,
        "pb": "0.8x",
        "pe": "10.1x",
        "sector": "Conglomerates / Holding Firms",
        "catalysts": "Broad portfolio earnings resilience, ACEN renewable power capacity additions, real estate recovery, and banking transaction volume growth.",
        "risks": "Holding company net asset value discount and macroeconomic interest rate sensitivity.",
        "commentary": "Trading in an accumulation corridor near its structural floor with balanced momentum. Valuation remains attractive relative to historical book value."
    },
    "BPI": {
        "name": "Bank of the Philippine Islands",
        "yf_sym": "BPI.PS",
        "current_price": 94.00,
        "support": 92.00,
        "resistance": 110.00,
        "rsi": 46.9,
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
        "current_price": 1126.00,
        "support": 1110.00,
        "resistance": 1250.00,
        "rsi": 48.2,
        "pb": "1.4x",
        "pe": "11.2x",
        "sector": "Telecommunications",
        "catalysts": "Capex tapering expanding free cash flows, enterprise data center leasing growth, and steady cash returns.",
        "risks": "Broadband market competition and debt servicing requirements.",
        "commentary": "Maintaining structural stability above its horizontal floor support with steady cash dividend yield."
    },
    "ALI": {
        "name": "Ayala Land, Inc.",
        "yf_sym": "ALI.PS",
        "current_price": 15.20,
        "support": 14.80,
        "resistance": 17.50,
        "rsi": 53.4,
        "pb": "0.6x",
        "pe": "8.9x",
        "sector": "Real Estate",
        "catalysts": "Commercial leasing recovery, stable residential presales volume, and provincial estate development.",
        "risks": "Mortgage rate sensitivity and building material input costs.",
        "commentary": "Trading at a steep discount to net asset value (NAV). Price action remains constructive above multi-month support."
    },
    "BDO": {
        "name": "BDO Unibank, Inc.",
        "yf_sym": "BDO.PS",
        "current_price": 117.10,
        "support": 110.00,
        "resistance": 125.00,
        "rsi": 57.2,
        "pb": "1.0x",
        "pe": "8.4x",
        "sector": "Banking",
        "catalysts": "Market-leading loan portfolio scale, fee income diversification, and resilient net interest margins.",
        "risks": "Credit cost sensitivity if monetary policy easing is delayed.",
        "commentary": "Constructive upward momentum trading in the upper half of its intermediate channel with balanced RSI."
    },
    "ICT": {
        "name": "Intl Container Terminal Services",
        "yf_sym": "ICT.PS",
        "current_price": 820.00,
        "support": 800.00,
        "resistance": 890.00,
        "rsi": 45.9,
        "pb": "3.5x",
        "pe": "18.2x",
        "sector": "Port Logistics",
        "catalysts": "Global volume throughput growth and USD tariff hedge advantages.",
        "risks": "Shipping route disruptions and port concession renewal capex.",
        "commentary": "Consolidating near ₱820.00 with neutral momentum following a test of overhead resistance."
    },
    "SMPH": {
        "name": "SM Prime Holdings",
        "yf_sym": "SMPH.PS",
        "current_price": 17.54,
        "support": 15.40,
        "resistance": 18.50,
        "rsi": 55.1,
        "pb": "1.1x",
        "pe": "14.5x",
        "sector": "Real Estate / Commercial Malls",
        "catalysts": "Provincial mall foot traffic, resilient tenant rental revenue yields, and residential pipeline expansion.",
        "risks": "Inflationary pressure on retail tenant sales.",
        "commentary": "Stabilizing with healthy momentum, approaching its structural resistance ceiling near ₱18.50."
    },
    "SM": {
        "name": "SM Investments Corp.",
        "yf_sym": "SM.PS",
        "current_price": 534.00,
        "support": 510.00,
        "resistance": 580.00,
        "rsi": 50.7,
        "pb": "1.3x",
        "pe": "13.2x",
        "sector": "Conglomerates",
        "catalysts": "Direct consumer proxy across retail, universal banking, and prime commercial property.",
        "risks": "Compression in discretionary consumer spending.",
        "commentary": "Trading in the middle of its historical trading band, mirroring broader Philippine domestic consumption."
    },
    "MBT": {
        "name": "Metrobank",
        "yf_sym": "MBT.PS",
        "current_price": 60.75,
        "support": 58.00,
        "resistance": 66.00,
        "rsi": 45.1,
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
        "current_price": 429.80,
        "support": 410.00,
        "resistance": 450.00,
        "rsi": 44.8,
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
        "current_price": 5.90,
        "support": 5.75,
        "resistance": 7.20,
        "rsi": 37.2,
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
        "current_price": 144.00,
        "support": 135.00,
        "resistance": 160.00,
        "rsi": 51.4,
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
        "current_price": 40.00,
        "support": 36.00,
        "resistance": 42.00,
        "rsi": 50.9,
        "pb": "0.8x",
        "pe": "10.4x",
        "sector": "Consumer Staples / Grocery Retail",
        "catalysts": "Everyday staple grocery volume resilience and strategic provincial footprint.",
        "risks": "Competition from discount format retailers.",
        "commentary": "Approaching its overhead resistance level with balanced momentum."
    }
}

# --------------------------------------------------------------------------
# Indicator Calculation Engine
# --------------------------------------------------------------------------
def calculate_wilders_rsi(series, period=14):
    """Calculates true 14-period Wilder's Smoothed RSI[cite: 1]."""
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

@st.cache_data(ttl=120)
def fetch_live_market_data():
    """Queries live daily exchange candles with fallback to accurate PSE baselines
