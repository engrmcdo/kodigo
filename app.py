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
# 15-Stock Watchlist & Verified PSE Market Baselines
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
        "pb":
